import os
import itertools

path=os.path.dirname(os.path.abspath(__file__))
wordsModelPath=path + '/topModelResults/words/'
lemmasModelPath=path + '/topModelResults/lemmas/'

modelDict={}
modelDict['lemmas'] = {}
modelDict['words'] = {}

for x in os.listdir(lemmasModelPath):
    if not os.path.isfile(lemmasModelPath + x):
        modelDict['lemmas'][x] = {}
        modelDict['lemmas'][x]['topics'] = {}
        with open(lemmasModelPath + x + '/topics.txt', 'r') as file:
            topicStrings = file.readlines()
        for z in topicStrings:
            z=z.replace('(','').replace(')','').replace('\'','').replace('\"','').replace(' ','').replace('\n','')
            topicsAndID=z.split(',')
            modelDict['lemmas'][x]['topics'][topicsAndID[0]] = []
            topicsAndValues=topicsAndID[1].split('+')
            allTopicsList=[]
            for j in topicsAndValues:
                topicsAndPercent=j.split('*')
                modelDict['lemmas'][x]['topics'][topicsAndID[0]].append(topicsAndPercent)
                allTopicsList.append(topicsAndPercent[1])
            modelDict['lemmas'][x]['topics'][str(topicsAndID[0])+'pairsx']=list(itertools.combinations(allTopicsList,2))
        for y in os.listdir(lemmasModelPath + x + '/'):
            if y!='topics.txt':
                with open(lemmasModelPath + x + '/' + y, 'r') as file:
                    topModFile=file.readlines()
                docId=topModFile[0].replace('\n','')
                modelDict['lemmas'][x][docId]=[]
                for k in topModFile[1:]:
                    k=k.replace('(','').replace(')','').replace(' ','').replace('\n','')
                    topPercent=k.split(',')
                    topPercent[0]=topPercent[0]
                    topPercent[1]=topPercent[1]
                    modelDict['lemmas'][x][docId].append(topPercent)

for x in os.listdir(wordsModelPath):
    if not os.path.isfile(wordsModelPath + x):
        modelDict['words'][x] = {}
        modelDict['words'][x]['topics'] = {}
        with open(wordsModelPath + x + '/topics.txt', 'r') as file:
            topicStrings = file.readlines()
        for z in topicStrings:
            z=z.replace('(','').replace(')','').replace('\'','').replace('\"','').replace(' ','').replace('\n','')
            topicsAndID=z.split(',')
            modelDict['words'][x]['topics'][topicsAndID[0]] = []
            topicsAndValues=topicsAndID[1].split('+')
            allTopicsList=[]
            for j in topicsAndValues:
                topicsAndPercent=j.split('*')
                modelDict['words'][x]['topics'][topicsAndID[0]].append(topicsAndPercent)
                allTopicsList.append(topicsAndPercent[0])
                modelDict['words'][x]['topics'][str(topicsAndID[1]) + 'pairsx'] = list(itertools.combinations(allTopicsList, 2))
        for y in os.listdir(wordsModelPath + x + '/'):
            if y!='topics.txt':
                with open(wordsModelPath + x + '/' + y, 'r') as file:
                    topModFile=file.readlines()
                docId=topModFile[0].replace('\n','')
                modelDict['words'][x][docId]=[]
                for k in topModFile[1:]:
                    k=k.replace('(','').replace(')','').replace(' ','').replace('\n','')
                    topPercent=k.split(',')
                    modelDict['words'][x][docId].append(topPercent)


with open('topModelCSV', 'w') as file:
    for x in modelDict.keys():
        for y in modelDict[x].keys():
            for z in modelDict[x][y].keys():
                if z!='topics' and z!='topicPairs':
                    for a in modelDict[x][y][z]:
                        file.write(x +','+y+','+z+','+a[0]+','+a[1]+'\n')

with open('topicsCSV', 'w') as file:
    for x in modelDict.keys():
        for y in modelDict[x].keys():
            for z in modelDict[x][y].keys():
                if z=='topics':
                    for a in modelDict[x][y][z].keys():
                        if 'pairsx' not in a:
                            for b in modelDict[x][y][z][a]:
                                file.write(x +','+y+','+z+','+a+','+b[0]+','+b[1]+'\n')

with open('topicPairsCSV', 'w') as file:
    for x in modelDict.keys():
        for y in modelDict[x].keys():
            for z in modelDict[x][y].keys():
                if z=='topics':
                    for a in modelDict[x][y][z].keys():
                        if 'pairsx' in a:
                            for b in modelDict[x][y][z][a]:
                                file.write(x +','+y+','+z+','+a+','+'('+','.join(b)+')\n')