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

gas_ = {}
def gas(t, s):
    if (t, s) not in gas_:
        if t == 14:
            gas_[t, s] = (0, 'finish')
        else:
            gas_[t, s] = max([(min(demand[t], s + n) * r - min(n, 1) * deliv_cost(n) + 
                               gas(t + 1, s + n - min(demand[t], s + n))[0], n, s + n - min(demand[t], s + n)) for n in range(0, cap - s + demand[t] + 1)])
    return gas_[t, s]

import numpy as np
import matplotlib.pyplot as plt

vals = np.zeros((14, 3))
for i in range(14):
    if i == 0:
        vals[i, :] = gas(0, 0)
    else:
        vals[i, :] = gas(i, vals[i - 1, 2])

fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(np.arange(0, 14, 1), vals[:, 1])
ax.set_xlim(0, 14)
ax.set_ylim(ymin=0)
ax.set_xlabel("Day")
ax.grid()
ax.set_ylabel("Number of Gas Cylinders to Order")

ax2 = ax.twinx()
ax2.plot(np.arange(0, 14, 1), vals[:, 0], c='tab:red')
ax2.set_ylim(ymin=0)
ax2.set_ylabel("Total Profit made in remaining days ($)")
    
fig.savefig('Comm11.png', bbox_inches='tight', dpi=300)
plt.close('all')