'''
Created on Dec 12, 2012

@author: yupeng
'''

import os
import platform
import subprocess


def run_planner(operators, facts):
    output_from_planner = ""
    
    print 'OPERATORS: ',operators
    print 'FACTS: ',facts
    
    print 'Current path',os.getcwd()
    ext_file = open("Output.txt", "w")
    
    if platform.system() == 'Windows':
        # Use windows executable
        ff_name = "GraphPlanWin" + os.sep + "graphplan.exe"
        operators_file = "GraphPlanWin" + os.sep + "ops.txt"
        facts_file = "GraphPlanWin" + os.sep + "facts.txt" 
        
        opsfile = open(operators_file, "w")
        opsfile.write(operators)
        opsfile.close()
        
        factfile = open(facts_file, "w")
        factfile.write(facts)
        factfile.close()
        
        print 'operators_file path ',operators_file
        print 'facts_file path ',facts_file
        
    elif platform.system() == 'Linux':
        # Use windows executable
        ff_name = "GraphPlanLinux" + os.sep + "graphplan"
        operators_file = "GraphPlanLinux" + os.sep + "ops.txt"
        facts_file = "GraphPlanLinux" + os.sep + "facts.txt" 
        
        opsfile = open(operators_file, "w")
        opsfile.write(operators)
        opsfile.close()
        
        factfile = open(facts_file, "w")
        factfile.write(facts)
        factfile.close()
        
        print 'operators_file path ',operators_file
        print 'facts_file path ',facts_file
        
    else:
        # Use windows executable
        ff_name = "GraphPlanMac" + os.sep + "graphplan"
        operators_file = "GraphPlanMac" + os.sep + "ops.txt"
        facts_file = "GraphPlanMac" + os.sep + "facts.txt" 
        
        opsfile = open(operators_file, "w")
        opsfile.write(operators)
        opsfile.close()
        
        factfile = open(facts_file, "w")
        factfile.write(facts)
        factfile.close()
        
        print 'operators_file path ',operators_file
        print 'facts_file path ',facts_file


    try:
        output_from_planner = subprocess.check_output([ff_name, "-o", operators_file, "-f", facts_file, "-d"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        # Some sort of error occured!
        output_from_planner = e.output
        print output_from_planner
        return None
    
    print output_from_planner
#    
    a = output_from_planner.split("\n\n")
    if len(a) == 1:
        print "A valid plan wasn't found! Return None."
        return None
    else:
        lines = a[1].split("\n")
        Actions = []
        for line in lines:
            if "entries in hash table" in line:
                break
            else:
                #print 'Reading: ',line
                Action = line.replace("_"," ")
                print Action
                Actions.append(Action)
        return Actions
#    # Now, work to extract the steps of the plan.
#    b = a[1].split("\n     \n")
#    c = b[0].split("\n")
#    
#    for i in range(len(c)):
#        splitted = c[i].strip().split(" ",1)
#        if len(splitted) > 1:
#            c[i] = splitted[1]
#        else:
#            c = []
#            break
#    
#    commands = []
#    for i in range(len(c)):
#        commands.append("(" + c[i] + ")")
#    
#    return commands