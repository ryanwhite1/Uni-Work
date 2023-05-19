# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:00:37 2023

@author: ryanw
"""

def deliv_cost(n, L):
    ''' Delivery cost for ordering n small gas cylinders and L large gas cylinders
    '''
    return 300 + 50 * n + 80 * L

def profit(t, s, L, small_order, large_order):
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
    
    

demand = [7, 14, 8, 8, 12, 15, 6, 15, 7, 12, 13, 9, 6, 11]
high_demand = [12, 17, 17, 12, 18, 22, 14, 19, 11, 20, 19, 18, 13, 20]
large_demand = [3, 2, 3, 3, 3, 4, 2, 4, 2, 3, 3, 4, 4, 5]
p = 0.4
r = 120
large_r = 230
cap = 30
large_cap = 2
Dcap = 1000
Mcyl = 45
Mcyl_L = 90

gas_ = {}
def gas(t, s, L):
    if (t, s, L) not in gas_:
        if t == 14:
            gas_[t, s, L] = (0, 'finish')
        else:
            gas_[t, s, L] = max([(profit(t, s, L, n, N) + 
                                  p * gas(t + 1, s + n - min(high_demand[t], s + n), L + N - large_demand[t])[0] +
                                  (1 - p) * gas(t + 1, min(cap, s + n - min(demand[t], s + n)), L + N - large_demand[t])[0], 
                                  [n, N]) \
                                  for N in range(min(large_demand[t], max(0, large_demand[t] - L)), 
                                                min(large_cap - L + large_demand[t], Dcap // Mcyl_L) + 1) \
                                  for n in range(0, min(cap - s + high_demand[t], (Dcap - N * Mcyl_L) // Mcyl) + 1)
                                  ])
    return gas_[t, s, L]
    
print(gas(0, 0, 0))

