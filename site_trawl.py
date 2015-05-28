import requests
from bs4 import BeautifulSoup
import sys
import Queue
import logging
import threading
import urlparse
from time import sleep

class LinkSpider(object):
    ''' class which creates a set of in-scope URLs from a domain,
    then performs an action on each
    '''
    def __init__(self, baseurl, num_threads, limit_domain, thread_timeout, req_limit):
        self.baseurl = baseurl
        self.num_threads = num_threads
        self.limit_domain = limit_domain # should we spider inside of the same domain?
        self.q = Queue.Queue()
        self.visited = set()
        self.q.put(self.baseurl)
        self.thread_timeout = thread_timeout
        self.req_limit = req_limit
        self.status_codes = {}
        self.threads = []

    # helper method for setting params in the requests call
    def get_page(self, url, user_agent='https://github.com/delucks/scripts/site_trawl.py'):
        headers = {'User-Agent': user_agent}
        sleep(self.req_limit)
        return requests.get(url, headers=headers)

    # check if a particular URL is in the scope of the scan
    def scope_url(self, url):
        base_split = urlparse.urlsplit(self.baseurl)
        url_split = urlparse.urlsplit(url)
        if self.limit_domain:
            return base_split.netloc == url_split.netloc
        else:
            return True

    def sanitize(self, url):
        split = urlparse.urlsplit(url)
        i = ['http']
        i.extend(split[1:]) # make sure the scheme is http
        u = urlparse.urlunsplit(i)
        if '#' in u:
            u = u.split('#')[0] # get rid of all anchors
        return u.rstrip('/') # trailing slashes

    # look through an iterable and yield results if they haven't been visited yet
    def yield_unvisited(self, iterable, base):
        for item in iterable:
            h = item.get('href')
            if h is not None:
                san = self.sanitize(h)
                if not san in self.visited:
                    yield san

    # grab a page, add all the URLs to the queue being served by the worker
    def page_parse(self, url):
        if url in self.visited:
            return
        self.visited.add(url)
        r = self.get_page(url)
        self.status_codes[url] = r.status_code
        soup = BeautifulSoup(r.text)
        for link in self.yield_unvisited(soup.find_all('a'), url):
            if self.scope_url(link):
                logging.info('Adding {u} to queue'.format(u=link))
                self.q.put(link)

    # worker method, call in a thread to pull a page off the queue and run (action) on it
    def worker(self, t_id):
        queue_available = True
        while queue_available:
            try:
                u = self.q.get(True, timeout=self.thread_timeout)
                logging.info('[{i}] processing {u}'.format(i=t_id, u=u))
                self.page_parse(u)
            except Queue.Empty:
                logging.info('[{i}] thread finished'.format(i=t_id))
                queue_available = False

    # main method
    def run(self):
        # start all ya threads
        for thread_id in range(self.num_threads):
            t = threading.Thread(target=self.worker, args = (thread_id,))
            t.start()
            self.threads.append(t)
        # wait for all threads to terminate
        for item in self.threads:
            item.join()
        return self.visited

if (__name__ == '__main__'):
    logging.basicConfig(
        format='%(asctime)s:%(filename)s:%(levelname)s:%(message)s',
        stream=sys.stderr,
        level=logging.INFO)
    import argparse
    p = argparse.ArgumentParser(description='spider a site')
    p.add_argument('url', help='the starting URL for the spider')
    p.add_argument('-s', '--show-status', help='output status codes of all links', action='store_true')
    p.add_argument('-u', '--show-urls', help='output all links', action='store_true')
    p.add_argument('-t', '--threads', help='the amount of threads to spawn', type=int, default=3)
    p.add_argument('-l', '--request-limit', help='delay between thread requests', type=int, default=3)
    p.add_argument('--thread-timeout', help='time to wait for data', type=int, default=30)
    p.add_argument('--no-domain', help='don\'t limit spidering to the same domain', action='store_true')
    args = p.parse_args()
    s = LinkSpider(baseurl=args.url,
        num_threads=args.threads,
        limit_domain=not args.no_domain,
        thread_timeout=args.thread_timeout,
        req_limit=args.request_limit)
    links = s.run()
    for url, code in s.status_codes.iteritems():
        if args.show_status:
            print '{u},{c}'.format(u=url, c=code)
        elif args.show_urls:
            print url
