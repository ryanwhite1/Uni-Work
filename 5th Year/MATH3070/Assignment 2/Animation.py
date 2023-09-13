# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 18:31:50 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib import animation

plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family']='serif'
plt.rcParams['mathtext.fontset']='cm'

fig, ax = plt.subplots(figsize=(9, 5))

def animate(alpha):
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
    
    ax.clear()
    # define our lists of desired initial conditions/colours
    x0 = [0, 0.1, 0.01, 1]
    y0 = [1.5, 0, 1, 0.8]
    colours = ['tab:purple', 'tab:blue', 'tab:red', 'tab:green']
    
    # define timespan that we simulate
    times = np.linspace(0, 120, 10000)
    # dt = times[1] - times[0]
    
    # create figure to plot the behaviour on
    
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
    ax.set_xlim(-0.1, 2.1)
    ax.set_ylim(-0.08, 2)
    ax.set_title(fr"$\alpha = {round(alpha, 3)}$, $\gamma = {gamma}$")
    
    print(np.argwhere(alphas == alpha).flatten()[0], "/", len(alphas))
    return fig,

# define some nice non-dimensionalised constants
alphas = np.linspace(0, 1.05, 200)
gamma = 2
beta = 1

ani = animation.FuncAnimation(fig, animate, frames=alphas, cache_frame_data=False, blit=True)
ani.save(f"animation.gif", writer='pillow', fps=15, dpi=400)
plt.close('all')






