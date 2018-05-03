import json
from urllib import request, parse
import time
from urllib import parse
import ssl
from selenium import webdriver
from selenium.webdriver.support.ui import Select


#Open the bib file and parse using bibtextparser library
with open('bibjson.json', 'r') as bibtexFile:
    bibString=bibtexFile.read()
bibDB = json.loads(bibString)
#create a standard python dictionary from bibtexparser object
titles={}
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)


z=14000
l=0
paperDict={}
journals={}
papers=set()
publishers={}


for x in bibDB:
    if x['_gddid'] not in papers:
        papers.add(x['_gddid'])
        if x['publisher'] in publishers.keys():
            publishers[x['publisher']]['count']+=1
        else:
            publishers[x['publisher']] = {}
            publishers[x['publisher']]['count'] = 1
        if x['journal']['name'] in publishers[x['publisher']].keys():
            publishers[x['publisher']][x['journal']['name']]+=1
        else:
            publishers[x['publisher']][x['journal']['name']] = 1





print(publishers)
print(journals)
print(len(papers))

publisherFile=open('publisherList.txt','w')
papersFile=open('papersList.txt','w')


for x in papers:
    papersFile.write(x + '\n')
for x in publishers.keys():
    publisherFile.write(x + ' total count: ' + str(publishers[x]['count']) + '\n')
    for y in publishers[x].keys():
        if y!='count':
            publisherFile.write('    ' + y + ': ' + str(publishers[x][y]) + '\n')