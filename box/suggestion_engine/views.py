from django.http import HttpResponse
import docsims
import textextract
import models
import docsearch

def do_analysis(request):
    text = textextract.extract_text()
    return HttpResponse(text)
#    sim_pairs = docsims.generate_doc_sims.delay()
#    return HttpResponse(str(sim_pairs.get()))

def get_similar_docs(request):
    path_info = request.META['PATH_INFO']
    query  = path_info[path_info.find('=')+1:]
    sim_docs = docsearch.get_similar_docs(query)
    response = []
    for doc in sim_docs:
        response.append(doc.get_stored_fields())
    
    return HttpResponse(str(response))
    
