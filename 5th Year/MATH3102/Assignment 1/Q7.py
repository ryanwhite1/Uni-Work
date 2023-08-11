# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:12:22 2023

@author: ryanw
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
    
def solution(x, eps):
    return 1 + (1 - 2**(-3/2)) * (np.exp(-3 * x / eps) - 1) + (2 - x)**(-3/2) - 2**(-3/2)

# y0 = [0, 1]

xs = np.linspace(0, 1, 500)
# ys = odeint(func, y0, xs)

eps = np.logspace(-5, 0, 6)

fig, ax = plt.subplots(figsize=(8, 4))
for ep in eps:
    ax.plot(xs, solution(xs, ep), label=f"$\epsilon = {ep}$")
ax.set_xlabel("$x$")
ax.set_ylabel("Solution")
ax.legend()
# ax.set_yscale('log')
# ax.set_xscale('log')

fig.savefig("Q7.png", dpi=400, bbox_inches='tight')