from box.haystack.views import SearchView
from django.http import QueryDict

class FakeRequest(object):
    def __init__(self, get):
        self.GET = get
        
def get_similar_docs(query):
    s = SearchView()
    q = QueryDict('q=' + query)
    s.request = FakeRequest(q)
    s.form = s.build_form()
    
    print "HERERR GANGSTA: " + str(s.get_results())
    
    return s.get_results()