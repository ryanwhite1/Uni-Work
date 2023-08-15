# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 22:47:46 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family']='serif'
plt.rcParams['mathtext.fontset']='cm'

def dxdt(x, t, m, h):
    return x * (1 - x) + m - h * x

def equilibria(h, m):
    a = 0.5 * (1 - h)
    b = 0.5 * np.sqrt(1 - 2 * h + h**2 + 4 * m)
    return [a - b, a + b]

x0 = 1

ms = [-0.02, 0, 0.02]
times = np.linspace(0, 1500, 1500)
dt = times[1] - times[0]
hs = np.linspace(0, 1, 500)

fig, axes = plt.subplots(nrows=len(ms), sharex=True)
fig.subplots_adjust(hspace=0)

for i, m in enumerate(ms):
    # ys = np.ones((len(hs), len(times))) * x0
    # for j, h in enumerate(hs):
    #     for k in range(1, len(times)):
    #         x = ys[j, k - 1]
    #         ys[j, k] = x + dt * dxdt(x, 0, m, h)
    # for k in range(1000, 1500):
    #     lab = f"$m={m}$" if k == 1000 else ""
    #     axes[i].scatter(hs, ys[:, k], s=0.01, c='tab:blue', label=lab)
    top = [equilibria(h, m)[1] for h in hs]
    bottom = [equilibria(h, m)[0] for h in hs]
    axes[i].scatter(hs, top, s=0.1, c='tab:blue', label=f"$m={m}$")
    axes[i].scatter(hs, bottom, s=0.1, c='tab:blue')
    # axes[i].plot(ys[:, ])
    axes[i].legend()
    axes[i].set_ylim(-0.1, 1)
    axes[i].set_xlim(0, 1)

for i, ax in enumerate(axes):
    labels = ax.get_yticklabels()
    if i in [0, 1]:
        labels[0] = ""
    ax.set_yticklabels(labels)
            
        
axes[-1].set_xlabel("Harvest rate $h$")
axes[1].set_ylabel("Late time population")


# fig, ax = plt.subplots(figsize=(8, 5))

# times = np.linspace(0, 1500, 1500)

# pops = np.zeros((len(rs), len(times)))

# for i in range(len(rs)):
#     pops[i, 0] = x0


      
# for i in range(1000, 1500):
#     ax.scatter(rs, pops[:, i] / (rs * k), s=0.01, c='tab:blue')
# # ax.plot(rs, pops[:, 1000:1500])
    
# ax.set_xlabel("Proliferation Value, $r$")
# ax.set_ylabel("Late time population (prop. of $k$)")
fig.savefig('Q2e.png', dpi=400, bbox_inches='tight')
fig.savefig('Q2e.pdf', dpi=400, bbox_inches='tight')