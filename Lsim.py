#!/usr/bin/env python2
import re
import sys
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
labels = ['E'] # include E because indexing here starts at 1

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

'''
should probably have the true index of lbls in the list
then just bump it up when encoding/returning it
we can put E nowhere, and put the var encoding of those to inf
'''
encodings = []
# second pass, goedel encoding phase
for item in raw_prg:
    # pull out its label number
    tokens = item.split()
    plbl = getlabel(tokens)
    lbl_idx = 0
    if plbl is not None:
        lbl_idx = labels.index(plbl)
        tokens = tokens[1:]
    # pull out the encoding of var used
    if tokens[0].lower() == 'if':
        inst_type = labels.index(tokens[-1]) + 2 # dest lbl idx + 2
        var_idx = variables.index(tokens[1]) # pull out the var
    else:
        var_idx = variables.index(tokens[0])
        joined = ' '.join(tokens).strip()
        inst_type = 0
        if arith_reg.match(joined):
            inst_type = 1 if (tokens[-2] is '+') else 2
    print item.strip()
    print 'label: %s, var_idx: %s, instr: %s' % (lbl_idx, var_idx, inst_type)
    # pull out type of inst
    # call pair(...,pair(...,...)), append to encodings
    encodings.append(pair(lbl_idx,pair(inst_type,var_idx)))

# pass encodings to goedel()
