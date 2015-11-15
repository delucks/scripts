#!/usr/bin/env python2
import sys

count = {}
with open(sys.argv[1]) as f:
  for char in f.read():
    if char not in '\n\t\ ':
      if char in count:
        count[char] += 1
      else:
        count[char] = 1

for item in count.keys():
  print "{key} {val}".format(key=item,val=count[item])
