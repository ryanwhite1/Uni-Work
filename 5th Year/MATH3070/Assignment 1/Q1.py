# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 22:47:46 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family']='serif'
plt.rcParams['mathtext.fontset']='cm'



### Q1d ###
def model(x, k, r):
    return r * x * np.exp(- np.log(r) * x / k)

# initialise variables and parameters of interest
x0 = 0.1
k = 1
rs = np.linspace(0.001, 35, 500)

fig, ax = plt.subplots(figsize=(8, 5))

times = np.linspace(0, 1500, 1500)

pops = np.zeros((len(rs), len(times)))

pops[:, 0] = x0

for i, r in enumerate(rs):
    for j, t in enumerate(times):
        if j != 0:
            pops[i, j] = model(pops[i, j - 1], k, r) # calculate population for this time, based on the previous time population
      
for i in range(1000, 1500):
    ax.scatter(rs, pops[:, i] / k, s=0.01, c='tab:blue') # plot the late time pops as single markers
    
ax.set_xlabel("Proliferation Value, $r$")
ax.set_ylabel("Late time population (prop. of $k$)")
fig.savefig('Q1d.png', dpi=400, bbox_inches='tight')
fig.savefig('Q1d.pdf', dpi=400, bbox_inches='tight')


### Q1e ###
# analogous to 1d code above
def modelH(x, k, r):
    if x < k / r:
        return r * x
    if x >= k / r:
        return k

x0 = 0.1
k = 1
rs = np.linspace(0.001, 35, 500)

fig, ax = plt.subplots(figsize=(8, 5))

times = np.linspace(0, 1500, 1500)

pops = np.zeros((len(rs), len(times)))

pops[:, 0] = x0

for i, r in enumerate(rs):
    for j, t in enumerate(times):
        if j != 0:
            pops[i, j] = modelH(pops[i, j - 1], k, r)
      
for i in range(1000, 1500):
    ax.scatter(rs, pops[:, i] / k, s=0.01, c='tab:blue')
    
ax.set_xlabel("Proliferation Value, $r$")
ax.set_ylabel("Late time population (prop. of $k$)")
fig.savefig('Q1e.png', dpi=400, bbox_inches='tight')
fig.savefig('Q1e.pdf', dpi=400, bbox_inches='tight')



### Q1g ###

from scipy.optimize import brentq # bisection function in python

def rx_deriv_root(s, r, k):
    # corresponds to R'(S) - 1 = 0
    return r * np.exp(-np.log(r) * s / k) * (1 - np.log(r) * s / k) - 1 
k = 1
r = 2

root = brentq(rx_deriv_root, 0.0001, k, args=(r, k)) # find the root
print(f"Q1g root is S = {root}")


### Q1h ###

rs = np.linspace(1, 3, 1000)
k = 1 

R_escape = np.zeros(len(rs))
H_escape = k / rs # can just calculate the escapement for H

for i, r in enumerate(rs):
    R_escape[i] = brentq(rx_deriv_root, 0.0001, k, args=(r, k)) # find the root for this proliferation

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(rs, H_escape, ls='--', c='k', label='$H(X_t - h_t)$')
ax.plot(rs, R_escape, c='tab:red', label='$R(X_t - h_t)$')
ax.legend()
ax.set_xlabel("Proliferation, $r$")
ax.set_ylabel("Optimal Escapement (prop. of $k$), $S$")

fig.savefig('Q1h.png', dpi=400, bbox_inches='tight')
fig.savefig('Q1h.pdf', dpi=400, bbox_inches='tight')