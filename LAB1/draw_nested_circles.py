"""
Created on Thu Feb  7 14:38:08 2019

@author: Robert Marc
"""

import matplotlib.pyplot as plt
import numpy as np
import math

def circle(center,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

def draw_nested_circles(ax,n,center,radius):
    if n>0:
        x,y = circle(center,radius)
        ax.plot(x,y,color='k')
        new_r = radius*(1/3)                                              #Calculates radius of circles for next level at 1/3rd that of current radius
        draw_nested_circles(ax,n-1,center,new_r)                          #Draws center circle and that circles nested circles.
        draw_nested_circles(ax,n-1,[center[0],center[1]+(2*new_r)],new_r) #Draws north circle and that circles nested circles.
        draw_nested_circles(ax,n-1,[center[0],center[1]-(2*new_r)],new_r) #Draws south circle and that circles nested circles.
        draw_nested_circles(ax,n-1,[center[0]+(2*new_r),center[1]],new_r) #Draws east circle and that circles nested circles.
        draw_nested_circles(ax,n-1,[center[0]-(2*new_r),center[1]],new_r) #Draw west circle and that circles nested circles.
        
plt.close("all")
fig, ax = plt.subplots()
d = 2                                   #Depth of recursion requested
draw_nested_circles(ax,d,[100,0],100)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('nested_circles.png')