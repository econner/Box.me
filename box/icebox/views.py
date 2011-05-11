import uuid

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as auth_logout
from users.models import UserProfile

from boxdotnet import BoxDotNet
import diff_match_patch as dmp_module
import urllib

import socket
import os

# mobwrite port
PORT = 3017
    
def index(request):
    """
    handle the index request
    """
    message = ""
    return render_to_response("index.html", {"message": message, "user": request.user})
    
def sync(request):
    form = request.POST
    if form.has_key("q"):
        # Client sending a sync.  Requesting text return.
        outStr = form["q"]
    elif form.has_key("p"):
        # Client sending a sync.  Requesting JS return.
        outStr = form["p"]
    print form["q"]

    inStr = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("localhost", PORT))
    except socket.error, msg:
        s = None
    
    if not s:
        # Python CGI can't connect to Python daemon.
        inStr = "\n"
    else:
        # Timeout if MobWrite daemon dosen't respond in 10 seconds.
        s.settimeout(10.0)
        s.send(outStr)
        while 1:
            line = s.recv(1024)
            if not line:
                break
            inStr += line
        s.close()

    if form.has_key("p"):
        # Client sending a sync.  Requesting JS return.
        inStr = inStr.replace("\\", "\\\\").replace("\"", "\\\"")
        inStr = inStr.replace("\n", "\\n").replace("\r", "\\r")
        inStr = "mobwrite.callback(\"%s\");" % inStr
    print inStr
    return HttpResponse(inStr + "\n")

def editor(request):
    return render_to_response("editor.html", {"doc_id": request.GET['doc_id']})