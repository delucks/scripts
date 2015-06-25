#!/usr/bin/env python2
# Roman Numeral Engine, by delucks
# I learned python like this
import argparse

def encode(value):
	final = []
	try:
		thou = int(str(value)[:-3])
	except ValueError:
		thou = 0
	try:
		hund = int(str(value)[-3])
	except IndexError:
		hund = 0
	try:
		tens = int(str(value)[-2])
	except IndexError:
		tens = 0
	try:
		ones = int(str(value)[-1])
	except IndexError:
		ones = 0
	final.append("M"*thou)
	if (hund == 9):
		final.append("CM")
	elif (hund >= 5):
		final.append("D"+"C"*(hund%5))
	elif (hund == 4):
		final.append("CD")
	else:
		final.append("C"*hund)
	if (tens == 9):
		final.append("XC")
	elif (tens >= 5):
		final.append("L"+"X"*(tens%5))
	elif (tens == 4):
		final.append("XL")
	else:
		final.append("X"*tens)
	if (ones == 9):
		final.append("IX")
	elif (ones >= 5):
		final.append("V"+"I"*(ones%5))
	elif (ones == 4):
		final.append("IV")
	else:
		final.append("I"*ones)
	return ''.join(final)

def value(c):
    numerals = {'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000,
            }
    return numerals[c]

def decode(numeral):
	final = 0
	current = 1
	for c in numeral[::-1]:
		if (value(c) < current):
			final = final - value(c)
		elif (value(c) == current):
			final = final + value(c)
		else:
			final = final + value(c)
			current = value(c)
	return final

def optimize(numeral):
	return encode(decode(numeral))

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--decode", action="store_true", help="Decode a numeral")
parser.add_argument("-e", "--encode", action="store_true", help="Encode a number")
parser.add_argument("-o", "--optimize", action="store_true", help="Optimize a numeral")
parser.add_argument("number", type=str, help="Input the number or string to decode")
args = parser.parse_args()
if args.decode:
	print decode(args.number)
elif args.encode:
	print encode(int(args.number))
elif args.optimize:
	print optimize(args.number)
else:
	print "Please specify an option"
