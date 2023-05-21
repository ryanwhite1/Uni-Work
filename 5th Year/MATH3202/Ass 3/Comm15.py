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
    return min(cap, s + n - min(demand[t], s + n))

def high_step(t, s, L, n, N):
    ''' Performs one high demand small cylinder inventory time step 
    '''
    return s + n - min(high_demand[t], s + n)

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
    if (t, s, L) not in gas_:
        if t == 14:
            gas_[t, s, L] = (0, 'finish')
        else:
            gas_[t, s, L] = max([(profit(t, s, L, n, N) + 
                                  p * gas(t + 1, high_step(t, s, L, n - 2 * deficit(t, L, N), N), large_step(t, L, N))[0] +
                                  (1 - p) * gas(t + 1, small_step(t, s, L, n - 2 * deficit(t, L, N), N), large_step(t, L, N))[0], 
                                  [n, N, p * high_step(t, s, L, n - 2 * deficit(t, L, N), N) + (1 - p) * small_step(t, s, L, n - 2 * deficit(t, L, N), N), large_step(t, L, N)]) \
                                  for N in range(0, min(large_cap - L + large_demand[t], Dcap // Mcyl_L) + 1) \
                                  for n in range(0, min(cap - s + high_demand[t] + 2 * deficit(t, L, N), (Dcap - N * Mcyl_L) // Mcyl) + 1)
                                  ])
    return gas_[t, s, L]
    
print(gas(0, 0, 0))

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))

vals = np.zeros((14, 4))
money = np.zeros(14)
for i in range(14):
    if i == 0:
        money[i], vals[i, :] = gas(0, 0, 0)
    else:
        s = int(vals[i - 1, 2]); ps = vals[i - 1, 2] - s
        L = int(vals[i - 1, 3])
        money[i] = ps * gas(i, s + 1, L)[0] + (1 - ps) * gas(i, s, L)[0]
        vals[i, :] = ps * np.array(gas(i, s + 1, L)[1]) + (1 - ps) * np.array(gas(i, s, L)[1])
        
ax.scatter(np.arange(0, 14, 1), vals[:, 0], c='tab:blue', label="Small Cylinders")
ax.scatter(np.arange(0, 14, 1), vals[:, 1], c='tab:purple', label="Large Cylinders")
ax.set_xlim(0, 14)
ax.set_ylim(ymin=0)
ax.set_xlabel("Day")
ax.grid()
ax.legend()
ax.set_ylabel("Expected Number of Gas Cylinders to Order")

ax2 = ax.twinx()
for j in range(100):
    store = np.zeros((14, 4))
    money = np.zeros(14)
    
    for i in range(14):
        if i == 0:
            money[i], store[i, :] = gas(0, 0, 0)
        else:
            s = int(store[i - 1, 2]); ps = store[i - 1, 2] - s
            L = int(store[i - 1, 3]); pL = store[i - 1, 3] - L
            if np.random.uniform(0, 1) < ps:
                if np.random.uniform(0, 1) < pL:
                    money[i], store[i, :] = gas(i, s + 1, L + 1)
                else:
                    money[i], store[i, :] = gas(i, s + 1, L)
            else:
                if np.random.uniform(0, 1) < pL:
                    money[i], store[i, :] = gas(i, s, L + 1)
                else:
                    money[i], store[i, :] = gas(i, s, L)
    ax2.plot(np.arange(0, 14, 1), money, c='tab:red', alpha=1/25)
# ax.set_xlabel("Day")
# ax.set_xlim(0, 14)
# ax.grid()
ax2.set_ylim(ymin=0)
ax2.set_ylabel("Expected Profit From Remaining Days ($)")
fig.savefig("Comm15Expected Profit.png", bbox_inches='tight', dpi=300)

plt.close('all')
