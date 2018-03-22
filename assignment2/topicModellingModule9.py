# set up logging so we see what's going on
#This is all based off of a tutorial found here: https://rare-technologies.com/tutorial-on-mallet-in-python/#gensim_wrapper

import logging
import os
from gensim import corpora, models, utils
import gensim
# logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)


def iter_documents(reuters_dir):
    """Iterate over Reuters documents, yielding one document at a time."""
    for fname in os.listdir(reuters_dir):
        # read each document as one big string
        document = open(os.path.join(reuters_dir, fname)).read()
        # parse document into a list of utf8 tokens
        yield utils.simple_preprocess(document)


class trainingCorpus(object):
    def __init__(self, reuters_dir):
        self.reuters_dir = reuters_dir
        self.dictionary = corpora.Dictionary(iter_documents(reuters_dir))
        self.dictionary.filter_extremes()  # remove stopwords etc

    def __iter__(self):
        for tokens in iter_documents(self.reuters_dir):
            yield self.dictionary.doc2bow(tokens)


# set up the streamed corpus
documentPath='Path To Documents to Model'
corpus = trainingCorpus('Path To Corpus')
# INFO : adding document #0 to Dictionary(0 unique tokens: [])
# INFO : built Dictionary(24622 unique tokens: ['mdbl', 'fawc', 'degussa', 'woods', 'hanging']...) from 7769 documents (total 938238 corpus positions)
# INFO : keeping 7203 tokens which were in no less than 5 and no more than 3884 (=50.0%) documents
# INFO : resulting dictionary: Dictionary(7203 unique tokens: ['yellow', 'four', 'resisted', 'cyprus', 'increase']...)

# train 10 LDA topics using MALLET
mallet_path = '/Users/samuelhansen/Downloads/mallet-2.0.8/bin/mallet'
model = models.wrappers.LdaMallet(mallet_path, corpus, num_topics=10, id2word=corpus.dictionary)
# print(model[my_vector])
# ...
# 0 5   spokesman ec government tax told european today companies president plan added made commission time statement chairman state national union
# 1 5   oil prices price production gas coffee crude market brazil international energy opec world petroleum bpd barrels producers day industry
# 2 5   trade japan japanese foreign economic officials united countries states official dollar agreement major told world yen bill house international
# 3 5   bank market rate stg rates exchange banks money interest dollar central week today fed term foreign dealers currency trading
# 4 5   tonnes wheat sugar mln export department grain corn agriculture week program year usda china soviet exports south sources crop
# 5 5   april march corp record cts dividend stock pay prior div board industries split qtly sets cash general share announced
# 6 5   pct billion year february january rose rise december fell growth compared earlier increase quarter current months month figures deficit
# 7 5   dlrs company mln year earnings sale quarter unit share gold sales expects reported results business canadian canada dlr operating
# 8 5   shares company group offer corp share stock stake acquisition pct common buy merger investment tender management bid outstanding purchase
# 9 5   mln cts net loss dlrs shr profit qtr year revs note oper sales avg shrs includes gain share tax
#
# <1000> LL/token: -7.5002
#
# Total time: 34 seconds
# input(model.print_topics(num_topics=10))
# # now use the trained model to infer topics on a new document
for fname in os.listdir(documentPath):
    # read each document as one big string
    doc = open(os.path.join(documentPath, fname)).read()
    # parse document into a list of utf8 tokens
    # doc=utils.simple_preprocess(document)
    bow = corpus.dictionary.doc2bow(utils.simple_preprocess(doc))
    print(fname)
    for x in model[bow]: # print list of (topic id, topic weight) pairs
        print(x)
    print('\n')
# [[(0, 0.0903954802259887),
#   (1, 0.13559322033898305),
#   (2, 0.11299435028248588),
#   (3, 0.0847457627118644),
#   (4, 0.11864406779661017),
#   (5, 0.0847457627118644),
#   (6, 0.0847457627118644),
#   (7, 0.10357815442561205),
#   (8, 0.09981167608286252),
#   (9, 0.0847457627118644)]]