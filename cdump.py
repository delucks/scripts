#!/bin/env python2
from bs4 import BeautifulSoup
import requests
from ParserCommon import docurl
import argparse

# these are the only ones I care about, if you want more add them yourself
BOARDLIST=['fua','sya','bia','bka','bfa','ppa','cla','ela','gra','msa','pha','vga']
# your location here
BASEURL="https://delaware.craigslist.org"
# defaults to tab, change this if you think you're gonna get dirty input. was a comma, but turns out lots of titles use commas
SEPARATOR=u'	'
# set your useragent. this one is a default mac running chrome, so 50% of people
USER_AGENT = "python craigslist searcher"
headers = {'User-Agent': USER_AGENT}

# scrape a page of craigslist
def scrapepage(url,price,location):
    r = requests.get(url, headers=headers)
    rootsoup = BeautifulSoup(r.text)
    for post in rootsoup.find_all('p',"row"):
		try:
			#print post
			title = post.find('span',"pl").find('a').text
			link = BASEURL + post.find('span',"pl").find('a').get('href')
			amt = ""
			loc = ""
			if post.find('span',"price") is not None:
				amt = post.find('span',"price").text.strip()
			if post.find('span',"pnr").small is not None:
				# [1:-1] is to get rid of the ()
				loc = post.find('span',"pnr").small.text.strip()[1:-1]
			if (price and location):
				print title + SEPARATOR + amt + SEPARATOR + loc + SEPARATOR + link
			elif (price):
				print title + SEPARATOR + amt + SEPARATOR + link
			elif (location):
				print title + SEPARATOR + loc + SEPARATOR + link
			else:
				print title + SEPARATOR + link
		except UnicodeEncodeError:
			pass

p = argparse.ArgumentParser(description="scrape listings from craigslist so you can grep them")
p.add_argument("board", help="the craigslist board you want to scrape", choices=BOARDLIST)
p.add_argument("-l", "--location", help="show location along with post title", action="store_true")
p.add_argument("-p", "--price", help="show price along with post title", action="store_true")
p.add_argument("-n", "--number", type=int, help="number of posts you want (be reasonable). defaults to 100", default=100)
args = p.parse_args()

scrapepage(BASEURL+"/"+args.board+"/", args.price, args.location)
if (args.number > 100):
	for page in range(100, args.number, 100):
		scrapepage(BASEURL+"/"+args.board+"/index"+str(page)+".html", args.price, args.location)
