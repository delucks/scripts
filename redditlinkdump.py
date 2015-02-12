#!/usr/bin/python2
import praw
import argparse

p = argparse.ArgumentParser(description="dump top n links from subreddit")
p.add_argument("board", help="the subreddit you want to scrape")
p.add_argument("-n", "--number", type=int, help="number of links you want (be reasonable). defaults to 100", default=100)
args = p.parse_args()

r = praw.Reddit(user_agent='links dumper by u/delucks')
subm = r.get_subreddit(args.board).get_top_from_all(limit=args.number)
links = [x.url for x in subm if not x.is_self]
for l in links:
    print l
