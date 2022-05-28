# -*- coding: utf-8 -*-
"""
Created on Thu May 26 12:02:29 2022

@author: ryanw
"""
import numpy as np
import matplotlib.pyplot as plt

x1 = np.random.uniform(0, 1, 50000)
x2 = np.random.uniform(0, 1, 50000)

x1 = 2**(x1 - 1)
x2 = 2**(x2 - 1)

z1 = x1 * x2
z2 = x1

plt.scatter(z2, z1)
plt.ylabel("$Y = Z_1 = X_1 X_2$"); plt.xlabel("$Z_2 = X_1$")
plt.savefig("1aInverseTransform.png")