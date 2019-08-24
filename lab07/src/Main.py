"""
By: Joaquin Hidalgo
Lab 07

Created on Sat 20 Apr 4:20:00 2019
Instructor: Olac Fuentes
TA: Dita and Mali
Last modified Fri 26 Apr 14:12:37

Use a disjoint forrest set to create a VxV matrix of rows and columns.
If two cells are apart of different sets, union them and pop walls to create
a perfect maze, a maze with not enough popped walls and multiple solution maze.
Then, preform BFS, DFS, or DFS(recurssion) to find a soltion of the maze
starting at point 0 to the top right cell (n-1) and compare running times
"""

from collections import deque #queue
import matplotlib.pyplot as plt #draw lines
import numpy as np
import random
import time

#Create and set disjoint forest by size
def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1

def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r
    return r

def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri

def NumSets(S):
    count =0
    for i in range(len(S)):
        if S[i]<0:
            count += 1
    return count

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

#Get path to solution from (0 to n-1) cell
def GetPath(path, source):    
    global path_of_search
    
    if path[source] != -1:
        GetPath(path, path[source])
    path_of_search.append(source)
    
#Converts Path to solution to an EDGE LIST to DRAW LINES later...
def Path_to_EdgeList(li):
    res = []
    for i in range(1,len(li)):
        res.append([li[i-1],li[i]])
    return res
    
#take in an adjceny list and starting point
def Bfs_iter(adj, source):
    global visted
    global prev
    # iniztilze queue
    Q = deque()
    
    Q.append(source)
    visted[source] = True
    while(len(Q) != 0 ):
        current = Q.popleft()
        for i in adj[current]:
            if (visted[i] == False):
                visted[i] = True
                prev[i] = current
                Q.append(i)

def Dfs_rec(adj, source):
    global visted
    global prev

    visted[source] = True
    for i in adj[source]:
        if(visted[i] == False):
            prev[i] = source
            Dfs_rec(adj, i)

def Dfs_iter(adj, source):
    global visted
    global prev
    #initilize stack
    stack = []
    
    stack.append(source)
    visted[source] = True
    while(len(stack) != 0 ):
        current = stack.pop()
        for i in adj[current]:
            if (visted[i] == False):
                visted[i] = True
                prev[i] = current
                stack.append(i)

def Draw_maze_cells(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    
    # draw lines that are INSIDE the maze
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
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k') # connect points
    sx = maze_cols
    sy = maze_rows
    
    #draw the OUTER edge of Maze
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)
    
