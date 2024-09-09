# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 08:20:42 2024

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def potential(x):
    return x**2
def hermite(k, x):
    if k == 0:
        return 1
    elif k == 1:
        return 2 * x
    elif k == 2:
        return 4 * x**2 - 2
    elif k == 3:
        return 8 * x**3 - 12 * x 
    else:
        return np.inf
def analytic(k, x):
    return (1 / (np.sqrt(2**k * np.math.factorial(k) * np.sqrt(np.pi)))) * np.exp(-x**2 / 2) * hermite(k, x)
def sqrt_var(xs, us):
    return np.sqrt(np.sum(xs**2 * us) / np.sum(us))
def average_location(us, xs):
    return np.sum(xs * us) / np.sum(us)
def norm(us, dx):
    return dx * np.sum(us)


def schrodinger_scheme(us, xs, ts):
    
    all_us = np.zeros((len(xs), len(ts)), dtype=complex)
    all_us[:, 0] = us
    
    dt = ts[1] - ts[0]
    dx = xs[1] - xs[0]
    
    N = len(xs) - 2
    r = 1j * dt / dx**2
    ai = -r * np.ones(N - 1)
    bi = 2 + 1j * dt * potential(xs[1:-1]) + 2j * dt / dx**2
    ci = -r * np.ones(N - 1)
    A = np.diag(ai, -1) + np.diag(bi, 0) + np.diag(ci, 1)
    A_inv = np.linalg.inv(A)
    
    for t in tqdm(range(1, len(ts))):
        d = np.zeros(N, dtype=complex)
        for i in range(1, len(xs) - 1):
            d[i - 1] = (2 - 1j * dt * potential(xs[i]) - 2j * dt / dx**2) * all_us[i, t-1] + r * (all_us[i + 1, t-1] + all_us[i - 1, t-1])
        left_bound = 0; right_bound = 0;
        d[0] += r * left_bound
        d[-1] += r * right_bound
        
        temp = np.zeros(N + 2, dtype=complex)
        temp[1:N+1] = A_inv @ d
        all_us[:, t] = temp
    
    return all_us

xs = np.linspace(-20, 20, 2000)
dt = 0.0025
ts = np.arange(0, 10+dt, dt)
# ts = [0, dt]
# D = 0.05
# sigma = 0.3
# gamma = 2.
# centroid = -0.
# u_back = 0.
# us = np.exp(-0.5 * ((xs - centroid)/sigma)**2) + u_back
us = analytic(3, xs)
us[0] = 0; us[-1] = 0

# mode = 'FTCS'

gifname = 'Workshop8'

all_us = schrodinger_scheme(us, xs, ts)
all_us = np.abs(all_us)**2
# analytic_us = 

sqrt_vars = [sqrt_var(xs, all_us[:, i]) for i in range(len(all_us[0, :]))]
# analytic_sqrt_vars = [sqrt_var(xs, analytic_us[:, i]) for i in range(len(analytic_us[0, :]))]
norms = [norm(all_us[:, i], xs[1] - xs[0]) for i in range(len(all_us[0, :]))]
ave_locs = [average_location(all_us[:, i], xs) for i in range(len(all_us[0, :]))]

fig, ax = plt.subplots()
ax.plot(ts, sqrt_vars, label='Numerical')
# ax.plot(ts, analytic_sqrt_vars, label='Analytic')
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

every = 50

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