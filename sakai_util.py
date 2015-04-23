import mechanize
import cookielib
from bs4 import BeautifulSoup
import re

'''
This script interacts with the Sakai site
Can use in interactive and noninteractive mode
Requires mechanize and beautifulsoup4
''' 
class SakaiUtil(object):
    def __init__(self, eid, pw, baseurl='https://sakai.udel.edu/portal'):
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

    def get_classes(self):
        self.br.open(self.baseurl)
        self.br.select_form(nr=0)
        self.br.form['eid'] = self.eid
        self.br.form['pw'] = self.pw
        self.br.submit()
        soup = BeautifulSoup(self.br.response().read())
        class_uids = []
        for item in soup.find_all('a', role='menuitem'):
            link = item.get('href')
            if self.class_url_re.match(link):
                class_uids.append(link.split('/')[-1])
        return class_uids

    def list_files(self, soup):
        folders = set([])
        for item in soup.find_all('li',class='folder'):
            full_url = urljoin()
            folders.add(item.get('href'))

    def get_files_for_class(self, class_uid):
        unformatted = re.sub('portal','dav/{uid}', self.baseurl)
        dav_baseurl = unformatted.format(uid=class_uid)
        #self.br.add_password(dav_baseurl, self.eid, self.pw)
        #self.br.open(dav_baseurl)
        self.br.open('https://sakai.udel.edu/access/content/group/{uid}/'.format(uid=class_uid))
        self.br.select_form(nr=0)
        self.br.form['eid'] = self.eid
        self.br.form['pw'] = self.pw
        self.br.submit()
        soup = BeautifulSoup(self.br.response().read())
        return soup

def main():
    import argparse
    p = argparse.ArgumentParser(description='work with sakai sites')
    p.add_argument('-u', '--user', help='username')
    p.add_argument('-p', '--password', help='password')
    args = p.parse_args()
    su = SakaiUtil(eid=args.user, pw=args.password)
    print su.get_files_for_class('020bfd02-8090-4d17-9109-aa98817feeea').prettify()

if __name__=='__main__':
    main()
