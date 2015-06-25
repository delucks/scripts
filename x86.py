#!/usr/bin/python2

import requests
from bs4 import BeautifulSoup
import argparse
from urlparse import urljoin

USER_AGENT = 'x86 lookup helper by delucks'
headers = {'User-Agent': USER_AGENT}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('opcode', help='the operation you want to look up')
    p.add_argument('-m', action='store_true', help='dump the mnemonic')
    args = p.parse_args()
    page = 'http://x86.renejeschke.de/'
    r = requests.get(page, headers=headers)
    soup = BeautifulSoup(r.text)
    for item in soup.find_all('tr'):
        if item.td is not None:
            if item.td.text == args.opcode:
                if args.m:
                    print item.find_all('td')[1].text
                    break
                else:
                    url = urljoin(page, item.td.a.get('href'))
                    print requests.get(url, headers=headers).text

if (__name__ == '__main__'):
    main()
