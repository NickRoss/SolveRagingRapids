#!/usr/bin/env python3

import numpy as np
import itertools
import string

num2alpha = dict(zip(range(0, 26), string.ascii_lowercase))

### piece_list conains a list of the pieces. Starting from their knees (piece looking at spot 0)
### and going clockwise, a 1 means "out" and a 0 means "in", refering to the type of connection.
### On the bottom of each piece is a letter (A-L). The zeroth element is "A", 1st element is "B", etc.


### Note that the basic solution is to solve the corners first, and then itterate over every possibly within 
### that search space. Since the number of tiles which fit into a corner is quite small, this reduces the 
### search space from 12! to something much more manageable. Note that the code has two overriding issues I'm 
### too lazy to fix: shitty globals/naming and the main loop doesn't stop when it finds a solution.


piece_list = [
    [0,1,0,1,1,0] #A
    ,[0,0,1,1,0,1] #B
    ,[1,0,1,0,0,1] #C
    ,[0,1,0,0,1,0] #D
    ,[1,1,0,1,1,0] #E
    ,[0,0,1,0,1,0] #F
    ,[1,1,0,0,1,0] #G
    ,[0,0,1,1,1,0] #H
    ,[1,1,0,1,0,1] #I
    ,[1,0,1,1,1,0] #J
    ,[1,1,0,0,0,1] #K
    ,[0,1,0,0,0,1] #L
]


### The variables "backropedir" and "faceropedir" contain information about 
### what the pieces have to be. We call each element a "frame filter"
### There are three different values 1,0 and 2
### A 1 means that there is an outer tab in that position, 0 means there is an 
### inner tab in the position and 2 means that anything can be in the position.

### The order of the list is as follows -- for the back_rope_dir, hold the frame with 
### The rope in the back and then read as 
### 0,1,2
### 3,4,5
### 6,7,8
### 9,10,11

### For face_rope_dir, hold the frame with the rope at the front and then:
### 0,1,2
### 3,4,5
### 6,7,8
### 9,10,11

back_rope_dir = [
      [1,2,2,2,1,0] #0
    , [1,2,2,2,2,2] #1
    , [1,0,1,2,2,2] #2
    , [2,2,2,2,1,0] #3
    , [2,2,2,2,2,2] #4
    , [2,1,0,2,2,2] #5
    , [2,2,2,2,1,0] #6
    , [2,2,2,2,2,2] #7
    , [2,1,0,2,2,2] #8
    , [2,2,2,0,0,1] #9
    , [2,2,2,0,2,2] #10
    , [2,1,0,0,2,2] #11  
]


face_rope_dir = [
    [0,2,2,2,1,0] #0 
    , [0,2,2,2,2,2] #1
    , [0,0,1,2,2,2] #2
    , [2,2,2,2,1,9] #3 
    , [2,2,2,2,2,2] #4
    , [2,1,0,2,2,2] #5 
    , [2,2,2,2,1,0] #6 
    , [2,2,2,2,2,2] #7 
    , [2,1,0,2,2,2] #9
    , [2,2,2,1,0,1] #9
    , [2,2,2,1,2,2] #10
    , [2,1,0,1,2,2] #11
]

### all_set is the set of all numbers and is used to determine which pieces are left
### to go in the puzzle
all_set = set(range(12))

### Set the following to 1/0 depending on which direction you wish to solve
if 1 == 0:
    ### This does back_rope_dir
    np_filters = [np.array(x) for x in back_rope_dir]
else:
    ### This does face_rope_dir
    np_filters = [np.array(x) for x in face_rope_dir]
    
np_piece_list = [np.array(x) for x in piece_list]    

### All of the above are converted to np arrays so that some functions below 
### (which I no longer remember) can be used.


def piece_fit(dlst, flt):
    ### Return a true/false as to if a piece passes a frame filter
    ### Logic is elem by elem subtraction. If the subraction is zero that
    ### means that there is a 1 - 1 or 0 - 0, which fails. 
    for sval in dlst - flt:
        if sval == 0:
            return False
    else:
        return True

def genvalst(nplst, npfltrs):
    val = []
    vallst = []
    for x in range(len(nplst)):
        val.append( [x,[piece_fit(np_piece_list[x],y) for y in np_filters]])
        vallst.append([piece_fit(np_piece_list[x],y) for y in np_filters] )

    return val, vallst


def setcorners(vallst):
    
    sp = []
    
    for spt in [0,2,9,11]:
        
        sptlst = []
        for x in range(len(val)):

            if val[x][1][spt] == True:
                sptlst.append(x)

        sp.append(sptlst)
        
    lst2 = sp
    j = list(itertools.product(*lst2))
    cornersols = []
    for t in j:
        if len(set(t)) != 4:
            continue
        else:
            cornersols.append(t)    
    return cornersols


def used(sol):
    ### Returns a list of used tiles from a solution 
    return set(sol) - set([None] )

def unused(allS, sol):
    ### Return unused tiles
    return allS - set(sol) 

def ltor(lst, ltile, rtile):
    lefttile = lst[ltile]
    righttile = lst[rtile]
    return lefttile[1] - righttile[5] != 0 and lefttile[2] - righttile[4] != 0

def ttob(lst, ttile, btile):
    toptile = lst[ttile]
    bottile = lst[btile]

    return toptile[3] - bottile[0] != 0
    
def checkint(possol):
    ### this goes through a list and verifies that the pieces can work together
    sidetoside = [0,1,3,4,6,7,9,10]
    toptobottom =[0,1,2,3,4,5,6,7,8]
    
    failed = 0
    for x in sidetoside:        
        if ltor(piece_list, possol[x], possol[x+1]) == False:
            failed = 1
            break
    
    for x in toptobottom:
        if ttob(piece_list, possol[x], possol[x+3]) == False:
            #print(x, 'ttob')
            failed = 1
            break
            
    return failed

[val, vallst] = genvalst(np_piece_list, np_filters)
cornersols = setcorners(vallst)
finalsol = []

for csol in cornersols:
    
    sol = [None] * 12
    sol[0] = csol[0]
    sol[2] = csol[1]
    sol[9] = csol[2]
    sol[11] = csol[3]
    
    used = set(sol) - set([None] )    
    
    for x in itertools.permutations(list(unused(all_set, sol))):
        vlst = list(x)
        newsol = []
        for pos in range(len(sol)):
            if sol[pos] == None:
                possval = vlst.pop() 
                if vallst[possval][pos] == False:
                    break
                else:
                    newsol.append(possval)
            else:
                newsol.append( sol[pos] )

        if len(newsol) == 12:
            if checkint(newsol) == 0:
                finalsol = newsol
                break

print('finished computation')
### Final Solution
print( list( map(lambda x: num2alpha[x], finalsol) ))


## EOF ##
