# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 16:34:41 2023

@author: ryanw
"""

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt


def func(x, eps):
    return np.sin(x + eps) - x
def prime(x, eps):
    return 4 * eps * x**3 - 1
    
def solone(eps):
    return eps**(1/3) * np.cbrt(6) - eps

eps = np.logspace(-5, 0, 50)
# xs = np.linspace(0, 2, 200)
ys = np.zeros(len(eps))
for i, ep in enumerate(eps):
    # roots = opt.brentq(func, -2, ep**(-1/3), args=(ep,))
    ys[i] = opt.fsolve(func, -4, args=(ep,))
    # print(roots)
    # ys[i] = 

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(eps, ys, c='tab:blue', label='Numerical Solution')
ax.plot(eps, solone(eps), c='tab:red', label="Asymptotic Sol")
ax.set_xlabel("Epsilon")
ax.set_ylabel("First Solution")
ax.legend()
ax.set_xscale('log')
ax.set_yscale('log')
# ax.set_yscale('log')
# ax.set_xscale('log')

fig.savefig("Q3.png", dpi=400, bbox_inches='tight')