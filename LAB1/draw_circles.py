"""
Created on Wed Feb  6 18:37:48 2019

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

def draw_circles(ax,n,center,radius,w):
    if n>0:
        x,y = circle(center,radius)
        ax.plot(x,y,color='k')
        center[0] = center[0]-(center[0]-center[0]*w) #Moves the center for the next circle over by the difference between the current radius and next radius
        draw_circles(ax,n-1,center,radius*w,w)        #Draws next circle with new center and scaled radius
        
plt.close("all")
fig, ax = plt.subplots()
c = 50                                  #Number of circles to be drawn
w = .6 + (c/200)                        #Calculates the weight for scaling based on the number of circles to be drawn
if w < 1:                               #If the number of circles causes the weight to equal 1 or more, console prints message that number of circles is too high
    draw_circles(ax,c,[100,0],100,w)
    ax.set_aspect(1.0)
    ax.axis('off')
    plt.show()
    fig.savefig('circles.png')
else:
    print("Number of circles has caused the weight of radius reduction to be too high. Please choose a smaller number.")