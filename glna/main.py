# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 19:07:08 2020

Wrapper script for dentatgyrusnet2005.hoc
Allows you to specify some hoc parameters in python
Can access hoc results variables after run (or load in from file)
And can plot results

@author: mbezaire
"""

import sys

print("Simulation start!")

# Set default values here in case not passed in via command line
caovar = 0.5     # External calcium concentration (mM)
caivar = caovar * 5.e-6 / 2 # Internal calcium concentration (mM)

plotstyle = 1 # 1: normal spikeraster, 2: interspersed spikeraster, 0: no plots
printstyle = 1 # 2: print a lot of status lines / updates, 1: print some lines, 0: print minimal

mytstop = 100	# 1500 ms, duration of simulation

simname = "lnatest"
#%% Now check for command line args:

print("Checking cmd args!")

argadd = 1
startlen = 1
import subprocess
result = subprocess.run('hostname', stdout = subprocess.PIPE)
if (result.stdout.decode('utf-8')[:3] == "scc"): # scc has an odd way of accounting for command line arguments
    argadd = 2
    startlen = 5
    plotsyle = 0
    
if len(sys.argv)>(startlen):
    simname = sys.argv[startlen]
    if len(sys.argv)>(argadd+startlen):
        caovar = float(sys.argv[argadd+startlen]) # must convert to float if scientific notation
        if len(sys.argv)>(2*argadd+startlen): # if not scientific notation can convert to float or int
            caivar = caovar * 5.e-6 / 2 if sys.argv[2*argadd+startlen]=='-1' else float(sys.argv[2*argadd+startlen])
            if len(sys.argv)>(3*argadd+startlen):
                mytstop = int(sys.argv[3*argadd+startlen])
                        
                        
rmchars=['"',"'","\\"," "]

for i in rmchars:
    simname = simname.replace(i,"")


#%% Set up the NEURON environment
print("Setting up NEURON!")

from neuron import h
import os

# First, define our parameters in the NEURON environment
h('strdef RunName')
h('caivar = '+str(caivar)) # Internal calcium concentration (mM)
h('caovar = '+str(caovar)) # External calcium concentration (mM)
h('nrnplot = 0')
h('mytstop = '+str(mytstop))
h('plotstyle = '+str(plotstyle))
h('printstyle = '+str(printstyle))
# After defining these variables in the NEURON environment, now you
# can refer to them in a pythonic way as for example:
# h.caivar
# h.caovar

# But remember, any variables you set in this wrapper script, you
# want to stop defining in hoc (or else it gets overwritten).
#
# However, if you want to ability to have it defined in hoc only
# when you did not already define it in this wrapper script, set it
# using the default_var function (see examples in hoc for caivar, caovar)

# Note, the python variables caivar and caovar are not directly related to
# h.caivar, h.caovar. You must explicitly set them equal if you want updates to
# caivar and caovar to alter h.caivar and h.caovar

#%% This code creates a unique results directory for each run of your code
h.RunName = simname+'_o{}'.format(int(caovar) if caovar % 1 == 0 else caovar) # simname and calcium concentration (external)
print("Creating new results directory.")

if (not os.path.exists("results")):
    os.mkdir("results")
# check if dir exists
# update RunName if necessary
while (os.path.exists("results/"+h.RunName)):
    sto=h.RunName.find("_")
    st=h.RunName[sto+1:].find("_")+sto+1 #the one after o
    if (st>sto and h.RunName[st+1:].isdigit()):
        b='{:0'+str(len(h.RunName[st+1:]))+'d}'
        h.RunName = h.RunName[:st+1] + b.format(int(h.RunName[st+1:])+1)
    else:
        h.RunName += '_00'

#%%        
os.mkdir("results/"+h.RunName)

print("Loading hoc file now.")
h.load_file(1,"A-lna.hoc")

print("This simulation is called: " + h.RunName)

ROI = h.RunName
#%%
      
if (plotstyle>0):
    import plots
    plots.plotPostSim(ROI, plotstyle)

