from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core import serializers

import textextract
import models
import notesims
import os

import pickle
import boxdocsims
from aprestatagger.tagger import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as auth_logout
from notesims import filter_html_tags
from boxdotnet import BoxDotNet

MAX_DOCS = 6
dict_path = os.path.join(settings.PROJECT_ROOT, 'box/suggestion_engine/aprestatagger/data/dict.pkl')
weights = pickle.load(open(dict_path, 'rb'))
mytagger = Tagger(Reader(), Stemmer(), Rater(weights))

def get_keywords_from_text(text, num_query_words):
    keywords_raw = mytagger(text, num_query_words) 
    keywords = []
    for word in keywords_raw: 
        without_quotes = str(word)[1:-1] #remove enclosing quotes
        single_words = without_quotes.split() #keyword may be multiple words
        keywords.extend(single_words)
    return keywords
    
def get_similar_notes(request):   
    text = request.POST['text']
    text = filter_html_tags(text)
    note_id = request.POST['note_id']
    keywords = get_keywords_from_text(text, 1 + len(text) / 20)
    sim_note_revs = notesims.generate_note_sims(text, note_id, keywords)
    print sim_note_revs
    json = simplejson.dumps(sim_note_revs) 
    return HttpResponse(json, mimetype='application/json')

     
def get_similar_docs(request):
    profile = request.user.get_profile()
    text = request.POST['text']
    text = filter_html_tags(text)
    
    keywords = get_keywords_from_text(text, 2)
    
    query = ' '.join(keywords)
    sim_box_docs = boxdocsims.box_search_file(profile, query, settings.BOX_API_KEY)

    files_info = []
    if sim_box_docs == -1:
        return HttpResponse(BoxDotNet().get_login_url(settings.BOX_API_KEY))
    elif sim_box_docs is not None:
        num_docs = 1
        for files in sim_box_docs.file:
            if num_docs > MAX_DOCS:
                break
            file_id = files.id[0].elementText
            file_name = files.name[0].elementText
            url = boxdocsims.box_preview(file_id, profile, settings.BOX_API_KEY)
            files_info.append(dict(file_id=file_id, file_name=file_name, url=url))
            num_docs = num_docs + 1
            
    json = simplejson.dumps(files_info)
    return HttpResponse(json, mimetype='application/json')

