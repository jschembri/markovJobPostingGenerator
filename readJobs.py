# -*- coding: utf-8 -*-

import urllib2
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import codecs
import html2text
import re


try:
    from settings import indeedAPIKey
except ImportError:
    indeedAPIKey = os.environ['indeedAPIKey']

# Figuring out the maximum number of entries, creating a file, running read_in jobs
def mainReadJobs(searchJobs):
   page = urllib2.urlopen("http://api.indeed.com/ads/apisearch?publisher="+indeedAPIKey+"&q="+searchJobs+"&sort=&radius=&st=&jt=&start=1&limit=25&fromage=&filter=&latlong=5&co=ca&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2")
   xmlPage = page.read()
   page.close()
   f = open('markovJobs.txt','w')
   f.close()

   b = open('bulletmarkovJobs.txt','w')
   b.close()

   tree = ET.fromstring(xmlPage)
   maximumJobs = tree[4].text
   i = 0
   limit = 100
   while(i < maximumJobs and i < limit):
      start = i
      if limit < 25:
         end = limit
         i = limit
      elif(i+25 > limit ):
         end = limit 
      elif(i+25 > maximumJobs ):
         end = maximumJobs 
      else:
         end = start + 25
      read_in_jobs(searchJobs, start, end)
      i = i+25
      #print i,start, end
   #print i, start, end


def read_in_jobs(searchJobs,start,end):
   # Getting list of jobs
   page = urllib2.urlopen("http://api.indeed.com/ads/apisearch?publisher="+indeedAPIKey+"&q="+searchJobs+"&sort=&radius=&st=&jt=&start="+str(start)+"&limit="+str(end)+"&fromage=&filter=&latlong=5&co=ca&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2")

   xmlPage = page.read()
   page.close()

   tree = ET.fromstring(xmlPage)


   urlList = []



   for child in tree[8]:
      urlList.append( child[9].text)



   for job in urlList:
      page = urllib2.urlopen(job)
      html = page.read()
      soup = BeautifulSoup(html, 'html.parser')
      nonBulletText = []
      with codecs.open('markovJobs.txt','a', encoding='utf8') as f:
         theSoup = str(soup.find('span',{"id": "job_summary"})).strip("\xe2\x80\xa2")
         theSoupText = theSoup.replace('</span>','').replace('<span class="summary" id="job_summary">','').strip("\xe2\x80\xa2") #removing the spans
         theSoupText = re.sub(r'\xe2\x80\xa2','', theSoupText) 
         theSoupText = theSoupText.replace('</b>','').replace('<b>','') #removing the bolds
         theSoupText = theSoupText.replace('</i>','').replace('<i>','') #removing the bolds
         theFinalSoup = theSoupText.strip("\xe2\x80\xa2")
         theText    = html2text.html2text( theFinalSoup.strip("\xe2\x80\xa2").decode('utf-8') )

         for sentence in theText.split('\n'):
            if sentence.startswith('  * '):
               if sentence[-1].isalpha():
                  sentence = sentence + u';'
               else:
                  newSentence = list(sentence)
                  newSentence[-1] = ';'
                  sentence = "".join(newSentence)
               with codecs.open('bulletmarkovJobs.txt','a', encoding='utf8') as b:
                  b.write( sentence )
                  b.write('\n')
            else:
               nonBulletText.append(sentence)

                     
           
         f.write( ' '.join(nonBulletText) )   
         f.write("\n")




   f.close()
   b.close()


