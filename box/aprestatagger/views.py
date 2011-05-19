from django.http import HttpResponse
from tagger import *
import pickle
import glob

KEYWORDS_TO_GET = 3

def keywords(request):
    weights = pickle.load(open('aprestatagger/data/dict.pkl', 'rb'))
    
    documents = glob.glob('*/tests/*')
    mytagger = Tagger(Reader(), Stemmer(), Rater(weights))
    allkeywords = []
    for doc in documents:
        with open(doc, 'r') as file:
            keywords = mytagger(file.read(), 3)
            allkeywords.append(keywords)
    return HttpResponse(str(allkeywords))