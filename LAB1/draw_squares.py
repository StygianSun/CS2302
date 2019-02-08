"""
Created on Mon Feb  4 23:06:53 2019

@author: Robert Marc
"""

import numpy as np
import matplotlib.pyplot as plt

def draw_squares(ax,d,p,s):
    if d > 0:
        ax.plot(p[:,0],p[:,1],color = 'k')
        shrink = s/4                                #Shrink value for the corner squares of the current square.
        j = len(p)-2                                #Counter for number of corner squares
        for i in range(4):                          #For and while loop for drawing the corner squares for the current level
            while j >= 0:
                nd = np.array([[p[j,0]-shrink,p[j,1]-shrink],[p[j,0]-shrink,p[j,1]+shrink],  #Builds array for coordinates of next square
                               [p[j,0]+shrink,p[j,1]+shrink],[p[j,0]+shrink,p[j,1]-shrink],
                               [p[j,0]-shrink,p[j,1]-shrink]])
                draw_squares(ax,d-1,nd,s/2)                                                  #Calls for a corner square to be drawn, and that square's corner squares if need be
                j -= 1
        
plt.close("all")
orig_size = 1000
p = np.array([[0,0],[0,orig_size],[orig_size,orig_size],[orig_size,0],[0,0]])
fig, ax = plt.subplots()
draw_squares(ax,4,p,orig_size)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('squares.png')