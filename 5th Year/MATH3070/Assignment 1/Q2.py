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

def equilibria(h, m):
    # returns each equilibrium for a given h and m 
    a = 0.5 * (1 - h)
    b = 0.5 * np.sqrt(1 - 2 * h + h**2 + 4 * m)
    return [a - b, a + b]

ms = [-0.02, 0, 0.02] # m parameters of interest
times = np.linspace(0, 1500, 1500) 
hs = np.linspace(0, 1, 500)

fig, axes = plt.subplots(nrows=len(ms), sharex=True)
fig.subplots_adjust(hspace=0)

for i, m in enumerate(ms):
    top = [equilibria(h, m)[1] for h in hs] # get top equilibria
    bottom = [equilibria(h, m)[0] for h in hs] # get bottom equilibria 
    # now plot each of them as a point on the plot
    axes[i].scatter(hs, top, s=0.1, c='tab:blue', label=f"$m={m}$")
    axes[i].scatter(hs, bottom, s=0.1, c='tab:blue')
    axes[i].legend()
    axes[i].set_ylim(-0.25, 1)
    axes[i].set_xlim(0, 1)

# now play around with the labels a bit to make it pretty
for i, ax in enumerate(axes):
    labels = ax.get_yticklabels()
    if i in [0, 1]:
        labels[0] = ""
    ax.set_yticklabels(labels)
            
        
axes[-1].set_xlabel("Harvest rate $h$")
axes[1].set_ylabel("Late time population")

fig.savefig('Q2e.png', dpi=400, bbox_inches='tight')
fig.savefig('Q2e.pdf', dpi=400, bbox_inches='tight')