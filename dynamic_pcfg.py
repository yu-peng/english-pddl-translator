'''
Created on Dec 3, 2012

@author: yupeng
'''
import nltk.data
from nltk.grammar import *
from nltk.tree import ProbabilisticTree

def best_parse(grammar, sentence, trace=0):
    words = sentence.split()
    table, splits = parse_table(grammar, words, trace)
    return make_tree(table, splits, 0, len(words), grammar.start())

def make_tree(table, splits, left, right, nonterminal):
    if isinstance(nonterminal, basestring):
        # actually a terminal -- we're done
        return nonterminal

    try:
        leftsym, rightsym, split = splits[left, right, nonterminal]
        prob = table[left, right, nonterminal]
    except KeyError:
        return None

    if rightsym is None:
        # unary production
        tree = make_tree(table, splits, left, right, leftsym)
        return ProbabilisticTree(nonterminal.symbol(), [tree], prob=prob)

    else:
        left_tree = make_tree(table, splits, left, split, leftsym)
        right_tree = make_tree(table, splits, split, right, rightsym)
        return ProbabilisticTree(nonterminal.symbol(), [left_tree, right_tree],
                                 prob=prob)

def parse_table(grammar, words, trace=0):
    table = {}
    splits = {}
    n = len(words)
    
    proddict = {}
    
    # base case
    for prod in grammar.productions():
        lhs = prod.lhs()
        rhs = prod.rhs()
        # store this production in a lookup dictionary
        proddict.setdefault(lhs, set()).add(prod)
    
    for i in range(n):
        for prod in grammar.productions():
            lhs = prod.lhs()
            rhs = prod.rhs()
        
            if isinstance(rhs[0], basestring):
                if words[i] == rhs[0]:
                    table[i, i+1, lhs] = prod.prob()
                    splits[i, i+1, lhs] = (words[i], None, None)
                    if trace > 0:
                        display_prod(i, i+1, n, lhs, rhs, prod.prob())
    
    # main loop
    total = 0
    for length in range(2, n+1):
        for left in range(n-length+1):
            right = left+length
            for lhs in proddict:
                best = 0
                for prod in proddict.get(lhs, set()):
                    rhs = prod.rhs()
                    if len(rhs) == 2:
                        for s in range(left+1, right): # split point
                            l, m = rhs
                            prob = (prod.prob() * table.get((left, s, l), 0)
                                                * table.get((s, right, m), 0))
                            if prob > best:
                                best = prob
                                splits[left, right, lhs] = (l, m, s)
                                if trace > 0:
                                    display_prod(left, right, n, lhs, rhs, prod.prob())
                    
                    elif len(rhs) == 1:
                        # handle unary productions
                        m = rhs[0]
                        prob = (prod.prob() * table.get((left, right, m), 0))
                        if prob > best:
                            best = prob
                            splits[left, right, lhs] = (m, None, None)
                            if trace > 0:
                                display_prod(left, right, n, lhs, rhs, prod.prob())
                    
                table[left, right, lhs] = best
                
    return table, splits

def display_prod(left, right, n, lhs, rhs, prob):
    wp = WeightedProduction(lhs, rhs, prob=prob)
    print '|' + '.'*left + '='*(right-left) + '.'*(n-right) + '|', wp

def demo():
    simple_grammar = nltk.data.load('nltk:grammars/toy1.pcfg')
    print best_parse(simple_grammar, 'I saw John with my telescope', trace=1)

if __name__ == '__main__':
    demo()
