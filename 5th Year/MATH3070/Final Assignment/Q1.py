# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 10:04:23 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family']='serif'
plt.rcParams['mathtext.fontset']='cm'

r = 2
k = 100
def function(x, phi):
    return x + (r - 1) * x * (1 - (x / k)**phi)

x = np.linspace(0, 150, 1000)

fig, ax = plt.subplots(figsize=(5, 4))
for phi in [0.5, 1, 2]:
    ax.plot(x, function(x, phi), label=f"$\phi = {phi}$")
ax.plot(x, x, ls=':', c='k', alpha=0.5)
ax.legend()
ax.set(ylabel="$x_{t+1}$", xlabel="$x_t$")
fig.savefig("Q1a.pdf", bbox_inches='tight', dpi=400)