# set up logging so we see what's going on
#This is all based off of a tutorial found here: https://rare-technologies.com/tutorial-on-mallet-in-python/#gensim_wrapper

import logging
import os
from gensim import corpora, models, utils
import random
import psycopg2
import math
import os
import datetime
# Define our connection string

def modelTopics(runType):
    connString = "host='' dbname='' user='' password=''"
    timeHash = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    dirPath = os.path.dirname(os.path.realpath(__file__))
    fileDir = dirPath + '/{}/' + timeHash
    fileDir.format(runType)
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)

    def iterDocuments(corpusList):
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(connString)
        for x in corpusList:
            # get text of document from
            # parse document into a list of utf8 tokens
            # cur=conn.cursor
            sql='select array_to_string(array_agg(sentence),\' \') as sentences ' \
                'from (SELECT docid, array_to_string(words, \' \') as sentence ' \
                'FROM sentences) as s where docid=\'{}\' ;'.format(x)
            # cur.execute(sql)
            cursor = conn.cursor()
            cursor.execute(sql)
            doc=cursor.fetchall()
            document=''.join(doc[0])
            # does preprocessing and tokenization
            yield utils.simple_preprocess(document)
        conn.close()

    class trainingCorpus(object):
        def __init__(self, corpusList):
            self.corpusList = corpusList
            self.dictionary = corpora.Dictionary(iterDocuments(corpusList))
            self.dictionary.filter_extremes()  # remove stopwords etc

        def __iter__(self):
            for tokens in iterDocuments(self.corpusList):
                yield self.dictionary.doc2bow(tokens)


    def determineCorpusSample():
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(connString)
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()
        # get all doument ids
        cursor.execute('Select distinct docid from sentences')
        docIds=cursor.fetchall()
        numDocs=len(docIds)
        corpLen=math.ceil(numDocs/3)
        # split off 1/3 to build the corpus dictionary
        sampleIDs=random.sample(docIds,corpLen)
        corpIDs=[]
        for x in sampleIDs:
            corpIDs.append(''.join(x))
            docIds.remove(x)
        toModelIDs=[]
        for x in docIds:
            toModelIDs.append(''.join(x))
        conn.close()
        return corpIDs, toModelIDs



    corpusIDs=[]
    modellingIDs=[]
    corpusIDs, modellingIDs=determineCorpusSample()
    #build the corpus
    corpus=trainingCorpus(corpusIDs)
    # point gensim lda wrapper at mallet
    malletPath = '/Users/samuelhansen/Downloads/mallet-2.0.8/bin/mallet'
    # create the model
    model = models.wrappers.LdaMallet(malletPath, corpus, num_topics=10, id2word=corpus.dictionary)
    with open(fileDir + '/' + 'topics.txt','a') as topicFile:
        for x in model.print_topics(10,20):
            topicFile.write(''.join(str(x)))
            topicFile.write('\n')
    conn = psycopg2.connect(connString)
    for x in modellingIDs:
        # parse document into a list of utf8 tokens
        sql = 'select array_to_string(array_agg(sentence),\' \') as sentences ' \
              'from (SELECT docid, array_to_string(words, \' \') as sentence ' \
              'FROM sentences) as s where docid=\'{}\' ;'.format(x)
        # cur.execute(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        doc = cursor.fetchall()
        document = ''.join(doc[0])
        #determine a document's topics
        bow = corpus.dictionary.doc2bow(utils.simple_preprocess(document))
        with open(fileDir + '/' + x + '.txt','a') as docFile:
            docFile.write(x)
            docFile.write('\n')
            for y in model[bow]: # print list of (topic id, topic weight) pairs
                docFile.write(''.join(str(y)))
                docFile.write('\n')

runTypes=['words','lemmas']
for x in runTypes:
    modelTopics(x)
