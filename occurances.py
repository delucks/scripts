#!/usr/bin/env python3
'''command-with-stdout.py | ./occurances.py [options] [<method>] [<input file>] [<output file>]

perform basic statistics on input
like "sort | uniq -c | sort -nr" by default
doesn't do any column selection, this is for use in a pipe silly

Methods:
  count: unique line count of the input (default)
  percentage: unique line count of the input, with percentages of the total
  dimensions: describe the character dimensions of the input text
  char: count of characters in the input, with percentages of the total
  word: word count of the input

author: delucks
'''

from collections import Counter
import sys
import string
import argparse


class Methods:
    '''summary or statistical functions that output the data with markup
    signature: func(stats: Stats, delimiter: str, header: bool)
    '''
    def count(stats, delimiter, header):
        # sort | uniq -c | sort -nr (default behavior)
        for item, count in sorted(stats.c.items(), key=lambda x: x[1]):
            if item in string.whitespace:
                item = repr(item).replace("'", '')
            yield '{}{d}{}'.format(count, item, d=delimiter)
        if header:
            yield 'Count{d}Term'.format(d=delimiter)

    def word_count(stats, delimiter, header):
        # space-delimited "word count"
        local_count = Counter(stats.text.split())
        for item, count in sorted(local_count.items(), key=lambda x: x[1]):
            if item in string.whitespace:
                item = repr(item).replace("'", '')
            yield '{}{d}{}'.format(count, item, d=delimiter)
        if header:
            yield 'Count{d}Word'.format(d=delimiter)

    def percentage(stats, delimiter, header, precision=2):
        # display a percentage of the frequency of occurance of each line
        total = sum(stats.c.values())
        for item, count in stats.c.items():
            if item in string.whitespace:
                item = repr(item).replace("'", '')
            yield '{}{d}{}{d}{}%'.format(item, count, round(count/total*100, precision), d=delimiter)
        if header:
            yield 'Count{d}Term{d}Percent'.format(d=delimiter)

    def dimensions(stats, delimiter, header):
        # describe the # of lines, columns, etc
        lengthiest = 0
        for idx, line in enumerate(stats.text.splitlines()):
            if len(line) > lengthiest:
                lengthiest = len(line)
            yield '{}{d}{}{d}{}'.format(idx, len(line), line, d=delimiter)
        if header:
            yield 'Row{d}Length{d}Contents'.format(d=delimiter)
            yield 'The passed in text is {} lines by {} characters maximum'.format(idx+1, lengthiest)

    def character_count(stats, delimiter, header):
        # character frequency
        local_count = Counter(stats.text)
        for item, count in sorted(local_count.items(), key=lambda x: x[1]):
            if item in string.whitespace:
                item = repr(item).replace("'", '')
            yield '{}{d}{}'.format(count, item, d=delimiter)
        if header:
            yield 'Count{d}Character'.format(d=delimiter)


class Stats:
    def __init__(self, body, strip):
        self.c = Counter()
        for line in body.splitlines():
            if strip:
               self.c[line.strip()] += 1 
            else:
               self.c[line] += 1 
        self.text = body


def main():
    methods = {
        'percent': Methods.percentage,
        'dimensions': Methods.dimensions,
        'count': Methods.count,
        'char': Methods.character_count,
        'word': Methods.word_count,
    }
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('method', choices=methods.keys(), help='what information to display', default='count', nargs='?')
    p.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='specify a file to read from (defaults to stdin)')
    p.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='specify a file to write to (defaults to stdout)')
    p.add_argument('--header', help='print a header describing the columns along with the output', action='store_true')
    p.add_argument('-r', '--reverse', help='reverse the sort order', action='store_true')
    p.add_argument('-s', '--strip', help='strip all whitespace from each line before passing', action='store_true')
    p.add_argument('--delimiter', help='string to print between fields', default=' ')
    args = p.parse_args()

    s = Stats(args.infile.read(), args.strip)
    output_gen = methods[args.method](s, args.delimiter, args.header)
    output_lines = output_gen if args.reverse else reversed(list(output_gen))
    for line in output_lines:
        print(line, file=args.outfile)


if __name__ == '__main__':
    main()
