import os
import itertools
import math

path=os.path.dirname(os.path.abspath(__file__))
path+='/runsAnalysis'
def round_sigfigs(num, sig_figs):
    if num != 0:
        return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
    else:
        return 0  # Can't take the log of 0

textFileList=['wordRunsProb.txt','lemmaRunsProb.txt','allRunsProb.txt']
for x in textFileList:
    file=open(x,'r')
    perList=file.readlines()
    perDict={}
    for y in perList:
        if '=' not in y:
            currentType=y.strip()
            perDict[currentType]={}
        else:
            z=y.split('=')
            perType=z[0].strip()
            perString=z[1].strip()
            q=perString.split('/')
            perValue=round_sigfigs(int(q[0])/int(q[1])*100,4)
            perDict[currentType][perType]=[perString,perValue]
    writeFileName=x.split('.')[0]+'.csv'
    writeFile=open(path + '/' + writeFileName,'w')
    for x in perDict.keys():
        columnString=''
        valuesString=''
        writeFile.write(x + '\n')
        for y in perDict[x].keys():
            writeFile.write(y + ',' + perDict[x][y][0] + ',' + str(perDict[x][y][1]) + '\n')