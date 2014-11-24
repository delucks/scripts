# usage: python2 linkvalidate.py http://my.cool.website.com
from ParserCommon import docurl
from bs4 import BeautifulSoup

import argparse
from urlparse import urljoin

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("page",type=str,help="First argument: the url to validate")
  args = parser.parse_args()
  r = docurl(args.page)
  soup = BeautifulSoup(r.text)
  # make the urls unique
  unique = {}
  for item in soup.find_all('a'):
    unique[item.get('href')] = 1
  # check response code for each, print it
  for url in unique:
    if (url.split(':')[0] == "mailto"):
      continue
    if ((url.split(':')[0] != "http")or(url.split(':')[0] != "https")):
        url = urljoin(args.page,url)
    req = docurl(url)
    print "%i %s" % (req.status_code,url)

if (__name__=='__main__'):
  main()
