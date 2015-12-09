#!/usr/bin/env python2
import praw
import argparse
import Queue
import threading

p = argparse.ArgumentParser(description="check if two subreddits have common posting users")
p.add_argument("first", help="the board you want to get users from")
p.add_argument("second", help="the board you want to check if they've posted in")
p.add_argument("-u", "--user", help="just check a user instead of two boards", action="store_true")
args = p.parse_args()

def checkuser(username,board):
  content = username.get_submitted(sort='new',time='all',limit=None)
  for submission in content:
    if submission.subreddit.__str__() == board:
      print submission
      print submission.permalink
      print

def worker(queue,thread_num):
  queue_available = True
  while queue_available:
    try:
      user = queue.get(False)
      print "[%i] %s" % (thread_num,user)
      checkuser(user,args.second)
    except Queue.Empty:
      print "[%i Thread] Finished" % thread_num
      queue_available = False

r = praw.Reddit(user_agent='subreddit crosslisting bot by u/delucks')
if not args.user:
  q = Queue.Queue()
  submissions = r.get_subreddit(args.first).get_new(limit=1000)
  unique = {}
  for item in submissions:
    unique[item.author] = 1
  for key in unique.keys():
    q.put(key)

  for i in range(20):
    t = threading.Thread(target=worker, args = (q,i))
    t.start()
else:
  checkuser(r.get_redditor(args.first),args.second)
