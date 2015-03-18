#!/usr/bin/python2
import sys

count = {}
with open(sys.argv[1]) as f:
  for word in f.read().split():
      if word in count:
        count[word] += 1
      else:
        count[word] = 1

for item in count.keys():
    print "{key} {val}".format(key=count[item],val=item)
