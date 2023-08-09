# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:12:22 2023

@author: ryanw
"""

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

def func(x, eps):
    return eps * x**4 - x - 1
def prime(x, eps):
    return 4 * eps * x**3 - 1
    
def solone(eps):
    return -1
def soltwo(eps):
    return eps**(-1/3) + 1/3

y0 = [0, 1]

eps = np.logspace(-5, 0, 50)
# xs = np.linspace(0, 2, 200)
ys = np.zeros((len(eps), 2))
for i, ep in enumerate(eps):
    # roots = opt.brentq(func, -2, ep**(-1/3), args=(ep,))
    ys[i, 0] = opt.fsolve(func, -1, fprime=prime, args=(ep,))
    ys[i, 1] = opt.fsolve(func, 1/3 + ep**(-1/3), fprime=prime, args=(ep,))
    # print(roots)
    # ys[i] = 

fig, ax = plt.subplots(figsize=(8, 4), nrows=2, sharex=True)
fig.subplots_adjust(hspace=0)
ax1, ax2 = ax
ax1.plot(eps, ys[:, 0], c='tab:blue', label='Numerical Solution')
ax2.plot(eps, ys[:, 1], c='tab:blue')
ax1.plot(eps, len(eps) * [-1], c='tab:red', label="First Sol")
ax2.plot(eps, soltwo(eps), c='tab:green', label="Second Sol")
ax2.set_xlabel("Epsilon")
ax1.set_ylabel("First Solution")
ax2.set_ylabel("First Solution")
ax1.legend()
ax2.legend()
ax1.set_xscale('log')
ax2.set_yscale('log')
# ax.set_yscale('log')
# ax.set_xscale('log')

fig.savefig("Q6.png", dpi=400, bbox_inches='tight')







