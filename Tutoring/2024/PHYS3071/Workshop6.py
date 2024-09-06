# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 08:40:21 2024

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

def average_location(us, xs):
    return np.sum(xs * us) / np.sum(us)
def norm(us, dx):
    return dx * np.sum(us)

def FTCS_step(u, v, dt, dx):
    new_u = u.copy()
    for i in range(1, len(u) - 1):
        new_u[i] = u[i] - (v * dt / (2 * dx)) * (u[i + 1] - u[i - 1])
    return new_u

def LF_step(u, v, dt, dx):
    new_u = u.copy()
    for i in range(1, len(u) - 1):
        new_u[i] = 0.5 * (u[i-1] + u[i+1]) - (v * dt / (2 * dx)) * (u[i + 1] - u[i - 1])
    return new_u

def transport_scheme(us, xs, ts, v, mode='FTCS'):
    
    all_us = np.zeros((len(xs), len(ts)))
    all_us[:, 0] = us
    
    dt = ts[1] - ts[0]
    dx = xs[1] - xs[0]
    
    for i in range(1, len(ts)):
        if mode == 'FTCS':
            all_us[:, i] = FTCS_step(all_us[:, i-1], v, dt, dx)
        elif mode == "LF":
            all_us[:, i] = LF_step(all_us[:, i-1], v, dt, dx)
    
    return all_us

xs = np.linspace(-1.5, 1.5, 300)
ts = np.arange(0, 4.04, 0.04)
v = 0.25
sigma = 0.1
centroid = -1.
us = np.exp(-((xs - centroid)/sigma)**2)
us[0] = 0; us[-1] = 0

all_us = transport_scheme(us, xs, ts, v, mode='LF')

norms = [norm(all_us[:, i], xs[1] - xs[0]) for i in range(len(all_us[0, :]))]
ave_locs = [average_location(all_us[:, i], xs) for i in range(len(all_us[0, :]))]

fig, ax = plt.subplots()
ax.plot(ts, norms)
ax.set(xlabel='Time', ylabel="Norm Value")

fig, ax = plt.subplots()
ax.plot(ts, ave_locs)
ax.set(xlabel='Time', ylabel='Average Position')


### Animation code below this line:

from matplotlib.animation import FuncAnimation

every = 1

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
ani.save("Workshop6-Stable.gif", fps=fps)   # save the animation to file with predetermined fps

plt.close(fig)


# ### Animation using movie.py --- GIVES ACCESS DENIED ERROR

# for i in range(len(ts)):
#     if i % 20 == 0:
#         print(i)
#     fig, ax = plt.subplots()
    
#     ax.plot(xs, all_us[:, i])
#     fig.savefig(f'ws6plot{i:04d}.png')
#     plt.close(fig)


# import imageio.v2 as imageio
# import glob as glob
# # import subprocess

# images = []
# frames = []

# # frames = subprocess.getoutput('find . -name "*png" | sort -k1 ')
# # frames = frames.split('\n')

# frames = glob.glob("*.png")

# for filename in frames:
#     images.append(imageio.imread(filename))

# imageio.mimsave('animation.gif', images)




