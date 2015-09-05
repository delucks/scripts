#!/usr/bin/env python2
import fileinput

count = {}

for line in fileinput.input():
    for token in line.split():
        word = token.lower()
        if word in count:
            count[word] += 1
        else:
            count[word] = 1

for item in count.keys():
    print "{key} {val}".format(key=count[item],val=item)
