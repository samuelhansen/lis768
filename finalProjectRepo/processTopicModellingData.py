import os
import itertools

path=os.path.dirname(os.path.abspath(__file__))
wordsModelPath=path + '/topModelResults/words/'
lemmasModelPath=path + '/topModelResults/lemmas/'

modelDict={}
topicDict={}

modelFile=open('topModelCSV.csv', 'r')
paperList=modelFile.readlines()
for x in paperList[1:]:
    y=x.split(',')
    if y[2] in modelDict.keys():
        if y[1] in modelDict[y[2]].keys():
            if int(y[3]) in modelDict[y[2]][y[1]].keys():
                modelDict[y[2]][y[1]][int(y[3])]['percent'] = float(y[4].strip())
                modelDict[y[2]][y[1]]['type'] = y[0]
            else:
                modelDict[y[2]][y[1]][int(y[3])] = {}
                modelDict[y[2]][y[1]][int(y[3])]['percent'] = float(y[4].strip())
                modelDict[y[2]][y[1]]['type'] = y[0]
        else:
            modelDict[y[2]][y[1]] = {}
            modelDict[y[2]][y[1]][int(y[3])] = {}
            modelDict[y[2]][y[1]][int(y[3])]['percent'] = float(y[4].strip())
            modelDict[y[2]][y[1]]['type'] = y[0]
    else:
        modelDict[y[2]]={}
        modelDict[y[2]][y[1]] = {}
        modelDict[y[2]][y[1]][int(y[3])]={}
        modelDict[y[2]][y[1]][int(y[3])]['percent'] = float(y[4].strip())
        modelDict[y[2]][y[1]]['type'] = y[0]



topicFile=open('topicsCSVCoded.csv', 'r')
topicList=topicFile.readlines()
for x in topicList[1:]:
    y=x.split(',')
    if y[1] in topicDict.keys():
        if int(y[3]) in topicDict[y[1]].keys():
            topicDict[y[1]][int(y[3])].append([float(y[4]), 'Undefined' if y[6].strip()=='' else y[6].strip()])
        else:
            topicDict[y[1]][int(y[3])] = []
            topicDict[y[1]][int(y[3])].append([float(y[4]),'Undefined' if y[6].strip()=='' else y[6].strip()])
    else:
        topicDict[y[1]]={}
        topicDict[y[1]][int(y[3])] = []
        topicDict[y[1]][int(y[3])].append([float(y[4]),'undefined' if y[6].strip()=='' else y[6].strip()])

# for x in topicDict.keys():
#     for y in topicDict[x].keys():
#         print(x)
#         print(y)
#         input(topicDict[x][y])
#         break
#     break
# print(topicDict['20180417_1243'][0])

for x in modelDict.keys():
    for y in modelDict[x].keys():
        for z in modelDict[x][y]:
            if z != 'type':
                modelDict[x][y][z]['codes']={}
                modelDict[x][y][z]['codes']['codesPercent']={}
                modelDict[x][y][z]['codes']['codesTotal']={}
                modelDict[x][y][z]['codes']['list']=[]
                for j in topicDict[y][z]:
                    if j[1] in modelDict[x][y][z]['codes']['list']:
                        modelDict[x][y][z]['codes']['codesPercent'][j[1]] += j[0]
                        modelDict[x][y][z]['codes']['codesTotal'][j[1]] += 1
                    else:
                        modelDict[x][y][z]['codes']['codesPercent'][j[1]] = j[0]
                        modelDict[x][y][z]['codes']['codesTotal'][j[1]] = 1
                        modelDict[x][y][z]['codes']['list'].append(j[1])
                modelDict[x][y][z]['codes']['list']=sorted(modelDict[x][y][z]['codes']['list'], key=str.lower)


for x in modelDict.keys():
    for y in modelDict[x].keys():
        file=open('paperCodeValues' + y, 'a')
        codeList = []
        topicCodePerValues = {}
        topicCodeTotalValues = {}
        topicCodePerCountValues = {}
        topicCodeString = ''
        for z in modelDict[x][y].keys():
            if z != 'type':
                for k in modelDict[x][y][z]['codes']['list']:
                    if k not in codeList:
                        codeList.append(k)
                        topicCodePerValues[k] = modelDict[x][y][z]['codes']['codesPercent'][k] * \
                                                modelDict[x][y][z]['percent']
                        topicCodePerCountValues[k] = modelDict[x][y][z]['codes']['codesTotal'][k] * \
                                                     modelDict[x][y][z]['percent']
                        topicCodeTotalValues[k] = modelDict[x][y][z]['codes']['codesTotal'][k]
                    else:
                        topicCodePerValues[k] += modelDict[x][y][z]['codes']['codesPercent'][k] * \
                                                modelDict[x][y][z]['percent']
                        topicCodePerCountValues[k] += modelDict[x][y][z]['codes']['codesTotal'][k]* \
                                                     modelDict[x][y][z]['percent']
                        topicCodeTotalValues[k] += modelDict[x][y][z]['codes']['codesTotal'][k]


        topicCodeString += ',totals'
        maxCode=''
        maxCodeValue=0
        code2=''
        code2Value=0
        for l in codeList:
            if topicCodePerValues[l]>maxCodeValue:
                if maxCodeValue>code2Value:
                    code2Value=maxCodeValue
                    code2=maxCode
                maxCode=l
                maxCodeValue=topicCodePerValues[l]
            elif topicCodePerValues[l]>code2Value:
                code2=l
                code2Value=topicCodePerValues[l]
            topicCodeString += ',' + l + ',' + str(topicCodePerValues[l])
        #startString='paperID,run,totals,code,percent,code,percent,code,percent,code,percent,code,percent,code,percent,code,percent,code,percent,code,percent,maxCode,maxpercent,code2,code2percent'
        fullPaperCodeString = str(x) + ',' + str(y) + topicCodeString + ',' + maxCode + ',' + \
                              str(maxCodeValue) + ',' + code2 + ',' + str(code2Value)
        file.write(fullPaperCodeString + '\n')
    # for x in modelDict.keys():
    #     for y in modelDict[x].keys():
    #         topicCodeString=''
    #         for z in modelDict[x][y].keys():
    #             if z != 'type':
    #                 for k in modelDict[x][y][z]['codes']:
    #                     if k not in codeList:
    #                         codeList.append(k)
    #
    #                 topicCodeString+=',' + str(z) + ',' + str(modelDict[x][y][z]['percent'])
    #                 for j in modelDict[x][y][z]['codes']['list']:
    #                     topicCodeString += ',' + j + ',' +  str(modelDict[x][y][z]['codes']['codesPercent'][j]) +\
    #                                        ',' + str(modelDict[x][y][z]['codes']['codesTotal'][j])
    #         fullPaperCodeString=str(x) + ',' + str(y) + topicCodeString
    #         file.write(fullPaperCodeString + '\n')