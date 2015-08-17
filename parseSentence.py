'''
Created on Dec 6, 2012

@author: yupeng
'''
import nltk
import fetchStanfordOnline

import makeParser
from nltk.draw import tree
from nltk.tree import Tree 
from nltk.draw.util import * 
from nltk.draw.tree import *

parser = makeParser.Viterbi_fromfile("wsjp.cfg")
print parser


def parseEnglish(sent,parsertype):
            
    if parsertype == 3:
        print 'using Viterbi parser and customized grammar'
        tree = parser.parse(sent.split())
        return tree
    
    elif parsertype == 1:
        print 'using Stanford online parser'
        treeString = treeString = fetchStanfordOnline.getTreeString(sent)
        tree = Tree(treeString)
        return tree
    
    #treeview.draw_tree(tree)

    
def drawTree(parseTree,frame):
    
#    def fill(cw): 
#          cw['fill'] = '#%06d' % random.randint(0,999999) 
       
    cf = CanvasFrame(parent=frame,width=550, height=450, closeenough=2) 
    t = parseTree
    
    tc = TreeWidget(cf.canvas(), t, draggable=1,  
                      node_font=('helvetica', -14, 'bold'), 
                      leaf_font=('helvetica', -12, 'italic'), 
                      roof_fill='white', roof_color='black', 
                      leaf_color='green4', node_color='blue2') 
    cf.add_widget(tc,10,10) 
    
    return cf.canvas()

def getCanvas(frame,parseTree):
        
    cf = drawTree(parseTree,frame)
    
    return cf


if __name__ == '__main__':
    
    sentence = 'go to school quickly.'
    #treeString = '(ROOT  (S    (NP (PRP$ My) (NN dog))    (ADVP (RB also))    (VP (VBZ likes)      (S        (VP (VBG eating) (NP (NN sausage))))) (. .)))'
    
    #treeString = fetchStanfordOnline.getTreeString(sentence)
    
    #parseTree = Tree(treeString)
    
    #print parseTree
    
    
    