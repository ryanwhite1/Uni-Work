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

### --- Q1 h --- ###
# in this section we want to plot a phase portrait showing the 3 qualitative behaviours of the predator-prey model for some parameters

# define some nice non-dimensionalised constants
alpha = 0.4
gamma = 2
beta = 1

# define each of our non-dimensionalised predator/prey models
def dxdtau(x, y):
    timestep = x * (1 - x / gamma - y / (1 + x))
    return timestep
def dydtau(x, y):
    timestep = beta * y * (x / (1 + x) - alpha)
    return timestep

def non_dimen_pred_prey(t, z):
    # this is a function that interfaces the pred/prey models with the ivp solving function
    x, y = z
    return [dxdtau(x, y), dydtau(x, y)]

# define our lists of desired initial conditions/colours
x0 = [0, 0.1, 0.01, 1]
y0 = [1.5, 0, 1, 0.8]
colours = ['tab:purple', 'tab:blue', 'tab:red', 'tab:green']

# define timespan that we simulate
times = np.linspace(0, 100, 10000)
dt = times[1] - times[0]

# create figure to plot the behaviour on
fig, ax = plt.subplots(figsize=(9, 5))
ax.grid()
for i in range(len(x0)):
    ax.scatter(x0[i], y0[i], marker='x', c=colours[i])  # put a little cross at the starting location
    
    sol = solve_ivp(non_dimen_pred_prey, [0, max(times)], [x0[i], y0[i]], dense_output=True)    # solve the ivp for our initial state
    
    z = sol.sol(times)  # get the array of solutions for all times
    prey, preds = z
    
    ax.plot(prey, preds, label=f'$(x_0, y_0) = ({x0[i]}, {y0[i]})$', c=colours[i])  # now plot the pred/prey pops for all times

# define list of expected equilibria to plot
equilibria = [(0, 0), (gamma, 0), (alpha / (1 - alpha), (gamma - alpha / (1 - alpha)) / ((1 - alpha) * gamma))]
for i, equilibrium in enumerate(equilibria):
    x, y = equilibrium  # lets plot the location of each equilibrium
    label = 'Equilibrium' if i == 0 else None
    ax.scatter(x, y, marker='o', c='k', label=label)
ax.set_ylabel("Non-Dimensionalised Predator Population, $y$")
ax.set_xlabel("Non-Dimensionalised Prey Population, $x$")
ax.legend()

for extension in [".png", ".pdf"]: # now save the figure
    fig.savefig("PhasePortrait" + extension, dpi=400, bbox_inches='tight')
    
    
### --- Q1 i --- ###
# in this section we create a qualitative bifurcation diagram for the predator-prey system
# start by defining the domain of parameter values
a_vals = np.linspace(0, 2, 1000)
gammas = np.linspace(0, 3, 1000)
agam_mesh = np.zeros((len(a_vals), len(gammas)))    # initialise a matrix to store the stability case of each parameter pair

# now iterate over all combinations of parameter values
for i, a in enumerate(a_vals):
    for j, gam in enumerate(gammas):
        if (a > gam / (1 + gam)):   # pred extinct stable
            if (gam < 1 + 2 * a / (1 - a)) and (gam > a / (1 - a)):     # both stable
                agam_mesh[i, j] = 3
            else:   # only predator extinct is stable
                agam_mesh[i, j] = 1 
        elif (gam < 1 + 2 * a / (1 - a)) and (gam > a / (1 - a)):   # only coexistence stable
            agam_mesh[i, j] = 2
        else:   # neither of them are stable
            agam_mesh[i, j] = 0

        
        
# now want to plot the stability conditions, with some text in the relevant regions. 
fig, ax = plt.subplots(figsize=(8, 6))
img = ax.pcolormesh(a_vals, gammas, agam_mesh.T)
ax.set_xlabel(r"Non-dimensional Predator Mortality $\alpha$")
ax.set_ylabel(r"Non-dimensional Prey Carrying Capacity $\gamma$")
ax.text(1.05, 1.5, "Predator Extinction\nStable")
ax.text(0.1, 2.5, "Neither\nStable")
ax.text(0.25, 1.2, "Coexistence\nStable")
fig.colorbar(img, label='Type of Stable Equilibria')
for extension in [".png"]:
    fig.savefig("BifurcationDiagram" + extension, dpi=400, bbox_inches='tight')




