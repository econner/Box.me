from django.http import HttpResponse
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

def do_analysis(request):
#    text = textextract.extract_text()
#    return HttpResponse(text)
    sim_pairs = docsims.generate_doc_sims.delay()
    return HttpResponse(str(sim_pairs.get()))

def get_similar_notes(request):    
    text = request.POST['text']
    note_id = request.POST['note_id']
    sim_note_revs = notesims.generate_note_sims(text, note_id)
    response_revs = serializers.serialize('json', sim_note_revs)

    json = simplejson.dumps(response_revs) 
    
    return HttpResponse(json, mimetype='application/json')

  
def get_similar_docs(request):
    weights = pickle.load(open('suggestion_engine/aprestatagger/data/dict.pkl', 'rb'))
    profile = request.user.get_profile()
    
    #text = request.POST['text'] # not working, where to add in?
    mytagger = Tagger(Reader(), Stemmer(), Rater(weights))
    keywords = mytagger("b word words not here a the", 2) # alter so its just 'text' once the POST request is working
    query = ""
    for word in keywords:
        query += str(word)+ " "
        
    sim_box_docs = boxdocsims.box_search_file(profile, query, settings.BOX_API_KEY) # have it return full XML for now
    
    for files in sim_box_docs.file:
        print "\nFILE ID: " + files.id[0].elementText + "\nFILE NAME: " + files.name[0].elementText
    
    return HttpResponse(str(sim_box_docs))

