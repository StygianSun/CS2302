# Implementation of hash tables with chaining using strings
import numpy as np

class HashTableC(object):
    # Builds a hash table of size 'size'
    # Item is a list of (initially empty) lists
    # Constructor
    def __init__(self,size):  
        self.item = []
        self.numItems = 0
        for i in range(size):
            self.item.append([])
        
def InsertC(H,k,l):
    # Inserts k in appropriate bucket (list) 
    # Does nothing if k is already in the table
    b = h(k,len(H.item))
    H.item[b].append([k,l])
    H.numItems += 1
   
def FindC(H,k):
    # Returns bucket (b) and index (i) 
    # If k is not in table, i == -1
    b = h(k,len(H.item))
    for i in range(len(H.item[b])):
        if H.item[b][i][0] == k:
            return H.item[b][i][1]
    return b, -1, -1
 
def h(s,n):
    """
    Modified formula to r = (r*50 + ord(c))% n from r = (r*n + ord(c))% n
    """
    r = 0
    for c in s:
        r = (r*255 + ord(c))% n
    return r

def load(H):
    """
    Calculates load of hash table
    """
    return H.numItems/len(H.item)

def empty(H):
    """
    Counts the number of empty buckets
    Returns percentage of empty buckets in hash table
    """
    e = 0
    for i in range(len(H.item)):
        if len(H.item[i]) == 0:
            e += 1
    return (e/len(H.item))*100

def standDev(H):
    """
    Calculates standard deviation of the length of lists
    """
    lengths = []
    for b in H.item:
        lengths.append(len(b))
    return np.std(lengths)