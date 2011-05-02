import os
from box import constants
from box.haystack.views import SearchView
from django.http import QueryDict
from celery.decorators import task
from suggestion_engine import models, textextract

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
    # Save latest files from Box into temp_files directory
    
     
    # Convert files in temp_files into plain text and save to db
    # Then, clean up files in temp_files
    for filename in os.listdir(constants.TEMP_FILES_DIR):
        extracted_text = textextract.extract_text(filename)
        d = models.Document(file_id=100, last_changed='1990-10-18', text=extracted_text)
        d.save()
        # Delete once done processing
        os.remove(constants.TEMP_FILES_DIR + filename)
    
    
    # Rebuild index
    os.system('python manage.py rebuild_index')