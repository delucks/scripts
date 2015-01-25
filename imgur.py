import requests
from bs4 import BeautifulSoup
import sys

def main(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text)
  for item in soup.find_all('img','thumb-title'):
    print "https:" + item.get('data-src')[:-5] + ".jpg"

main(sys.argv[1])
