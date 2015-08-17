#!/usr/bin/env python
# a program to parse specific sentences from a text file
# given a grammar file
# usage: $0 <grammar file> <sentence file> <sentence number [from 0]>

import sys
import nltk
from nltk.parse.chart import *
from datetime import datetime
import time
      
if __name__ == '__main__':
    if len(sys.argv) < 2:
	print "usage: %s <grammar file> <output>" %(sys.argv[0])
	exit(1)

    grammarfile = sys.argv[1]
    outputfile = sys.argv[2]

    fd = open(grammarfile)
    productions = fd.readlines()
    production_map = {}
    start = None
    for production in productions:
	production = production.strip()
	parts = production.split("->")
	lhs = parts[0].strip()
	rhs = parts[1].strip()
	if not production_map.has_key(lhs):
	    production_map[lhs] = []
	production_map[lhs].append(rhs)

    out = open(outputfile, "w")
    start_rhs = production_map["S"]
    out.write("%s -> %s\n" %("S", " | ".join(start_rhs)))
    for lhs, rhs in production_map.items():
	if (lhs != "S"):
	    out.write("%s -> %s\n" %(lhs, " | ".join(rhs)))
    out.close()
