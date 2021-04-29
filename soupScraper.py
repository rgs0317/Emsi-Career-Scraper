# -*- coding: utf-8 -*-
"""
@author: Gavin
"""

'''
Script designed to scrape data from Emsi's career page.
This version uses BeautifulSoup to parse the HTML
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import json

#initialize driver
path = r'C:\\Users\\Gavin\\Chromedriver\\chromedriver.exe' 
driver = webdriver.Chrome(executable_path = path)

#connect to landing page and pull the loaded html
driver.get('https://www.economicmodeling.com/open-positions')
html= driver.page_source


soup0 = BeautifulSoup(html, "html.parser")

jobListings = {}

#this loops through the different links on the open positions page
for currentIndex,link in enumerate(soup0.find_all("a", class_="job-title")):
    #this pulls just the url part of the <a> tag
    url=link.attrs['href']
    
    #Using the unique part of URLs for job listing id (?)
    tmpId= url[-36:]
    
    
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    #convert from bytes to string
    tmpHTML = mybytes.decode('utf8')
    fp.close()
    
    soup1 = BeautifulSoup(tmpHTML, "html.parser")
    
    #pulls job title
    jobTitle= soup1.find("h2").text


    #team the job is on, and cleans up a space and "/" with [:-2]
    #and switching \u2013 to "-"
    teamName=soup1.find("div", class_='sort-by-team posting-category medium-category-label').text[:-2].replace("\u2013", "-")
    
    
    #job description
    teamDesc=soup1.find('div', class_='section page-centered').text
    
    
    #commitment of the position (full time, intern, etc.)
    jobCommit = soup1.find('div', class_='sort-by-commitment posting-category medium-category-label').text
    
    #location with cleaning off space and "/"
    jobLocat= soup1.find('div', class_='sort-by-time posting-category medium-category-label').text[:-2]

    ##company name. I could not find a consistent "Esri" nesting across all 
    ##listings so I used EconomicModeling.com
    ##this commented out version works for "esri" on all listings except one. 
    #compName= soup1.find("a", href="http://EconomicModeling.com").text[:4]
    
    compName= soup1.find("a", href="http://EconomicModeling.com").attrs['href']

    #structuring dict for easy json output
    jobListings[currentIndex] = {'jobTitle':jobTitle,
           'companyName':compName, 
           'teamName':teamName,
           'jobCommittment':jobCommit,
           'jobLocation':jobLocat,
           'jobDescription': teamDesc,
           'id':tmpId,
           'url': url
        }
    

driver.quit()

#output as json
json_object = json.dumps(jobListings, indent = 4)  
print(json_object) 
