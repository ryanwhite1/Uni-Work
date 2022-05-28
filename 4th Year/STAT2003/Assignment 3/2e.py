# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:31:13 2022

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

rho = 0.75
prob = 1 - rho
lam = 1

U = np.random.uniform(0, 1, 50)
V = np.random.exponential(lam, 50)
W = np.zeros(len(V))
X = np.zeros(len(V) + 1)
X[0] = np.random.exponential(lam)

number = np.arange(0, 50)

for num in number:
    if U[num] <= prob:
        W[num] = V[num - 1] 
    else:
        W[num] = 0

for i in range(1, 51):
    X[i] = rho * X[i - 1] + W[i - 1]

plt.scatter(np.arange(0, 51), X)
plt.xlabel("Iteration $n$"); plt.ylabel("Value of $X_n$")
plt.xlim(xmin=0); plt.ylim(bottom=0)
plt.savefig("q2e.png", dpi=200, bbox_inches='tight', pad_inches = 0.01)
