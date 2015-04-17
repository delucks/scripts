#!/usr/bin/env python2
import re
import sys
import term_escapes as c
'''
encoder for L-languages
Only matches the most basic language features:

    V <- V
    V <- V + 1
    V <- V - 1
    if V != 0 goto L
    # Accepts comments starting with a hash

Will break on malformed input, this is for my personal use
Written by delucks 04/15/2015
''' 
# matches [A]
lbl_reg = re.compile(r'\[[A-Z]\]')
# matches (V <- V)
assign_reg = re.compile(r'([A-Z])\ ?<-\ ?\1')
# matches (V <- V +- 1)
arith_reg = re.compile(r'([A-Z])\ ?<-\ ?\1\ ?([+-])\ ?1')

inpath = sys.argv[1]
with open(inpath, 'r') as f:
    raw_prg = [line for line in f.readlines() if not line.startswith('#')]

variables = []
labels = []

# pass it a .split()'d string
def getlabel(input_tokens):
    if lbl_reg.match(input_tokens[0]):
        return input_tokens[0].strip('[]')
    else:
        return None

def pair(x, y):
    return ((2**x)*((2*y) + 1)) - 1

# information gathering stage
for item in raw_prg:
    tokens = item.split()
    # check if there's a label and add it
    potential_label = getlabel(tokens)
    if potential_label is not None:
        if potential_label not in labels:
            labels.append(potential_label)
        tokens = tokens[1:]
    # check if there's a new variable in the expression
    var_tok = tokens[0]
    if not var_tok.lower().strip() == 'if':
        if var_tok not in variables:
            variables.append(var_tok)

encodings = []
# second pass, pairing phase
for item in raw_prg:
    tokens = item.split()
    plbl = getlabel(tokens)
    lbl_idx = 0
    if plbl is not None: # there is a label!
        if plbl == 'E': # bad, bad programmer
            print '{d}[ERR] Next instruction\'s label is \'E\'{s}'.format(d=c.get_color('red'),s=c.get_color('reset'))
        else:
            lbl_idx = labels.index(plbl) + 1 # otherwise assign it the correct index
        tokens = tokens[1:] # strip out the label for further work
    if tokens[0].lower() == 'if': # check for a conditional goto
        try:
            inst_type = labels.index(tokens[-1]) + 3 # dest lbl idx + 2 + 1 (for human-encoding)
        except ValueError, e:
            print '{d}[ERR] Next goto\'s label doesn\'t exist!\n[ERR] {m}{s}'.format(d=c.get_color('red'),s=c.get_color('reset'),m=e.message)
            inst_type = 0 # poor goto :(
        var_idx = variables.index(tokens[1]) # pull out the var
    else: # we've got either an arithmetic or a direct assignment
        var_idx = variables.index(tokens[0])
        joined = ' '.join(tokens).strip()
        inst_type = 0
        if arith_reg.match(joined):
            inst_type = 1 if (tokens[-2] is '+') else 2
    print c.get_color('green') + item.strip() + c.get_color('reset')
    paired = pair(lbl_idx,pair(inst_type,var_idx))
    print '<%s, <%s, %s>> = %s' % (lbl_idx, inst_type, var_idx, paired) # check out dem pairing functions
    encodings.append(paired)

# pass encodings to goedel()
