# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:12:22 2023

@author: ryanw
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

eps = 0.05
def func(u, t):
    y, ydash = u
    return (ydash, -ydash - (1 + eps * y)**-2)
    
def oneterm(t):
    return -2 * np.exp(-t) - t + 2
def twoterm(t):
    return oneterm(t) + eps * (np.exp(-t) * (-np.exp(t) * (t - 3)**2 + 4 * t + 9))

y0 = [0, 1]

xs = np.linspace(0, 2, 200)
ys = odeint(func, y0, xs)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(xs, ys[:, 0], label='Numerical Solution')
ax.plot(xs, oneterm(xs), label="1 Term")
ax.plot(xs, twoterm(xs), label="2 Term")
ax.set_xlabel("Time")
ax.set_ylabel("Height")
ax.legend()
# ax.set_xscale('log')

fig.savefig("Q5.png", dpi=400, bbox_inches='tight')