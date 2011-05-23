from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers

import docsims
import textextract
import models
import docsearch
import notesims

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
    path_info = request.META['PATH_INFO']
    query  = path_info[path_info.find('=')+1:]
    sim_docs = docsearch.get_similar_docs(query)
    response = []
    for doc in sim_docs:
        response.append(doc.get_stored_fields())
    
    return HttpResponse(str(response))
    
