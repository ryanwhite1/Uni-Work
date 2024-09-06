# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 08:20:42 2024

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

def analytic(xs, t, sigma, D, gamma, u_back):
    return (1/np.sqrt(2 * np.pi * (sigma**2 + gamma * D * t))) * np.exp(-0.5 * xs**2 / (sigma**2 + gamma * D * t)) + u_back
def sqrt_var(xs, us):
    return np.sqrt(np.sum(xs**2 * us) / np.sum(us))
def average_location(us, xs):
    return np.sum(xs * us) / np.sum(us)
def norm(us, dx):
    return dx * np.sum(us)


def FTCS_step(u, D, dt, dx):
    new_u = u.copy()
    for i in range(1, len(u) - 1):
        new_u[i] = u[i] + (D * dt / dx**2) * (u[i + 1] - 2 * u[i] + u[i - 1])
    return new_u

def diffusion_scheme(us, xs, ts, D, mode='FTCS'):
    
    all_us = np.zeros((len(xs), len(ts)))
    all_us[:, 0] = us
    
    dt = ts[1] - ts[0]
    dx = xs[1] - xs[0]
    
    if mode == 'FTCS':
        for i in range(1, len(ts)):
            all_us[:, i] = FTCS_step(all_us[:, i-1], D, dt, dx)
    elif mode == 'Crank-Nicolson':
        N = len(xs) - 2
        r = D * dt / dx**2
        ai = -r * np.ones(N - 1)
        bi = 2 * (1 + r) * np.ones(N)
        ci = -r * np.ones(N - 1)
        A = np.diag(ai, -1) + np.diag(bi, 0) + np.diag(ci, 1)
        A_inv = np.linalg.inv(A)
        
        for t in range(1, len(ts)):
            d = np.zeros(N)
            for i in range(1, len(xs) - 1):
                d[i - 1] = 2 * (1 - r) * all_us[i, t-1] + r * (all_us[i + 1, t-1] + all_us[i - 1, t-1])
            left_bound = 0; right_bound = 0;
            d[0] += r * left_bound
            d[-1] += r * right_bound
            
            temp = np.zeros(N + 2)
            temp[1:N+1] = A_inv @ d
            all_us[:, t] = temp
    
    return all_us

xs = np.linspace(-3, 3, 100)
dt = 0.005
ts = np.arange(0, 7+dt, dt)
# ts = [0, dt]
D = 0.05
sigma = 0.3
gamma = 2.
centroid = -0.
u_back = 0.
us = np.exp(-0.5 * ((xs - centroid)/sigma)**2) + u_back
us[0] = 0; us[-1] = 0

# mode = 'FTCS'
mode = 'Crank-Nicolson'

gifname = 'Workshop7-UnStable' if mode == 'FTCS' else 'Workshop7-Stable'

all_us = diffusion_scheme(us, xs, ts, D, mode=mode)
analytic_us = np.array([analytic(xs, t, sigma, D, gamma, u_back) for t in ts]).T

sqrt_vars = [sqrt_var(xs, all_us[:, i]) for i in range(len(all_us[0, :]))]
analytic_sqrt_vars = [sqrt_var(xs, analytic_us[:, i]) for i in range(len(analytic_us[0, :]))]
norms = [norm(all_us[:, i], xs[1] - xs[0]) for i in range(len(all_us[0, :]))]
ave_locs = [average_location(all_us[:, i], xs) for i in range(len(all_us[0, :]))]

fig, ax = plt.subplots()
ax.plot(ts, sqrt_vars, label='Numerical')
ax.plot(ts, analytic_sqrt_vars, label='Analytic')
ax.set(xlabel='Time', ylabel="Standard Deviation")
ax.legend()

fig, ax = plt.subplots()
ax.plot(ts, norms)
ax.set(xlabel='Time', ylabel="Norm Value")

fig, ax = plt.subplots()
ax.plot(ts, ave_locs)
ax.set(xlabel='Time', ylabel='Average Position')


### Animation code below this line:

from matplotlib.animation import FuncAnimation

every = 10

fig, ax = plt.subplots()
line = ax.plot(xs, all_us[:, 0])    # plot the initial wavefunction at timestep 0

length = 4 # seconds
fps = len(ts[::every]) / length

def animate(i):
    if i % 20 == 0:
        print(i)
    line[0].set_ydata(all_us[:, i]) # replace the existing data on the figure with the wavefunction at timestep i
    return fig,

ani = FuncAnimation(fig, animate, frames=np.arange(len(all_us[0, :]))[::every])  # animate the wavefunction evolution
ani.save(f"{gifname}.gif", fps=fps)   # save the animation to file with predetermined fps

plt.close(fig)