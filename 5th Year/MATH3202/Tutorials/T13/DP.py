# -*- coding: utf-8 -*-
"""
Created on Thu May 25 10:57:20 2023

@author: ryanw
"""

r = 12
bc = 50
bn = 10
sc = 0.5
sales = [14, 8, 17, 22, 12, 6]
r_end = 1

V_ = {}
def V(t, s):
    if (t, s) not in V_:
        if t == 6:
            V_[t, s] = (r_end * s, "finish")
        else:
            profit = 
            V_[t, s] = max()
    return V_[t, s]
        