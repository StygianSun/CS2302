# Code to implement a B-tree 
# Programmed by Olac Fuentes
# Last modified February 28, 2019

"""
@Course: CS2302 MW 1:30-2:50 pm
@Author: Robert Marc, 80487972
@Assignment: Lab 4
@Instructor: Dr. Olac Fuentes
@TAs: Anindita Nath and Maliheh Zargaran
@Date of Last Modification: 3/24/19 @11:31 PM
@Purpose: To implement different operations on B-Trees
"""

class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
        
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])
        
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)
    
#Begin Student Code
        
def Height(T):
    """
    Calculates the height of BTree T
    If the method reaches a leaf it returns 1, adding 1 for everytime it moves
    down
    """
    if T.isLeaf:
        return 1
    return 1 + Height(T.child[0])

def BTreeToList(T):
    """
    Moves through the BTree in order
    Whenever it reaches a node that is a leaf, it appends the items to the list
        in order. It concatenates the list together through recursive calls
    """
    temp = []
    if T.isLeaf:
        for i in T.item:
            temp.append(i)
        return temp
    for j in range(len(T.item)):
        temp = temp + BTreeToList(T.child[j])
        temp.append(T.item[j])
    return temp + BTreeToList(T.child[len(T.item)])

def MinAtDepth(T,d):
    """
    Moves to the furthest left item and returns the minimum element
    """
    if d == Height(T):
        print("Requested depth greater than tree depth.")
    elif d == 0:
        return T.item[0]
    else:
        return MinAtDepth(T.child[0],d-1)
    
def MaxAtDepth(T,d):
    """
    Moves to the furthest right item and returns the minimum element
    """
    if d == Height(T):
        print("Requested depth greater than tree depth.")
    elif d == 0:
        return T.item[len(T.item)-1]
    else:
        return MaxAtDepth(T.child[len(T.child)-1],d-1)
    
def NodesAtDepth(T,d):
    """
    Recursively progresses to nodes until the requested depth
        Returns 1 when it reaches a node at the requested depth
        Uses a for loop to add up all nodes at that depth
    """
    if d == Height(T):
        print("Requested depth greater than tree depth.")
    elif d == 0:
        return 1
    else:
        temp = 0
        for i in range(len(T.child)):
            temp += NodesAtDepth(T.child[i],d-1)
        return temp
    
def ElementsAtDepth(T,d):
    """
    Functions in the same way as NodesAtDepth without returning 1
        Prints the elements in order at each node at the requested depth
    """
    if d == Height(T):
        print("Requested depth greater than tree depth.")
    elif d == 0:
        for i in T.item:
            print(i, end=' ')
    else:
        for j in range(len(T.child)):
            ElementsAtDepth(T.child[j],d-1)
            
def FullNodes(T):
    """
    Progresses through the tree in order checking for full nodes
        Returns 1 when a full node is found
        Uses a for loop to count up all of the full nodes in the BTree
    """
    if IsFull(T):
        return 1
    else:
        temp = 0
        for i in range(len(T.child)):
            temp += FullNodes(T.child[i])
        return temp
    
def FullLeaves(T):
    """
    Functions the same way as FullNodes, but also checks if the node is a leaf
    """
    if T.isLeaf and IsFull(T):
        return 1
    else:
        temp = 0
        for i in range(len(T.child)):
            temp += FullLeaves(T.child[i])
        return temp
    
def DepthOfKey(T,k):
    """
    Main method for DepthOfKey, only returns results of DepthOfKeyHelper
    """
    return DepthOfKeyHelper(T,k,0)
    
def DepthOfKeyHelper(T,k,d):
    """
    Progresses through the tree in order, keeping track of the depth
        If key is found, changes the holder for the depth. If the holder
        changes away from -1, it stops recursively calling, and returns the
        found depth
    """
    for i in range(len(T.item)):
        if T.item[i] == k:
            return d
    temp = -1
    for j in range(len(T.child)):
        if temp == -1:
            temp = DepthOfKeyHelper(T.child[j],k,d+1)
    return temp
        
L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6]
T = BTree()    
for i in L:
    Insert(T,i)
    
PrintD(T,' ')
    
print(Height(T))
BuiltList = BTreeToList(T)
print(BuiltList)
print(MinAtDepth(T,0))
print(MaxAtDepth(T,0))
print(NodesAtDepth(T,0))
ElementsAtDepth(T,0)
print()
print(FullNodes(T))
print(FullLeaves(T))
print(DepthOfKey(T,4))
