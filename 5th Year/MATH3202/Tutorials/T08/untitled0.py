# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 09:58:58 2023

@author: ryanw
"""

### Factorial function

def fact(x):
    if x == 0:
        return 1
    else:
        return x * fact(x - 1)
    

### Minimal Studying problem

probs = [[0.2, .3, .35, .38, .4],
         [.25, .3, .33, .35, .38],
         [.1, .3, .4, .45, .5]]


def angie(j, s):
    ''' Min probability of failing subject j with s hours of study
    Parameters
    ----------
    j : int
        Subject number between 1 and 3 inclusive
    s : int
        Number of hours of study, between 0 and 4 inclusive
    '''
    if j == 3:
        return (1, "End")
    else:
        minProb = (1, None)
        for a in range(s + 1):
            p = (1 - probs[j][a]) * angie(j + 1, s - a)[0]
            if p < minProb[0]:
                minProb = (p, a, s - a)
        return minProb
    
def angie_one(j, s):
    '''One line version of angie(j, s)'''
    if j == 3:
        return (1, "End")
    else:
        return min([((1 - probs[j][a]) * angie_one(j + 1, s - a)[0], a, s - a) for a in range(s + 1)])

def angie_sol():
    s = 4
    for j in range(3):
        v = angie_one(j, s)
        if j == 0:
            print(f"Max probability of passing is p = {round(1 - v[0], 3)}")
        print(f"Spend {v[1]} hours on subject {j}")
        s = v[2]
    




### Knapsack problem
sizes = {1: 7, 2: 4, 3: 3}
values = {1: 25, 2: 12, 3: 8}
# we want knap(1, 20)
def knap(j, s):
    ''' Maximum value of packing in object j with container size s
    '''
    if j not in sizes:
        return (1, "End")
    else:
        maxpack = s // sizes[j]
        return max([(values[j] * a + knap(j + 1, s - sizes[j] * a)[0], a, s - sizes[j] * a) for a in range(maxpack + 1)])


### Knapsack TWO: electric boogaloo
knap2_ = {}
def knap2(s):
    if s < min([sizes[j] for j in sizes]):
        return (0, 'Full')
    if s not in knap2_:
        knap2_[s] = max([(values[a] + knap2(s - sizes[a])[0], a) for a in sizes if sizes[a] <= s])
    return knap2_[s]

### fibonacci 

fib_ = {1: 1, 2: 1}

def fib(n):
    if n not in fib_:
        fib_[n] = fib(n - 1) + fib(n - 2)
    return fib_[n]







