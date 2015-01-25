import requests
from bs4 import BeautifulSoup
import sys
from urllib import urlretrieve
import os

# this script is shitty hack level. don't expect it to be friendly or error-tolerant.

# helper
def getimage(img,outfolder):
    # give it the http:// link as img, and folder to save to as outfolder
    filename = img.split("/")[-1]
    outpath = os.path.join(outfolder,filename)
    urlretrieve(img, outpath)

def main(url,outfolder):
  r = requests.get(url)
  soup = BeautifulSoup(r.text)
  for item in soup.find_all('img','thumb-title'):
    href = "https:" + item.get('data-src')[:-5] + ".jpg"
    print href
    getimage(href,outfolder)

main(sys.argv[1],sys.argv[2])
