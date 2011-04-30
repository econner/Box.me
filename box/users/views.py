import uuid

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as auth_logout
from models import UserProfile

from boxdotnet import BoxDotNet
import diff_match_patch as dmp_module
import urllib

from datetime import datetime
import json
from models import Message

import stomp

conn = stomp.Connection()
conn.start()
conn.connect()
conn.subscribe(destination='/messages', ack='auto')

dmp = dmp_module.diff_match_patch()

# Create your views here.

def _perform_diff(text1, text2):
    diff = dmp.diff_main(text1, text2, True)
    print diff
    if (len(diff) > 2):
      dmp.diff_cleanupSemantic(diff)
    
    patch_list = dmp.patch_make(text1, text2, diff)
    return patch_list;

def _perform_patch(patches, text):
    results = dmp.patch_apply(patches, text)
    print results
    result_text = results[0]
    return result_text

def index(request):
    """
    handle the index request
    """
    message = Message.objects.get(pk=1)
    message.msg = "Macs had the original point and click UI."
    message.save()
    
    serverShadow = Message.objects.get(pk=2)
    serverShadow.msg = "Macs had the original point and click UI."
    serverShadow.save()
    
    return render_to_response("index.html", {"message":message})

def addMessage(request):
    patchText = urllib.unquote(request.POST.get("patches", ""))
    patches = dmp.patch_fromText(patchText)
    
    clientText = urllib.unquote(request.POST.get("text", ""))
    
    # server shadow must be the same as client text after every iteration
    serverShadow = Message.objects.get(pk=2)
    serverShadow.msg = clientText
    serverShadow.save()
    
    # patch the server text
    serverText = Message.objects.get(pk=1)
    patchedText = _perform_patch(patches, serverText.msg)
    serverText.msg = patchedText
    serverText.save()
    
    print "SERVER TEXT: %s" % serverText.msg
    print "SERVER SHADOW: %s" % serverShadow.msg
    
    # diff server text with server shadow
    patches = _perform_diff(serverText.msg, serverShadow.msg)
    
    # copy server text into server shadow
    serverShadow.msg = serverText.msg
    serverShadow.save()
    
    msg_to_send = json.dumps({"patches": dmp.patch_toText(patches), "serverText": serverText.msg})
    print msg_to_send
    conn.send(msg_to_send, destination='/messages') 
    return HttpResponse("ok")


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