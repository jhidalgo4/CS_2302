#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 18:30:12 2019

@author: joaquin
"""

import numpy as np
import matplotlib.pyplot as plt 

def drawLines(ax,n,side, c):
    #Base case
    if n>0:
        
        #Create matrix 5x2 of square plots
        p = np.array( [ [c[0]-(side//2) , c[1]-((side//2)+(side//2))], [c[0] ,c[1] ] ] )
        #plot the matrix
        ax.plot(p[:,0],p[:,1],color='k')
        
        #Everything below this line is performed after the recursion call..
        
        #p[0] = Bottom left square center point
        drawLines(ax,n-1,side/2,p[0])
        #Top left square
        drawLines(ax,n-1,side/2,p[2])



plt.close("all") 
fig, ax = plt.subplots()


#Paramters
# *****************************
orig_side_length = 4000  # Length of the side
center = [0,0]      #Center coordinates of the 1st square
depth = 5      # Depth of recursion squares
# *****************************

# The Recursive call
drawLines(ax,depth,orig_side_length, center)

ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('square_1a.png')