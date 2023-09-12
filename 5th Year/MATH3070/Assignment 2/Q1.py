# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 20:38:46 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family']='serif'
plt.rcParams['mathtext.fontset']='cm'

# ### --- Q1 h --- ###

# # define some nice non-dimensionalised constants
# alpha = 0.3
# gamma = 2
# beta = 1

# def dxdtau(x, y):
#     timestep = x * (1 - x / gamma - y / (1 + x))
#     return timestep
# def dydtau(x, y):
#     timestep = beta * y * (x / (1 + x) - alpha)
#     return timestep

# def non_dimen_pred_prey(t, z):
#     x, y = z
#     return [dxdtau(x, y), dydtau(x, y)]

# x0 = [0, 0.1, 0.01, 1]
# y0 = [1.5, 0, 1, 0.8]
# colours = ['tab:purple', 'tab:blue', 'tab:red', 'tab:green']

# times = np.linspace(0, 100, 10000)
# dt = times[1] - times[0]

# fig, ax = plt.subplots(figsize=(9, 5))
# ax.grid()
# for i in range(len(x0)):
#     ax.scatter(x0[i], y0[i], marker='x', c=colours[i])
    
#     sol = solve_ivp(non_dimen_pred_prey, [0, max(times)], [x0[i], y0[i]], dense_output=True)
    
#     z = sol.sol(times)
#     prey, preds = z
    
#     ax.plot(prey, preds, label=f'$(x_0, y_0) = ({x0[i]}, {y0[i]})$', c=colours[i])

# equilibria = [(0, 0), (gamma, 0), (alpha / (1 - alpha), (gamma - alpha / (1 - alpha)) / ((1 - alpha) * gamma))]
# for i, equilibrium in enumerate(equilibria):
#     x, y = equilibrium
#     label = 'Equilibrium' if i == 0 else None
#     ax.scatter(x, y, marker='o', c='k', label=label)
# ax.set_ylabel("Non-Dimensionalised Predator Population, $y$")
# ax.set_xlabel("Non-Dimensionalised Prey Population, $x$")
# ax.legend()

# for extension in [".png", ".pdf"]:
#     fig.savefig("PhasePortrait" + extension, dpi=400, bbox_inches='tight')
    
    
### --- Q1 i --- ###
a_vals = np.linspace(0, 2, 1000)
gammas = np.linspace(0, 3, 1000)
agam_mesh = np.zeros((len(a_vals), len(gammas)))

for i, a in enumerate(a_vals):
    for j, gam in enumerate(gammas):
        # # print(gam / (1 + gam))
        # if a > (gam / (1 + gam)):   # (gamma, 0) stable
        #     if gam > (a / (1 - a)): # coexistence stable
        #         if a > 1:
        #             val = 6
        #         else:
        #             val = 1
        #     else:
        #         val = 3 
            
        # elif gam > (a / (1 - a)):
        #     # if a < 1:
        #     #     val = 4
        #     # else:
        #     #     val = 5
        #     val = 2
        # else: 
        #     val = 0
        # agam_mesh[i, j] = val
        
        if (a > 1) and (a < gam / (1 + gam)):
            agam_mesh[i, j] = 0
        elif (gam > a / (1 - a)) and (a < 1): # coexistence!
            if (a > gam / (1 + gam)):   # predator extinct
                agam_mesh[i, j] = 1
            else:
                agam_mesh[i, j] = 2
        elif (a > gam / (1 + gam)): # only predator extinct
            agam_mesh[i, j] = 3
        else:
            agam_mesh[i, j] = 0

        
        
        
fig, ax = plt.subplots(figsize=(8, 6))
img = ax.pcolormesh(a_vals, gammas, agam_mesh.T)
ax.set_xlabel(r"Non-dimensional Predator Mortality $\alpha$")
ax.set_ylabel(r"Non-dimensional Prey Carrying Capacity $\gamma$")
ax.text(1, 1.5, "Predator Extinction\nStable")
# ax.text(0.75, 2.5, "Both\nExtinction")
# ax.text(0.5, 0.6, "Both Stable")
ax.text(0.2, 2, "Coexistence\nand Predator\nExtinction\nStable")
fig.colorbar(img, label='Type of Stable Equilibria')
for extension in [".png"]:
    fig.savefig("BifurcationDiagram" + extension, dpi=400, bbox_inches='tight')




