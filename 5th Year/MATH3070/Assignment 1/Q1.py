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

def model(x, k, r):
    return r * x * np.exp(- x/k)

x0 = 1
k = 1
rs = np.linspace(0, 35, 500)

fig, ax = plt.subplots(figsize=(8, 5))

times = np.linspace(0, 1500, 1500)

pops = np.zeros((len(rs), len(times)))

pops[:, 0] = x0

for i, r in enumerate(rs):
    for j, t in enumerate(times):
        if j != 0:
            pops[i, j] = model(pops[i, j - 1], k, r)
      
for i in range(1000, 1500):
    ax.scatter(rs, pops[:, i], s=0.01, c='tab:blue')
# ax.plot(rs, pops[:, 1000:1500])
    
ax.set_xlabel("Proliferation Value, $r$")
ax.set_ylabel("Late time population (prop. of $k$)")
fig.savefig('Q1d.png', dpi=400, bbox_inches='tight')
fig.savefig('Q1d.pdf', dpi=400, bbox_inches='tight')