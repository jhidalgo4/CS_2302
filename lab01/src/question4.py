#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 18:55:12 2019

@author: joaquin
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

def drawCircle(ax,n,center,radius,w):
    #base case
    if n>0:
        
        #get x,y coordinates of circle
        x,y = get_circle_points(center,radius)
        #draw the circle
        ax.plot(x,y,color='k')
        

        
        

        # recurrsion call with new center and radius decreasing by ratio 'w'
        # Generate new x,y coordinates of the NEXT circle
        
        #Top
        drawCircle(ax,n-1, [center[0], center[1]+(radius/1.5)] , radius/3, w)
        
        
        #Bottom
        drawCircle(ax,n-1, [center[0], center[1]-(radius/1.5)] , radius/3, w)
        
        #Left
        drawCircle(ax,n-1, [center[0]-(radius/1.5), center[1]] , radius/3, w)
        
        #Right
        drawCircle(ax,n-1, [center[0]+(radius/1.5), center[1]] , radius/3, w)
        
        #Center
        drawCircle(ax,n-1, [center[0], center[1] ] , radius/3, w)
        
      
plt.close("all") 
fig, ax = plt.subplots() 

#Paramters
# *****************************
x_coord = 0
y_coord = 0
radius_length = 100
ratio = .6             #Best if between 0 and 1
depth = 3             #Number of circles
# *****************************

center_point = np.array( [x_coord, y_coord] )

#The recurrsion call
drawCircle(ax, depth, center_point, radius_length, ratio)

ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circle_1a.png')