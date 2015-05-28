#!/usr/bin/env python2

import os
import sys
import requests
import urlparse
from bs4 import BeautifulSoup
from urllib import urlretrieve

# quick hack to download all the yearbook files from past years at UD

year_links = []
BASEURL='http://udspace.udel.edu'

def get_resource(res,outfolder):
    # give it the http:// link as res, and folder to save to as outfolder
    print 'Downloading resource {r} to {p}'.format(r=res, p=outfolder)
    filename = res.split('/')[-1]
    outpath = os.path.join(outfolder,filename)
    urlretrieve(res, outpath)

def extract_files(page):
    r = requests.get(page)
    soup = BeautifulSoup(r.text)
    file_links = []
    for item in soup.find_all('div', 'file-wrapper'):
        file_links.append(urlparse.urljoin(BASEURL, item.a.get('href').split('?')[0]))
    for item in soup.table.find_all('tr'):
        contents = item.td.contents[0]
        if contents.isnumeric():
            year = contents
    return file_links, year

# I downloaded the two list files, get @ me

with open(sys.argv[1], 'r') as f:
    soup = BeautifulSoup(f.read())
    print 'Parsing input file'
    for item in soup.find_all('div', 'artifact-title'):
        year_links.append(urlparse.urljoin(BASEURL, item.a.get('href')))

for resource_link in year_links:
    files, year = extract_files(resource_link)
    try:
        os.mkdir(year)
    except OSError:
        pass
    for item in files:
        get_resource(item, year)
