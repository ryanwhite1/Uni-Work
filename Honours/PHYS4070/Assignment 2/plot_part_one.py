import numpy as np
import matplotlib.pyplot as plt

part_11_data = np.genfromtxt("part1_1.txt", delimiter='\t')

data_shape = part_11_data.shape

moon_indices = np.arange(0, data_shape[0], 3) + 1
moon_data = part_11_data[moon_indices, :]

proj_inds = np.arange(0, data_shape[0], 3) + 2
proj_data = part_11_data[proj_inds, :]

fig, ax = plt.subplots()

ax.plot(moon_data[:, 0], moon_data[:, 1], rasterized=True, label='Moon Trajectory')
ax.plot(proj_data[:, 0], proj_data[:, 1], rasterized=True, label='Projectile Trajectory')
ax.set(aspect='equal', xlabel='$x$ (non-dim units)', ylabel='$y$ (non-dim units)')
ax.legend()

fig.savefig('Part_1_12e_Trajectories.png', dpi=400, bbox_inches='tight')
fig.savefig('Part_1_12e_Trajectories.pdf', dpi=400, bbox_inches='tight')

fig, ax = plt.subplots()
dist = np.sqrt((moon_data[:, 0] - proj_data[:, 0])**2 + (moon_data[:, 1] - proj_data[:, 1])**2)
min_index = np.where(dist == min(dist))[0][0]
min_time = moon_data[min_index, -1]

ax.plot(moon_data[:, -1], dist, rasterized=True)
ax.axvline(min_time, c='tab:purple', label=f'$t$ at min sep. = {np.round(min_time, 1)}')
ax.set(xlabel='Time (non-dim units)', ylabel='Projectile-Moon Separation (non-dim units)', ybound=(0, None))
ax.legend()
fig.savefig('Part_1_12d_Distances.png', dpi=400, bbox_inches='tight')
fig.savefig('Part_1_12d_Distances.pdf', dpi=400, bbox_inches='tight')





part_123_data = np.genfromtxt("part1_23.txt", delimiter='\t')

data_shape = part_123_data.shape
moon_indices = np.arange(0, data_shape[0], 3) + 1
moon_data = part_123_data[moon_indices, :]

proj_inds = np.arange(0, data_shape[0], 3) + 2
proj_data = part_123_data[proj_inds, :]

fig, ax = plt.subplots()

ax.plot(moon_data[:, 0], moon_data[:, 1], rasterized=True, label='Moon Trajectory')
ax.plot(proj_data[:, 0], proj_data[:, 1], rasterized=True, label='Projectile Trajectory')
ax.set(aspect='equal', xlabel='$x$ (non-dim units)', ylabel='$y$ (non-dim units)', 
       xlim=(-1, 1.2 * max(moon_data[:, 0])), ybound=(1.2 * min(moon_data[:, 1]), None))
ax.legend()

fig.savefig('Part_1_23_Trajectories.png', dpi=400, bbox_inches='tight')
fig.savefig('Part_1_23_Trajectories.pdf', dpi=400, bbox_inches='tight')

fig, ax = plt.subplots()
dist = np.sqrt((moon_data[:, 0] - proj_data[:, 0])**2 + (moon_data[:, 1] - proj_data[:, 1])**2)
min_index = np.where(dist == min(dist))[0][0]
rmp = 0.5
rmp_index = np.where(np.round(dist, 2) == np.round(rmp, 2))[0][0]
min_time = moon_data[min_index, -1]
rmp_time = moon_data[rmp_index, -1]

ax.plot(moon_data[:, -1], dist, rasterized=True)
ax.axvline(min_time, c='tab:purple', lw=1, label=f'$t$ at min sep. = {np.round(min_time, 1)}')
ax.axvline(rmp_time, c='tab:red', ls='--', lw=1, label=f'$t$ at $r_{{mp}}$ = {np.round(rmp_time, 1)}')
ax.set(xlabel='Time (non-dim units)', ylabel='Projectile-Moon Separation (non-dim units)', ylim=(0, 50), xlim=(0, 80))
ax.legend()

fig.savefig('Part_1_24_Distances.png', dpi=400, bbox_inches='tight')
fig.savefig('Part_1_24_Distances.pdf', dpi=400, bbox_inches='tight')





part_126_data = np.genfromtxt("part1_26.txt", delimiter='\t')

data_shape = part_126_data.shape
moon_indices = np.arange(0, data_shape[0], 3) + 1
moon_data = part_126_data[moon_indices, :]

proj_inds = np.arange(0, data_shape[0], 3) + 2
proj_data = part_126_data[proj_inds, :]

fig, ax = plt.subplots()

ax.plot(moon_data[:, 0], moon_data[:, 1], rasterized=True, label='Moon Trajectory')
ax.plot(proj_data[:, 0], proj_data[:, 1], rasterized=True, label='Projectile Trajectory')
ax.set(aspect='equal', xlabel='$x$ (non-dim units)', ylabel='$y$ (non-dim units)')
ax.legend()

fig.savefig('Part_1_26_Trajectories.png', dpi=400, bbox_inches='tight')
fig.savefig('Part_1_26_Trajectories.pdf', dpi=400, bbox_inches='tight')

fig, ax = plt.subplots()
ax.plot(proj_data[:, 0] - moon_data[:, 0], proj_data[:, 1] - moon_data[:, 1], rasterized=True, label='Projectile\nTrajectory')
ax.set(aspect='equal', xlabel='$x$ (non-dim units)', ylabel='$y$ (non-dim units)')
ax.legend()

fig.savefig('Part_1_26_Trajectories(Moon-Centered).png', dpi=400, bbox_inches='tight')
fig.savefig('Part_1_26_Trajectories(Moon-Centered).pdf', dpi=400, bbox_inches='tight')