# standard lib
import cookielib
import re
from urlparse import urljoin
import logging
import sys

# install these
import mechanize
from bs4 import BeautifulSoup

'''
This script interacts with the Sakai site
Can use in interactive and noninteractive mode
Requires mechanize and beautifulsoup4
''' 
class SakaiUtil(object):
    def __init__(self, eid, pw, baseurl):
        self.baseurl = baseurl
        self.eid = eid
        self.pw = pw
        self.class_url_re = re.compile(self.baseurl + '/site/[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}')
        # initialize the browser object we'll be using for everything
        self.br = mechanize.Browser()
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)
        self.br.set_debug_responses(True)
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    '''
    Open up the portal site and post the login form with your supplied user ID and password
    '''
    def login(self):
        self.br.open(self.baseurl)
        self.br.select_form(nr=0)
        self.br.form['eid'] = self.eid
        self.br.form['pw'] = self.pw
        return_code = self.br.submit()
        logging.debug('Logged in with return code {r}'.format(r=return_code))

    '''
    Checks the Sakai main page for all classes you're enrolled in
    '''
    def get_classes(self):
        self.br.open(self.baseurl)
        soup = BeautifulSoup(self.br.response().read())
        class_uids = []
        for item in soup.find_all('a', role='menuitem'):
            link = item.get('href')
            if self.class_url_re.match(link):
                class_uids.append(link.split('/')[-1])
        return class_uids

    '''
    Retrieves a remote url to a local path
    '''
    def download_file(self, url, path):
        logging.debug('Downloading {u} to {p}'.format(u=url,p=path))
        with open(path,'wb') as f:
            remote = self.br.urlopen(url)
            f.write(remote.read())

    '''
    Recursively spiders from the top of the DAV directory to get all files in "Resources"
    '''
    def list_files(self, url):
        logging.debug('Spidering {u}'.format(u=url))
        self.br.open(url)
        soup = BeautifulSoup(self.br.response().read())
        folders = set([])
        files = set([])
        for fo in soup.find_all('li', 'folder'):
            folder_url = urljoin(url, fo.a.get('href'))
            folders.add(folder_url)
        for fi in soup.find_all('li', 'file'):
            file_url = urljoin(url, fi.a.get('href'))
            files.add(file_url)
        for item in folders:
            files = files.union(self.list_files(item))
        return files

    '''
    Authenticates against the bulk-download URL if necessary
    Then calls list_files to get all the files listed under that class' "Resources" page
    '''
    def get_files_for_class(self, class_uid):
        url = 'https://sakai.udel.edu/access/content/group/{uid}/'.format(uid=class_uid)
        self.br.open(url)
        if (len([i for i in self.br.forms()]) == 1):
            logging.info('Not logged in when querying bulk download')
            self.br.select_form(nr=0)
            self.br.form['eid'] = self.eid
            self.br.form['pw'] = self.pw
            self.br.submit()
        return self.list_files(url)

'''
Interactive use
'''
def main():
    import argparse
    logging.basicConfig(format='%(asctime)s:%(filename)s:%(levelname)s:%(message)s', stream=sys.stderr, level=logging.DEBUG)
    p = argparse.ArgumentParser(description='work with sakai sites')
    p.add_argument('-s', '--sakai', help='the base url of the sakai site', default='https://sakai.udel.edu/portal')
    p.add_argument('-u', '--user', help='username')
    p.add_argument('-p', '--password', help='password')
    args = p.parse_args()
    su = SakaiUtil(eid=args.user, pw=args.password, baseurl=args.sakai)
    su.login()
    print su.get_classes()
    #print su.get_files_for_class('020bfd02-8090-4d17-9109-aa98817feeea')

if __name__=='__main__':
    main()
