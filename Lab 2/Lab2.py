"""
@Course: CS2302 MW 1:30-2:50 pm
@Author: Robert Marc, 80487972
@Assignment: Lab 2
@Instructor: Dr. Olac Fuentes
@TAs: Anindita Nath and Maliheh Zargaran
@Date of Last Modification: 2/24/19 @3:58 AM
@Purpose: Iplement different sorting methods, then searching for the 
    median of the sorted lists, while counting comparisons for time complexity analysis
"""
import random

#Node Functions
class Node(object):
    # Constructor
    def __init__(self, item, next=None):  
        self.item = item
        self.next = next 
        
def PrintNodes(N):
    if N != None:
        print(N.item, end=' ')
        PrintNodes(N.next)
        
def PrintNodesReverse(N):
    if N != None:
        PrintNodesReverse(N.next)
        print(N.item, end=' ')
        
#List Functions
class List(object):   
    # Constructor
    def __init__(self): 
        self.head = None
        self.tail = None
        
def IsEmpty(L):  
    return L.head == None     
        
def Append(L,x): 
    # Inserts x at end of list L
    if IsEmpty(L):
        L.head = Node(x)
        L.tail = L.head
    else:
        L.tail.next = Node(x)
        L.tail = L.tail.next
        
def Print(L):
    # Prints list L's items in order using a loop
    temp = L.head
    while temp is not None:
        print(temp.item, end=' ')
        temp = temp.next
    print()  # New line 

def PrintRec(L):
    # Prints list L's items in order using recursion
    PrintNodes(L.head)
    print() 
    
def Remove(L,x):
    # Removes x from list L
    # It does nothing if x is not in L
    if L.head==None:
        return
    if L.head.item == x:
        if L.head == L.tail: # x is the only element in list
            L.head = None
            L.tail = None
        else:
            L.head = L.head.next
    else:
         # Find x
         temp = L.head
         while temp.next != None and temp.next.item !=x:
             temp = temp.next
         if temp.next != None: # x was found
             if temp.next == L.tail: # x is the last node
                 L.tail = temp
                 L.tail.next = None
             else:
                 temp.next = temp.next.next
         
def PrintReverse(L):
    # Prints list L's items in reverse order
    PrintNodesReverse(L.head)
    print()     
   
    #Begin student code
    
def ListFill(n):
    #Fills a list of size n with random integers between 0 and n
    L = List()
    for i in range(n):
        Append(L,random.randint(0,n))
    return L

def BubbleSort(L):
    #Bubble sorts list L, swapping incorrectly ordered elements until sorted
    changed = True
    global bubbleCounter
    while changed:
        curNode = L.head
        changed = False
        while curNode.next != None:
            bubbleCounter += 1
            if curNode.item > curNode.next.item:
                temp = curNode.item
                curNode.item = curNode.next.item
                curNode.next.item = temp
                changed = True
            curNode = curNode.next
            
def Length(L):
    #Returns length of the list L
    count = 0
    temp = L.head
    if temp != None:
        count += 1
        while temp.next != None:
            count += 1
            temp = temp.next
            
    return count

def Copy(L):
    #Copies list L to temp and returns temp
    temp = List()
    curNode = L.head
    
    while curNode != None:
        Append(temp,curNode.item)
        curNode = curNode.next
        
    return temp

def GetElementAt(L,n):
    #Returns the item of element n in List L
    curNode = L.head
    pointer = 0
    
    while pointer != n:
        curNode = curNode.next
        pointer += 1
        
    return curNode.item
           
def MergeSort(L):
    #Separates given list into left and right, until one element remains, then merges
    
    #Checks that there is only one element in list L, base case
    if L.head == None or L.head.next == None:
        return L
    
    len = Length(L)
    
    left, right = SplitList(L)

    left = MergeSort(left)
    right = MergeSort(right)
    
    return MergeLists(left, right)
    
def SplitList(L):
    #Splits the given list into left and right
    
    len = Length(L)
    tempL = List()
    tempR = List()
    curNode = L.head
    
    for i in range(len):
        if i < len//2:
            Append(tempL,curNode.item)
            curNode = curNode.next
        else:
            Append(tempR,curNode.item)
            curNode = curNode.next
    
    return tempL, tempR
   
