import uuid

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as auth_logout
from models import UserProfile, Revision, Message

from boxdotnet import BoxDotNet
import diff_match_patch as dmp_module
import urllib

from datetime import datetime
import json

def _get_next(request):
    """
    Returns a url to redirect to after the login
    """
    if 'next' in request.session:
        next = request.session['next']
        del request.session['next']
        return next
    elif 'next' in request.GET:
        return request.GET.get('next')
    elif 'next' in request.POST:
        return request.POST.get('next')
    else:
        return getattr(settings, 'LOGIN_REDIRECT_URL', '/')

def box_login(request, extra_context=dict(), account_inactive_template='TODO'):
    box = BoxDotNet()
    
    # if initial visit of this page, redirect to the box login screen
    if not 'ticket' in request.GET:
        url = box.get_login_url(settings.BOX_API_KEY)
        return HttpResponseRedirect(url)
    
    # if we have a ticket, then get the auth token
    tokenNode = box.login(settings.BOX_API_KEY, request.GET['ticket'])
    print tokenNode.xml
    token = tokenNode.auth_token[0].elementText
    
    # authenticate the user using this auth token
    user = authenticate(token=token)
    
    if user is None:
        # we have a token but no user, create one
        user = User()
        user.email = tokenNode.user[0].email[0].elementText
        # we need a username so generate one randomly..
        user.username = str(uuid.uuid4())[:30]
        user.save()
        
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.token = token
        user_profile.save()
        
        # Authenticate and login
        user = user_profile.authenticate()
    
    # here we will have valid user so login
    login(request, user)
    
    print request.user.is_authenticated()

    if not user.is_active:
        return render_to_response(account_inactive_template, extra_context,
             context_instance=RequestContext(request))

    return HttpResponseRedirect(_get_next(request))