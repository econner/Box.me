from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core import serializers

import docsims
import textextract
import models
import docsearch
import notesims

import pickle
import boxdocsims
from aprestatagger.tagger import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as auth_logout

def get_similar_notes(request):    
    text = request.POST['text']
    note_id = request.POST['note_id']
    sim_note_revs = notesims.generate_note_sims(text, note_id)
    response_revs = serializers.serialize('json', sim_note_revs)

    json = simplejson.dumps(response_revs) 
    
    return HttpResponse(json, mimetype='application/json')

NUM_QUERY_WORDS = 2
  
def get_similar_docs(request):
    weights = pickle.load(open('suggestion_engine/aprestatagger/data/dict.pkl', 'rb'))
    profile = request.user.get_profile()
    text = request.POST['text']
    
    mytagger = Tagger(Reader(), Stemmer(), Rater(weights))
    keywords = mytagger(text, NUM_QUERY_WORDS) # alter so its just 'text' once the POST request is working
    query = ' '.join(str(word)[2:-1] for word in keywords)
     
    sim_box_docs = boxdocsims.box_search_file(profile, query, settings.BOX_API_KEY) # have it return full XML for now
    
    files_info = []
    
    for files in sim_box_docs.file:
        file_id = files.id[0].elementText
        file_name = files.name[0].elementText
        url = boxdocsims.box_preview(file_id, profile, settings.BOX_API_KEY)
        files_info.append(dict(file_id=file_id, file_name=file_name, url=url))
        
    json = simplejson.dumps(files_info)
    return HttpResponse(json, mimetype='application/json')

