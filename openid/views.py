import re
# import requests
# import json

from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

# OpenID auth modules
from .authentication import Authentication
from .verification import Verification
from .exceptions import OpenIDVerificationFailed

# Project imports
# from data.config import api_key
# from data.models import Player, Clan

def open_id(request, realm):

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
        realm = match.group(1)
        account_id = match.group(2)
        nickname = match.group(3)

        # log user in
        login_user(request, nickname, account_id, realm)
        query_strings = f'?nickname={nickname}&accountID={account_id}&realm={realm}'

    # if unsuccessful OpenID authentication
    except OpenIDVerificationFailed:

        # make sure user is logged out
        logout(request)

    # redirect back to frontend
    # return redirect(reverse('frontend'))                                             # for use with production, when Django is serving SPA frontend
    return redirect(f'http://localhost:3000/complete_login{query_strings}')           # while developing with seperate frontend       


def open_id_logout(request):
    logout(request)
    # return redirect(reverse('frontend'))                  # for use with production, when Django is serving SPA frontend
    return redirect('http://localhost:3000/')               # while developing with seperate frontend


def login_user(request, nickname, wgid, realm):
    '''
    '   Helper function for loggin in (or creating) a user
    '''

    # try to find user from backend
    try:
        user = User.objects.get(email__exact=wgid)      # using the email field for the WG player ID

    # if unable to get the user, create a new one
    except ObjectDoesNotExist:
        password = User.objects.make_random_password(length=255)
        user = User.objects.create_user(nickname, wgid, password)
        user.last_name = realm                         # using the last_name field for the players realm
        user.save()

    # login user with django's built-in auth system
    login(request, user)
    return user 