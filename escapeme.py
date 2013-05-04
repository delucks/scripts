#! /usr/bin/env python2

# Made to get rid of that pesky problem with nested escaped string sequences

import argparse

chars=[';','&','|','<','>','*','?','`','$','(',')','{','}','[',']','!','#',' ','\\']

def escape(unsafe):
	outstr = ''
	for c in range(0, len(unsafe)):
		if any(item == unsafe[c] for item in chars):
			outstr += '\\'
		outstr += unsafe[c]
	return outstr 

parser = argparse.ArgumentParser()
parser.add_argument("jaunski", type=str, help="Input the string to be escaped")
args = parser.parse_args()

print escape(args.jaunski)
