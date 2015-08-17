'''
Created on Dec 6, 2012

@author: yupeng
'''

import nltk

def Viterbi_fromfile(grammarfile):
    
    print 'Build a parser from ',grammarfile
    f = open(grammarfile)
    grammarstring = f.read()
    f.close()
    grammar = nltk.parse_pcfg(grammarstring)
    
    print 'Grammar size: ',len(grammar.productions())
    return nltk.ViterbiParser(grammar)


def Viterbi_fromgrammar(grammar):
    return nltk.ViterbiParser(grammar)