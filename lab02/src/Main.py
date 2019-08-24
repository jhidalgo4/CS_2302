#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 19:04:39 2019
Dr. Fuentes

@author: joaquin
"""
import random

class Node(object):
    def __init__(self, item, next = None):
        self.item = item
        self.next = next
        
class List(object):
    def __init__(self):
        self.head = head
        self.tail = tail
######################################   

#Method 'IsEmpty' returns a boolean checking if 'List' is empty        
def IsEmpty(L):
    return L.head == None

def Append(L, ins):
    if IsEmpty(L):
        L.head = ins
        L.tail = L.head
    else:
        L.tail.next = Node(ins);
        L.tail = L.tail.next

#Method 'GenerateList' returns nothin but appens random integers from (1-10) to list Nums
def GenerateList(L, n):
    for i in range(n):
        Append(Nums, random.randint(1,10) )

#Methog 'Print' prints all the elements in the 'List'
def Print(L):
    iterator = L.head
    while iterator is not None:
        print(iterator.item, end=' ')
        iterator = iterator.next
    print()
    
#Method 'GetLength' returns an integer which is the length of 'List'
def GetLength(L):
    counter = 0
    if IsEmpty(L):
        return counter
    t = L.head
    while t is not None:
        counter += 1
        t = t.next
    return counter

#Method 'GetMiddle' returns an integer the index of the middle element in 'List'
def GetMiddle(L):
    lengthList = GetLength(L)
    if lengthList <= 2:
        return 0
    else:
        if lengthList % 2 == 0:
            lengthList = (lengthList//2) - 1
        else:
            lengthList = lengthList//2
        return lengthList

def BubbleSort(L):
    if GetLength(L) <= 0:
        return 0
    count = 0
    flag = True
    while flag:
        temp = L.head
        flag = False
        
    
    
def BubbleSort(L):
    count = 0
    flag = True
    while flag:
        temp = L.head
        flag = False
        while temp.next != None:
            
            if temp.item > temp.next.item:
                #SWAP
                swapee = temp.item
                temp.item = temp.next.item
                temp.next.item = swapee
                flag = True
                
            count += 1
            temp = temp.next
    return count



def MergeList(l,r):
    count = 0
    
    result = List()
    
    
    while(l != None and r != None):
        if l.head.item<= r.head.item:
            count +=1
            Append(result, l.head.item)
            l.head = l.next
        else:
            count +=1
            Append(result, r.head.item)
            r.head= r.next
    if l != None:
        count +=1
        Append(result, l.head)
        l.head = l.next
    if r != None:
        count +=1
        Append(result, r.head)
        r.head = r.next
    
        
    return result.head
    
   
def MergeSort(L):
    if L.head == None or L.head.next == None:
        return 
    middle = GetMiddleElem(L)
    afterMiddle = middle.next
    middle.next = None
    
    leftSide = MergeSort(L)
    rightSide = MergeSort(afterMiddle)
    
    
    
    newHead = MergeList(leftSide, rightSide)
    L = newHead

    
        



#Main
####################################################################


#length of list
#length_of_list= int(input("Enter the length of your array: "))  #gets input from user
length_of_list = 4

#Create List
Nums = List()

#Generate random List of nums
GenerateList(Nums, length_of_list)



