from bs4 import BeautifulSoup
import urllib
import re
import sys

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib import urlopen

relations = []
#'Page','Location','Word','Vector_representation','Relative_Position','IsNER','InLink','Relations','RelatedWords','General_Rank','Relative_Rank'

'''Defining URLS'''
#url1 = "http://csee.essex.ac.uk/staff/udo/index.html"
url1 = "https://www.essex.ac.uk/departments/computer-science-and-electronic-engineering"

'''Reading URLs' content'''
Page1 = urlopen(url1.strip('\'"'))
#Page2 = urlopen(url2.strip())
Page1 = BeautifulSoup(Page1)
#Page2 = BeautifulSoup(Page2)

'''Acquiring links and links text'''
links = []
headers = []
sentences = []
'''===================
Get links
===================='''
for link in Page1.findAll('a', attrs={'href': re.compile("^http://")}):
    text = re.sub('\s+',' ',link.text)
    linkObject = [link.get('href'), text]
    links.append(linkObject)
    #print(linkObject)
for link in Page1.findAll('a', attrs={'href': re.compile("^https://")}):
    text = re.sub('\s+',' ',link.text)
    linkObject = [link.get('href'), text]
    links.append(linkObject)
'''===================
Get Headers
===================='''
hdrs = Page1.find_all(lambda tag: tag and tag.name.startswith("h"))
for header in hdrs:
    headers.append(header)
'''===================='''
'''Pure text processing after getting links'''
Page1Text = re.sub('\s+',' ',Page1.text)
print(Page1Text)
'''===================
Sentences tokenization
===================='''
import nltk.tokenize.api
sntnss = sent_detector.tokenize(Page1Text.strip())

'''===================
Words tokenization
===================='''

'''===================
Multi-words tokenization
===================='''


'''===================
Normalization
===================='''

'''===================
POS tagging
===================='''

'''===================
Remove stop-words
===================='''

'''===================
Bag of words
===================='''

'''===================
NER
===================='''

'''===================
Index building
===================='''







