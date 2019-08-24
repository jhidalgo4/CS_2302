"""
Created on Sat Feb 2 08:27:37 2019

author: joaquin
CS 2302 MW 1:30pm
lab01
"""

import matplotlib.pyplot as plt
import numpy as np
import math 

#This method returns all x,y coordinates that generates a circle with sin&cos
def get_circle_points(center,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

def base_circle(ax,n,center,radius,w):
    #base case
    if n>0:
        
        #get x,y coordinates of circle
        x,y = get_circle_points(center,radius)
        #draw the circle
        ax.plot(x,y,color='k')

        # Generate new x,y coordinates of the NEXT circle
        center[0] = center[0] - radius*(1-w)
        #Generate new radius of the NEXT circle
        radius = radius*w

        # recurrsion call with new center and radius decreasing by ratio 'w'
        base_circle(ax,n-1, center , radius, w)
        
      
plt.close("all") 
fig, ax = plt.subplots() 

#Paramters
# *****************************
x_coord = 12
y_coord = 26
radius_length = 100
ratio = .6             #Best if between 0 and 1
depth = 10             #Number of circles
# *****************************

center_point = np.array( [x_coord, y_coord] )

#The recurrsion call
base_circle(ax, depth, center_point, radius_length, ratio)

ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circle_1a.png')