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
                               gas_stoc(t, s, n), [n, p * (s + n - min(high_demand[t], s + n)) + (1 - p) *  min(cap, s + n - min(demand[t], s + n))]) for n in range(0, min(cap - s + high_demand[t], Ncyl) + 1)])
    return gas_[t, s]

def gas_stoc(t, s, n):
    return p * gas(t + 1, s + n - min(high_demand[t], s + n))[0] + (1 - p) * gas(t + 1, min(cap, s + n - min(demand[t], s + n)))[0]

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))

# fig, ax = plt.subplots(figsize=(8, 6))
vals = np.zeros((14, 2))
money = np.zeros(14)
for i in range(14):
    if i == 0:
        money[i], vals[i, :] = gas(0, 0)
    else:
        s = int(vals[i - 1, 1]); ps = vals[i - 1, 1] - s
        money[i] = ps * gas(i, s + 1)[0] + (1 - ps) * gas(i, s)[0]
        vals[i, :] = ps * np.array(gas(i, s + 1)[1]) + (1 - ps) * np.array(gas(i, s)[1])
        
ax.scatter(np.arange(0, 14, 1), vals[:, 0])
ax.set_xlim(0, 14)
ax.set_ylim(ymin=0)
ax.set_xlabel("Day")
ax.grid()
ax.set_ylabel("Expected Number of Gas Cylinders to Order")

ax2 = ax.twinx()
for j in range(100):
    store = np.zeros((14, 2))
    money = np.zeros(14)
    
    for i in range(14):
        if i == 0:
            money[i], store[i, :] = gas(0, 0)
        else:
            s = int(store[i - 1, 1]); ps = store[i - 1, 1] - s
            if np.random.uniform(0, 1) < ps:
                money[i], store[i, :] = gas(i, s + 1)
            else:
                money[i], store[i, :] = gas(i, s)
    ax2.plot(np.arange(0, 14, 1), money, c='tab:red', alpha=1/25)
# ax.set_xlabel("Day")
# ax.set_xlim(0, 14)
# ax.grid()
ax2.set_ylim(ymin=0)
ax2.set_ylabel("Expected Profit From Remaining Days ($)")
fig.savefig("Comm13Expected Profit.png", bbox_inches='tight', dpi=300)

plt.close('all')

