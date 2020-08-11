# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 19:07:08 2020

Wrapper script for dentatgyrusnet2005.hoc
Allows you to specify some hoc parameters in python
Can access hoc results variables after run (or load in from file)
And can plot results

@author: mbezaire
"""

# Set default values here in case not passed in via command line
caivar = 5.e-6 # Internal calcium concentration (mM)
caovar = 2     # External calcium concentration (mM)

plotstyle = 1 # 1: normal spikeraster, 2: interspersed spikeraster, 0: no plots
printstyle = 1 # 2: print a lot of status lines / updates, 1: print some lines, 0: print minimal
mytstop = 10	# 1500 ms, duration of simulation

#%% Now check for command line args:
argadd = 1
startlen = 1
import subprocess
result = subprocess.run('hostname', stdout = subprocess.PIPE)
if (result.stdout.decode('utf-8')[:3] == "scc"): # scc has an odd way of accounting for command line arguments
    argadd = 2
    startlen = 5
    
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

if (not os.path.exists("results")):
    os.mkdir("results")
# check if dir exists
# update RunName if necessary
while (os.path.exists("results/"+h.RunName)):
    st=h.RunName.find("_")
    if (st>-1 and h.RunName[st+1:].isdigit()):
        b='{:0'+str(len(h.RunName[st+1:]))+'d}'
        h.RunName = h.RunName[:st+1] + b.format(int(h.RunName[st+1:])+1)
    else:
        h.RunName += '_00'

#%%        
os.mkdir("results/"+h.RunName)

h.load_file(1,"A-DG500_M7.hoc")

print("This simulation is called: " + h.RunName)

ROI = h.RunName
#%%
import csv 

cell_ranges = {}
with open('results/'+ROI+'/celltype.dat') as f:
    cell_reader = csv.DictReader(f,delimiter="\t")
    for cell in cell_reader:
        cell_ranges[cell["celltype"]] = [int(cell["rangeStart"]),int(cell["rangeEnd"])+1]


#%%
        
if (plotstyle>0):
    import numpy as np
    import matplotlib.pyplot as plt
    
    
    detaildata = np.loadtxt('results/'+ROI+'/currents_potentials.dat',skiprows=1)
    # plt.figure()
    # plt.plot(detaildata[:,0],detaildata[:,1])
    # plt.xlabel('Time (ms')
    # plt.ylabel('Membrane Potential for Gcell[0]')
    # plt.show()

    # detaildata[:,2] # somatic calcium concentration
    # detaildata[:,3] # somatic sodium channel current
    
    
    plt.figure()
    
    mydata = np.loadtxt('results/'+ROI+'/spikeraster.dat')
    
    if (plotstyle==1):
        plt.scatter(mydata[:,0],mydata[:,1],s=.01)
        plt.ylabel("Cell #")
    
    else:
        # Plotting interspersed cells in different colors by cell type:
        pt_colors=[np.array([1,1,0]),np.array([.2,.2,.2]),np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1])]
        #pt_colors=[np.array([1,1,0]),np.array([.2,0,.4]),np.array([1,.5,0]),np.array([.2,1,.9]),np.array([.8,.5,.8])]
        pt_c=0
        for key in cell_ranges:
            tmpdata = mydata[(mydata[:,1]>=cell_ranges[key][0]) & (mydata[:,1]<cell_ranges[key][1])]
            plotpos = (tmpdata[:,1] - cell_ranges[key][0])/(cell_ranges[key][1]-cell_ranges[key][0])*1000
            if (len(plotpos)==1 and plotpos[0]==0):
                plt.scatter(tmpdata[:,0],plotpos,s=20,c=pt_colors[pt_c].reshape(1,-1),label=key)
            elif (len(plotpos)/len(mydata)<.5):
                plt.scatter(tmpdata[:,0],plotpos,s=4,c=pt_colors[pt_c].reshape(1,-1),label=key)
            else:
                plt.scatter(tmpdata[:,0],plotpos,s=.05,c=pt_colors[pt_c].reshape(1,-1),label=key)
            pt_c += 1
            
        plt.ylabel("Cells (positioned)")
        plt.legend(loc="upper left",fontsize=8)
        
    #plt.xlim([200, 300])
    plt.title("{} with [Ca_i] = {} mM, [Ca_o] = {} mM".format(ROI, caivar, caovar))
    plt.xlabel("Time (ms)")

    #plt.show()
    plt.savefig(filename="./results/{}/spikeraster_{}.png".format(ROI,ROI))
