from django.http import HttpResponse
import docsims
import models

def do_analysis(request):
    sim_pairs = docsims.generate_doc_sims.delay()
    return HttpResponse(str(sim_pairs.get()))