#!/usr/bin/python2
from bs4 import BeautifulSoup

import base64
import time
import urllib2
import urllib
import os
import argparse
import threading
import Queue

# required for image uploading! fill in with yers
IMGUR_API_KEY = ''

'''
downloads an image to a folder, if it doesn't already exist
'''
def get_image(img, outfolder):
    # give it the http:// link as img, and folder to save to as outfolder
    filename = img.split('/')[-1]
    outpath = os.path.join(outfolder,filename)
    if not os.path.isfile(outpath): # doesn't check if the file is whole, meh
        print 'Downloading {} to {}'.format(img, outfolder)
        urllib.urlretrieve(img, outpath)

'''
repeatedly calls get_image() on a queue
'''
def thread_helper(thread_id, queue):
    queue_available = True
    while queue_available:
        try:
            href, outfolder = queue.get()
            print 'Thread {}: {} to {}'.format(thread_id, href, outfolder)
            get_image(href, outfolder)
            queue.task_done()
        except Queue.Empty:
            queue_available = False

'''
grabs all img links of an album, adds to thread queue
'''
def enqueue(url, outfolder, queue):
    # setup
    print 'Queueing all images from {}'.format(url)
    USER_AGENT = 'imgur downloader (https://github.com/delucks/scripts/blob/master/imgur.py)'
    headers = {'User-Agent': USER_AGENT}
    r = urllib2.Request(url, None, headers)
    soup = BeautifulSoup(urllib2.urlopen(r).read())
    # folder handling
    if outfolder is None:
        album_title = str(soup.title.text.strip())
        #if album_title.endswith('- Album on Imgur'):
        #    album_title = album_title[:-16].strip() # strip off album text
        outfolder = album_title.translate(None, '/')
    if not os.path.isdir(outfolder):
        os.mkdir(outfolder)
    # pulling out the image links
    img_links = []
    for item in soup.find_all('img','thumb-title'):
        href = 'https:' + item.get('data-src')[:-5] + '.jpg'
        queue.put((href, outfolder))

'''
launches a team of threads to attack the queue
'''
def main(queue, num_threads):
    # launch a thread pool
    for thread_id in range(num_threads):
        t = threading.Thread(target=thread_helper, args = (thread_id, queue))
        t.setDaemon(True)
        t.start()

def upload(local_path, api_key):
    img_data = base64.b64encode(open(local_path,'rb').read())
    data = urllib.urlencode({'key':api_key, 'image':urllib.quote(img_data)})
    site = urllib2.Request('http://imgur.com/api/upload.json', data)
    s = urllib2.urlopen(site)
    return s.read()

p = argparse.ArgumentParser(description='download an entire imgur album to the folder of your choice')
group = p.add_mutually_exclusive_group(required=True)
group.add_argument('-a', '--album', help='the link to the imgur album, e.g. https://imgur.com/a/jv4jO')
group.add_argument('-l', '--album-list', help='a file containing a list of albums to download. all will be put in the same dir')
group.add_argument('-u', '--upload', help='upload a local file to imgur')
p.add_argument('-t', '--threads', help='number of threads to run', type=int, default=1)
p.add_argument('directory', help='optionally, the directory to save all files to. If not given, it will default to the title of the album', nargs='?')
args = p.parse_args()

q = Queue.Queue() 
if args.album_list is not None:
    with open(args.album_list, 'r') as f:
        album_list = f.readlines()
        for item in album_list:
            enqueue(item, args.directory, q)
elif args.album is not None:
    enqueue(args.album, args.directory, q)
else: # args.upload
    if IMGUR_API_KEY is not '':
        upload(args.upload, IMGUR_API_KEY)
    else:
        print 'You must fill out the IMGUR_API_KEY variable inside of source, line 14'
        os.sys.exit(1)

main(q, args.threads)
q.join() # wait for the queue to be empty
