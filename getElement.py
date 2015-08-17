'''
Created on Dec 7, 2012

@author: yupeng
'''


class ActionGroup:
    
    def __init__(self):
        self.Actions = []
        self.PPs = []
        self.NPs = []
        
    def addAction(self,actionString):
        self.Actions.append(actionString)
        
    def addActions(self,actionList):
        self.Actions = self.Actions + actionList
        
    def addPP(self,PP):
        self.PPs.append(PP)
        
    def addPPs(self,PPList):
        self.PPs = self.PPs + PPList

    def addNP(self,NP):
        self.NPs.append(NP)
        
    def addNPs(self,NPList):
        self.NPs = self.NPs + NPList      
        
    def getActions(self):
        return self.Actions
    
    def getPPs(self):
        return self.PPs
    
    def getNPs(self):
        return self.NPs
    
    def getString(self):
        
        AGString = 'Action: '
        
        for action in self.Actions:
            AGString = AGString + action + '; '
        
        AGString = AGString + '  NPs: '
        
        for NP in self.NPs:
            AGString = AGString + NP.getString() + '; '
        
        AGString = AGString + '  PPs: '
        
        for PP in self.PPs:
            AGString = AGString + PP.getString() + '; '
        
        return AGString
    
    def getActionString(self):
        
        ActionString = ''
        
        for action in self.Actions:
            ActionString = ActionString + action
        
        return ActionString
    
    def getPPString(self):
        
        PPString = ''
        
        for PP in self.PPs:
            PPString = PPString + '-' + PP.getOriginalString()
        
        return PPString[1:]
    
    def getTargetString(self):
        
        TargetString = ''
        
        for NP in self.NPs:
            TargetString = TargetString + '-' + NP.getNounString()
        
        return TargetString[1:]
    
    
class NounGroup:
    
    def __init__(self):
        self.NPs = []
        self.PPs = []
        
    def addPP(self,PP):
        self.PPs.append(PP)
        
    def addPPs(self,PPList):
        self.PPs = self.PPs + PPList

    def addNP(self,NPString):
        self.NPs.append(NPString)
        
    def addNPs(self,NPList):
        self.NPs = self.NPs + NPList      
        
    def getPPs(self):
        return self.PPs
    
    def getNPs(self):
        return self.NPs
    
    def getString(self):
        
        NGString = 'NounPhrase: '
        
        for NP in self.NPs:
            NGString = NGString + NP + '; '
        
        NGString = NGString + '  PPs: '
        
        for PP in self.PPs:
            NGString = NGString + PP.getString() + '; '
        
        return NGString
    
    def getNounString(self):
        
        NounString = ''
        
        for NP in self.NPs:
            NounString = NounString + '-' + NP
        
        return NounString[1:]
    
    def getPPString(self):
        
        PPString = ''
        
        for PP in self.PPs:
            PPString = PPString + '-' + PP.getOriginalString()
        
        return PPString[1:]
    
    
class PPGroup:
    
    def __init__(self):
        self.Propositions = []
        self.NPs = []
        self.String = ''
        
    def addProp(self,PPString):
        self.Propositions.append(PPString)
        
    def addProps(self,PPList):
        self.Propositions = self.Propositions + PPList

    def addNP(self,NP):
        self.NPs.append(NP)
        
    def addNPs(self,NPList):
        self.NPs = self.NPs + NPList 
        
    def setString(self,PPString):
        self.String = PPString 
        
    def getOriginalString(self):
        return self.String 
        
    def getProps(self):
        return self.Propositions
    
    def getNPs(self):
        return self.NPs
    
    def getString(self):
        
        PropString = 'Propositions: '
        
        for Proposition in self.Propositions:
            PropString = PropString + Proposition + '; '
            
        PropString = PropString + '  NPs: '        
        
        for NP in self.NPs:
            PropString = PropString + NP.getString() + '; '
            
        return PropString
    
    
    def getPropString(self):
        
        PropString = ''
        
        for Proposition in self.Propositions:
            PropString = PropString+'-'+Proposition
            
        return PropString[1:]
    
    
        
def getAgent(tree):
    
    # Extract the agent from a noun phrase
    
    if (tree.node != 'NP'):
        print 'The given substree is not rooted at a NP'
        return None
    else:
        # Determine the number of agents
        agent_count = 0
        for subtree1 in tree:
            if (subtree1.node == 'NP'):
                agent_count = agent_count + 1
        
        if (agent_count < 2):
            
            #single agent
            agent = ''                
            for leave in tree.leaves():
                agent = agent+'-'+str(leave)
                    
            return [agent[1:]]
        
        else:
            #multiple agent
            agent = []
            for subtree1 in tree:
                if (subtree1.node == 'NP'):                    
                    NewAgent = getAgent(subtree1)
                    print 'adding ',NewAgent,' to ',agent
                    if NewAgent != None:
                        agent = agent + NewAgent
                    
            return agent


        
