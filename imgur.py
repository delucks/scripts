#!/usr/bin/python2
import requests
from bs4 import BeautifulSoup
import sys
from urllib import urlretrieve
import os
import argparse

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

p = argparse.ArgumentParser(description="download an entire imgur album to the folder of your choice")
p.add_argument("album", help="the link to the imgur album, e.g. https://imgur.com/a/jv4jO")
p.add_argument("directory", help="optionally, the directory to save all files to. If not given, it will default to the title of the album", nargs="?")
args = p.parse_args()

if args.directory is None:
  r = requests.get(args.album)
  s = BeautifulSoup(r.text)
  destdir = s.title.text.strip()
else:
  destdir = args.directory

if not os.path.isdir(destdir):
  os.mkdir(destdir)

main(args.album,destdir)
