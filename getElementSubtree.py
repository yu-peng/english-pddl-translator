'''
Created on Dec 13, 2012

@author: yupeng
'''

def ExtractActionSubtree(tree):
    
    if tree.node != 'VP':
        for subtree in tree:
            if isinstance(subtree, list):
                action = ExtractActionSubtree(subtree)
                if action != None:
                    return action
    else:
        print ' '
        # if this subtree start with an NP
        # check if it is in fact an agent            
        isAClause = False
        
        for subtree in tree:                
            if (subtree.node == 'S'):
                isAClause = True
                if isinstance(subtree, list):
                    action = ExtractActionSubtree(subtree)
                    if action != None:
                        return action
        
        if not isAClause:
            return tree
           
                   
    return None
    
    
def ExtractAgentSubtree(tree):
    
    if tree.node != 'NP' and tree.node != 'VP':
        for subtree in tree:
            if isinstance(subtree, list):
                #print subtree
                agent = ExtractAgentSubtree(subtree)
                if agent != None:
                    return agent
            
    elif tree.node == 'NP':
        print ' '
        # if this subtree start with an NP
        # check if it is in fact an agent
        
        return tree
        
    return None