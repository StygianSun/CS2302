"""
@Course: CS2302 MW 1:30-2:50 pm
@Author: Robert Marc, 80487972
@Assignment: Lab 8
@Instructor: Dr. Olac Fuentes
@TAs: Anindita Nath and Maliheh Zargaran
@Date of Last Modification: 5/7/19 @9:08 PM
@Purpose: To design algorithms that 'discover' and test trigonometric identies
"""

import math
import random
import numpy as np
import time

def trigBuild(t):
    """
    Builds an array that holds all the calculate values for particular
        trigonometric identies. This is to prevent the testing program
        from continuously recalculating identies. The string version of the
        identity is also held.
    """
    print("t = ",t)
    print()
    trig = []
    trig.append([math.sin(t),"sin(t)"])                                #0
    trig.append([math.cos(t),"cos(t)"])                                #1
    trig.append([math.tan(t),"tan(t)"])                                #2
    trig.append([(1/math.cos(t)),"sec(t)"])                            #3
    trig.append([-trig[0][0],"-sin(t)"])                               #4
    trig.append([-trig[1][0],"-cos(t)"])                               #5
    trig.append([-trig[2][0],"-tan(t)"])                               #6
    trig.append([math.sin(-t),"sin(-t)"])                              #7
    trig.append([math.cos(-t),"cos(-t)"])                              #8
    trig.append([math.tan(-t),"tan(-t)"])                              #9
    trig.append([(math.sin(t)/math.cos(t)),"sin(t)/cos(t)"])           #10
    trig.append([(2*math.sin(t/2)*math.cos(t/2)),"2sin(t/2)cos(t/2)"]) #11
    trig.append([math.pow(math.sin(t),2),"sin^2(t)"])                  #12
    trig.append([(1-math.pow(math.cos(t),2)),"1-cos^2(t)"])            #13
    trig.append([((1-math.cos(2*t))/2),"(1-cos(2t))/2"])               #14
    trig.append([(1/math.cos(t)),"1/cos(t)"])                          #15    
    return trig

def trigTest(trig):
    """
    Builds an array that holds every combination of identities. It then uses
        the combinations of to determine if they are true or not.
    """
    test = []
    equal = []
    notEqual = []
    tol = 0.0000000001
    for u in range(16):
        for v in range(u,16):
            if u != v:
                test.append([u,v])
    for t in test:
        if abs(trig[t[0]][0]-trig[t[1]][0]) < tol:
            equal.append([t[0],t[1]]) #appends matrix indices of identities that are equal
        else:
            notEqual.append([t[0],t[1]]) #appends matrix indices of identities that are not equal
    for n in notEqual: #prints each identities value and that they are not equal
        print(trig[n[0]][1]," = ",trig[n[0]][0])
        print(trig[n[1]][1]," = ",trig[n[1]][0])
        print(trig[n[0]][1]," != ",trig[n[1]][1])
        print("Tolerance: ",tol)
        print()
    for e in equal: #prints each identities value and that they are equal
        print(trig[e[0]][1]," = ",trig[e[0]][0])
        print(trig[e[1]][1]," = ",trig[e[1]][0])
        print(trig[e[0]][1]," = ",trig[e[1]][1])
        print("Tolerance: ",tol)
        print()
    
            
def partition(S,n):
    """
    If the sum of set S is not even, no partition can exist for the given set.
    If the sum of set S is even, passes the set, the length of the set, and 
        half the sum of the whole set to the subset helper method.
    The subset helper method returns true or false depending on if a
        partition is found.
    If the partition is found, prints that a partition does exist for set S
    If the partition is not found, prints that a partition does not exist for set S
    Then returns the boolean value on if a partition was found.
    """
    k = sum(S)
    if k%2 != 0:
        print("No partition exists for set: ",S)
        return False, []
    subExists, s1 = subset(S,n,k/2)
    if subExists:
        print("Partition exists for set: ",S)
    else:
        print("Partition does not exist for set: ",S)
    return subExists, s1

def subset(S,n,k):
    """
    Base case 1: The sum is equal to 0: partition has been found, return true
    Base case 2: The remaining number of elements that can be chosen is 0 and
        the sum does not equal 0: return false
    If the next number to be chosen would exceed the remaining sum, skip
    Save the results of picking and not picking the next number.
    If the result of picking the next number is true AND the result of not
        picking the next number is false, appends the chosen number to a global
        subset s1 and returns the result of picking the next number.
    If the result of not picking the next number is true, does nothing and
        returns the result of not picking the next number.
    """
    if k == 0:
        return True, []
    if n<0 or k<0:
        return False, []
    se, ss = subset(S,n-1,k-S[n-1])
    if se:
        ss.append(n-1)
        return True, ss
    else:
        return subset(S,n-1,k)
"""
Code for testing of trigonometric identities. Generates a number between -pi and pi,
    then passes that to the trigBuild function, storing the resulting array in
    trig, then passes that onto trigTest
""" 
elapsed = 0
for i in range(10): 
    t = random.uniform(-math.pi,math.pi)
    start = time.time()
    trig = trigBuild(t)
    trigTest(trig)
    elapsed += time.time()-start
print (elapsed/10)

"""
Code for testing of partition problem. Uses both given sets S so that it can be
    tested against a set that has a partition possible and a set that does not
    have a partition possible.
Sorts the given set first.
Passes the set and length of the set to the partition method:
    Receives the returned boolean of true if a partition is possible and false
        if a partition is not possible.
If a partition is possible
    Builds the two subsets by appending the values of the indices of S found in
        the list of indices returned by partition into s1, and those indices
        not found in the list to s2.
    Prints subset 1 (s1).
    Prints subset 2 (s2).

Then tests against a set that does not have a partition possible.
"""
elapsed = 0
n = 5
S=np.zeros(n,dtype=int)
for j in range(10):
    for i in range(n):
        S[i] = random.randint(0,n)
    S.sort()
    start = time.time()
    sub, ss = partition(S,len(S))
    if sub:
        s1 = []
        s2 = []
        for i in range(len(S)):
            if i in ss:
                s1.append(S[i])
            else:
                s2.append(S[i])
        print(s1)
        print(s2)
    elapsed += time.time()-start
    
print(elapsed/10)
"""   
S = [2,4,5,9,13]
S.sort()
s1 = []
sub = partition(S,len(S))
if sub:
    if (sum(S)/2) != 1:
        s1.pop()
    s2 = []
    for i in S:
        if i not in s1:
            s2.append(i)
    print(s1)
    print(s2)
"""