def getAction(tree):
    
    # Extract the action from a verb phrase
    VPList = ['VP','VB','VBD','VBG','VBN','VBP','VBZ']
    TerminalList = ['VB','VBD','VBG','VBN','VBP','VBZ']
    
    PPList = ['PP','ADVP','ADVP']
    NPList = ['NP']
    
    if not any(tree.node == tag for tag in VPList):
        print 'The given substree is not rooted at a verb phrase'
        return None
    else:
        # Determine the number of agents
        PPs = []
        NPs = []
        NewActions = []
        ChildrenActions = []
        actionList = []
        
        for subtree in tree:
            if any(subtree.node == tag for tag in PPList): 
                PPs.append(getPPforVP(subtree))
            elif any(subtree.node == tag for tag in NPList): 
                NPs = NPs + getTargets(subtree)
            elif any(subtree.node == tag for tag in TerminalList):
                NewAction = ''
                for leave in subtree.leaves():
                    NewAction = NewAction+' '+str(leave)
                NewActions.append(NewAction[1:])
            elif subtree.node == 'VP':
                ChildrenActions = ChildrenActions + getAction(subtree)         
        
        for action in NewActions:
            NewAction = ActionGroup()
            NewAction.addAction(action)
            NewAction.addPPs(PPs)
            NewAction.addNPs(NPs)
            actionList.append(NewAction)
            
        for action in ChildrenActions:
            action.addPPs(PPs)
            action.addNPs(NPs)
            actionList.append(action)

        return actionList


def getTargets(tree):
    
    # Extract the agent from a noun phrase
    
    if (tree.node != 'NP'):
        print 'The given substree is not rooted at a NP'
        return None
    else:
                
        PPs = []
        ChildrenTargets = []
        targetList = []
        
        for subtree in tree:
            if subtree.node == 'NP': 
                ChildrenTargets = ChildrenTargets + getTargets(subtree)
            elif subtree.node == 'PP':  
                PPs.append(getPPforNP(subtree))
                
        if (len(ChildrenTargets) < 1):
            
            #This is a bottom level NP
            TargetString = ''                
            for leave in tree.leaves():
                if leave == 'and' or leave == 'or':
                    NewTarget = NounGroup() 
                    NewTarget.addNP(TargetString[1:]) 
                    targetList.append(NewTarget)  
                    TargetString = ''
                else:  
                    TargetString = TargetString+' '+str(leave)
            
            NewTarget = NounGroup() 
            NewTarget.addNP(TargetString[1:]) 
            targetList.append(NewTarget)  
            return targetList
        
        else:
            for Target in ChildrenTargets:
                Target.addPPs(PPs)
                targetList.append(Target)
            
            #print 'returning ',targetList 
            return targetList
        



def getAgents(tree):
    
    # Extract the agent from a noun phrase
    
    if (tree.node != 'NP'):
        print 'The given substree is not rooted at a NP'
        return None
    else:
                
        PPs = []
        ChildrenTargets = []
        targetList = []
        
        for subtree in tree:
            if subtree.node == 'NP': 
                ChildrenTargets = ChildrenTargets + getTargets(subtree)
            elif subtree.node == 'PP':  
                PPs.append(getPPforNP(subtree))
                
        if (len(ChildrenTargets) < 1):
            
            #This is a bottom level NP
            TargetString = ''                
            for leave in tree.leaves():
                if leave == 'and' or leave == 'or':
                    NewTarget = NounGroup() 
                    NewTarget.addNP(TargetString[1:]) 
                    targetList.append(NewTarget)  
                    TargetString = ''
                else:  
                    TargetString = TargetString+' '+str(leave)
            
            NewTarget = NounGroup() 
            NewTarget.addNP(TargetString[1:]) 
            targetList.append(NewTarget)  
            return targetList
        
        else:
            for Target in ChildrenTargets:
                Target.addPPs(PPs)
                targetList.append(Target)
            
            #print 'returning ',targetList 
            return targetList


def getPPforVP(tree):
    
    # Extract the modifier for a verb phrase
    PPList = ['PP','ADVP']

    if not any(tree.node == tag for tag in PPList):
        print 'The given substree is not a PP for verb phrase'
        return None
    else:
        #Get all leaves
        
        PP = PPGroup()
        PropositionList = []  
        PPString = ''
        
        for subtree in tree:
            if subtree.node == 'NP': 
                PP.addNPs(getTargets(subtree))
            else:
                PropositionList = PropositionList + subtree.leaves()
                
            for leave in subtree.leaves():    
                PPString = PPString + ' ' + leave
        
        PropositionString = ''
        for proposition in PropositionList:
            PropositionString = PropositionString + ' ' + proposition
        
        PP.addProp(PropositionString[1:])
        PP.setString(PPString[1:])
            
        return PP
    
    
    
    
def getPPforNP(tree):
    
    # Extract the modifier for a verb phrase
    PPList = ['PP','ADJP']

    if not any(tree.node == tag for tag in PPList):
        print 'The given substree is not a PP for verb phrase'
        return None
    else:
        #Get all leaves
        
        PP = PPGroup()
        PropositionList = []
        PPString = ''
        
        for subtree in tree:
            if subtree.node == 'NP': 
                PP.addNPs(getTargets(subtree))
            else:
                PropositionList = PropositionList + subtree.leaves()
            for leave in subtree.leaves():    
                PPString = PPString + ' ' + leave
                
        PropositionString = ''
        for proposition in PropositionList:
            PropositionString = PropositionString + ' ' + proposition
        
        PP.addProp(PropositionString[1:])
        PP.setString(PPString[1:])
        
        return PP
