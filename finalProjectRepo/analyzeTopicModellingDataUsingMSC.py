import os
import itertools
import re

path=os.path.dirname(os.path.abspath(__file__))
wordsModelPath=path + '/topModelResults/words/'
lemmasModelPath=path + '/topModelResults/lemmas/'

codeDict={}
runCodesDict={}
paperCodesDict={}

def analyzeRuns(runList,type):
    allCodes=set()
    allIDs=set()
    graphTheoryPapers=set()
    mscPapers=set()
    mscRE=re.compile('^[0-9]{2}[A-Z]{1}[0-9]{2}$')
    for x in runList:
        runPaperCodeFile=open(path + '/runsAnalysis/paperCodeValues' + x + '.csv', 'r')
        mscPaperCodeFile=open(path + '/paperData/mathReviewInfo1.txt','r')
        runPaperCodeList=runPaperCodeFile.readlines()
        mscPaperCodeList=mscPaperCodeFile.readlines()
        for y in runPaperCodeList[1:]:
            z=y.split(',')
            paperID=z[0]
            paperCode1=z[21]
            paperCode2=z[23]
            allIDs.add(paperID)
            allCodes.add(paperCode1)
            allCodes.add(paperCode2)
            if paperID in paperCodesDict.keys():
                paperCodesDict[paperID][x]=paperCode1 + ',' + paperCode2
                if paperCode1 in paperCodesDict[paperID]['codes1'].keys():
                    paperCodesDict[paperID]['codes1'][paperCode1] += 1
                else:
                    paperCodesDict[paperID]['codes1'][paperCode1] = 1
                if paperCode2 in paperCodesDict[paperID]['codes2'].keys():
                    paperCodesDict[paperID]['codes2'][paperCode2] += 1
                else:
                    paperCodesDict[paperID]['codes2'][paperCode2] = 1
            else:
                paperCodesDict[paperID] = {}
                paperCodesDict[paperID][x] = paperCode1 + ',' + paperCode2
                paperCodesDict[paperID]['codes1'] = {}
                paperCodesDict[paperID]['codes1'][paperCode1] = 1
                paperCodesDict[paperID]['codes2'] = {}
                paperCodesDict[paperID]['codes2'][paperCode2] = 1
                paperCodesDict[paperID]['mscValues'] = ''
                paperCodesDict[paperID]['mscGTYesNo'] = ''
        for y in mscPaperCodeList[1:]:
            z=y[:-1].split(',')
            mscCodes=''
            mscGT='No'
            l=0
            for k in z:
                l += 1
                if k[0:4]=='http':
                    startIndex=l
            for j in z[startIndex:-1]:
                if mscRE.match(j):
                    mscCodes+= j + ' '
                    if '05C' in j or j in ['68R10', '81Q30', '81T15', '82B20', '82C20', '90C35', '92E10', '94C15']:
                        graphTheoryPapers.add(z[startIndex-3])
                        mscGT='Yes'
            if mscCodes!='':
                mscPaperID=z[startIndex-3]
                mscPapers.add(mscPaperID)
                if mscPaperID in allIDs:
                    paperCodesDict[mscPaperID]['mscValues']=mscCodes
                    paperCodesDict[mscPaperID]['mscGTYesNo']=mscGT

    for x in allIDs:
        for y in runList:
            if y not in paperCodesDict[x].keys():
                paperCodesDict[x][y]=','
    for x in allIDs:
        for y in allCodes:
            if y not in paperCodesDict[x]['codes2'].keys():
                paperCodesDict[x]['codes2'][y]=0
        if 'graph theory' not in paperCodesDict[x]['codes1'].keys():
            paperCodesDict[x]['codes1']['graph theory'] = 0
        if 'Undefined' not in paperCodesDict[x]['codes1'].keys():
            paperCodesDict[x]['codes1']['Undefined'] = 0

    paperTopicMSCMatch={}
    paperTopicMSCMatch['correct']=0
    paperTopicMSCMatch['notMSCGTmodelGT'] = 0
    paperTopicMSCMatch['mscGTNotModelGT'] = 0
    paperTopicMSCMatch['correctUsingCode2']=0
    paperTopicMSCMatch['notMSCGTmodelGTUsingCode2'] = 0
    paperTopicMSCMatch['mscGTNotModelGTUsingCode2'] = 0
    papersCount=0
    papersCount2 = 0
    papersCountAll = 0
    for x in mscPapers:
        if x in allIDs:
            papersCountAll += 1
            if paperCodesDict[x]['codes1']['graph theory']>0:
                if x in graphTheoryPapers:
                    paperTopicMSCMatch['correct'] += 1
                    papersCount += 1
                else:
                    paperTopicMSCMatch['notMSCGTmodelGT'] += 1
            else:
                if x in graphTheoryPapers:
                    paperTopicMSCMatch['mscGTNotModelGT'] += 1
                    papersCount += 1
        if x in allIDs:
            if paperCodesDict[x]['codes1']['graph theory']>0 or paperCodesDict[x]['codes2']['graph theory']>0:
                if x in graphTheoryPapers:
                    paperTopicMSCMatch['correctUsingCode2'] += 1
                    papersCount2 += 1
                else:
                    paperTopicMSCMatch['notMSCGTmodelGTUsingCode2'] += 1
            else:
                if x in graphTheoryPapers:
                    paperTopicMSCMatch['mscGTNotModelGTUsingCode2'] += 1
                    papersCount2 += 1

    currentDir = os.path.dirname(os.path.realpath(__file__))
    countFileDir = currentDir + '/runsAnalysis/' + type + '/'
    if not os.path.exists(countFileDir):
        os.makedirs(countFileDir)
    countFile=open(countFileDir + 'paperCountData.txt','w')
    countFile.write('Count papers with MSC value: ')
    countFile.write(str(papersCountAll))
    countFile.write('\n Count papers with an MSC Graph Theory Value: ')
    countFile.write(str(papersCount))
    countFile.write('\n Count papers with highest percentage model value being graph '
                    'theory that are graph theory according to MSC: ')
    countFile.write(str((paperTopicMSCMatch['correct'])))
    countFile.write('\n Count papers with highest percentage model value being graph '
                    'theory that are not graph theory according to MSC: ')
    countFile.write(str((paperTopicMSCMatch['notMSCGTmodelGT'])))
    countFile.write('\n Count papers with highest percentage model value not being graph '
                    'theory that are graph theory according to MSC: ')
    countFile.write(str((paperTopicMSCMatch['mscGTNotModelGT'])))
    countFile.write('\n Count papers with highest or second highest percentage model value being graph '
                    'theory that are graph theory according to MSC: ')
    countFile.write(str((paperTopicMSCMatch['correctUsingCode2'])))
    countFile.write('\n Count papers with highest or second highest percentage model value being graph '
                    'theory that are not graph theory according to MSC: ')
    countFile.write(str((paperTopicMSCMatch['notMSCGTmodelGTUsingCode2'])))
    countFile.write('\n Count papers with highest or second highest percentage model value not being graph '
                    'theory that are graph theory according to MSC: ')
    countFile.write(str((paperTopicMSCMatch['mscGTNotModelGTUsingCode2'])))
    paperFileDir=currentDir + '/runsAnalysis/' + type + '/'
    if not os.path.exists(paperFileDir):
        os.makedirs(paperFileDir)
    paperFile=open(paperFileDir + 'paperMSCAndCodes1and2.csv','w')
    paperFile.write('paperID,mscCodes,mscGraphTheoryYesNo,graphTheory,Undefined')
    for x in allCodes:
        paperFile.write(',' + x + 'asCode2')
    for x in runList:
        paperFile.write(',' + x + 'code1,' + x + 'code2')
    paperFile.write('\n')
    for x in paperCodesDict.keys():
        paperFile.write(x + ',' + paperCodesDict[x]['mscValues'] + ',' + paperCodesDict[x]['mscGTYesNo'] + ',' +
                        str(paperCodesDict[x]['codes1']['graph theory']) + ','
                        + str(paperCodesDict[x]['codes1']['Undefined']))
        for y in allCodes:
            paperFile.write(',' + str(paperCodesDict[x]['codes2'][y]))
        for y in runList:
            paperFile.write(',' + paperCodesDict[x][y])
        paperFile.write('\n')

allRunsList=['20180417_1243','20180418_0913','20180416_0825','20180413_0920','20180416_1241','20180417_1554']
lemmaRunList=['20180417_1243','20180418_0913','20180416_0825']
wordRunList=['20180413_0920','20180416_1241','20180417_1554']

analyzeRuns(allRunsList, 'all')
analyzeRuns(lemmaRunList, 'lemma')
analyzeRuns(wordRunList, 'word')