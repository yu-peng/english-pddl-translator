'''
Created on Dec 7, 2012

@author: yupeng
'''
import urllib
import urllib2
import re

from xml.dom.minidom import parse, parseString


def getTreeString(sent):

    url = 'http://nlp.stanford.edu:8080/parser/index.jsp'
    values = {'query' : sent,
              'parserSelect': 'English'}
    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    
    #print the_page
    
    matchstart = re.search('<pre id="parse" class="spacingFree">', the_page, re.IGNORECASE)
    
    
    if matchstart:
        
        matchend = re.search('</pre>', the_page, matchstart.end())
        
        if matchend:
            treeString = the_page[matchstart.end():matchend.start()]
            #print treeString
            #treeString = '(S  (VP    (VB have)    (NP (NN dinner))    (PP (IN in) (NP (CD three) (NNS minutes))))  (. .))'
            return treeString


#xmlData = parseString(xmlString)

#itemlist = xmlData.getElementsByTagName('pre') 


