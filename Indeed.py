#!/usr/bin/python
# Indeed Project
import sys, getopt
from indeed import IndeedClient
import pandas as pd
import urllib.request
import re
import time
from bs4 import BeautifulSoup
import pyprind
import openpyxl

# Funtion grabs 100 results and returns them as a dataframe
def get_indeed_job_list(query,radius,location):
    client = IndeedClient(publisher = 2863621289879018)
    bar = pyprind.ProgBar(4, title='Searching For Jobs')
    resultspd = pd.DataFrame()
    for start in range(0,100,25):
        params = {
                'q' : query,
                'radius' : radius,
                'l' : location,
                'userip' : "1.2.3.4",
                'limit' : '25',
                'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
                'start' : start
            }
        search_response = client.search(**params)
        resultspd = pd.concat([resultspd,pd.DataFrame.from_dict(search_response['results'])],axis=0)
        bar.update()
    resultspd.reset_index(drop=True,inplace=True)
    resultspd['date'] = pd.to_datetime(resultspd.date)
    resultspd.drop(['country','formattedLocation','formattedLocationFull','onmousedown','stations','state','sponsored'],axis=1,inplace=True)
    return resultspd

# get descriptions of jobs and add to pandas dataframe
def get_descriptions(jobs):
    bar = pyprind.ProgBar(len(jobs), title='Scraping Job Descriptions')
    description = pd.DataFrame()
    for joburl in jobs.url:
        html = urllib.request.urlopen(joburl).read()
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.findAll(text=True)
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element)):
                return False
            return True
        descriptionhtml = list(filter(visible, texts))
        descriptionhtml = [a for a in descriptionhtml if a != '\n'] # removes new lines
        description = description.append([[descriptionhtml]])
        description.reset_index(drop=True,inplace=True)
        bar.update()
    return description

# Search description for signs of an entry level job and return 1 if entry level
def entry_level_check(jobs):
    entry_level_lookup = ['entry', 'Entry','entry level','Entry level','0-1','0-2','0-3','0-4','0-5']
    entry_level = pd.DataFrame()
    bar = pyprind.ProgBar(len(jobs.description), title='Checking For Entry Level')
    def check_description(job):
            for sentence in range(0,len(jobs.description[job])):
                for line in entry_level_lookup: #check jobs.description[job][sentence] for entrylevel
                    if line in jobs.description[job][sentence]:
                        return True
    for job in range(0,len(jobs.description)):
        if check_description(job) == True: # set column in pandas dataframe to 1
            entry_level = entry_level.append([1])
        else:
            entry_level = entry_level.append([0])
        bar.update()
    entry_level.reset_index(drop=True,inplace=True)
    return entry_level

# return pandas dataframe with jobs and description and entry level status and outputs excel file
def main(argv):
    query = ''
    location = ''
    radius = ''
    try:
        opts, args = getopt.getopt(argv,"hq:l:r:",["query=","loc=","radius="])
    except getopt.GetoptError:
        print('indeed.py -q <jobquery> -l <location> -r <radius>')
        sys.exit(2)
    if len(sys.argv) == 1:
        print('indeed.py -q <jobquery> -l <location> -r <radius>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('indeed.py -q <jobquery> -l <location> -r <radius>')
            sys.exit()
        elif opt in ("-q", "--query"):
            query = arg
        elif opt in ("-l", "--loc"):
            location = arg
        elif opt in ("-r", "--radius"):
            radius = arg
    jobs = get_indeed_job_list(query,radius,location)
    jobs['description'] = get_descriptions(jobs)
    jobs['entry_level'] = entry_level_check(jobs)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = query + '-' + radius + '-' + location + '-' + timestr + '.xlsx'
    jobs.to_excel(filename)
    return jobs

if __name__ == "__main__":
    main(sys.argv[1:])