import json
from urllib import request, parse
import time
from urllib import parse
import ssl
from selenium import webdriver
from selenium.webdriver.support.ui import Select

url='https://patron.library.wisc.edu/authn/login?url=' \
    'https://mathscinet-ams-org.ezproxy.library.wisc.edu/mathscinet/index.html'
path=os.path.dirname(os.path.abspath(__file__))
file1=open(path + '/paperData/' + 'mathReviewInfo1.txt', 'a')
file1.write('title,gddid,mrNumber,mrURL,mrCode\n')
browser=webdriver.Chrome()

x=browser.get(url)

select=Select(browser.find_element_by_id('campus-select'))
select.select_by_visible_text('UW-Madison')
browser.find_element_by_id('submit-go').click()
userName=''
password=''

uName = browser.find_element_by_id("j_username") #username form field
pWord = browser.find_element_by_id("j_password") #password form field
uName.send_keys(userName)
pWord.send_keys(password)
submitButton = browser.find_element_by_name('_eventId_proceed')
submitButton.click()

#Open the bib file and parse using bibtextparser library
with open(path + '/paperData/' +'bibjson.json', 'r') as bibtexFile:
    bibString=bibtexFile.read()
bibDB = json.loads(bibString)
#create a standard python dictionary from bibtexparser object
titles={}
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)


z=0
l=0
paperDict={}
while z<len(bibDB):
    paperDict[l]={}
    j=0
    fullBatchString=''
    while j < 25:
        if z < len(bibDB):
            x = bibDB[z]
        else:
            break
        paperDict[l][j]={}
        paperDict[l][j]['title']=x['title']
        paperDict[l][j]['_gddid'] = x['_gddid']
        j+=1
        z+=1
        batchString='|'+x['journal']['name']+'|'
        for y in x['author']:
            lastName=y['name'].split(',')[0]
            batchString+=lastName + ' and '
        batchString=batchString[:-1] + '|' + x['volume'] + '|' + x['number'] + '||' + x['year'] + '||||' + x['title'] + '\n'
        batchString = parse.quote(batchString)
        fullBatchString+=batchString
    mathBatchLookup='http://www.ams.org/batchmrlookup?&api=xref&qdata=' + fullBatchString
    req = request.Request(mathBatchLookup, headers={'User-Agent': USER_AGENT})
    feedRequest = request.urlopen(req, timeout=60, context=context)
    batchResponse=feedRequest.read()
    print(batchResponse)
    batchResponseList=str(batchResponse).split('\\n')
    mrNumbers=[]
    d=0
    for k in batchResponseList:
        if k.count('|')>=9:
            mrNum=k.split('|')[9]
            mrNumbers.append(mrNum)
            # mrNum='3554722'
            paperDict[l][d]['mrNumber']=mrNum
            paperDict[l][d]['msnURL']='https://mathscinet-ams-org.ezproxy.library.wisc.edu/mathscinet/' \
                                                'search/publdoc.html?arg3=&co4=AND&co5=AND&co6=AND&co7=AND&dr=all&pg4=' \
                                                'MR&pg5=TI&pg6=PC&pg7=ALLF&pg8=ET&r=1&review_format=html&s4={}&s5=' \
                                                '&s6=&s7=&s8=All&sort=Newest&vfpref=html&yearRangeFirst=' \
                                                '&yearRangeSecond=&yrop=eq'.format(mrNum)
            # reqMathSciNet = request.Request(urlString, headers={'User-Agent': USER_AGENT})
            # responseMathSciNet = request.urlopen(req, timeout=60, context=context)
            # mathSciNetPage = feedRequest.read()
            url = paperDict[l][d]['msnURL']
            x = browser.get(url)
            time.sleep(2)
            mathSciNetPage = browser.execute_script("return document.body.innerHTML")
            codeLocation=mathSciNetPage.find('/mathscinet/search/mscdoc.html?code=')
            codeLocation2=mathSciNetPage.find('"',codeLocation+37)
            mrCode=mathSciNetPage[codeLocation+36:codeLocation2]
            paperDict[l][d]['mrCode']=mrCode.replace('(','').replace(')','').strip()
            writeString = ''
            for e in paperDict[l][d].keys():
                writeString = writeString + paperDict[l][d][e] + ','
            writeString = writeString + str(l * 25 + d)
            file1.write(writeString)
            file1.write('\n')
            d += 1
    l+=6




