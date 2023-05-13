# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:00:37 2023

@author: ryanw
"""
import math

def deliv_cost(n, L):
    return 300 + 50 * n + 80 * L

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
Ncyl = math.floor(Dcap / Mcyl)

gas_ = {}
def gas(t, s, L):
    if (t, s, L) not in gas_:
        if t == 14:
            gas_[t, s, L] = (0, 'finish')
        else:
            gas_[t, s, L] = max([((p * min(high_demand[t], s + n) + (1 - p) * min(demand[t], s + n)) * r + large_demand[t] * large_r - 
                                  min(n + N, 1) * deliv_cost(n, N) + gas_stoc(t, s, L + N - large_demand[t], n), [n, N]) \
                                 for N in range(min(large_demand[t], max(0, large_demand[t] - L)), 
                                                min(large_cap - L + large_demand[t], math.floor(Dcap / Mcyl_L)) + 1) \
                                 for n in range(0, min(cap - s + high_demand[t], math.floor((Dcap - N * Mcyl_L) / Mcyl)) + 1)
                                 ])
    return gas_[t, s, L]

def gas_stoc(t, s, L, n):
    return p * gas(t + 1, s + n - min(high_demand[t], s + n), L)[0] + (1 - p) * gas(t + 1, min(cap, s + n - min(demand[t], s + n)), L)[0]
