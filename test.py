import sys, getopt
from indeed import IndeedClient
import pandas as pd
import urllib.request
import re
import time
from bs4 import BeautifulSoup
import pyprind
import openpyxl


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

get_indeed_job_list('Engineer','Baltimore','50')