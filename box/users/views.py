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
	
    token = tokenNode.auth_token[0].elementText
    user_id = tokenNode.user[0].user_id[0].elementText
    print user_id
    
    # authenticate the user using this auth token
    user = authenticate(box_user_id=user_id)
    
    if user is None:
        # we have a token but no user, create one
        user = User()
        user.email = tokenNode.user[0].email[0].elementText
        # use box.net user_id as username
        user.username = user_id
        user.save()
        
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.token = token
        user_profile.box_user_id = user_id
        user_profile.save()
    
    # here we will have valid user so login
    login(request, user)

    if not user.is_active:
        return render_to_response(account_inactive_template, extra_context,
             context_instance=RequestContext(request))

    return HttpResponseRedirect(_get_next(request))

# take a user, and search his files for a given query - HA
def box_search_file(request):
	box = BoxDotNet()
	profile = request.user.get_profile()
	query = "word" # change, need query to be part of request
	searchFiles = box.get_search(settings.BOX_API_KEY, profile.token, query)
	return HttpResponseRedirect("http://www.google.com") # change
	
def box_download_file(request):
    boxsearch = BoxDotNet()
    query = "blah" # obviously, not going to be used here, fileid should be param?
    auth_token = request.user.get_profile().token
    fileid = boxsearch.get_search(settings.BOX_API_KEY, auth_token, query) # change eventually
    downloadurl = 'https://www.box.net/api/1.0/download/%s/%s' % (auth_token, fileid)
    return HttpResponseRedirect(downloadurl) # change
    
def box_versions(request):
    box = BoxDotNet()
    auth_token = request.user.get_profile().token
    fileid = box.get_search(settings.BOX_API_KEY, auth_token, 'blah') # change eventually
    versions = box.get_version_history(settings.BOX_API_KEY, auth_token, fileid)
    print versions.version[0].author[0].elementText

