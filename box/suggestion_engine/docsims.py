import os
from box import constants
from gensim import corpora, models, similarities
from celery.decorators import task

class IceCorpus(object):
    def __init__(self, dictionary, filenames):
        self.dictionary = dictionary
        self.filenames = filenames
        
    def __iter__(self):
        # For now, corpus iterates through docs 1 at a time
        for filename in self.filenames:
            f = open(constants.TEMP_PT_FILES_DIR + filename)
            yield self.dictionary.doc2bow(f.read().lower().split())
            f.close()
            
def get_file_info():
    filenames = list()
    file_ids = list()
    fm = open(constants.TEMP_PT_FILES_DIR + '_file_info.txt')
    for line in fm:
        s = line.split()
        filenames.append(s[0])
        file_ids.append(s[1])
    return (filenames, file_ids)

# Currently prints out all document pairs that have similarity above
# some threshold value
@task()
def generate_doc_sims():
    (filenames, file_ids) = get_file_info()

    dictionary = corpora.Dictionary()
    for filename in filenames:
        f = open(constants.TEMP_PT_FILES_DIR + filename)
        dictionary.doc2bow(f.read().lower().split(), True)
        f.close()
    
    corpus = IceCorpus(dictionary, filenames)
    sims = similarities.docsim.Similarity(corpus, 3)
    
    high_sim_pairs = list()
    for sim in sims:
        for i in range(1, len(sim)):
            sim_tuple = sim[i]
            if sim_tuple[1] < constants.SIM_INDEX_THRESHOLD: break
            high_sim_pairs.append( (filenames[sim[0][0]], filenames[sim_tuple[0]], sim_tuple[1]) )
    return high_sim_pairs