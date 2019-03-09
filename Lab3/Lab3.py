# Code to implement a binary search tree 
# Programmed by Olac Fuentes
# Last modified February 27, 2019
"""
@Course: CS2302 MW 1:30-2:50 pm
@Author: Robert Marc, 80487972
@Assignment: Lab 3
@Instructor: Dr. Olac Fuentes
@TAs: Anindita Nath and Maliheh Zargaran
@Date of Last Modification: 3/8/19 @8:31 PM
@Purpose: To implement different methods using binary search trees
"""
import matplotlib.pyplot as plt
import numpy as np
import math

class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      
        
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T

def Delete(T,del_item):
    if T is not None:
        if del_item < T.item:
            T.left = Delete(T.left,del_item)
        elif del_item > T.item:
            T.right = Delete(T.right,del_item)
        else:  # del_item == T.item
            if T.left is None and T.right is None: # T is a leaf, just remove it
                T = None
            elif T.left is None: # T has one child, replace it by existing child
                T = T.right
            elif T.right is None:
                T = T.left    
            else: # T has two chldren. Replace T by its successor, delete successor
                m = Smallest(T.right)
                T.item = m.item
                T.right = Delete(T.right,m.item)
    return T
         
def InOrder(T):
    # Prints items in BST in ascending order
    if T is not None:
        InOrder(T.left)
        print(T.item,end = ' ')
        InOrder(T.right)
  
def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item)
        InOrderD(T.left,space+'   ')
  
def SmallestL(T):
    # Returns smallest item in BST. Returns None if T is None
    if T is None:
        return None
    while T.left is not None:
        T = T.left
    return T   
 
def Smallest(T):
    # Returns smallest item in BST. Error if T is None
    if T.left is None:
        return T
    else:
        return Smallest(T.left)

def Largest(T):
    if T.right is None:
        return T
    else:
        return Largest(T.right)   

def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item == k:
        return T
    if T.item<k:
        return Find(T.right,k)
    return Find(T.left,k)
    
def FindAndPrint(T,k):
    f = Find(T,k)
    if f is not None:
        print(f.item,'found')
    else:
        print(k,'not found')
        
#Begin Student Code
        
def IterSearch(T,k):
    """
    Iterative Search of a Binary Tree
    searches tree T for key k
    If found, returns the first note the key can be found in
    If not, returns None
    Begins with the head of the tree and compares k to the item in the current node
    If k > current item, advances current node to the right
    If K < current item, advances current node to the left
    """
    global IterSearchCount
    cur = T
    while cur != None:
        if k > cur.item:
            IterSearchCount += 1
            cur = cur.right
        elif k < cur.item:
            IterSearchCount += 1
            cur = cur.left
        else: 
            return cur
    return None

def BuildFromList(L):
    """
    Build a balanced binary search tree from a sorted list, L
    Find the element in the middle of the list and adds that element to the tree
    Split the remainder of the list into two, slicing out the middle element
    Recursively call BuildFromList using the sliced lists to build the left and right branches of the tree
    then returns the head of the Tree
    """
    global BuildFromListCount
    if len(L) != 0:
        BuildFromListCount += 1
        mid = len(L)//2
        T = BST(L[mid])
        L1 = L[:mid]
        L2 = L[mid+1:]
        T.left = BuildFromList(L1)
        T.right = BuildFromList(L2)
        return T
    return

def BuildFromTree(T):
    """
    Build a sorted list from a binary search tree, T
    Starting at the head of the tree:
        If the current node has a left and right branch:
            Recursively calls BuildFromTree on the left branch while adding on the current elemnt to the middle
            and recursively calls BuildFromTree on the right branch
        If the current node does not have a left branch:
            Recursively calls BuildFromTree on the right branch while adding the result to the current element
        If the current node does not have a right branch:
            Recursively calls BUildFromTree on the left branch while adding the middle element to the result
        If the current node has no left or right branch
            Returns the current element
    This process builds the list by traversing the tree in order
    """
    global BuildFromTreeCount
    cur = T
    if cur.left != None and cur.right != None:
        BuildFromTreeCount += 1
        return BuildFromTree(T.left) + [T.item] + BuildFromTree(T.right)
    elif cur.left != None:
        BuildFromTreeCount += 1
        return BuildFromTree(T.left) + [T.item]
    elif cur.right != None:
        BuildFromTreeCount += 1
        return [T.item] + BuildFromTree(T.right)
    else:
        BuildFromTreeCount += 1
        return [T.item]
    
