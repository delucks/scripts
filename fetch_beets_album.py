#!/usr/bin/env python3
'''Download an artist or album from a beets (https://github.com/beetbox/beets)
music collection using the web API, then compress it. If the (-z/--zip)
argument is not provided, the resulting directory structure will be moved into
the default music directory (~/Music). I *think* this only works on Linux but
truly, who knows.
'''
import os
import time
import json
import shutil
import argparse
import threading
import urllib.request
from tempfile import mkdtemp
from urllib.parse import urljoin, quote

__version__ = '0.0.7'
__author__  = 'delucks'

BEETS_WEB_ROOT = os.environ.get('BEETS_API')
USER_AGENT = '{0} {1}'.format(os.path.basename(__file__), __version__)
DEFAULT_MUSIC_PATH = os.path.expanduser('~/Music')

def http_get(url, user_agent=USER_AGENT):
    '''url -> string'''
    r = urllib.request.Request(url, None, {'User-Agent': user_agent})
    with urllib.request.urlopen(r) as resp:
        return resp.read()

def endpoint_json(suffix, webroot):
    '''endpoint path -> dict'''
    url = urljoin(webroot, quote(suffix))
    return json.loads(http_get(url).strip().decode('utf8'))

def download_item(item_info, basepath, webroot):
    '''item information struct -> file on disk'''
    # Construct 04 - Song Title.filename
    # TODO add more zeros to the pad amount if there are > 99 tracks in this album
    fn = '{num:02d} - {title}.{fmt}'.format(
        num=int(item_info['track']),
        title=item_info['title'],
        fmt=item_info['format'].lower()
    )
    filename = fn.replace('/', '_')  # TODO find a better way to get around /
    file_endpoint = urljoin(webroot, 'item/{0}/file'.format(item_info['id']))
    # download the file
    print(':: Worker downloading {0} to {1}'.format(filename, basepath))
    return urllib.request.urlretrieve(file_endpoint, os.path.join(basepath, filename))

def fetch_to_temp_folder(querystring, webroot=BEETS_WEB_ROOT):
    resp = endpoint_json('/item/query/{0}'.format(querystring), webroot)
    out_folder = mkdtemp(prefix='album_zip_')
    artists = set()
    # set up threads for concurrency on this slow network operation
    fabric = []
    for item in resp['results']:
        item_info = endpoint_json('item/{0}'.format(item['id']), webroot)
        # Construct /tmp/foobar/Artist/Album/, and keep track of the base folder to zip it up later
        album_path = os.path.join(out_folder, item_info['albumartist'], item_info['album'])
        artists.add(item_info['albumartist'])
        if not os.path.exists(album_path):
            os.makedirs(album_path)
        t = threading.Thread(target=download_item, args=(item_info, album_path, webroot))
        fabric.append(t)
        t.start()
    for th in fabric:
        th.join()
    return out_folder, list(artists)

def validate_api_available(endpoint):
    if endpoint is None:
        return False
    try:
        resp = http_get(endpoint)
        return b'<title>beets</title>' in resp
    except urllib.error.HTTPError:
        return False

def main():
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--artist', help='download all of an artist')
    group.add_argument('--album', help='download an entire album')
    p.add_argument('-z', '--zip', action='store_true', help='zip up the files')
    p.add_argument('--api', help='the root path of the beets web API')
    args = p.parse_args()
    webroot = args.api or BEETS_WEB_ROOT
    if not validate_api_available(webroot):
        print('[FATAL] API cannot be contacted! Check your --api argument or set the environment variable BEETS_API')
        os.sys.exit(1)
    # Assemble the beets query and download it to a temp folder
    qs = 'artist:' + args.artist if args.artist else 'album:' + args.album
    print('Starting download of query {0}'.format(qs))
    basename, dirs = fetch_to_temp_folder(qs, webroot)
    # post-process the created files
    print('Downloaded successfully.')
    if args.zip:
        # make a zip file out of the directories taken down
        zip_name = os.path.expanduser('~/{0}_{1}'.format(args.artist or args.album, int(time.time())))
        shutil.make_archive(zip_name, format='zip', root_dir=basename, base_dir='.')
        print('Music should be in {0}'.format(zip_name + '.zip'))
        shutil.rmtree(basename)
    else:
        # move the folder structure into the default music location
        if not os.path.exists(DEFAULT_MUSIC_PATH):
            os.makedirs(DEFAULT_MUSIC_PATH)
        for fulldir in [os.path.join(basename, d) for d in dirs]:
            shutil.move(fulldir, DEFAULT_MUSIC_PATH)
        print('Music should be in {0}'.format(DEFAULT_MUSIC_PATH))

if __name__ == '__main__':
    main()
