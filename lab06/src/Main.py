"""
By: Joaquin Hidalgo
Lab 06

Created on Wed Apr 10 20:26:23 2019
Instructor: Olac Fuentes
TA: Dita and Mali
Last modified Sun 14 Apr 23:48:28

Create a maze where each cell starts off in its own set, randomly
picking walls of the maze to delete, once you delete a wall, you join
the two cells sets and keep on doing until there is only 1 set which is 1 path.
Use standard Union vs Union by size with compression
"""

import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import interpolate
import time

#Create and set disjoint forest by size
def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1

#Standard find by root
def FindRoot(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return FindRoot(S,S[i])

def FindRoot_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = FindRoot_c(S,S[i]) 
    S[i] = r 
    return r

#Returns true or false if two nums are in set
def CheckSameSet(S,i,j):
    # Joins i's tree and j's tree, if they are different
    root1 = FindRoot(S,i) 
    root2 = FindRoot(S,j) 
    if root1!=root2: # if r1 != r2, then they are different set
        return False, root1, root2
    return True, root1, root2

def CheckSameSet_c(S,i,j):
    root1 = FindRoot_c(S,i) 
    root2 = FindRoot_c(S,j)
    if root1!=root2: # if r1 != r2, then they are different set
        return False, root1, root2
    return True, root1, root2
    

#Iterates thru disjoint forest and counts amount of sets
def NumSets(S):
    c =0
    for i in range(len(S)):
        if S[i] <0:
            c+=1
    return c

# Creates a list with all the walls in the maze
def wall_list(maze_rows, maze_cols):  
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell, cell+1])
            if r!=maze_rows-1:
                w.append([cell, cell+maze_cols])
    return w

def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0]==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)
    
def draw_dsf(S):
    scale = 2
    fig, ax = plt.subplots()
    for i in range(len(S)):
        if S[i]<0: # i is a root
            ax.plot([i*scale,i*scale],[0,scale],linewidth=1,color='k')
            ax.plot([i*scale-1,i*scale,i*scale+1],[scale-2,scale,scale-2],linewidth=1,color='k')
        else:
            x = np.linspace(i*scale,S[i]*scale)
            x0 = np.linspace(i*scale,S[i]*scale,num=5)
            diff = np.abs(S[i]-i)
            if diff == 1: #i and S[i] are neighbors; draw straight line
                y0 = [0,0,0,0,0]
            else:      #i and S[i] are not neighbors; draw arc
                y0 = [0,-6*diff,-8*diff,-6*diff,0]
            f = interpolate.interp1d(x0, y0, kind='cubic')
            y = f(x)
            ax.plot(x,y,linewidth=1,color='k')
            ax.plot([x0[2]+2*np.sign(i-S[i]),x0[2],x0[2]+2*np.sign(i-S[i])],[y0[2]-1,y0[2],y0[2]+1],linewidth=1,color='k')
        ax.text(i*scale,0, str(i), size=20,ha="center", va="center",
         bbox=dict(facecolor='w',boxstyle="circle"))
    ax.axis('off') 
    ax.set_aspect(1.0)

# Main
##################################################################

if __name__ == '__main__': 
    plt.close("all")
    m_rows= int(input('enter number of rows: '))
    m_cols = int(input('enter number of columns: '))
    userChoice = int(input('1. standard union   2.  union by size with path compression '))
    startTime = time.time()
    
########################## choice 1    
    if userChoice == 1:
        
        S = DisjointSetForest(m_rows*m_cols)
    
        #Creates 'wall_list' a set of two cells who have a wall between them
        wall_list = wall_list(m_rows,m_cols)

        
        while True:
            d = random.randint(0,len(wall_list)-1) # pick random wall
            a,b = wall_list[d] #obtain the num of the two cells
            flag, r1, r2 = CheckSameSet(S,a,b) # checks if same root, standard
            
            if flag == False:
                
                #Union two cell nums
                S[r2] = r1
                #Pop wall
                wall_list.pop(d)
                
            if (NumSets(S) < 2):
                break
        
        draw_maze(wall_list,m_rows,m_cols) #draw maze
        
        endTime = time.time()
        draw_dsf(S)
        print('runtime is: ', endTime-startTime)
        
########################## choice 2        
    elif userChoice == 2:
        
        S = DisjointSetForest(m_rows*m_cols)
        
        #Creates 'wall_list' a set of two cells who have a wall between them
        wall_list = wall_list(m_rows,m_cols)
        
        while True:
            d = random.randint(0,len(wall_list)-1) # pick random wall
            a,b = wall_list[d] #obtain the num of the two cells
            flag, r1, r2 = CheckSameSet_c(S,a,b) # checks if same root w/ compression
            
            if flag == False:
                #Union two cell nums 
                if r1!=r2:
                    if S[r1]>S[r2]: # j's tree is larger
                        S[r2] += S[r1]
                        S[r1] = r2
                    else:
                        S[r1] += S[r2]
                        S[r2] = r1
                #Pop wall
                wall_list.pop(d)
                
            if (NumSets(S) < 2):
                break
        
        draw_maze(wall_list,m_rows,m_cols) #draw maze
        
        endTime = time.time()
        draw_dsf(S)
        print('runtime is: ', endTime-startTime)
    
    else:
        print('Please try again...')
            
        