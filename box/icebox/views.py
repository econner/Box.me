import uuid

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from icebox.models import *

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

def _get_icebox_folder_id(user):
    """
    Gets the id of the icebox folder corresponding
    to this user.
    """
    icebox_folder = "icebox"
    
    # get the folder to store notes
    box = BoxDotNet()
    profile = user.get_profile()
    rsp = box.get_account_tree(api_key=settings.BOX_API_KEY, auth_token=profile.token, folder_id=0, params=['nozip'])
    # make sure the response came back ok
    if rsp.status[0].elementText != box.RETURN_CODES['get_account_tree']:
        return -1
    
    # iterate through the folders by name
    folder_id = -1
    if hasattr(rsp.tree[0].folder[0], "folders"):
        for folder in rsp.tree[0].folder[0].folders[0].folder:
            try:
                my_folder = Folder.objects.get(folder_id=folder['id'])
                folder_id = my_folder.folder_id
            except Folder.DoesNotExist:
                pass
    
    # create folder if not found
    if folder_id == -1:
        created_folder = box.create_folder(api_key=settings.BOX_API_KEY, auth_token=profile.token, parent_id=0, name=icebox_folder, share=1)
        if created_folder.status[0].elementText != box.RETURN_CODES['create_folder']:
            return -1
        
        folder_id = int(created_folder.folder[0].folder_id[0].elementText)
        my_folder = Folder(folder_id=folder_id, name=icebox_folder, owner=user)
        my_folder.save()
    
    return folder_id

@login_required
def index(request):
    """
    handle the index request
    """
    folder_id = _get_icebox_folder_id(request.user)
    if folder_id == -1:
        return HttpResponse("Failed to retrieve icebox note folder.")
    try:
        folder = Folder.objects.get(folder_id=folder_id)
    except Folder.DoesNotExist:
        return HttpResponse("Bad icebox folder.")
    
    note_qset = Note.objects.filter(box_folder=folder)
    notes = []
    for note in note_qset:
        note.revisions = note.noterevision_set.all().order_by("-created")
        notes.append(note)
    
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
    validTags = 'img br b blockquote code del dd dl dt em h1 h2 h3 i kbd li ol p pre s sup sub strong strike ul'.split()
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
    print request.POST['text']
    try:
        note = Note.objects.get(pk = request.POST['note_id'])
        
        # create a new revision of this note
        revision = NoteRevision(note = note)
        
        revision.collaborators = [request.user]
        revision.text = sanitizeHtml(request.POST['text'])
        revision.title = request.POST['title']
        revision.save()
        
        # save this note to box.net
        folder_id = _get_icebox_folder_id(request.user)
        if folder_id == -1:
            return HttpResponse("Failed to retrieve icebox note folder.")
        
        box = BoxDotNet()
        action = ""
        entity_id = -1
        # if we haven't already uploaded this file to box.net
        if revision.title != "":
            if note.box_file_id == -1:
                action = "upload"
                entity_id = folder_id
            else:
                action = "overwrite"
                entity_id = note.box_file_id
        
        # upload the file
        if action:
            profile = request.user.get_profile()
            uploaded_file = box.upload(filename="%s.txt" % revision.title, data=revision.text, action=action, 
                                api_key=settings.BOX_API_KEY, auth_token=profile.token, entity_id=entity_id, share=1)
        
            if uploaded_file.status[0].elementText != box.RETURN_CODES['upload']:
                return HttpResponse("Failed to upload file to box.net")
        
            file_obj = uploaded_file.files[0].file[0]
            note.box_file_id = int(file_obj['id'])
            note.save()
         
    except Note.DoesNotExist:
        pass
    
    return HttpResponse("blah")
    

def note(request, id):
    # get the note
    try:
        note = Note.objects.get(pk=id)
    except Note.DoesNotExist:
        return HttpResponse("Bad note id")
        
    # get note's latest revision
    note.revisions = note.noterevision_set.all().order_by("-created")
    
    return render_to_response("note.html", {"note": note})

@login_required
def editor(request):
    """
    Display the editor view.  If no doc_id is found in
    the GET request, assume use wants to create a new note.
    """
    folder_id = _get_icebox_folder_id(request.user)
    if folder_id == -1:
        return HttpResponse("Failed to retrieve icebox note folder.")
        
    try:
        folder = Folder.objects.get(folder_id=folder_id)
    except Folder.DoesNotExist:
        return HttpResponse("Bad icebox folder.")
    
    note = None
    note_id = ""
    if not 'note_id' in request.GET:
        # user wants a new note
        note = Note()
        note.creator = request.user
        note.box_folder = folder
        note.box_file_id = -1 # hasn't been saved yet
        note.save()
        note_id = note.pk
        
        # ok, now we've created a new note, redirect them back to the editor w/ this pk
        # perhaps this should be its own view?
        return HttpResponseRedirect("/editor?note_id=%d" % note.pk) 
    else:
        # user wants to retrieve existing note
        note_id = request.GET['note_id']
        try:
            note = Note.objects.get(pk=note_id, box_folder=folder)
        except Note.DoesNotExist:
            return HttpResponse("Bad note id or folder id")
            
    # get the latest revision of the note
    revisions = note.noterevision_set.all().order_by("-created")
    revision = None
    if revisions:
        revision = revisions[0] 
    else:
        revision = NoteRevision(title = "", text = "")
    print revision.title
    msg_to_send = json.dumps({"message": "%s is now editing this note." % request.user.email})
    print note_id
    
    # setup stomp so that we can push messages to the browser
    conn = stomp.Connection()
    conn.start()
    conn.connect()
    conn.subscribe(destination='/messages-%s' % note_id, ack='auto')
    conn.send(msg_to_send, destination="/messages-%s" % note_id)
    
    return render_to_response("editor.html", {"note": note, "revision": revision})