#!/usr/bin/python2
# usage: python2 linkvalidate.py http://my.cool.website.com
import requests
from bs4 import BeautifulSoup

import argparse
from urlparse import urljoin

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('page',type=str,help='First argument: the url to validate')
  parser.add_argument('-u', '--useragent', type=str, help='Alternate User-Agent field to use')
  args = parser.parse_args()
  if args.useragent:
      headers = {'User-Agent': args.useragent}
  else:
    USER_AGENT = 'python link validation https://github.com/delucks/scripts/linkvalidate.py'
    headers = {'User-Agent': USER_AGENT}
  r = requests.get(args.page, headers=headers)
  soup = BeautifulSoup(r.text)
  # make the urls unique
  unique = {}
  for item in soup.find_all('a'):
    unique[item.get('href')] = 1
  # check response code for each, print it
  for url in unique:
    if (url.split(':')[0] == 'mailto'):
      continue
    if ((url.split(':')[0] != 'http')or(url.split(':')[0] != 'https')):
        url = urljoin(args.page,url)
    req = docurl(url)
    print '%i %s' % (req.status_code,url)

if (__name__=='__main__'):
  main()
