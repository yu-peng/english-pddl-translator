'''
Created on Dec 6, 2012

@author: yupeng
'''

#from PIL import Image, ImageTk 
from Tkinter import *
from ttk import *
from notebook import *

from parseSentence import *
from getElement import *
from getElementSubtree import *
from GraphPlanWrapper import *

class UhuraGUI(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="azure2")   
         
        self.parent = parent
        self.initUI()


    def initUI(self):
        
        
        self.parent.title("Uhura V0.2: An English -> RMPL/PDDL Translator    by Peng Yu and Jonathan Trevino")
        
        self.style = Style()
        self.style.theme_use("default")
        
        self.pack(fill=BOTH, expand=1)
                
        w = 940
        h = 1000

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        
        
        #TranslatorFrame = Frame(self,width=980, height=880,borderwidth=1, background="azure2")
        
        
        Tabs = notebook(self, TOP)
        TranslatorFrame = Frame(Tabs(),width=930, height=980,borderwidth=1, background="azure2")        
        self.buildTranslatorFrame(TranslatorFrame)
        RMPLTestFrame = Frame(Tabs(),width=930, height=980,borderwidth=1, background="azure2")
        self.buildRMPLFrame(RMPLTestFrame)
        PDDLTestFrame = Frame(Tabs(),width=930, height=980,borderwidth=1, background="azure2")
        self.buildPDDLFrame(PDDLTestFrame)
        

        Tabs.add_screen(TranslatorFrame, "        Translator        ")
        Tabs.add_screen(RMPLTestFrame, "        RMPL Test        ")
        Tabs.add_screen(PDDLTestFrame, "        PDDL Test        ")

     
        
         
        print 'Done making GUI'
        
        
    def buildPDDLFrame(self,PDDLTestFrame):
        
        NameLabel = Label(PDDLTestFrame, text="Specify the goals of a planning problem using English sentences. \n "+
        "The translator will generate the PDDL expressions and ask a planner to find solutions. \n"+
        "This test focuses on the spatial relations of the goal states.", background="azure2")
        NameLabel.place(x=10,y=10)
        
        
        ProblemDesLabel = Label(PDDLTestFrame, text="Choose a sample scenario:", background="azure2")
        ProblemDesLabel.place(x=10,y=70)
        
        self.PDDLscenario = IntVar()
        self.PDDLscenario.set(1)
        Radiobutton(PDDLTestFrame, text="Block world", variable=self.PDDLscenario, value=1, background="azure2",command=self.changePDDLDomain).place(x=200,y=70)
        Radiobutton(PDDLTestFrame, text="Lunar exploration", variable=self.PDDLscenario, value=2, background="azure2",command=self.changePDDLDomain).place(x=360,y=70)

        ProblemDesFrame = Frame(PDDLTestFrame,width=580, height=170,borderwidth=2,relief=RIDGE)
        ProblemDesFrame.place(x=10,y=90)
        
        self.PDDLProblemDes = Label(ProblemDesFrame,text='', justify=LEFT)
        self.PDDLProblemDes.place(x=0,y=0) 
        
        GiveInput = Label(PDDLTestFrame, text="Describe your goals in English:", background="azure2")
        GiveInput.place(x=10,y=270)
        
        InputPDDLGoalFrame = Frame(PDDLTestFrame, height=50, width=290)
        InputPDDLGoalFrame.pack_propagate(0) # don't shrink
        InputPDDLGoalFrame.place(x=10,y=290)
        
        self.InputPDDLGoal = Text(InputPDDLGoalFrame)
        self.InputPDDLGoal.pack(fill=BOTH, expand=1)
        self.InputPDDLGoal.insert(1.0, '')
        
        AddPDDLButtonFrame = Frame(PDDLTestFrame, height=40, width=120)
        AddPDDLButtonFrame.pack_propagate(0) # don't shrink
        AddPDDLButtonFrame.place(x=15,y=350)
        
        AddPDDLButton = Button(AddPDDLButtonFrame, text="\nAdd to PDDL\n",command=self.AddPDDL)
        AddPDDLButton.pack(fill=BOTH, expand=1)
        
        RemoveLastPDDLButtonFrame = Frame(PDDLTestFrame, height=40, width=120)
        RemoveLastPDDLButtonFrame.pack_propagate(0) # don't shrink
        RemoveLastPDDLButtonFrame.place(x=170,y=350)
        
        RemoveLastPDDLButton = Button(RemoveLastPDDLButtonFrame, text="\nRemove last input\n",command=self.RemovePDDL)
        RemoveLastPDDLButton.pack(fill=BOTH, expand=1)
        
        PlanPDDLButtonFrame = Frame(PDDLTestFrame, height=50, width=290)
        PlanPDDLButtonFrame.pack_propagate(0) # don't shrink
        PlanPDDLButtonFrame.place(x=10,y=400)
        
        PlanPDDLButton = Button(PlanPDDLButtonFrame, text="\nPlan!\n",command=self.PlanPDDL)
        PlanPDDLButton.pack(fill=BOTH, expand=1)
        
        ReceivedPDDLLabel = Label(PDDLTestFrame, text="Received PDDL goals:", background="azure2")
        ReceivedPDDLLabel.place(x=310,y=270)
        
        ReceivedPDDLFrame = Frame(PDDLTestFrame, height=170, width=290)
        ReceivedPDDLFrame.pack_propagate(0) # don't shrink
        ReceivedPDDLFrame.place(x=310,y=290)
        
        self.ReceivedPDDL = Text(ReceivedPDDLFrame)
        self.ReceivedPDDL.pack(fill=BOTH, expand=1)
        self.ReceivedPDDL.insert(1.0, '')
        
        ReceivedPDDLActionsLabel = Label(PDDLTestFrame, text="Received Actions (will not be used in the planner):", background="azure2")
        ReceivedPDDLActionsLabel.place(x=610,y=270)
        
        ReceivedPDDLActionsFrame = Frame(PDDLTestFrame, height=170, width=290)
        ReceivedPDDLActionsFrame.pack_propagate(0) # don't shrink
        ReceivedPDDLActionsFrame.place(x=610,y=290)
        
        self.ReceivedPDDLActions = Text(ReceivedPDDLActionsFrame)
        self.ReceivedPDDLActions.pack(fill=BOTH, expand=1)
        self.ReceivedPDDLActions.insert(1.0, '')
        
        InitialPDDLConditionLabel = Label(PDDLTestFrame, text="Initial Condition:", background="azure2")
        InitialPDDLConditionLabel.place(x=610,y=70)
        InitialPDDLConditionFrame = Frame(PDDLTestFrame,width=290, height=170,borderwidth=2,relief=RIDGE, background="azure2")
        InitialPDDLConditionFrame.place(x=610,y=90)
        self.InitialConditionPDDL = Label(InitialPDDLConditionFrame,text='', justify=LEFT, background="azure2")
        self.InitialConditionPDDL.place(x=0,y=0)
        
        InitialPDDLActionLabel = Label(PDDLTestFrame, text="Available Actions:", background="azure2")
        InitialPDDLActionLabel.place(x=10,y=480)
        InitialPDDLActionFrame = Frame(PDDLTestFrame,width=350, height=400,borderwidth=2,relief=RIDGE, background="azure2")
        InitialPDDLActionFrame.place(x=10,y=500) 
        self.DomainConditionPDDL = Label(InitialPDDLActionFrame,text='', justify=LEFT, background="azure2")
        self.DomainConditionPDDL.place(x=0,y=0)        
        
        PDDLPlanLabel = Label(PDDLTestFrame, text="Generated Plan:", background="azure2")
        PDDLPlanLabel.place(x=380,y=480)
        PDDLPlanFrame = Frame(PDDLTestFrame,width=520, height=400,borderwidth=2,relief=RIDGE, background="azure2")
        PDDLPlanFrame.place(x=380,y=500)
        self.PDDLPlan = Label(PDDLPlanFrame,text='', justify=LEFT, background="azure2")
        self.PDDLPlan.place(x=0,y=0)  
        
        self.SetPDDLBlockWorld()
        
        self.ReceivedPDDLStrings = [] 
        self.ReceivedPDDLActionStrings = [] 
 
    def changePDDLDomain(self):
        
        if self.PDDLscenario.get() == 1:
            # Blocksworld domain
            self.SetPDDLBlockWorld()
        elif self.PDDLscenario.get() == 2:
            # Lunar domain
            self.SetPDDLLunarMission()
            
         
    def buildRMPLFrame(self,RMPLTestFrame):
        
        NameLabel = Label(RMPLTestFrame, text="Specify the goals of a planning problem using English sentences. \n "+
        "The translator will generate the RMPL expressions and ask a planner to find solutions. \n"+
        "This test focuses on the temporal relations of the goal states.", background="azure2")
        NameLabel.place(x=10,y=10)
        
        
        ProblemDesLabel = Label(RMPLTestFrame, text="Choose a sample scenario:", background="azure2")
        ProblemDesLabel.place(x=10,y=70)
        
        self.RMPLscenario = IntVar()
        self.RMPLscenario.set(2)
