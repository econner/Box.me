import uuid

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from icebox.models import Note

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
    notes = Note.objects.filter(creator = request.user)
    return render_to_response("index.html", {"notes" : notes, "user": request.user})
    
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


def save_note(request):
    """
    Save the specified note.
    Expects note to be passed as a post request with
    text and id fields.
    """
    try:
        note = Note.objects.get(pk = request.POST['note_id'])
        note.text = request.POST['text']
        note.save()
    except Note.DoesNotExist:
        pass
    
    return HttpResponse("blah")

@login_required
def editor(request):
    """
    Display the editor view.  If no doc_id is found in
    the GET request, assume use wants to create a new note.
    """
    note = None
    if not 'note_id' in request.GET:
        # user wants a new note
        note = Note()
        note.creator = request.user
        note.save()
        note_id = note.pk
    else:
        # user wants to retrieve existing note
        note_id = request.GET['note_id']
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            pass
    
    return render_to_response("editor.html", {"note": note})