#!/usr/bin/python2
import requests
from bs4 import BeautifulSoup

import sys
from urllib import urlretrieve
import os
import argparse
import threading
import Queue

# helper
def getimage(img, outfolder):
    # give it the http:// link as img, and folder to save to as outfolder
    filename = img.split('/')[-1]
    outpath = os.path.join(outfolder,filename)
    urlretrieve(img, outpath)

def thread_helper(thread_id, queue, outfolder):
    queue_available = True
    while queue_available:
        try:
            href = queue.get(True)
            print 'Thread {} {}'.format(thread_id, href)
            getimage(href, outfolder)
        except Queue.Empty:
            print 'Thread {} finished'.format(thread_id)
            queue_available = False

def main(url, outfolder, num_threads):
    r = requests.get(url)
    q = Queue.Queue()
    soup = BeautifulSoup(r.text)
    for item in soup.find_all('img','thumb-title'):
        href = 'https:' + item.get('data-src')[:-5] + '.jpg'
        q.put(href)
    threads = []
    for item in range(num_threads):
        t = threading.Thread(target=thread_helper, args = (item, q, outfolder))
        t.start()
        threads.append(t)
    for item in threads:
        item.join()

p = argparse.ArgumentParser(description='download an entire imgur album to the folder of your choice')
p.add_argument('album', help='the link to the imgur album, e.g. https://imgur.com/a/jv4jO')
p.add_argument('directory', help='optionally, the directory to save all files to. If not given, it will default to the title of the album', nargs='?')
p.add_argument('-t', '--threads', help='number of threads to run', type=int, default=4)
args = p.parse_args()

if args.directory is None:
    r = requests.get(args.album)
    s = BeautifulSoup(r.text)
    destdir = s.title.text.strip()
else:
    destdir = args.directory

if not os.path.isdir(destdir):
    os.mkdir(destdir)

main(args.album, destdir, num_threads=args.threads)
