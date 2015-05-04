#!/usr/bin/env python2
import sys

count = {}

if len(sys.argv) == 3:
    input_file = sys.argv[2]
elif len(sys.argv) == 2:
    input_file = sys.argv[1]
else:
    print "Usage: python2 wordcount.py {-u} {filename}"
    print "       The -u option will lower() each word in the file"
    exit(1)

with open(input_file) as f:
    for token in f.read().split():
        if sys.argv[1] == '-u':
            word = token.lower()
        else:
            word = token
        if word in count:
            count[word] += 1
        else:
            count[word] = 1

for item in count.keys():
    print "{key} {val}".format(key=count[item],val=item)
