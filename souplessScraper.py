"""
@author: Gavin
For Emsi Data Engineer, Web Scraping positon
"""

'''
Script designed to scrape data from Emsi's career page.
<<<<<<< HEAD:souplessScraper.py
This version uses regular expressions to parse the html. 

=======
This version uses regular expressions to parse the html 
and then prints data as a JSON Object.
>>>>>>> c49bb179dd2e32787985b307d5d9aca41592ee77:careerScraper.py
'''


from selenium import webdriver
import re
import urllib.request
import json

#initialize headerless browser to load dynamic content
path = r'C:\\Users\\Gavin\\Chromedriver\\chromedriver.exe' 
driver = webdriver.Chrome(executable_path = path)

#connect to landing page and pull the loaded html
driver.get('https://www.economicmodeling.com/open-positions')
html= driver.page_source

#regex to pull all urls for jobs on the page
ids= re.findall('"job-title" href="https://jobs.lever.co/economicmodeling/(.*?)" "', html)

jobListings = {}

#I use enumerate here so that 
for currentIndex,tmpid in enumerate(ids):

    #build URL data element, while keeping the id separate
    link = 'https://jobs.lever.co/economicmodeling/'+tmpid
    
    fp = urllib.request.urlopen(link)
    mybytes = fp.read()
    #convert from bytes to string
    tmpHTML = mybytes.decode('utf8')
    fp.close()
    
    #job title 
    tmpTitle = re.findall('class="posting-headline"><h2>(.*?)</h2><div', tmpHTML)[0]    
  
    
    #team the job is on
    #and switching \u2013 to "-"
    tmpTeam = re.findall('team posting-category medium-category-label">(.*?)/</div><div href="', tmpHTML)[0].replace("\u2013", "-")

    
    #job description
    tmpDesc = re.findall('description" content="(.*?)"><meta',tmpHTML)[0]
   
    
    #commitment of the position (full time, intern, etc.)
    tmpCommit= re.findall('commitment posting-category medium-category-label">(.*?)</div></div>', tmpHTML)[0]

    
    #location
    tmpLocat= re.findall(':data1" value="(.*?)" /><meta name=', tmpHTML)[0]

    
    #company name
    tmpCompany= re.findall('"Organization","name": "(.*?)","logo"', tmpHTML)[0]
    
    #structuring dict for easy json output
    jobListings[currentIndex] = {'jobTitle':tmpTitle,
               'companyName':tmpCompany, 
               'teamName':tmpTeam,
               'jobCommittment':tmpCommit,
               'jobLocation':tmpLocat,
               'jobDescription':tmpDesc,
               'id':tmpid,
               'url': link
        }
<<<<<<< HEAD:souplessScraper.py
    
driver.quit()
=======
>>>>>>> c49bb179dd2e32787985b307d5d9aca41592ee77:careerScraper.py

    #output as json
json_object = json.dumps(jobListings, indent = 4)  
print(json_object) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
