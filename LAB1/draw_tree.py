"""
Created on Wed Feb  6 18:47:10 2019

@author: Robert Marc
"""

import matplotlib.pyplot as plt
import numpy as np

def draw_tree(ax,n,c,w,l):
    if n>0:
        x1 = c[0]-(w/4),c[0]                    #Calculates x coordinate for left branch and holds x coordinate for center
        x2 = c[0]+(w/4),c[0]                    #Calculates x coordinate for right branch and holds x coordinate for center
        y = c[1]-l,c[1]                         #Calculates y coordinate for both branches and holds y coordinate for center
        ax.plot(x1,y,color='k')                 #Draws left branch
        ax.plot(x2,y,color='k')                 #Draws right branch
        draw_tree(ax,n-1,[x1[0],y[0]],w/2,l)    #Calls for next level of the tree for the left branch, halves width for next level
        draw_tree(ax,n-1,[x2[0],y[0]],w/2,l)    #Calls for next level of the tree for the right branch, halves width for next level
        
plt.close("all")
orig_size = 1000
c = [0,orig_size]                           #Center point that scales to the height of the drawing
d = 5                                       #Depth of tree requested
fig, ax = plt.subplots()
draw_tree(ax,d,c,orig_size,orig_size/d)     #d = depth of tree, c = center coordinates, orig_size = width of 1st level of tree, orig_size/d = length of next level of branches
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('tree.png')