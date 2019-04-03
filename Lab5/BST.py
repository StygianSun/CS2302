# Code to implement a binary search tree 
# Programmed by Olac Fuentes
# Last modified February 27, 2019

class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      
        
def Insert(T,newItem):
    if T == None:
        T = BST(newItem)
    elif T.item[0] > newItem[0]:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T
         
def InOrder(T):
    # Prints items in BST in ascending order
    if T is not None:
        InOrder(T.left)
        print(T.item[0],end = ' ')
        InOrder(T.right)
  
def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item[0])
        InOrderD(T.left,space+'   ')

def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item[0] == k:
        return T.item[1]
    if T.item[0] < k:
        return Find(T.right,k)
    return Find(T.left,k)

def NumNodes(T):
    """
    Counts number of nodes
    """
    if T is None:
        return 0
    else:
        return 1 + NumNodes(T.left) + NumNodes(T.right)
    
def Height(T):
    """
    Finds height of tree
    """
    if T is None:
        return 0
    else:
        hLeft = Height(T.left)
        hRight = Height(T.right)
        if hLeft > hRight:
            return hLeft + 1
        else:
            return hRight + 1