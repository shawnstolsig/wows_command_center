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
        status = request.GET.get('status', '')
        access_token = request.GET.get('access_token', '')
        expires_at = request.GET.get('expires_at', '')
        account_id = request.GET.get('account_id', '')
        nickname = request.GET.get('nickname', '')

        # log user in
        login_user(request, nickname, account_id, realm)       

    # if unsuccessful OpenID authentication
    except OpenIDVerificationFailed:

        # get information about error
        status = request.GET.get('status', '')
        code = request.GET.get('code', '')        
        message = request.GET.get('message', '')    

        # make sure user is logged out
        logout(request)
    
    # redirect back to frontend
    return redirect(reverse('main:frontend'))


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