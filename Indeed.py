#!/usr/bin/python
# Indeed Project
import sys, getopt
from indeed import IndeedClient
import pandas as pd
import urllib.request
import re
from bs4 import BeautifulSoup
import pyprind


# Function grabs 100 results and returns them as a dataframe
def get_indeed_job_list(query, location, radius):
    client = IndeedClient(publisher=2863621289879018)
    progress_bar = pyprind.ProgBar(4, title='Searching For Jobs')
    results_pd = pd.DataFrame()
    for numb_results in range(0, 100, 25):
        params = {
            'q': query,
            'radius': radius,
            'l': location,
            'userip': "1.2.3.4",
            'limit': '25',
            'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
            'start': numb_results
        }
        search_response = client.search(**params)
        print(search_response)
        results_pd = pd.concat([results_pd, pd.DataFrame.from_dict(search_response['results'])], axis=0)
        progress_bar.update()
    if len(results_pd) == 0:
        sys.exit('Search did not return any jobs')
    results_pd.reset_index(drop=True, inplace=True)
    results_pd['date'] = pd.to_datetime(results_pd.date)
    results_pd.drop(
        ['country', 'formattedLocation', 'formattedLocationFull', 'onmousedown', 'stations', 'state', 'sponsored'],
        axis=1, inplace=True)
    return results_pd  # returns the search results as a pandas data frame


# get descriptions of jobs and add to pandas dataframe
def get_descriptions(jobs):
    bar = pyprind.ProgBar(len(jobs), title='Scraping Job Descriptions')
    description = pd.DataFrame()
    for job_url in jobs.url:
        html = urllib.request.urlopen(job_url).read()
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.findAll(text=True)

        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element)):
                return False
            return True

        description_html = list(filter(visible, texts))
        description_html = [a for a in description_html if a != '\n']  # removes new lines
        description = description.append([[description_html]])
        description.reset_index(drop=True, inplace=True)
        bar.update()
    return description


# Search description for signs of an entry level job and return 1 if entry level
def entry_level_check(jobs):
    entry_level_lookup = {'entry', 'Entry', 'entry level', 'Entry level', ' 0-1 ', ' 0-2 ', ' 0-3 ', ' 0-4 ', ' 0-5 '}
    entry_level = pd.DataFrame()
    progress_bar = pyprind.ProgBar(len(jobs.description), title='Checking For Entry Level')

    def check_description(job):
        for sentence in range(0, len(jobs.description[job])):
            for line in entry_level_lookup:  # check jobs.description[job][sentence] for entry level
                if line in jobs.description[job][sentence]:
                    return True

    for job in range(0, len(jobs.description)):
        if check_description(job):  # set column in pandas dataframe to 1 if true
            entry_level = entry_level.append([1])
        else:
            entry_level = entry_level.append([0])
        progress_bar.update()
    entry_level.reset_index(drop=True, inplace=True)
    return entry_level


# return pandas dataframe with jobs and description and entry level status and outputs excel file
def main(query, location, radius):
    jobs = get_indeed_job_list(query, location, radius)
    jobs['description'] = get_descriptions(jobs)
    jobs['entry_level'] = entry_level_check(jobs)
    return jobs
