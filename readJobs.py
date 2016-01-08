# -*- coding: utf-8 -*-

import urllib2
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import codecs
import html2text
import re
import os


try:
    from settings import indeedAPIKey
except ImportError:
    indeedAPIKey = os.environ['indeedAPIKey']

# Figuring out the maximum number of entries, creating a file, running read_in jobs
def mainReadJobs(searchJobs, jobtitleFilename, jobbulletFilename, limit):
   page = urllib2.urlopen("http://api.indeed.com/ads/apisearch?publisher="+indeedAPIKey+"&q="+searchJobs+"&sort=&radius=&st=&jt=&start=1&limit=25&fromage=&filter=&latlong=5&co=ca&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2")
   xmlPage = page.read()
   page.close()
   f = open(jobtitleFilename,'w')
   f.close()

   b = open(jobbulletFilename,'w')
   b.close()

   tree = ET.fromstring(xmlPage)
   maximumJobs = tree[4].text
   i = 0
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
      read_in_jobs(searchJobs, jobtitleFilename, jobbulletFilename, start, end)
      i = i+25
      #print i,start, end
   #print i, start, end


def read_in_jobs(searchJobs, jobtitleFilename, jobbulletFilename, start,end):
   # Getting list of jobs
   searchJobs = searchJobs.replace(" ", "+")
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

      # This is a hack
      with codecs.open(jobbulletFilename,'a', encoding='utf8') as b:
         b.write('\n')

      with codecs.open(jobtitleFilename,'a', encoding='utf8') as f:
         theSoup = str(soup.find('span',{"id": "job_summary"})).strip("\xe2\x80\xa2")
         theSoupText = theSoup.replace('</span>','').replace('<span class="summary" id="job_summary">','').strip("\xe2\x80\xa2") #removing the spans
         theSoupText = re.sub(r'\xe2\x80\xa2','', theSoupText) 
         theSoupText = theSoupText.replace('</b>','').replace('<b>','') #removing the bolds
         theSoupText = theSoupText.replace('</i>','').replace('<i>','') #removing the bolds
         theFinalSoup = theSoupText.strip("\xe2\x80\xa2")
         try:
            theText    = html2text.html2text( theFinalSoup.strip("\xe2\x80\xa2").decode('utf-8') )

            for sentence in theText.split('\n'):
               if sentence.startswith('  * '):
                  if sentence[-1].isalpha():
                     sentence = sentence + u';'
                  else:
                     newSentence = list(sentence)
                     newSentence[-1] = ';'
                     sentence = "".join(newSentence)
                  with codecs.open(jobbulletFilename,'a', encoding='utf8') as b:
                     b.write( sentence )
                     b.write('\n')
               else:
                  nonBulletText.append(sentence)
            f.write( ' '.join(nonBulletText) )   
            f.write("\n")
         except UnicodeDecodeError:
            print "UnicodeDecodeError"
            print theFinalSoup.strip("\xe2\x80\xa2")






   try:
      f.close()
   except:
      pass   
   try:   
      b.close()
   except:
      pass   


def existingJob(jobtitle, scraping):
   jobFilename = jobtitle.title().replace(" ", "")
   scapedJobFilename = 'scrapedJobs/' + jobFilename + '.txt'
   bulletScrapedJobFilename = 'scrapedJobs/bullet'+jobFilename + '.txt'
   searchedJobFilename = 'searchedJobs/' + jobFilename + '.txt'
   bulletSearchedJobFilename = 'searchedJobs/bullet'+jobFilename + '.txt'
   if( os.path.isfile(scapedJobFilename) and  os.path.isfile(bulletScrapedJobFilename) ):
      jobFilename = scapedJobFilename
      bulletJobFilename = bulletScrapedJobFilename
      newJob = False
   elif( os.path.isfile(searchedJobFilename) and os.path.isfile(bulletSearchedJobFilename)):
      jobFilename = searchedJobFilename
      bulletJobFilename = bulletSearchedJobFilename
      newJob = False
   elif scraping:
      jobFilename = scapedJobFilename
      bulletJobFilename = bulletScrapedJobFilename
      newJob = True      
   else:
      jobFilename = searchedJobFilename
      bulletJobFilename = bulletSearchedJobFilename
      newJob = True


   return (newJob, jobFilename, bulletJobFilename)
