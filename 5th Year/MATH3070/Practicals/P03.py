# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 13:03:31 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


def model(x, t, h):
    return x * (1 - x) * (x - 0.5) - h * x

times = np.linspace(0, 10, 50)
x0 = [0, 0.1, 0.4, 0.5, 0.6, 0.9, 1]
fig, axes = plt.subplots(figsize=(8, 15), nrows=3, sharex=True)

for i, h in enumerate([0, 0.05, 0.1]):
    for X in x0[::-1]:
        ys = odeint(model, X, times, args=(h,))
        axes[i].plot(times, ys, label=f'x0={X}')
        axes[i].set_title(f"h = {h}")
    axes[i].legend(loc='center right')

axes[-1].set_xlim(0, 13)
axes[-1].set_xlabel("Times")
axes[1].set_ylabel("Population (prop of K)")


fig, ax = plt.subplots()

hs = np.linspace(0, 0.1, 100)
yields = np.zeros(len(hs))

for i, h in enumerate(hs):
    yields[i] = h * odeint(model, 0.99, np.linspace(0, 1000, 200), args=(h,))[-1]

ax.plot(hs, yields)
arg = np.argmax(yields)
print(f"maximum yield equilibrium population = {yields[arg] / hs[arg]}\n maximum harvest = {hs[arg]}")
    