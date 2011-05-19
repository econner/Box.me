import uuid

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from icebox.models import Note, NoteRevision

from boxdotnet import BoxDotNet
import diff_match_patch as dmp_module
import urllib

import socket
import os
import json
# Enable long polling using stomp, orbited, twisted
# See: http://mischneider.net/?p=125
import stomp

# mobwrite port
PORT = 3017

@login_required
def index(request):
    """
    handle the index request
    """
    notes = Note.objects.all()
    return render_to_response("index.html", {"notes" : notes, "user": request.user})

@login_required  
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
    
import re
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup, Comment

def sanitizeHtml(value, base_url=None):
    """
    Utility method for sanitizing user entered html.
    """
    rjs = r'[\s]*(&#x.{1,7})?'.join(list('javascript:'))
    rvb = r'[\s]*(&#x.{1,7})?'.join(list('vbscript:'))
    re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
    validTags = 'b blockquote code del dd dl dt em h1 h2 h3 i kbd li ol p pre s sup sub strong strike ul'.split()
    validAttrs = 'href src width height'.split()
    urlAttrs = 'href src'.split() # Attributes which should have a URL
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        # Get rid of comments
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = tag.attrs
        tag.attrs = []
        for attr, val in attrs:
            if attr in validAttrs:
                val = re_scripts.sub('', val) # Remove scripts (vbs & js)
                if attr in urlAttrs:
                    val = urljoin(base_url, val) # Calculate the absolute url
                tag.attrs.append((attr, val))

    return soup.renderContents().decode('utf8')

@login_required
def save_note(request):
    """
    Save the specified note.
    Expects note to be passed as a post request with
    text and id fields.
    """
    try:
        note = Note.objects.get(pk = request.POST['note_id'])
        
        # create a new revision of this note
        revision = NoteRevision(note = note)
        
        revision.text = sanitizeHtml(request.POST['text'])
        revision.title = request.POST['title']
        revision.save()
    except Note.DoesNotExist:
        pass
    
    return HttpResponse("blah")
    

def note(request, id):
    print id
    # get the note
    try:
        note = Note.objects.get(pk=id)
    except Note.DoesNotExist:
        return HttpResponse("Bad note id")
        
    # get note's latest revision
    revisions = note.noterevision_set.all().order_by("-created")
    revision = None
    if revisions:
        revision = revisions[0]
    
    return render_to_response("note.html", {"revision": revision})

@login_required
def editor(request):
    """
    Display the editor view.  If no doc_id is found in
    the GET request, assume use wants to create a new note.
    """
    
    note = None
    note_id = ""
    if not 'note_id' in request.GET:
        # user wants a new note
        note = Note()
        note.creator = request.user
        note.save()
        note_id = note.pk
        # ok, now we've created a new note, redirect them back to the editor w/ this pk
        # perhaps this should be its own view?
        return HttpResponseRedirect("/editor?note_id=%d" % note.pk) 
    else:
        # user wants to retrieve existing note
        note_id = request.GET['note_id']
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            return HttpResponse("Bad note id")
            
    # get the latest revision of the note
    revisions = note.noterevision_set.all().order_by("-created")
    revision = None
    if revisions:
        revision = revisions[0] 
    else:
        revision = NoteRevision(title = "", text = "")
    print revision.title
    msg_to_send = json.dumps({"message": "%s is now editing this note." % request.user.username})
    print note_id
    # setup stomp so that we can push messages to the browser
    conn = stomp.Connection()
    conn.start()
    conn.connect()
    conn.subscribe(destination='/messages-%s' % note_id, ack='auto')
    conn.send(msg_to_send, destination="/messages-%s" % note_id)
    
    return render_to_response("editor.html", {"note": note, "revision": revision})