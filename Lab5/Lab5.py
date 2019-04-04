"""
@Course: CS2302 MW 1:30-2:50 pm
@Author: Robert Marc, 80487972
@Assignment: Lab 5
@Instructor: Dr. Olac Fuentes
@TAs: Anindita Nath and Maliheh Zargaran
@Date of Last Modification: 4/2/19 @6:19PM
@Purpose: To explore efficiency between binary search trees and hash tables
"""

import BST
import HashString
import time
import math

def BSTQuery():
    """
    Main method for Binary Search Tree runtime
    Reads glove file and stores in file object
    Starts timer and then calls BSTBuild to build the Binary Search Tree
    Ends timer on return.
    Prints simple statistics about constructed tree
    Reads comparisons file and stores in hold object
    Calls BSTCompQuery to start comparison queries
    Prints elapsed query time
    """
    print("Building binary search tree.",end="\n\n")
    glove = open("glove.6B.50d.txt",encoding='utf-8')
    lines = glove.readlines()
    glove.close()
    start = time.time()
    T = BSTBuild(lines)
    elapsed = time.time() - start
    print("Binary Search Tree Stats:")
    print("Number of Nodes: ",BST.NumNodes(T))
    print("Height: ",BST.Height(T))
    print("Running time for binary search tree construction: ",round(elapsed,2)," seconds",end="\n\n")
    print("Reading word file to determine similarities.",end="\n\n")
    comp = open("comparisons.txt")
    hold = comp.readlines()
    comp.close()
    print("Word similarities found:",end="\n\n")
    elapsed = BSTCompQuery(T,hold)
    print()
    print("Running time for binary search tree query processing: ",elapsed," seconds")
    
def BSTBuild(file):
    """
    Receives a file object and returns a build Binary Search Tree
    Slices off the first character of the file, as it is an encoding character
    Splits each line of the file into a string array
        stores the first element in word
        stores the remaining elements of the string array into embd as floats
        Uses permC as a character list of approved characters that a word can begin with
    Inserts each line into a node in the binary search tree
    returns the built tree
    """
    permC = 'abcdefghijklmnopqrstuvwxyz'
    file[0] = file[0][1:]
    s = file[0].split()
    word = s[0]
    embd = [float(k) for k in s[1:]]
    T = BST.BST([word,embd])
    if word[0] in permC:
        T = BST.Insert(T,[word,embd])
    for i in file[1:]:
        i = i.split()
        word = i[0]
        embd = [float(j) for j in i[1:]]
        if word[0] in permC:
            BST.Insert(T,[word,embd])
    return T

def BSTCompQuery(T,file):
    """
    Comparison query function for binary search tree
    For each line in the file, it stores the elapsed time,
        the two words to be compared (trimming non alphanumeric characters)
        and prints the return similarity results
    Returns total elapsed time not counting print functions
    """
    elapsed = 0
    permC = 'abcdefghijklmnopqrstuvwxyz'
    for i in file:
        start = time.time()
        s = i.split(",")
        if s[0][0] not in permC:
            s[0] = s[0][1:]
        if s[1][len(s[1])-1] not in permC:
            s[1] = s[1][:-1]
        elapsed += time.time()-start
        print("Similarity [",s[0],",",s[1],"] = ",sim(BST.Find(T,s[0]),BST.Find(T,s[1])))
    return elapsed
    
    
def HashQuery():
    """
    Main method for hash table with chaining runtime
    Reads glove file and stores in file object
    Starts timer and then calls HashBuild to build the hash table
    Ends timer on return.
    Prints simple statistics about constructed tree
    Reads comparisons file and stores in hold object
    Calls HashCompQuery to start comparison queries
    Prints elapsed query time
    """
    print("Building hash table with chaining.",end="\n\n")
    glove = open("glove.6B.50d.txt",encoding='utf-8')
    lines = glove.readlines()
    glove.close()
    start = time.time()
    size = 1
    H = HashBuild(lines,size)
    elapsed = time.time() - start
    print("Hash Table Stats:")
    print("Initial Table Size: ",size)
    print("Final Table Size: ",len(H.item))
    print("Load factor: ",round(HashString.load(H),2))
    print("Percentage of Empty Lists: ",round(HashString.empty(H),2),"%")
    print("Standard deviation of the lengths of the lists: ",round(HashString.standDev(H),3))
    print("Running time for hash table construction: ",round(elapsed,2)," seconds",end="\n\n")
    print("Reading word file to determine similarities.",end="\n\n")
    comp = open("comparisons.txt")
    hold = comp.readlines()
    comp.close()
    print("Word similarities found:",end="\n\n")
    elapsed = HashCompQuery(H,hold)
    print()
    print("Running time for hash table with chaining query processing: ",elapsed," seconds")
    

def HashBuild(file,size):
    """
    Receives a file object and returns a built hash table
    Slices off the first character of the file, as it is an encoding character
    Splits each line of the file into a string array
        stores the first element in word
        stores the remaining elements of the string array into embd as floats
        Uses permC as a character list of approved characters that a word can begin with
    Inserts each line into the hash table
    If the number of items in the table ever equals the current number of buckets,
        rebuilds the hash table with a new size equal to (size*3)+1
    returns the hash table
    """
    permC = 'abcdefghijklmnopqrstuvwxyz'
    file[0] = file[0][1:]
    s = file[0].split()
    word = s[0]
    embd = [float(k) for k in s[1:]]
    H = HashString.HashTableC(size)
    if word[0] in permC:
        HashString.InsertC(H,word,embd)
    for i in file[1:]:
        i = i.split()
        word = i[0]
        embd = [float(j) for j in i[1:]]
        if word[0] in permC:
            HashString.InsertC(H,word,embd)
        if H.numItems == size:
            size = (size*2)+1
            H = HashRebuild(H,size)
    return H
        
def HashRebuild(H,size):
    """
    Takes the passed hash table and builds a new table of the given size
        with all elements in the old table
    Returns new table
    """
    temp = HashString.HashTableC(size)
    for i in range(len(H.item)):
        for j in range(len(H.item[i])):
            HashString.InsertC(temp,H.item[i][j][0],H.item[i][j][1])
    return temp

def HashCompQuery(H,file):
    """
    Comparison query function for hash table
    For each line in the file, it stores the elapsed time,
        the two words to be compared (trimming non alphanumeric characters)
        and prints the return similarity results
    Returns total elapsed time not counting print functions
    """
    elapsed = 0
    permC = 'abcdefghijklmnopqrstuvwxyz'
    for i in file:
        start = time.time()
        s = i.split(",")
        if s[0][0] not in permC:
            s[0] = s[0][1:]
        if s[1][len(s[1])-1] not in permC:
            s[1] = s[1][:-1]
        elapsed += time.time()-start
        print("Similarity [",s[0],",",s[1],"] = ",sim(HashString.FindC(H,s[0]),HashString.FindC(H,s[1])))
    return elapsed
    
def sim(e0,e1):
    dot = 0.0
    uMag = 0.0
    vMag = 0.0
    for i in range(len(e0)):
        dot += (e0[i] * e1[i])
        uMag += e0[i]**2
        vMag += e1[i]**2
    uMag = math.sqrt(uMag)
    vMag = math.sqrt(vMag)
    return round(dot/(uMag * vMag),4)

print("Choose table implementation:")
choice = input("Type 1 for binary search tree or 2 for hash table with chaining:")
print("Choice: ",choice,end="\n\n")
if choice== "1":
    BSTQuery()
elif choice == "2":
    HashQuery()
else:
    print("Input not recognized, please try again.")