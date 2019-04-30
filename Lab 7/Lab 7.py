# Starting point for program to build and draw a maze
# Modify program using disjoint set forest to ensure there is exactly one
# simple path joiniung any two cells
# Programmed by Olac Fuentes
# Last modified March 28, 2019

"""
@Course: CS2302 MW 1:30-2:50 pm
@Author: Robert Marc, 80487972
@Assignment: Lab 7
@Instructor: Dr. Olac Fuentes
@TAs: Anindita Nath and Maliheh Zargaran
@Date of Last Modification: 4/29/19 @11:50 PM
@Purpose: To modify lab 6 code and implement pathfinding search algorithms
        to solve the mazes constructed
"""

import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import interpolate 

def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
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

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
        
def dsfToSetList(S):
    #Returns aa list containing the sets encoded in S
    sets = [ [] for i in range(len(S)) ]
    for i in range(len(S)):
        sets[find(S,i)].append(i)
    sets = [x for x in sets if x != []]
    return sets

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r
    
def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    """
    Modified to return True if a union is made, or False if nothing is changed
    """
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri
        return True
    return False

def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    """
    Modified to return True if a union is made, or False if nothing is changed
    """
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri
        return True
    return False
         
def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    """
    Modified to return True if a union is made, or False if nothing is changed
    """
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
            return True
        else:
            S[ri] += S[rj]
            S[rj] = ri
            return True
    return False

        
def draw_dsf(S):
    scale = 30
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
         
def maze(remove):
    """
    Modified maze construction using union by size with path compression
        Now builds an adjacency list alongside the DSF and wall list operations
    """
    adjList = []
    for i in range(rows*cols):
        adjList.append([])
    while remove > 0 and len(dsfToSetList(mazeDSF)) > 1:
        d = random.randint(0,len(walls)-1)
        #print('removing wall', walls[d])
        if union_by_size(mazeDSF,walls[d][0],walls[d][1]):
            remove -= 1
            adjList[walls[d][0]].append(walls[d][1])
            #adjList[walls[d][1]].append(walls[d][0])
            walls.pop(d)
    while remove > 0:
        d = random.randint(0,len(walls)-1)
        remove -= 1
        adjList[walls[d][0]].append(walls[d][1])
        #adjList[walls[d][1]].append(walls[d][0])
        walls.pop(d)    
    return adjList

def printPath(path,v):
    """
    Prints the appropriate path to take to solve the maze
    """
    if path[v] != -1:
        printPath(path,path[v])
        print(' -> ',end='')
    print(v,end='')
    

def breadthFirst(adjList):
    """
    Breadth first search, visits a cell, then all of its neighbers, and so on
        until all cells have been searched
    """
    visited = np.full(len(adjList),False,dtype=bool)
    path = np.zeros(len(adjList),dtype=int)-1
    q = []
    goal = len(adjList)-1
    q.append(0)
    visited[0] = True
    while len(q) > 0:
        v = q.pop(0)
        if v == goal:
            return path
        for adj in adjList[v]:
            if not visited[adj]:
                visited[adj] = True
                path[adj] = v
                q.append(adj)
    return path

def depthFirst(adjList):
    """
    Depth first search, visits a cell and the first of its neighbors, then
        continues to the farthest cell it can reach, then backs up and searches
        to the next farthest cell it can reach
    """
    visited = np.full(len(adjList),False,dtype=bool)
    path = np.zeros(len(adjList),dtype=int)-1
    s = []
    goal = len(adjList)-1
    s.append(0)
    visited[0] = True
    while len(s) > 0:
        v = s.pop()
        if v == goal:
            return path
        for adj in adjList[v]:
            if not visited[adj]:
                visited[adj] = True
                path[adj] = v
                s.append(adj)
    return path

def depthFirstR(adjList,v):
    """
    Recursive depth first search, same operation as normal depth first search,
        but instead of using a stack, it moves through the first adjacency in
        each cell before returning to move through to the next one
    """
    global visited
    global prev
    visited[v] = True
    for adj in adjList[v]:
        if not visited[adj]:
            prev[adj] = v
            depthFirstR(adjList,adj)
    return prev
            
plt.close("all") 
"""
Queries for input on maze construction
"""
print("Enter number of rows in maze: ")
rows = int(input())
print("Enter number of columns in maze: ")
cols = int(input())
cells = rows*cols
print("Number of cells in maze: ",cells)
print("How many walls should be removed?")
remove = int(input())
"""
Prints information on if there is a possible path in the maze.
"""
if remove < cells-1:
    print("A path from source to destination is not guaranteed to exist.")
elif remove == cells-1:
    print("There is a unique path from source to destination.")
else:
    print("There is at least one path from source to destination.")
"""
Maze construction and drawing
"""
walls = wall_list(rows,cols)
mazeDSF = DisjointSetForest(rows*cols) 
draw_maze(walls,rows,cols,cell_nums=True)
adjList = maze(remove)
draw_maze(walls,rows,cols)
"""
Queries for input on which pathfinding algorithm to use to solve the maze
"""
print("Choose pathfinding algorithm")
choice = input("Type 1 for breadth first, 2 for depth first, or 3 for recursive depth first:")
if choice== "1":
    path = breadthFirst(adjList)
    printPath(path,len(adjList)-1)
    print()
elif choice == "2":
    path = depthFirst(adjList)
    printPath(path,len(adjList)-1)
elif choice == "3":
    visited = np.full(len(adjList),False,dtype=bool)
    prev = np.zeros(len(adjList),dtype=int)-1
    path = depthFirstR(adjList,0)
    printPath(path,len(adjList)-1)
    print()
else:
    print("Input not recognized, please try again.") 
