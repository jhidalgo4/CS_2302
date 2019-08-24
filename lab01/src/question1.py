"""
Created on Wed Jan 30 13:46:19 2019

@author: joaquin
CS 2302 MW 1:30pm
lab01
"""

import numpy as np
import matplotlib.pyplot as plt 

def base_sqaure(ax,n,side, c):
    #Base case
    if n>0:
        
        #Create matrix 5x2 of square plots
        p = np.array([ [c[0] - side//2, c[1] - side//2 ], [c[0] - side//2, c[1] + side//2],[c[0] + side//2, c[1] + side//2],[c[0] + side//2, c[1] - side//2],[c[0] - side//2, c[1] - side//2] ])
        #plot the matrix
        ax.plot(p[:,0],p[:,1],color='k')
        
        #Everything below this line is performed after the recursion call..
        
        #p[0] = Bottom left square center point
        base_sqaure(ax,n-1,side*.5,p[0])
        #Top left square
        base_sqaure(ax,n-1,side*.5,p[1])
        #Top right square
        base_sqaure(ax,n-1,side*.5,p[2])
        #Bottom right square
        base_sqaure(ax,n-1,side*.5,p[3])
        

plt.close("all") 
fig, ax = plt.subplots()

#Paramters
# *****************************
orig_side_length = 800  # Length of the side
center = [0,0]      #Center coordinates of the 1st square
depth = 4        # Depth of recursion squares
# *****************************

# The Recursive call
base_sqaure(ax,depth,orig_side_length, center)

ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('square_1a.png')