def KeysAtDepth(T):
    """
    Main method for printing the keys at each depth
    Uses a recursive helper method to build a 2x2 array with each key at each depth
    Then uses two for loops to traverse the array while printing the keys
    """
    k = []
    KeysAtDepthHelper(T,0,k)
    global KeysAtDepthCount
    
    for i in range(len(k)):
        print("Keys at Depth ",i,":",end=' ')
        for j in range(len(k[i])):
            KeysAtDepthCount += 1
            print(k[i][j],end=' ')
        print()
    
def KeysAtDepthHelper(T,d,k):
    """
    Recursive helper method for building a 2x2 array with each key at each depth
    Each row of the array represents the depth of the tree
    Each column of the array represents the keys in that depth
    Uses a similar method to building a sorted list from a tree
    Instead of appending all elements to a 1-D list, it instead appends keys to the appropriate row for
        the current depth
    """
    global KeysAtDepthCount
    if T != None:
        KeysAtDepthCount += 1
        if len(k)-1 < d:
            k.append([])
        KeysAtDepthHelper(T.left,d+1,k)
        k[d].append(T.item)
        KeysAtDepthHelper(T.right,d+1,k)
    return

def Circle(center,rad):
    """
    Simple method from lab 1 to calculate coordinates for plotting a circle
    """
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

def DrawNode(ax,center,radius,N):
    """
    Method used to draw circles represnting nodes in a tree and the element in that node
    """
    if N != None:
        x,y = Circle(center,radius)
        ax.plot(x,y,color='k',zorder=2)
        ax.fill(x,y,color='w',zorder=2)
        ax.text(center[0]-50,center[1]-40,str(N.item),fontsize=20)
        
def DrawTreeHelp(ax,T,c,w,l):
    """
    Recursive helper method for drawing the lines between nodes of a tree
    This method first recursively draws the appropriate number of lines between the nodes,
        then draws the nodes at the intersections of these lines
    """
    global DrawTreeCount
    if T != None:
        x1 = c[0]-(w*.9),c[0]                    
        x2 = c[0]+(w*.9),c[0]                    
        y = c[1]-l,c[1]
        if T.left != None:
            ax.plot(x1,y,color='k',zorder=1)
            DrawTreeHelp(ax,T.left,[x1[0],y[0]],w/2,l)
        if T.right != None:                                      
            ax.plot(x2,y,color='k',zorder=1)
            DrawTreeHelp(ax,T.right,[x2[0],y[0]],w/2,l)
        DrawTreeCount += 1
        DrawNode(ax,c,100,T)
        
def DrawTree(T):
    """
    Main method for drawing a tree diagram of a given tree, T
    Sets up the subplots and original size of the plot as well as the starting coordinate of the tree
    Then calls the recursive helper method to draw the tree
    """
    global DrawTreeCount
    if T != None:
        plt.close("all")
        orig_size = 1000
        c = [0,orig_size]
        fig, ax = plt.subplots()
        DrawTreeHelp(ax,T,c,orig_size,orig_size)
        ax.set_aspect(1.0)
        ax.axis('off')
        plt.show()
        fig.savefig('tree.png')
        
IterSearchCount = 0
BuildFromListCount = 0
BuildFromTreeCount = 0
KeysAtDepthCount = 0
DrawTreeCount = 0

#Binary search tree given to use in the lab documentation, used as a control for testing
T = BST(10)
Insert(T,4)
Insert(T,15)
Insert(T,2)
Insert(T,8)
Insert(T,12)
Insert(T,18)
Insert(T,1)
Insert(T,3)
Insert(T,5)
Insert(T,9)
Insert(T,7)

#Sorted list using the same elements as those in the tree from the lab documentation, used as a control for testing
SL = [10,4,15,2,8,12,18,1,3,5,9,7]
SL.sort()

DrawTree(T)
print("DrawTreeCount: ",DrawTreeCount)
n = IterSearch(T,12)
print(n.item)
print("IterSearchCount when key is present: ",IterSearchCount)
IterSearchCount = 0
n = IterSearch(T,17)
print(n)
print("IterSearchCount when key isn't present: ",IterSearchCount)
TL = BuildFromList(SL)
print("Binary search tree built from a sorted list:")
InOrderD(T,' ')
print("BuildFromListCount: ",BuildFromListCount)
L = BuildFromTree(T)
print("Sorted list built from a binary search tree:")
print(L)
print("BuildFromTreeCount: ",BuildFromTreeCount)
KeysAtDepth(T)  
print("KeysAtDepthCount: ",KeysAtDepthCount)