def MergeLists(L, R):
    #Merges the two given lists while sorting them
    global mergeCounter
    
    temp = List()

    #Makes sure that the temp list is not a None value and the head and tail are intitialzed properly
    if L == None and R == None:
        temp.head = None
        temp.tail = None
    elif L == None: #If the Left list is empty, fills temp with the right list
        temp = Copy(L)
    elif R == None: #If the right list is empty, fills temp with the left list
        temp = Copy(R)
    else:
        curNodeL = L.head
        curNodeR = R.head
        while curNodeL and curNodeR: #Moves through both lists, sorting values into temp
            if curNodeL.item < curNodeR.item:
                mergeCounter += 1
                Append(temp,curNodeL.item)
                curNodeL = curNodeL.next
            else:
                mergeCounter += 1
                Append(temp,curNodeR.item)
                curNodeR = curNodeR.next
        if curNodeL == None: #If left list is processed before right finishes, finish filling with right
            while curNodeR != None:
                Append(temp,curNodeR.item)
                curNodeR = curNodeR.next
        elif curNodeR == None: #If right list is processed before left finishes, finish filling with right
            while curNodeL != None:
                Append(temp,curNodeL.item)
                curNodeL = curNodeL.next

    return temp

def QuickSort(L):
    #Sorts by splitting list into manageable sections and sorts before recursing quicksort on smaller segment
    global quickCounter
    
    #Base case
    if Length(L) <= 1:
        return L
    
    smaller = List()
    equal = List()
    larger = List()
    pivot = L.head
    curNode = L.head
    
    while curNode != None: #Sorts items into three lists, smaller, equal, and larger
        if curNode.item < pivot.item:
            quickCounter += 1
            Append(smaller, curNode.item)
        elif curNode.item == pivot.item:
            quickCounter += 1
            Append(equal, curNode.item)
        else:
            Append(larger, curNode.item)
        curNode = curNode.next
        
    return Concat(Concat(QuickSort(smaller),equal),QuickSort(larger)) #Rebuilds list with smaller pieces while recursively
                                                                        #calling QuickSort on smaller and larger lists

def Concat(L1,L2):
    #Function to build new list from two passed lists
    curNodeL1 = L1.head
    curNodeL2 = L2.head
    temp = List()
    while curNodeL1 != None:
        Append(temp,curNodeL1.item)
        curNodeL1 = curNodeL1.next
    while curNodeL2 != None:
        Append(temp,curNodeL2.item)
        curNodeL2 = curNodeL2.next
    
    return temp

def QuickSortMod(L,rank):
    #Modified QuickSort algorithm to find median without fully sorting list
    global modCounter
    
    #Base case if algorithm fails and rank becomes less than 0
    if Length(L) <= 1:
        return L.head.item
    
    smaller = List()
    largequal = List()
    pivot = L.head
    curNode = L.head.next
    
    while curNode != None: #Builds a list of elements smaller than the pivot and a list of elements
        if curNode.item < pivot.item:   #larger or equal to the pivot, not including the pivot itself
            modCounter += 1
            Append(smaller, curNode.item)
        else:
            modCounter += 1
            Append(largequal, curNode.item)
        curNode = curNode.next    
    
    if Length(smaller) < rank: #If List of smaller elements' length is less than rank, recur on largequal list
        return QuickSortMod(largequal,rank-Length(smaller)-1)
    elif Length(smaller) > rank: #If list of smaller elements' length is greater than rank, recur or smaller list
        return QuickSortMod(smaller,rank)
    elif Length(smaller) == rank: #If list of smaller elements' length is equal to rank, return the pivot's data point
        return pivot.item
    
def MedianBubble(L):
    #Makes a copy of passed list L, sorts using BubbleSort, then finds the median
    C = Copy(L)
    BubbleSort(C)
    median = GetElementAt(C,Length(C)//2)
    return median

def MedianMerge(L):
    #Makes a copy of passed list L, sorts using MergeSort, then finds the median
    C = Copy(L)
    C = MergeSort(C)
    median = GetElementAt(C,Length(C)//2)
    return median

def MedianQuick(L):
    #Makes a copy of passed list L, sorts using QuickSort, then finds the median
    C = Copy(L)
    C = QuickSort(C)
    median = GetElementAt(C,Length(C)//2)
    return median

test = ListFill(100)
bubbleCounter = 0
mergeCounter = 0
quickCounter = 0
modCounter = 0
Print(test)
print("BubbleSortMedian = ",MedianBubble(test))
print("BubbleSort Counter = ",bubbleCounter)
print("MergeSortMedian = ",MedianMerge(test))
print("MergeSort Counter = ", mergeCounter)
print("QuickSortMedian = ",MedianQuick(test))
print("QuickSort Counter = ", quickCounter)
print("QuickSortModMedian = ",QuickSortMod(test,Length(test)//2))
print("QuickSortMod Counter = ", modCounter)
BubbleSort(test)
Print(test)