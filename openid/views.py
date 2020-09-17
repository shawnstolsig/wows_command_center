import re

from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken

# OpenID auth modules
from .authentication import Authentication
from .verification import Verification
from .exceptions import OpenIDVerificationFailed

from clans.utils import refresh_clan_on_login


def open_id(request, realm):
    """
    "   This is the first step of the OpenID 2.0 authentication workflow.  It correctly configures
    "   a URL for WG to redirect to after the user logs in on WG's servers.
    """

    components = {
        'scheme': request.scheme,
        'host': request.get_host(),
        'path': reverse('openid:callback')
    }

    return_to = '{scheme}://{host}{path}'.format(**components)
    auth = Authentication(return_to=return_to)
    url = auth.authenticate(f'https://{realm}.wargaming.net/id/openid/')
    return redirect(url)

def open_id_callback(request):
    """
    "   This is the second step of the OpenID 2.0 authentication workflow.  It verifies the 
    "   callback URL and parameters from WG, and if the OpenID authentication is valid,
    "   it logs the user into the Django backend and also creates a JWT pair for frontend
    "   integration.
    """

    # TO DO: get the region from the url
    regex = r'https://(\w+).wargaming.net/id/([0-9]+)-(\w+)/'

    # open ID verification
    current = request.build_absolute_uri()
    verify = Verification(current)

    # if successfull OpenID authentication
    try:
        identities = verify.verify()

        # get info about user
        match = re.search(regex, identities['identity'])
        realm = match.group(1)                              # use realm on frontend, ie: 'na', 'eu', 'ru', 'asia'
        domain = convert_realm_to_domain(realm)             # put domain in backend, for WG API calls.  ie: 'com', 'eu', 'ru', 'asia'
        account_id = int(match.group(2))
        nickname = match.group(3)

        # log user in to Django session system
        logged_in_user = login_user(request, nickname, account_id, domain)

        # log user in by creating an access/refresh JWT pair for use by frontend
        tokens = get_tokens_for_user(logged_in_user)

        # format query strings that will be sent to frontend
        query_strings = f'?nickname={nickname}&accountID={account_id}&realm={realm}&access={tokens["access"]}&refresh={tokens["refresh"]}'

    # if unsuccessful OpenID authentication
    except OpenIDVerificationFailed:

        # make sure user is logged out
        logout(request)

    # redirect back to frontend
    # return redirect(reverse('frontend'))                                             # for use with production, when Django is serving SPA frontend
    return redirect(f'http://localhost:3000/complete_login{query_strings}')           # while developing with seperate frontend       


def open_id_logout(request):
    """
    "   Logs user out of Django's session system.
    """

    logout(request)
    # return redirect(reverse('frontend'))                  # for use with production, when Django is serving SPA frontend
    return redirect('http://localhost:3000/')               # while developing with seperate frontend


def login_user(request, nickname, wgid, domain):
    '''
    '   Helper function for loggin in (or creating) a user
    '''

    # try to find user from backend
    try:
        user = User.objects.get(id=wgid) 

        # update the User's clan information
        refresh_clan_on_login(user.player.clan.id, domain)


    # if unable to get the user, create a new one
    except ObjectDoesNotExist:

        password = User.objects.make_random_password(length=255)
        user = User.objects.create_user(nickname, id=wgid, password=password, last_name=domain)

    # login user with django's built-in auth system
    login(request, user)
    return user 

def get_tokens_for_user(user):
    """
    "   Creates a JSON Web Token pair for the user.  Used by frontend during autologin.
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def convert_realm_to_domain(realm):
    """
    "   Corrects the 'na' realm so that a useable domain is stored for WG API use ('na' = 'com')
    """
    if realm == 'na':
        return 'com'
    else:
        return realm