def Draw_maze_and_path(path2,walls2,maze_rows,maze_cols):
    fig, ax = plt.subplots()
    
    # draw PATH
    for w in path2:
        if w[1]-w[0] ==1: #new horzintal
            x0 = (w[0]%maze_cols)+.5#good
            y0 = (w[0]//maze_cols)+.5#
            x1 = (w[1]%maze_cols)+.5#good
            y1 = (w[1]//maze_cols)+.5#
        else:#new verticallll
            x0 = (w[0]%maze_cols)+.5#good
            y0 = (w[0]//maze_cols)+.5#
            x1 = (w[1]%maze_cols)+.5#good
            y1 = (w[1]//maze_cols)+.5#
        ax.plot([x0,x1],[y0,y1],linewidth=1.3,color='c')
    sx = maze_cols
    sy = maze_rows
    
    #draw INSIDE maze walls
    for w in walls2:
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
        
    #Draw OUTER edge of maze
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
                
    ax.axis('off') 
    ax.set_aspect(1.0)
    
def draw_solution_maze_only(walls,maze_rows,maze_cols,cell_nums=False):
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
    
    
# Main
#################################################################################################
if __name__ == '__main__':
    
    # USER-INPUT CHOICES
    m_rows= int(input('enter number of rows: '))
    m_cols = int(input('enter number of columns: '))
    n =  m_rows*m_cols
    print('\nThe number of cells: ',n)
    m = int(input('Enter the number of walls to remove: '))
    if (m == (n-1)):
        alt_choice =int(input('1. BFS 2. DFS 3. DFS(recursive): '))
    startTime = time.time()
    plt.close("all")
    
    #Allocate space for variables
    all_path_adj_list = [ [] for i in range(n) ] #Adjency list of all possible paths
    visted = np.zeros(n,dtype=bool) #visited nodes in graph
    prev = np.zeros(n,dtype=np.int)-1 #path taken of chosen method
    counter = 0 #keeps track of how many walls are Removed
    S = DisjointSetForest(n) #Dsf keeps track of which cells are in the same set
    path_of_search =  []
    
    #Case for PERFECT MAZE
    ########################################################
    if m == n-1:
        print('\nThe is a unique path from source to destination (when m = n − 1)')
        
        #Creates LIST that is all the walls that CAN BE popped
        deafult_wallList = wall_list(m_rows,m_cols)
        
        #Draw default maze with cells and numbers
        Draw_maze_cells(deafult_wallList,m_rows,m_cols,cell_nums=True)
        
        
        #Keep popping walls off 'deafult_wallList' untill desired 'm' == counter
        while True:
            d = random.randint(0,len(deafult_wallList)-1) # pick random wall
            a,b = deafult_wallList[d] #obtain the num of the two cells
            
            #Find be compression
            root1 = find_c(S,a)
            root2 = find_c(S,b)
            
            #Union by Size if two cells are in different Sets
            if root1 != root2:
                union_by_size(S,a,b)
                
                #Popping wall creates a pathway/space in maze to travel
                connection = deafult_wallList.pop(d) 
                
                all_path_adj_list[connection[0]].append(connection[1]) #create adj list of WHOLE PATH
                all_path_adj_list[connection[1]].append(connection[0]) #create adj list of WHOLE PATH
                counter += 1 # we popped a wall
                
            #Reached desired amount of walls popped
            if counter == m:
                break
        remaining_walls = deafult_wallList #Store all remaining walls
        
        print('\nAdjencency representation of maze:')
        print(all_path_adj_list)
        
        #Bread First Search
        ###################################
        if alt_choice == 1:
            
            print('\nBread First Search!!!\n')
            Bfs_iter(all_path_adj_list, 0) #Pass all possible pathways and starting point to start Search
            #Prev is now... BFS array... After method 'Bfs_iter'
            
            GetPath(prev, n-1)
            #path_of_search is now the adj list of to the Maze solution
            print('Path from cell 0 to ', n-1)
            print(path_of_search)
            
            edge_list_path = Path_to_EdgeList(path_of_search) #Connection of lines of the pathway DRAWN SOLUTION
            
            #Draw finished maze w/ Path
            Draw_maze_and_path(edge_list_path,remaining_walls,m_rows,m_cols)
            
            endTime = time.time()
            print('\nRunning time: ', endTime - startTime)
            print('\nlength of path: ', len(path_of_search))
            print('adj listtttttt')
            print(edge_list_path)
            
        
        
        #Depth First Search
        ###################################
        elif alt_choice == 2:
            
            print('\nDepth First Search!!!\n')
            Dfs_iter(all_path_adj_list, 0) #Pass all possible pathways and starting point to start Search
            #Prev is now... DFS array... After method 'Dfs_iter'
            
            GetPath(prev, n-1)
            #path_of_search is now the adj list of to the Maze solution
            print('Path from cell 0 to ', n-1)
            print(path_of_search)
            
            edge_list_path = Path_to_EdgeList(path_of_search) #Connection of lines of the pathway DRAWN SOLUTION
            
            #Draw finished maze w/ Path
            Draw_maze_and_path(edge_list_path,remaining_walls,m_rows,m_cols)
            
            endTime = time.time()
            print('\nRunning time: ', endTime - startTime)
            print('\nlength of path: ', len(path_of_search))
            
            
        #Depth First Search (Recurssion)
        ###################################
        elif alt_choice ==3:
            
            print('\nDepth First Search (Recurssion)!!!\n')
            Dfs_rec(all_path_adj_list, 0) #Pass all possible pathways and starting point to start Search
            #Prev is now... DFS array... After method 'Dfs_rec'
            
            GetPath(prev, n-1)
            #path_of_search is now the adj list of to the Maze solution
            print('Path from cell 0 to ', n-1)
            print(path_of_search)
            
            edge_list_path = Path_to_EdgeList(path_of_search) #Connection of lines of the pathway DRAWN SOLUTION
            
            #Draw finished maze w/ Path
            Draw_maze_and_path(edge_list_path,remaining_walls,m_rows,m_cols)
            
            endTime = time.time()
            print('\nRunning time: ', endTime - startTime)
            print('\nlength of path: ', len(path_of_search))
            
        else:
            print('Invalid input, please pay attention!!')
            
        
    #Case for NOT ENOUGH walls poped from maze
    ###############################################################
    elif m< n-1:
        print('\nA path from source to destination is not guaranteed to exist (when m < n − 1)')
       
        #Creates LIST that is all the walls that CAN BE popped
        deafult_wallList = wall_list(m_rows,m_cols)
        
        #Draw default maze with cells and numbers
        Draw_maze_cells(deafult_wallList,m_rows,m_cols,cell_nums=True)
        
        #Keep popping walls off 'deafult_wallList' untill desired 'm' == counter
        while True:
            d = random.randint(0,len(deafult_wallList)-1) # pick random wall
            a,b = deafult_wallList[d] #obtain the num of the two cells
            
            #Find be compression
            root1 = find_c(S,a)
            root2 = find_c(S,b)
            
            #Union by Size if two cells are in different Sets
            if root1 != root2:
                union_by_size(S,a,b)
                deafult_wallList.pop(d)
                counter += 1
            if counter == m:
                break
        remaining_walls = deafult_wallList #Store all remaining walls
        
        #Draw finished maze
        draw_solution_maze_only(remaining_walls,m_rows,m_cols)
        
        endTime = time.time()
        print('\nRunning time: ', endTime - startTime)
        
    #Case for MULTIPLE PATH MAZE
    ##############################################################
    else:
        print('\nThere is at least one path from source to destination (when m > n − 1)')
        
        #Creates LIST that is all the walls that CAN BE popped
        deafult_wallList = wall_list(m_rows,m_cols)
        
        #Draw default maze with cells and numbers
        Draw_maze_cells(deafult_wallList,m_rows,m_cols,cell_nums=True)
        
        #Keep popping walls off 'deafult_wallList' untill desired 'm' == counter
        while True:
            d = random.randint(0,len(deafult_wallList)-1) # pick random wall
            a,b = deafult_wallList[d] #obtain the num of the two cells
            
            #Find be compression
            root1 = find_c(S,a)
            root2 = find_c(S,b)
            
            #Union by Size if two cells are in different Sets
            if root1 != root2:
                union_by_size(S,a,b)
                deafult_wallList.pop(d)
                counter += 1
            if counter == n-1:
                break
        
        number_of_walls_to_pop = m - (n-1)
        
        for i in range(number_of_walls_to_pop): 
            d = random.randint(0,len(deafult_wallList)-1)
            deafult_wallList.pop(d)
            
        remaining_walls = deafult_wallList #Store all remaining walls to display
        
        #Draw finished maze
        draw_solution_maze_only(remaining_walls,m_rows,m_cols)
        
        endTime = time.time()
        print('\nRunning time: ', endTime - startTime)
        