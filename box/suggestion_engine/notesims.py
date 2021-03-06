import os
from box import constants
from gensim import corpora, models, similarities
from box.icebox.models import Note, NoteRevision
from BeautifulSoup import BeautifulSoup

# This line is taken from gen_stopwords/code.txt. Code generated from list of stopwords
stopwords = set(['about','above','across','after','again','against','all','almost','alone','along','already','also','although','always','among','an','and','another','any','anybody','anyone','anything','anywhere','are','area','areas','around','as','ask','asked','asking','asks','at','away','b','back','backed','backing','backs','be','became','because','become','becomes','been','before','began','behind','being','beings','best','better','between','big','both','but','by','c','came','can','cannot','case','cases','certain','certainly','clear','clearly','come','could','d','did','differ','different','differently','do','does','done','down','down','downed','downing','downs','during','e','each','early','either','end','ended','ending','ends','enough','even','evenly','ever','every','everybody','everyone','everything','everywhere','f','face','faces','fact','facts','far','felt','few','find','finds','first','for','four','from','full','fully','further','furthered','furthering','furthers','g','gave','general','generally','get','gets','give','given','gives','go','going','good','goods','got','great','greater','greatest','group','grouped','grouping','groups','h','had','has','have','having','he','her','here','herself','high','high','high','higher','highest','him','himself','his','how','however','i','if','important','in','interest','interested','interesting','interests','into','is','it','its','itself','j','just','k','keep','keeps','kind','knew','know','known','knows','l','large','largely','last','later','latest','least','less','let','lets','like','likely','long','longer','longest','m','made','make','making','man','many','may','me','member','members','men','might','more','most','mostly','mr','mrs','much','must','my','myself','n','necessary','need','needed','needing','needs','never','new','new','newer','newest','next','no','nobody','non','noone','not','nothing','now','nowhere','number','numbers','o','of','off','often','old','older','oldest','on','once','one','only','open','opened','opening','opens','or','order','ordered','ordering','orders','other','others','our','out','over','p','part','parted','parting','parts','per','perhaps','place','places','point','pointed','pointing','points','possible','present','presented','presenting','presents','problem','problems','put','puts','q','quite','r','rather','really','right','right','room','rooms','s','said','same','saw','say','says','second','seconds','see','seem','seemed','seeming','seems','sees','several','shall','she','should','show','showed','showing','shows','side','sides','since','small','smaller','smallest','so','some','somebody','someone','something','somewhere','state','states','still','still','such','sure','t','take','taken','than','that','the','their','them','then','there','therefore','these','they','thing','things','think','thinks','this','those','though','thought','thoughts','three','through','thus','to','today','together','too','took','toward','turn','turned','turning','turns','two','u','under','until','up','upon','us','use','used','uses','v','very','w','want','wanted','wanting','wants','was','way','ways','we','well','wells','went','were','what','when','where','whether','which','while','who','whole','whose','why','will','with','within','without','work','worked','working','works','would','x','y','year','years','yet','you','young','younger','youngest','your','yours','z'])

def filter_html_tags(text):
    soup = BeautifulSoup(text)
    for tag in soup.findAll(True):
        tag.hidden = True
    
    return soup.renderContents() 
    
def extract_text_from_note(note):
    wordlist = filter_html_tags(note.text).lower().split()
    filtered_wordlist = []
    for w in wordlist:
        if w not in stopwords:
            filtered_wordlist.append(w)

    return filtered_wordlist

def get_latest_note_revision(note):
    revisions = note.noterevision_set.all().order_by("-created")
    revision = None
    if revisions:
        revision = revisions[0]
    
    return revision

MAX_NUM_TO_RETURN = 5
SIM_THRESHOLD = 0
NUM_QUERY_WORDS = 3
WORD_RADIUS = 5

# Given text, returns a list of the private keys of the Note model entries that are
# deemed to be most similar.
def generate_note_sims(note_text, note_id, keywords):
    all_notes = Note.objects.all()
    texts = []
    text_revisions = []
    num_other_notes = 0
    for note in all_notes:
        revision = get_latest_note_revision(note)
        if revision is None or str(revision.note.pk) == note_id:
            continue
            
        texts.append(extract_text_from_note(revision))
        text_revisions.append(revision)
        num_other_notes = num_other_notes + 1
    
    if num_other_notes == 0:
        return []
    
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    sms = similarities.docsim.MatrixSimilarity(corpus, 10)
    vec = dictionary.doc2bow(note_text.lower().split())
    sims = sms[vec]
    
    best = [] 
    num_best = 0
    for sim in sims:
        if sim[1] < SIM_THRESHOLD or num_best >= MAX_NUM_TO_RETURN: break
       
        rev = text_revisions[sim[0]]
        rev_text = filter_html_tags(rev.text)
        words = rev_text.split()
        rev_text_lower = rev_text.lower()
        collaborators = []
        print "COLLABS:", len(rev.collaborators)
        for c in rev.collaborators:
            collaborators.append(c.email)

        sim_dict = dict({'title': rev.title, 'note': rev.note.pk, 'collaborators': ', '.join(collaborators)})

        found_keyword = False
        for keyword in keywords:
            if rev_text_lower.find(keyword) >= 0:
                w_ind = 0
                the_word = None
                for word in words:
                    if word.lower() == keyword:
                        the_word = word
                        break
                    w_ind = w_ind + 1
                if the_word is None:
                    continue
                begin_ind = w_ind - WORD_RADIUS
                end_ind = w_ind + WORD_RADIUS
                if begin_ind < 0:
                    begin_ind = 0
                num_words = len(words)
                if end_ind > num_words:
                    end_ind = num_words
                sim_dict['sim_text'] = ' '.join(words[begin_ind:end_ind])
                sim_dict['sim_word'] = the_word
                
                found_keyword = True
                break
                
                
        if found_keyword is False:
            sim_dict['sim_text'] = "couldn\'t find snippet"
            sim_dict['sim_word'] = ""
        
        best.append(sim_dict)
        num_best = num_best + 1
    return best