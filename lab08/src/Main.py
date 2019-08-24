"""
By: Joaquin Hidalgo
Lab 08

Created on Tues 7 May 18:32:21 2019
Instructor: Olac Fuentes
TA: Dita and Mali
Last modified Fri 10 May 23:29:11

Use combinations to test trig identies by computing random floats for -pi to pi.
Then evaulation a pair of identities and subtract the differnce of the two functions,
get the absolute value of the differnce and if differnce is above tolerance, we can say that they are not idetities versus if less than tolerance, then we do that identity until 'tries' to ensure it wasnt luck.

We use backtracking method to find the subset of a list of integers and partion
each set thus in the end, we have two subsets of the set such that,
s1 union s2 is Set and s1 intersection s2 is the empty set and the sum of s1 == sum of s2.
print and display the two sets if possible
"""

import random
import math
import numpy as np
from itertools import combinations 
import mpmath
import time

#Takes in a list 'eq' of all possible combinations in pairs of all identies
#Returns nothing but prints all trig identities found in 'eq'
def Test_Identities(eq, tol, tries):
    for i in eq:
        #Flag keeps track if 2 identities are IN-EQUAL
        flag = False
        
        trig1,trig2 = i
        for j in range(tries):
            x = random.uniform(-math.pi,math.pi) # generates random num for -pi to pi
            y1= eval(trig1)
            y2 = eval(trig2)
            difference = np.abs(y2-y1) # take difference of two equations/identites
           
            #Checks if differnece is greater than tolerance
            if difference > tol:
                flag = True
                
            #if flag == True, break from this speficic pair identity
            if flag:
                break
        if flag == False:
            print('eq1: ', trig1)
            print('eq2: ', trig2)
            print('difference:',difference)
            print('\n')
    
    
def subsetsum(S,last,goal):
    global subset1_indexs # set global subset1 index's
    
    #base casre
    if goal ==0:
        return True, []
    if goal<0 or last<0:
        return False, []
    
    res, subset= subsetsum(S,last-1,goal-S[last]) # Take S[last]
    
    if res:
        
        #Append indicies and actual elements of set
        subset1_indexs.append(last)
        subset.append(S[last])
        return True, subset
    else:
        return subsetsum(S,last-1,goal) # Don't take S[last]
    

def GetPartion(S, sumOfSet):
    
    # if sumOfSet%2 == 1 then no possible way to partion set into 2 sets that fit guidelines
    if sumOfSet % 2 != 0:
        return False, []
    #Use backtracking
    res, subset = subsetsum(S, len(S)-1, sumOfSet//2)
    return res, subset
    
def GetTwoSubSets(S, sumOfSet, subset, res):
    global subset1_indexs
    sub1 = []
    sub2 = []
    
    #If res == false then no possible partion
    if res == False:
        return sub1, sub2
    c = 0
    
    #iter thru set and every indice thats not in set1 add to 'c'
    for i in range(len(S)):
        if i not in subset1_indexs:
            c+= S[i]
            
    #Checks subset 1 to subset 2, if equal then append coresponding elements to subset1 and subset2
    if c == sum(subset):
        for j in range(len(S)):
            if j in subset1_indexs:
                sub1.append(S[j])
            else:
                sub2.append(S[j])
    return sub1, sub2


#Main
######################################################################

#Makes combo_eq have EXACTLY one pair of each identity to be compares
combo_eq = combinations(['math.sin(x)', 'math.cos(x)', 'math.tan(x)', 'mpmath.sec(x)', '-math.sin(x)','-math.cos(x)', '-math.tan(x)', 'math.sin(-x)', 'math.cos(-x)', 'math.tan(-x)', 'math.sin(x)/math.cos(x)', '2*math.sin(x/2)*math.cos(x/2)', 'math.sin(x)**2', '1-math.cos(x)**2', '(1-math.cos(2*x))/2', '1/math.cos(x)' ], 2)
tol = .001 #This defines tolerance to decide if identity is equal
tries = 100 # The number of tries each pair of identities is tested
setNum = [10,20,30,40,50,150] #Given set to partition
sumOfSet = sum(setNum)
subset1_indexs = [] # contains the indexes of the 1st subset to ensure s1 != s2

Test_Identities(combo_eq, tol, tries) # test and print ONLY trig identities

startBackTracking = time.time()
res, subset = GetPartion(setNum, sumOfSet) #res == True if possible to partion two sets, if so, subset contains nums of s1

subset1, subset2 = GetTwoSubSets(setNum, sumOfSet, subset, res) # obtains if possible both sets of the partion
endBackTracking = time.time()

# If subset1 U subset2 == All Set
# If subset1 n subset2 == Empty Set
if res:
    print('runtime: ', endBackTracking - startBackTracking)
    print('s1: ', subset1)
    print('s2: ', subset2)

else:
    print('No partition exists')
    print('runtime: ', endBackTracking - startBackTracking)


