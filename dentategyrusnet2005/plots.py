# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 16:49:35 2020

@author: tlu; code adapted from mbezaire

Description: Separate python script from main.py to generate plots after simulation
  Receives command line argument for which simulation and plotstyle, if run from cmd 
  Creates figures:
      - Spikeraster (plotstyle 1 for regular, 2 for interspersed)
      - Other parameters (Vm, Ca, Ina) vs time (if so desired)
"""
    
def plots(ROI, caovar, plotstyle=1): # originally took caivar--redundant now due to proportionality
    import csv 
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
        plt.scatter(mydata[:,0],mydata[:,1],s=1, marker="1")
        plt.ylabel("Cell #")
    
    else:
        cell_ranges = {}
        with open('results/'+ROI+'/celltype.dat') as f:
            cell_reader = csv.DictReader(f,delimiter="\t")
            for cell in cell_reader:
                cell_ranges[cell["celltype"]] = [int(cell["rangeStart"]),int(cell["rangeEnd"])+1]
        
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
    #plt.title("{} with [Ca_i] = {} mM, [Ca_o] = {} mM".format(ROI, caivar, caovar))
    plt.title("{} with [Ca_o] = {} mM".format(ROI, caovar))
    plt.xlabel("Time (ms)")
    
    plt.show() 
    plt.savefig("spikeraster_{}.png".format(ROI))

def plotPostSim(ROI, plotstyle=1):
    # given ROI string, run plots for that results folder
    assert plotstyle in [1,2]
    
    with open('results/'+ROI+'/runreceipt.dat') as f:
        # important simulation variables used for figure naming later
        # caivar is on line 1, caovar is on line 2
        caivar, caovar = (float(line[line.find('=')+1:].strip('\n')) for line in f.readlines())
    
    plots(ROI, caovar, plotstyle)

if __name__ == "__main__":
    # Must retrieve some variables if run as standalone file
    import sys
    # ROI - first arg
    if len(sys.argv) < 2: # not provided--ask for it 
        ROI = input('Please enter simulation name argument (including _xx):')
    else:
        ROI = sys.argv[1]
    # plotstyle - optional 2nd arg
    plotstyle = 1 if len(sys.argv) < 3 else int(sys.argv[2])
    while not plotstyle in [1,2]: # ask again
        plotstyle = int(input("Please provide either 1 or 2 for plotstyle:"))
    
    plotPostSim(ROI, plotstyle)