import numpy as np
import matplotlib.pyplot as plt

part_11_data = np.genfromtxt("part1_1.txt", delimiter='\t')

data_shape = part_11_data.shape

moon_indices = np.arange(0, data_shape[0], 3) + 1
moon_data = part_11_data[moon_indices, :]

proj_inds = np.arange(0, data_shape[0], 3) + 2
proj_data = part_11_data[proj_inds, :]

fig, ax = plt.subplots()

ax.plot(moon_data[:, 0], moon_data[:, 1], rasterized=True)
ax.plot(proj_data[:, 0], proj_data[:, 1], rasterized=True)
ax.set_aspect('equal')

fig.savefig('Part_1_1_Trajectories.png', dpi=400, bbox_inches='tight')
fig.savefig('Part_1_1_Trajectories.pdf', dpi=400, bbox_inches='tight')

fig, ax = plt.subplots()
dist = np.sqrt((moon_data[:, 0] - proj_data[:, 0])**2 + (moon_data[:, 1] - proj_data[:, 1])**2)
ax.plot(moon_data[:, -1], dist, rasterized=True)

fig.savefig('Part_1_1_Distances.png', dpi=400, bbox_inches='tight')
fig.savefig('Part_1_1_Distances.pdf', dpi=400, bbox_inches='tight')
