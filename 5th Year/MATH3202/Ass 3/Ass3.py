# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:00:37 2023

@author: ryanw
"""
import math

def deliv_cost(n):
    return 300 + 50 * n

demand = [7, 14, 8, 8, 12, 15, 6, 15, 7, 12, 13, 9, 6, 11]
high_demand = [12, 17, 17, 12, 18, 22, 14, 19, 11, 20, 19, 18, 13, 20]
p = 0.4
r = 120
cap = 30
Dcap = 1000
Mcyl = 45
Ncyl = math.floor(Dcap / Mcyl)

gas_ = {}
def gas(t, s):
    if (t, s) not in gas_:
        if t == 14:
            gas_[t, s] = (0, 'finish')
        else:
            gas_[t, s] = max([((p * min(high_demand[t], s + n) + (1 - p) * min(demand[t], s + n)) * r - min(n, 1) * deliv_cost(n) + 
                               gas_stoc(t, s, n), n) for n in range(0, min(cap - s + high_demand[t], Ncyl) + 1)])
    return gas_[t, s]

def gas_stoc(t, s, n):
    return p * gas(t + 1, s + n - min(high_demand[t], s + n))[0] + (1 - p) * gas(t + 1, min(cap, s + n - min(demand[t], s + n)))[0]
