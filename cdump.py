#!/usr/bin/env python2
from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import os
import json
import logging
import argparse
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', stream=os.sys.stdout, level=logging.INFO)

def http_get(url, user_agent):
    headers = {'User-Agent': user_agent}
    logging.debug('http_get {} {}'.format(url, user_agent))
    r = urllib2.Request(url, None, headers)
    return urllib2.urlopen(r).read()

# scrape a page of craigslist, return a list of post dictionaries
def scrapepage(url, user_agent, baseurl):
    r = http_get(url, user_agent)
    rootsoup = BeautifulSoup(r)
    posts_from_page = []
    for post in rootsoup.find_all('p','row'):
        try:
            listing = {}
            listing['repost'] = 'data-repost-of' in post.attrs
            pl_container = post.find('span', 'pl')
            listing['title'] = pl_container.find('a').text
            listing['url'] = urljoin(baseurl, pl_container.find('a').get('href'))
            listing['time'] = pl_container.find('time').get('datetime')
            if post.find('span','price') is not None:
                listing['price'] = post.find('span','price').text.strip()
            if post.find('span','pnr').small is not None:
                # [1:-1] is to get rid of the ()
                listing['location'] = post.find('span','pnr').small.text.strip()[1:-1]
            posts_from_page.append(listing)
        except UnicodeEncodeError:
            pass
    return posts_from_page

p = argparse.ArgumentParser(description='scrape listings from craigslist, give you the JSON')
p.add_argument('board', help='the craigslist board you want to scrape')
p.add_argument('-l', '--location', help='craigslist location, usually your state. defaults to sfbay', default='sfbay')
p.add_argument('-u', '--user-agent', help='UA string for all HTTP requests performed', default='python craigslist searcher')
p.add_argument('-n', '--number', type=int, help='number of posts you want (be reasonable). defaults to 100', default=100)
p.add_argument('-o', '--output', help='file to output all yer JSON to', default='cl-scrape.json')
p.add_argument('-d', '--dump-to-stdout', help='dump listings as you scrape them to STDOUT', action='store_true')
args = p.parse_args()

if os.path.isfile(args.output):
    logging.fatal('Outfile exists! Move {}'.format(args.output))
    os.sys.exit(1)

rough_num_pages = args.number / 100
num_pages =  rough_num_pages if (args.number % 100) == 0 else rough_num_pages+1

logging.info('Scraping {} pages of search results for {}'.format(num_pages, args.board))

#/search/sya?s={start}
baseurl='https://{}.craigslist.org'.format(args.location)

results = []
for i in range(0, num_pages):
    page_url = baseurl + '/search/{}?s={}00'.format(args.board, i)
    logging.info('Hitting {}'.format(page_url))
    page_results = scrapepage(page_url, args.user_agent, baseurl)
    if args.dump_to_stdout:
        for item in page_results:
            print item
    results.extend(page_results)

logging.info('Dumping resulting JSON to {}'.format(args.output))
with open(args.output, 'w') as outfile:
    outfile.write(json.dumps(results))
