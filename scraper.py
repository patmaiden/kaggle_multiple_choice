from bs4 import BeautifulSoup
import bs4
import urllib2 
import codecs
import re
import unicodedata
from collections import defaultdict
import operator
import sys
from nltk.corpus import stopwords
from nltk import word_tokenize
import pickle
import numpy as np
from collections import defaultdict
import math

"""Scrapes google for the search query
and returns clean HTML of the pages"""
def scrape(phrase, num_results):
    #replace spaces with plusses to convert them for the url
    phrase = 'wikipedia+' + phrase.replace(' ', '+')
    
    #generate the URLs of the google searches
    urls = []
    for i in range(0,num_results):
        urls.append('https://www.google.com/search?q='+ phrase +'&oq='+ phrase +'&aqs=chrome..69i57j0l5.375j0j4&sourceid=chrome&es_sm=93&ie=UTF-8&start='+ str(i))
    
    #collect the html - would be nice to do this in parallel
    html = ""
    for url in urls:
        request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        response = urllib2.urlopen(request)
        html += response.read()
    

    #select out the links associated with each search result
    soup = BeautifulSoup(html, "lxml")    
    headers = soup.findAll("h3", attrs={'class':'r'})
    links = []
    i = 0
    for h3 in headers:
        if i >= num_results: break
        i+=1
        link = str(h3.find("a"))
        link2 = re.search("<a href=\"\/url\?q=(.*)&amp;sa=U&amp;", link)
        if link2 != None:
            link = link2.group(1)
            link.join('')
        #print link
        links.append(link)
  
    #make the HTML requests and store the results
    documents = []
    to_remove = []
    
    for link in links:
        request = urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            html = urllib2.urlopen(request).read()
        except: #should figure out root cause here
            print "error opening", link
            to_remove.append(link)
            continue
        #print html
        soup = BeautifulSoup(html, "lxml")
        text = soup.findAll(text=True)
       
        #convert unicode to ascii
        visible_texts = map(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore'), text)

        # concatenate lines
        text = reduce(lambda x,y: x + ' ' +y.strip(), visible_texts, '')
        
        #remove everything but words and spaces
        text = ''.join(t for t in text.lower() if t.isalnum() or t == ' ')

        
        documents.append(text)
    
    #pull out bad links
    for x in to_remove:
        links.remove(x)

    return documents, links

x,y = scrape("roman language", 3)
for d in y:
    print d