#        Radiobutton(RMPLTestFrame, text="Around the campus", variable=self.RMPLscenario, value=1, background="azure2").place(x=200,y=70)
        Radiobutton(RMPLTestFrame, text="Weekend shopping", variable=self.RMPLscenario, value=2, background="azure2").place(x=360,y=70)
#        Radiobutton(RMPLTestFrame, text="Christmas trip", variable=self.RMPLscenario, value=3, background="azure2").place(x=520,y=70)
#        Radiobutton(RMPLTestFrame, text="Around the world", variable=self.RMPLscenario, value=4, background="azure2").place(x=680,y=70)

        
        ProblemDesFrame = Frame(RMPLTestFrame,width=900, height=150,borderwidth=2,relief=RIDGE)
        ProblemDesFrame.place(x=10,y=100)
        
        self.RMPLProblemDes = Label(ProblemDesFrame,text='It is a sunny Sunday morning and you are about to start a day trip around Cambridge.\n'+
                                   'You are going to pick up your clothes from a laundry store, have lunch in Chinatown and shop for grocery.\n'+
                                   'In addition, you have a smart car that can understand your requests and will generate the best travel plan that satisfies all your goals.\n'+
                                   'Please describe your requirements in the following text box, such as "go to the lunch place in 30 minutes" \n'+
                                   'or "visit the laundry store before the grocery store".', justify=LEFT)
        self.RMPLProblemDes.place(x=0,y=0) 
        
        GiveInput = Label(RMPLTestFrame, text="Describe your goals in English:", background="azure2")
        GiveInput.place(x=10,y=270)
        
        InputRMPLGoalFrame = Frame(RMPLTestFrame, height=35, width=400)
        InputRMPLGoalFrame.pack_propagate(0) # don't shrink
        InputRMPLGoalFrame.place(x=10,y=290)
        
        self.InputRMPLGoal = Text(InputRMPLGoalFrame)
        self.InputRMPLGoal.pack(fill=BOTH, expand=1)
        self.InputRMPLGoal.insert(1.0, 'The man with a coat wants to eat and drink a cake and two wings.')
        
        AddRMPLButtonFrame = Frame(RMPLTestFrame, height=50, width=160)
        AddRMPLButtonFrame.pack_propagate(0) # don't shrink
        AddRMPLButtonFrame.place(x=35,y=335)
        
        AddRMPLButton = Button(AddRMPLButtonFrame, text="\nAdd to RMPL\n",command=self.AddRMPL)
        AddRMPLButton.pack(fill=BOTH, expand=1)
        
        RemoveLastRMPLButtonFrame = Frame(RMPLTestFrame, height=50, width=160)
        RemoveLastRMPLButtonFrame.pack_propagate(0) # don't shrink
        RemoveLastRMPLButtonFrame.place(x=220,y=335)
        
        RemoveLastRMPLButton = Button(RemoveLastRMPLButtonFrame, text="\nRemove last input\n",command=self.RemoveRMPL)
        RemoveLastRMPLButton.pack(fill=BOTH, expand=1)
        
        PlanRMPLButtonFrame = Frame(RMPLTestFrame, height=50, width=380)
        PlanRMPLButtonFrame.pack_propagate(0) # don't shrink
        PlanRMPLButtonFrame.place(x=20,y=400)
        
        PlanRMPLButton = Button(PlanRMPLButtonFrame, text="\nPlan!\n",command=self.PlanRMPL)
        PlanRMPLButton.pack(fill=BOTH, expand=1)
        
        ReceivedRMPL = Label(RMPLTestFrame, text="Received RMPL goals:", background="azure2")
        ReceivedRMPL.place(x=430,y=270)
        
        ReceivedRMPLFrame = Frame(RMPLTestFrame, height=170, width=470)
        ReceivedRMPLFrame.pack_propagate(0) # don't shrink
        ReceivedRMPLFrame.place(x=430,y=290)
                
        self.ReceivedRMPL = Text(ReceivedRMPLFrame)
        self.ReceivedRMPL.pack(fill=BOTH, expand=1)
        self.ReceivedRMPL.insert(1.0, '')
        
        
        InitialRMPLConditionLabel = Label(RMPLTestFrame, text="Initial Condition:", background="azure2")
        InitialRMPLConditionLabel.place(x=10,y=480)
        InitialConditionRMPLFrame = Frame(RMPLTestFrame,width=250, height=400,borderwidth=2,relief=RIDGE, background="azure2")
        InitialConditionRMPLFrame.place(x=10,y=500)
        self.InitialConditionRMPL = Label(InitialConditionRMPLFrame,text='(t = 0) At home', justify=LEFT, background="azure2")
        self.InitialConditionRMPL.place(x=0,y=0) 
        
        RMPLPlanLabel = Label(RMPLTestFrame, text="Generated Plan:", background="azure2")
        RMPLPlanLabel.place(x=300,y=480)
        RMPLPlanFrame = Frame(RMPLTestFrame,width=600, height=400,borderwidth=2,relief=RIDGE, background="azure2")
        RMPLPlanFrame.place(x=300,y=500)
        self.RMPLPlan = Label(RMPLPlanFrame,text='', justify=LEFT, background="azure2")
        self.RMPLPlan.place(x=0,y=0) 
        
        self.ReceivedRMPLStrings = []
        
        
    def AddRMPL(self):
        
        sent = self.InputRMPLGoal.get(1.0,END)
        print sent
        # show parse tree
        tree = parseEnglish(sent,self.parser.get());
        self.showTree(tree)
        
        AgentSubtree = ExtractAgentSubtree(tree);
        ActionSubtree = ExtractActionSubtree(tree);
        
        print 'Agent: ',AgentSubtree
        print 'Actions: ',ActionSubtree

        agents = []
        actions = []
        
        # Given a NP subtree, get a list of agents inside
        if AgentSubtree != None:
            agents = getAgents(AgentSubtree) 
        # Given a VP subtree, get a list of actions inside
        if ActionSubtree != None:
            actions = getAction(ActionSubtree) 
        
        self.ClearOutputs()
        self.ShowResult(agents,actions)
        Result = self.GenerateRMPL(agents,actions)         
        self.ReceivedRMPLStrings.append(Result)
        self.showReceivedRMPL()

    
    def showReceivedRMPL(self):
        
        StringRMPL = ''
        
        StringMain = 'class Main {\n'
        StringRun = 'method run () {\n'
        StringRun = StringRun + 'parallel {\n'
        
        for input in self.ReceivedRMPLStrings:
        
            NewDefs = input[0]   
            NewActions = input[1]
            NewClasses = input[2]
        
            for NewDef in NewDefs:
                StringMain = StringMain + NewDef
                
            for NewAction in NewActions:
                StringRun = StringRun + NewAction
                
            for NewClass in NewClasses:
                StringRMPL = StringRMPL + NewClass
                
        StringRun = StringRun + '}\n}\n'
        StringMain = StringMain + StringRun + '}\n'
        StringRMPL = StringMain + StringRMPL        

        self.ReceivedRMPL.delete(1.0,END) 
        self.ReceivedRMPL.insert(END, StringRMPL+'\n')

    
    def RemoveRMPL(self):
        
        if len(self.ReceivedRMPLStrings) > 0:
            self.ReceivedRMPLStrings.pop()
        self.showReceivedRMPL()   
      
        
    def PlanRMPL(self):
        
        print 'Sorry, the RMPL temporal planner is not included in this distribution.'  


    def SetPDDLBlockWorld(self):
        
        self.InputPDDLGoal.delete(1.0,END) 
        self.ReceivedPDDL.delete(1.0,END) 
        
        self.PDDLProblemDes.config(text='This is a classic block world scenario.\n'+
                                    'You have three fruits: apple, pear, and orange lying on the table at the moment.\n'+
                                    'You have two available actions that can modify the states of these objects.\n'+
                                    'Describe the desired end states using English sentences,\n'+
                                    'such as "put apple on orange" (case sensitive).\n'+
                                    'Uhura will try to parse the desired states from your input.\n'+
                                    'It will also record the action in your input, but will not use it in the planning process.\n'+
                                    'You can always go back to the Translator tab to check the current parse tree\nand see what is going on.', justify=LEFT)
        
        self.InputPDDLGoal.insert(1.0, 'put apple on pear.')
        self.PDDLInitial = '(apple OBJECT)\n(pear OBJECT)\n(orange OBJECT)\n(preconds  (on-table apple)\n(on-table pear)\n(on-table orange)\n(clear apple)\n(clear pear)\n(clear orange)\n(arm-empty))'
        self.PDDLDomain = '(operator\nSTACK\n(params (<ob> OBJECT) (<underob> OBJECT))\n(preconds\n(clear <underob>) (holding <ob>))\n(effects\n(del holding <ob>) (del clear <underob>)\n(arm-empty) (clear <ob>) (on <ob> <underob>)))\n\n'+'(operator\nPICK-UP\n(params (<ob1> OBJECT))\n(preconds\n(clear <ob1>) (on-table <ob1>) (arm-empty))\n(effects\n(del on-table <ob1>) (del clear <ob1>)\n(del arm-empty) (holding <ob1>)))\n'
        self.InitialConditionPDDL.config(text=self.PDDLInitial, justify=LEFT, background="azure2")
        self.DomainConditionPDDL.config(text=self.PDDLDomain, justify=LEFT, background="azure2")
        
        self.ReceivedPDDLStrings = [] 
        self.ReceivedPDDLActionStrings = [] 


    def SetPDDLLunarMission(self):
        
        self.InputPDDLGoal.delete(1.0,END) 
        self.ReceivedPDDL.delete(1.0,END) 
        
        self.PDDLProblemDes.config(text='This is a lunar mission scenario.\n'+
                                    'You are a rover operator and was sent to the lunar surface with three lovely animals: dog, cat, and pig.\n'+
                                    'They are currently placed in the canyon, but you can transport them to two other places: mountain and river.\n'+
                                    'Describe the desired end states using English sentences,\n'+
                                    'such as "put dog in mountain" (case sensitive).\n'+
                                    'Uhura will try to parse the desired states from your input.\n'+
                                    'It will also record the action in your input, but will not use it in the planning process.\n'+
                                    'You can always go back to the Translator tab to check the current parse tree and see what is going on.', justify=LEFT)
        
        self.InputPDDLGoal.insert(1.0, 'put dog in mountain.')
        self.PDDLDomain = '(operator navigate\n(params (<placefrom> PLACE)\n(<placeto> PLACE))\n(preconds (at <placefrom>) (not-at  <placeto>))\n(effects (at <placeto>) (del at <placefrom>)\n(not-at  <placefrom>)))\n\n(operator pickup\n(params (<item> OBJECT)    (<place> PLACE))\n(preconds (at <place>) (in <item> <place>))\n(effects (del in <item> <place>) (has <item>)))\n\n(operator dropoff\n(params (<item> OBJECT) (<place> PLACE))\n(precons (at <place>) (has <item>))\n(effects (del has <item>) (in <item> <place>)))\n'
        self.PDDLInitial = '(dog OBJECT) (cat OBJECT) (pig OBJECT)\n(canyon PLACE) (mountain PLACE) (river PLACE)\n(preconds\n(at canyon)\n(not-at mountain)\n(not-at river)\n(in dog canyon)\n(in cat canyon)\n(in pig canyon))'
        self.InitialConditionPDDL.config(text=self.PDDLInitial, justify=LEFT, background="azure2")
        self.DomainConditionPDDL.config(text=self.PDDLDomain, justify=LEFT, background="azure2")
        
        self.ReceivedPDDLStrings = [] 
        self.ReceivedPDDLActionStrings = [] 
          

    def AddPDDL(self):
        
        sent = self.InputPDDLGoal.get(1.0,END)
        print sent
        # show parse tree
        tree = parseEnglish(sent,self.parser.get());
        self.showTree(tree)
        
        AgentSubtree = ExtractAgentSubtree(tree);
        ActionSubtree = ExtractActionSubtree(tree);
        
        print 'Agent: ',AgentSubtree
        print 'Actions: ',ActionSubtree

        agents = []
        actions = []
        
        # Given a NP subtree, get a list of agents inside
        if AgentSubtree != None:
            agents = getAgents(AgentSubtree) 
        # Given a VP subtree, get a list of actions inside
        if ActionSubtree != None:
            actions = getAction(ActionSubtree) 
        
        self.ClearOutputs()
        self.ShowResult(agents,actions)
        Result = self.GeneratePDDL(agents,actions) 
        PDDLStateStrings = Result[0]   
        PDDLActionStrings = Result[1]
        
        self.ReceivedPDDLStrings = self.ReceivedPDDLStrings + PDDLStateStrings
        self.ReceivedPDDLActionStrings = self.ReceivedPDDLActionStrings + PDDLActionStrings

        self.ReceivedPDDL.delete(1.0,END) 
        self.ReceivedPDDLActions.delete(1.0,END) 
        
        for string in self.ReceivedPDDLStrings:
            self.ReceivedPDDL.insert(END, string+'\n')
            
        for string in self.ReceivedPDDLActionStrings:
            self.ReceivedPDDLActions.insert(END, string+'\n')            
 
    
    def RemovePDDL(self):
        
        if len(self.ReceivedPDDLStrings) > 0:
            self.ReceivedPDDLStrings.pop()
            
        self.ReceivedPDDL.delete(1.0,END) 
        for string in self.ReceivedPDDLStrings:
            self.ReceivedPDDL.insert(END, string+'\n')    
 
        
    def PlanPDDL(self):
           
        PDDLs = self.ReceivedPDDL.get(1.0,END)

        operators = self.PDDLDomain
        facts = self.PDDLInitial 
        facts = facts + '\n(effects\n'
        facts = facts + PDDLs + ')'
            
        Actions = run_planner(operators,facts)
        
        if Actions == None:
            self.PDDLPlan.config(text='No feasible plan can be found.\nPlease modify your goal settings.')
        else:
            ActionString = ''
            for action in Actions:
                ActionString = ActionString + action +'\n'
            self.PDDLPlan.config(text=ActionString)
         
        
    def buildTranslatorFrame(self,TranslatorFrame):
        
        NameLabel = Label(TranslatorFrame, text="Translate the input English sentence to RMPL/PDDL expression \n"+
                          " by extracting the desired state evolution from its parse tree.", background="azure2")
        NameLabel.place(x=10,y=10)
        
        GiveInput = Label(TranslatorFrame, text="Enter your command in English:", background="azure2")
        GiveInput.place(x=10,y=50)
        
        self.Input = Text(TranslatorFrame,width=50, height=2)
        self.Input.place(x=10,y=70)
        #self.Input.insert(1.0, 'The man with a coat wants to eat and drink a cake and two wings in ten minutes .')
        self.Input.insert(1.0, 'The man with a coat wants to eat and drink a cake and two wings .')
        
        ParserLabel = Label(TranslatorFrame, text="Select an English parser:", background="azure2")
        ParserLabel.place(x=10,y=120)
        
        self.parser = IntVar()
        self.parser.set(1)
        Radiobutton(TranslatorFrame, text="Stanford (Online)", variable=self.parser, value=1, background="azure2").place(x=10,y=140)
        #Radiobutton(TranslatorFrame, text="Bikel-Collins", variable=self.parser, value=2, background="azure2").place(x=160,y=140)
        Radiobutton(TranslatorFrame, text="Viterbi Parser+Customer Corpus", variable=self.parser, value=3, background="azure2").place(x=280,y=140)

        OutputLabel = Label(TranslatorFrame, text="Select an output format:", background="azure2")
        OutputLabel.place(x=10,y=175)

        self.output = IntVar()
        self.output.set(1)
        Radiobutton(TranslatorFrame, text="RMPL", variable=self.output, value=1, background="azure2").place(x=200,y=175)
        Radiobutton(TranslatorFrame, text="PDDL", variable=self.output, value=2, background="azure2").place(x=320,y=175)

        TreeLabel = Label(TranslatorFrame, text="Parse Tree: ", background="azure2")
        TreeLabel.place(x=10,y=210)
        
        self.TreeFrame = Frame(TranslatorFrame,width=460, height=625,borderwidth=2, background="azure2",relief=RIDGE)
        self.TreeFrame.place(x=10,y=230)

        RMPLExpression = Label(TranslatorFrame, text="RMPL/PDDL Expression:", background="azure2")
        RMPLExpression.place(x=510,y=10)
        
        self.RMPL = Text(TranslatorFrame,width=50, height=10)
        self.RMPL.place(x=510,y=30)
        
        #CommandType = Label(TranslatorFrame, text="Type of Commands:", background="azure2")
        #CommandType.place(x=510,y=120)
        
        #self.Command = Text(TranslatorFrame,width=50, height=2)
        #self.Command.place(x=510,y=140)
        #self.Command.insert(1.0, 'Temporal goal / Spatial goal / A mix of both ')

        
        
        ElementsMapping = Label(TranslatorFrame, text="Elements Mapping:", background="azure2")
        ElementsMapping.place(x=510,y=200)
        
        
        AgentLabel = Label(TranslatorFrame, text="Agent -> ", background="azure2")
        AgentLabel.place(x=510,y=240)        
        self.Agent = Text(TranslatorFrame,width=36, height=1, background="azure2")
        self.Agent.place(x=620,y=240)
        
        
        AgentModifierLabel = Label(TranslatorFrame, text="Agent Modifier -> ", background="azure2")
        AgentModifierLabel.place(x=510,y=280)        
        self.AgentModifier = Text(TranslatorFrame,width=36, height=1, background="azure2")
        self.AgentModifier.place(x=620,y=280)
        
        
        TargetLabel = Label(TranslatorFrame, text="Target -> ", background="azure2")
        TargetLabel.place(x=510,y=320)        
        self.Target = Text(TranslatorFrame,width=36, height=1, background="azure2")
        self.Target.place(x=620,y=320)
        
        
        TargetModifierLabel = Label(TranslatorFrame, text="Target Modifier -> ", background="azure2")
        TargetModifierLabel.place(x=510,y=360)        
        self.TargetModifier = Text(TranslatorFrame,width=36, height=1, background="azure2")
        self.TargetModifier.place(x=620,y=360)
        
        
        InitialStateLabel = Label(TranslatorFrame, text="Initial State -> ", background="azure2")
        InitialStateLabel.place(x=510,y=400)        
        self.InitialState = Text(TranslatorFrame,width=36, height=1, background="azure2")
        self.InitialState.place(x=620,y=400)
        
        
        TargetStateLabel = Label(TranslatorFrame, text="Target State -> ", background="azure2")
        TargetStateLabel.place(x=510,y=440)        
        self.TargetState = Text(TranslatorFrame,width=36, height=1, background="azure2")
        self.TargetState.place(x=620,y=440)
        
        
        ActionLabel = Label(TranslatorFrame, text="Action -> ", background="azure2")
        ActionLabel.place(x=510,y=480)        
        self.Action = Text(TranslatorFrame,width=36, height=1, background="azure2")
        self.Action.place(x=620,y=480)
        
        ActionModifierLabel = Label(TranslatorFrame, text="Action Modifier -> ", background="azure2")
        ActionModifierLabel.place(x=510,y=520)
        self.ActionModifier = Text(TranslatorFrame,width=36, height=1, background="azure2")
        self.ActionModifier.place(x=620,y=520)
        
        
        MessageLabel = Label(TranslatorFrame, text="Execution message:", background="azure2")
        MessageLabel.place(x=510,y=600)
        
        self.MessageFrame = Frame(TranslatorFrame,width=200,height=100,borderwidth=1)
        self.MessageFrame.place(x=510,y=620)
        
        self.Message = Text(self.MessageFrame, wrap=WORD,width=47,height=12)
        self.Message.pack(side=LEFT)           
        MessageScrollbar = Scrollbar(self.MessageFrame)
        MessageScrollbar.pack(side=RIGHT, fill=Y) 
        self.Message.config(yscrollcommand=MessageScrollbar.set)
        MessageScrollbar.config(command=self.Message.yview)
        
        TranslateButtonFrame = Frame(TranslatorFrame, height=50, width=870)
        TranslateButtonFrame.pack_propagate(0) # don't shrink
        TranslateButtonFrame.place(x=35,y=1000-120)
        
        #b = Button(f, text="Sure!")
        #b.pack(fill=BOTH, expand=1)
        
        TranslateButton = Button(TranslateButtonFrame, text="\nTranslate!\n",command=self.translate)
        TranslateButton.pack(fill=BOTH, expand=1)
        
 
    def showTree(self,tree):

        canvas = getCanvas(self.TreeFrame,tree)

        xscrollbar = Scrollbar(self.TreeFrame, orient=HORIZONTAL)
        xscrollbar.grid(row=1,column=0, sticky=W+E)
        xscrollbar.config(command=canvas.xview)
        
        yscrollbar = Scrollbar(self.TreeFrame,orient=VERTICAL)
        yscrollbar.grid(row=0,column=1, sticky=N+S)
        yscrollbar.config(command=canvas.yview)
        
        canvas.config(width=430,height=600)
        canvas.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        canvas.grid(row=0,column=0, sticky=N+S)
   
        
    def translate(self):
        
        sent = self.Input.get(1.0,END)
        print sent
        if self.output.get() == 1:
            self.Message.insert(END,'Translating:\n '+sent+' to RMPL\n');
        elif self.output.get() == 2:
            self.Message.insert(END,'Translating:\n '+sent+' to PDDL\n');

        # show parse tree
        tree = parseEnglish(sent,self.parser.get());
        self.showTree(tree)
        # Extract agents and actions
        
        # Agent first
        
        AgentSubtree = ExtractAgentSubtree(tree);
        ActionSubtree = ExtractActionSubtree(tree);
        
        print 'Agent: ',AgentSubtree
        print 'Actions: ',ActionSubtree

        agents = []
        actions = []
        
        # Given a NP subtree, get a list of agents inside
        if AgentSubtree != None:
            agents = getAgents(AgentSubtree) 
        # Given a VP subtree, get a list of actions inside
        if ActionSubtree != None:
            actions = getAction(ActionSubtree) 
        #actions = actions+getAction(tree[0][1][1][0])
        
        #actions = getAction(tree[0][0]) 
        
        self.ClearOutputs()
        self.ShowResult(agents,actions)
        if self.output.get() == 1:
            self.GenerateRMPL(agents,actions)
        elif self.output.get() == 2:
            self.GeneratePDDL(agents,actions)
            

    def ShowResult(self,agents,actions):
        
        for agent in agents:
            if agent.getNounString() != '':
                self.Agent.insert(END,agent.getNounString()+'; '); 
            if agent.getPPString() != '':
                self.AgentModifier.insert(END,agent.getPPString()+'; '); 

        for action in actions:
            self.Action.insert(END,action.getActionString()+'; '); 
            if action.getPPString() != '':
                self.ActionModifier.insert(END,action.getPPString()+'; '); 
                
            self.Target.insert(END,'(');   
            self.TargetModifier.insert(END,'(');
            
            for target in action.getNPs():
                
                if target.getNounString() != '': 
                    self.Target.insert(END,target.getNounString()+';');
                if target.getPPString() != '': 
                    self.TargetModifier.insert(END,target.getPPString()+';');
                    
            self.Target.insert(END,') ');   
            self.TargetModifier.insert(END,') ');
                
                
    def GenerateRMPL(self,agents,actions):
        
        # Assume single agent
        Agent = ''
        Time = ''
        Action = ''
        Target = ''
        
        AgentModifier = ''
        ActionModifier = ''
        TargetModifier = ''
        
        StringRMPL = ''
        
        StringMain = 'class Main {\n'
        StringRun = 'method run () {\n'
        StringRun = StringRun + 'parallel {\n'
        
        NewClass = []
        NewAction = []
        NewDefinition = []

        #If there is at least one agent
        if (len(agents) < 1):
            #Build virtual agent
            agent = NounGroup()
            agent.addNP('VirtualAgent')
            agents.append(agent)

        for agent in agents:
            
            Agent = agent.getNounString() 
            AgentModifier = agent.getPPString() 
            
            StringClass = ''
            StringClass = 'class '+Agent.upper()+'{\n'
            StringDef = Agent.upper() + ' ' + Agent + ';\n'
            #StringMain = StringMain + Agent.upper() + ' ' + Agent + ';\n'    
            
            if AgentModifier != '':
                StringClass = StringClass + 'value ' + AgentModifier + ';\n'
                StringDef = StringDef + Agent+'=='+AgentModifier + ';' + '\n' 
                #StringMain = StringMain + Agent+'=='+AgentModifier + ';' + '\n'   
                     
            StringMain = StringMain + StringDef
            NewDefinition.append(StringDef)
            
            for action in actions:
                Action = action.getActionString()
                ActionModifier = action.getPPString()
                
                StringClass = StringClass + 'method ' + Action +'();\n'
                 
                for target in action.getNPs():
                    Target = Target + ',"' +target.getNounString()+'"'                     
                    TargetModifier = target.getPPString()             
                    if TargetModifier != '':
                          Target = Target + '['+TargetModifier+']'
                    
                NewActionString = Agent + '.' + Action + '[' + ActionModifier + ']'+ '(' + Target[1:] + ')\n'  
                StringRun = StringRun + NewActionString
                NewAction.append(NewActionString)
                Action = ''
                Target = ''
                ActionModifier = ''
                TargetModifier = ''
                
            StringClass = StringClass + '}\n'
            StringRMPL = StringRMPL + StringClass
            NewClass.append(StringClass)
            
        StringRun = StringRun + '}\n}\n'
        StringMain = StringMain + StringRun + '}\n'
        StringRMPL = StringMain + StringRMPL
        self.RMPL.insert(END, StringRMPL)
        
        return[NewDefinition,NewAction,NewClass]


    def GeneratePDDL(self,agents,actions):
        
        PDDLStateStrings = []
        PDDLActionStrings = []

        for action in actions:
            
            #build a virtual target, if no target
            if len(action.getNPs()) == 0:
                VirtualTarget = NounGroup()
                VirtualTarget.addNP(' ')
                action.addNP(VirtualTarget)
                
            
            for target in action.getNPs():
                

                
                if len(action.getPPs()) > 0:
                    
                    PP = action.getPPs()[0]
                    Prop = PP.getPropString()
                    
                    #if there is a NP in the PP
                    if len(PP.getNPs()) > 0:                    
                        for PPNP in PP.getNPs():
                            
                            PDDLActionString = '('
                            PDDLStateString = '('
                            PDDLActionString = PDDLActionString + action.getActionString()
    
                            PDDLActionString = PDDLActionString + '-' + Prop + ' ' + target.getNounString()
                            PDDLActionString = PDDLActionString + ' ' + PPNP.getNounString()
    
                            PDDLStateString = PDDLStateString + Prop + ' ' + target.getNounString()
                            PDDLStateString = PDDLStateString + ' ' + PPNP.getNounString()
                        
                    
                            if target.getPPString() != '': 
                                PDDLActionString = PDDLActionString + '-' + target.getPPString() 
                    
                            PDDLActionString = PDDLActionString + ')'   
                            PDDLStateString = PDDLStateString + ')'                                     
                            PDDLActionStrings.append(PDDLActionString)
                            PDDLStateStrings.append(PDDLStateString)
                                   
                            self.RMPL.insert(END, PDDLActionString+'\n')
                            self.RMPL.insert(END, PDDLStateString+'\n')
                    else:
                        # If there is a PP but no NP inside
                        PDDLActionString = '('
                        PDDLActionString = PDDLActionString + action.getActionString()

                        PDDLActionString = PDDLActionString + '-' + Prop + ' ' + target.getNounString()
                
                        if target.getPPString() != '': 
                            PDDLActionString = PDDLActionString + '-' + target.getPPString() 
                
                        PDDLActionString = PDDLActionString + ')'                                   
                        PDDLActionStrings.append(PDDLActionString)
                               
                        self.RMPL.insert(END, PDDLActionString+'\n')
                        
                else:
                    
                    PDDLActionString = '('
                    PDDLActionString = PDDLActionString + action.getActionString()                    
                    PDDLActionString = PDDLActionString + ' ' + target.getNounString()
                    if target.getPPString() != '': 
                        PDDLActionString = PDDLActionString + '-' + target.getPPString() 
                    
                    PDDLActionString = PDDLActionString + ')'                          
                    PDDLActionStrings.append(PDDLActionString)
                           
                    self.RMPL.insert(END, PDDLActionString+'\n')
                    
        return [PDDLStateStrings,PDDLActionStrings]

                
    def ClearOutputs(self):
        
        self.RMPL.delete(1.0,END); 
        self.Agent.delete(1.0,END); 
        self.AgentModifier.delete(1.0,END); 
        self.Target.delete(1.0,END); 
        self.TargetModifier.delete(1.0,END); 
        self.InitialState.delete(1.0,END); 
        self.TargetState.delete(1.0,END); 
        self.Action.delete(1.0,END); 
        self.ActionModifier.delete(1.0,END); 
       
       
def main():
  
    root = Tk()
    Uhura = UhuraGUI(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  