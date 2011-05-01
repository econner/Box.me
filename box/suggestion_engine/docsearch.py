import os
from box.haystack.views import SearchView
from django.http import QueryDict
from celery.decorators import task

class FakeRequest(object):
    def __init__(self, get):
        self.GET = get

def get_similar_docs(query):
    s = SearchView()
    q = QueryDict('q=' + query)
    s.request = FakeRequest(q)
    s.form = s.build_form()
    
    return s.get_results()

@task()
def update_suggestion_engine():
     #Pull latest files from Box and save to db
    
    #Rebuild index
    os.system('python manage.py rebuild_index')