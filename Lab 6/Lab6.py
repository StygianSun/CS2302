# Starting point for program to build and draw a maze
# Modify program using disjoint set forest to ensure there is exactly one
# simple path joiniung any two cells
# Programmed by Olac Fuentes
# Last modified March 28, 2019

"""
@Course: CS2302 MW 1:30-2:50 pm
@Author: Robert Marc, 80487972
@Assignment: Lab 6
@Instructor: Dr. Olac Fuentes
@TAs: Anindita Nath and Maliheh Zargaran
@Date of Last Modification: 4/14/19 @6:08PM
@Purpose: Use Disjoint set forests to create a maze
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
    
def regMaze():
    """
    Uses standard union algorithm to construct maze
    Uses provided algorithm bod modified into a while loop that continues until
    everything has been put into a single set.
    If a union is made, pop the current wall pair.
    """
    while len(dsfToSetList(maze)) > 1:
        d = random.randint(0,len(walls)-1)
        print('removing wall ',walls[d])
        if union(maze,walls[d][0],walls[d][1]):
            walls.pop(d)
            
def compMaze():
    """
    Uses union algorithm with path compression to construct maze
    Uses provided algorithm bod modified into a while loop that continues until
    everything has been put into a single set.
    If a union is made, pop the current wall pair.
    """
    while len(dsfToSetList(maze)) > 1:
        d = random.randint(0,len(walls)-1)
        print('removing wall', walls[d])
        if union_c(maze,walls[d][0],walls[d][1]):
            walls.pop(d)
            
def sizeMaze():
    """
    Uses union by size algorithm with path compression to construct maze
    Uses provided algorithm bod modified into a while loop that continues until
    everything has been put into a single set.
    If a union is made, pop the current wall pair.
    """
    while len(dsfToSetList(maze)) > 1:
        d = random.randint(0,len(walls)-1)
        print('removing wall', walls[d])
        if union_by_size(maze,walls[d][0],walls[d][1]):
            walls.pop(d)
            
plt.close("all") 

print("Enter number of rows in maze: ")
maze_rows = int(input())
print("Enter number of columns in maze: ")
maze_cols = int(input())

print("Choose DSF Implementation: ")
print("Type 1 for regular DSF, 2 for path compression, and 3 for Union by Size")
choice = input()
if choice== "1":
    walls = wall_list(maze_rows,maze_cols)
    maze = DisjointSetForest(maze_rows*maze_cols) 
    draw_maze(walls,maze_rows,maze_cols,cell_nums=True)
    regMaze()
    draw_maze(walls,maze_rows,maze_cols) 
elif choice == "2":
    walls = wall_list(maze_rows,maze_cols)
    maze = DisjointSetForest(maze_rows*maze_cols) 
    draw_maze(walls,maze_rows,maze_cols,cell_nums=True)
    compMaze()
    draw_maze(walls,maze_rows,maze_cols) 
elif choice == "3":
    walls = wall_list(maze_rows,maze_cols)
    maze = DisjointSetForest(maze_rows*maze_cols) 
    draw_maze(walls,maze_rows,maze_cols,cell_nums=True)
    sizeMaze()
    draw_maze(walls,maze_rows,maze_cols) 
else:
    print("Input not recognized, please try again.") 
