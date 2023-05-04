# -*- coding: utf-8 -*-
"""
Created on Wed May  3 13:40:51 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family']='serif'
plt.rcParams['mathtext.fontset']='cm'

fs = 3.568 # figure size, inches

fig, ax = plt.subplots(figsize=(fs, 72/96 * fs))
fig.tight_layout()

frames = 18
fps = 4

def animate(i):
    print(i)
    ax.clear()
    image = plt.imread(f"Few Mode/{i+1}.jpg")
    ax.imshow(image)
    ax.set_aspect('equal')
    ax.set_xlabel("Horizontal Pixel")
    ax.set_ylabel("Vertical Pixel")
    
    return fig,

ani = animation.FuncAnimation(fig, animate, frames=frames, interval=int(1000/fps))


plt.show()

ani.save(f'Few Mode/Animation.gif', writer='pillow')

plt.close('all')
