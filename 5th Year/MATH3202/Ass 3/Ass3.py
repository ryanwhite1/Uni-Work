# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:00:37 2023

@author: ryanw
"""
import math

def deliv_cost(n):
    return 300 + 50 * n

demand = [7, 14, 8, 8, 12, 15, 6, 15, 7, 12, 13, 9, 6, 11]
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
            print(t)
            gas_[t, s] = max([(min(demand[t], s + n) * r - min(n, 1) * deliv_cost(n) + 
                               gas(t + 1, s + n - min(demand[t], s + n))[0], n) for n in range(0, min(cap - s + demand[t], Ncyl) + 1)])
    return gas_[t, s]