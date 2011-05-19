import os
from box import constants
from gensim import corpora, models, similarities
from celery.decorators import task
from box.icebox.models import Note, NoteRevision

dummy_texts = [ 'the cat and the dog went to the park and used an iPhone', \
    'yesterday, i visited my cat and dog, then scolded them for going to the park and using my brand-new iPhone',\
     'i have a feeling that this will work. then again, many things do not seem to work nowadays',\
      'i am going to randomly insert words such as cat dog and iPhone to test the docsim stuff park']
      
sim_threshold = 0
      
def create_dummy_noterevisions():
    for i in range(1,len(dummy_texts)+1):
       note = Note.objects.get(pk=i)
       
       revision = NoteRevision(note=note)

       revision.text = dummy_texts[i-1]
       revision.title = 'the note num ' + str(i)
       revision.save()
           
def get_note_revision(note):
    revisions = note.noterevision_set.all().order_by("-created")
    revision = None
    if revisions:
        revision = revisions[0]
    
    return revision

# Given text, returns a list of the private keys of the Note model entries that are
# deemed to be most similar.
def generate_note_sims(note_text):
    all_notes = Note.objects.all()
    
    texts = []
    text_ids = []
    for note in all_notes:
        revision = get_note_revision(note)
        texts.append(revision.text.lower().split())
        text_ids.append(note.pk)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    sms = similarities.docsim.MatrixSimilarity(corpus, 10)
    
    vec = dictionary.doc2bow(note_text.lower().split())
    sims = sms[vec]
    
    best = [] 
    for sim in sims:
        if sim[1] < sim_threshold: break
        best.append(text_ids[sim[0]])
        
    return best