# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:00:37 2023

@author: ryanw
"""

def deliv_cost(n, L):
    ''' Delivery cost for ordering n small gas cylinders and L large gas cylinders
    '''
    return 300 + 50 * n + 80 * L

def profit(t, s, L, n, N):
    ''' Calculates the profit for predetermined (stochastic) demand and delivering costs
    Parameters
    ----------
    t : int
        Current day
    s : int
        Number of small cylinders currently in storage
    L : int
        "" for large cylinders
    n : int
        Number of small cylinders ordering in on day t
    N : int
        "" large cylinders
    '''
    small_revenue = (p * min(high_demand[t], s + n - 2 * deficit(t, L, N)) + (1 - p) * min(demand[t], s + n - 2 * deficit(t, L, N))) * r
    large_revenue = large_demand[t] * large_r
    cost = min(n + N, 1) * deliv_cost(n, N)
    return small_revenue + large_revenue - cost
    
def deficit(t, L, N):
    ''' Calculates the deficit in available large gas cylinders to meet the mandatory demand. 
    '''
    return max(0, large_demand[t] - L - N)

def small_step(t, s, L, n, N):
    ''' Performs one normal demand small cylinder inventory time step 
    '''
    return s + n - 2 * deficit(t, L, N) - min(demand[t], s + n - 2 * deficit(t, L, N))

def high_step(t, s, L, n, N):
    ''' Performs one high demand small cylinder inventory time step 
    '''
    return s + n - 2 * deficit(t, L, N) - min(high_demand[t], s + n - 2 * deficit(t, L, N))

def large_step(t, L, N):
    ''' Performs one large cylinder inventory time step 
    '''
    return L + N - large_demand[t] + deficit(t, L, N)

demand = [7, 14, 8, 8, 12, 15, 6, 15, 7, 12, 13, 9, 6, 11]              # base demand for small cylinders on each day
high_demand = [12, 17, 17, 12, 18, 22, 14, 19, 11, 20, 19, 18, 13, 20]  # possible high demand for small cylinders on each day
large_demand = [3, 2, 3, 3, 3, 4, 2, 4, 2, 3, 3, 4, 4, 5]               # mandatory sales of large cylinders on each day
p = 0.4         # probability of high demand sales
r = 120         # sale price of a small cylinder
large_r = 230   # sale price of a large cylinder
cap = 30        # storage cap for small cylinders
large_cap = 2   # storage cap for large cylinders
Dcap = 1000     # delivery mass capacity
Mcyl = 45       # mass of a small cylinder
Mcyl_L = 90     # mass of a large cylinder

gas_ = {}   # stores all calculations so far (memoization)
def gas(t, s, L):
    '''
    Parameters
    ----------
    t : int
        Current day
    s : int
        Number of small cylinders currently in storage
    L : int
        "" for large cylinders
    Returns
    -------
    tuple
        Consists of (x, [n, N]) where x is the expected profit to be made for the remaining 14-t days, n is the number of 45kg cylinders
        to order on day t, and N is the number of 90kg cylinders to order.
    '''
    if (t, s, L) not in gas_:
        if t == 14: # base case
            gas_[t, s, L] = (0, [0, 0])
        else: 
            gas_[t, s, L] = max([(profit(t, s, L, n, N) +                                                                                   # calculate profit                          
                                  p * gas(t + 1, high_step(t, s, L, n, N), large_step(t, L, N))[0] +                                        # first stochastic recursive step
                                  (1 - p) * gas(t + 1, small_step(t, s, L, n, N), large_step(t, L, N))[0],                                  # second stochastic recursive step
                                  [n, N])                                                                                                   # save ordering history
                                  for N in range(0, min(large_cap - L + large_demand[t], Dcap // Mcyl_L) + 1)                               # large cylinders
                                  for n in range(0, min(cap - s + high_demand[t] + 2 * deficit(t, L, N), (Dcap - N * Mcyl_L) // Mcyl) + 1)  # small cylinders
                                  ])
    return gas_[t, s, L]
    
print(gas(0, 0, 0))


















### --- All below functions are for communications <15 --- ###

## Comm 14 ##
def profit14(t, s, L, small_order, large_order):
    ''' Calculates the profit for predetermined (stochastic) demand and delivering costs
    Parameters
    ----------
    t : int
        Current day
    s : int
        Number of small cylinders currently in storage
    L : int
        "" for large cylinders
    small_order : int
        Number of small cylinders ordering in on day t
    large_order : int
        "" large cylinders
    '''
    small_revenue = (p * min(high_demand[t], s + small_order) + (1 - p) * min(demand[t], s + small_order)) * r
    large_revenue = large_demand[t] * large_r
    cost = min(small_order + large_order, 1) * deliv_cost(small_order, large_order)
    return small_revenue + large_revenue - cost

def gas14(t, s, L):
    if (t, s, L) not in gas_:
        if t == 14:
            gas_[t, s, L] = (0, 'finish')
        else:
            gas_[t, s, L] = max([(profit(t, s, L, n, N) + 
                                  p * gas14(t + 1, s + n - min(high_demand[t], s + n), L + N - large_demand[t])[0] +
                                  (1 - p) * gas14(t + 1, min(cap, s + n - min(demand[t], s + n)), L + N - large_demand[t])[0], 
                                  [n, N, p * s + n - min(high_demand[t], s + n) + (1 - p) * s + n - min(demand[t], s + n), L + N - large_demand[t]]) \
                                  for N in range(min(large_demand[t], max(0, large_demand[t] - L)), 
                                                min(large_cap - L + large_demand[t], Dcap // Mcyl_L) + 1) \
                                  for n in range(0, min(cap - s + high_demand[t], (Dcap - N * Mcyl_L) // Mcyl) + 1)
                                  ])
    return gas_[t, s, L]





## Comm 13 ##
def deliv_cost11(n):
    return 300 + 50 * n

Ncyl = Dcap // Mcyl
def gas13(t, s):
    if (t, s) not in gas_:
        if t == 14:
            gas_[t, s] = (0, 'finish')
        else:
            gas_[t, s] = max([((p * min(high_demand[t], s + n) + (1 - p) * min(demand[t], s + n)) * r - min(n, 1) * deliv_cost11(n) + 
                               gas_stoc(t, s, n), [n, p * (s + n - min(high_demand[t], s + n)) + (1 - p) *  min(cap, s + n - min(demand[t], s + n))]) for n in range(0, min(cap - s + high_demand[t], Ncyl) + 1)])
    return gas_[t, s]

def gas_stoc(t, s, n):
    return p * gas13(t + 1, s + n - min(high_demand[t], s + n))[0] + (1 - p) * gas13(t + 1, min(cap, s + n - min(demand[t], s + n)))[0]






## Comm 12 ##

def gas12(t, s):
    if (t, s) not in gas_:
        if t == 14:
            gas_[t, s] = (0, 'finish')
        else:
            gas_[t, s] = max([(min(demand[t], s + n) * r - min(n, 1) * deliv_cost11(n) + 
                               gas12(t + 1, s + n - min(demand[t], s + n))[0], n, s + n - min(demand[t], s + n)) for n in range(0, min(cap - s + demand[t], Ncyl) + 1)])
    return gas_[t, s]





## Comm 11 ##

def gas11(t, s):
    if (t, s) not in gas_:
        if t == 14:
            gas_[t, s] = (0, 'finish')
        else:
            gas_[t, s] = max([(min(demand[t], s + n) * r - min(n, 1) * deliv_cost11(n) + 
                               gas11(t + 1, s + n - min(demand[t], s + n))[0], n, s + n - min(demand[t], s + n)) for n in range(0, cap - s + demand[t] + 1)])
    return gas_[t, s]
