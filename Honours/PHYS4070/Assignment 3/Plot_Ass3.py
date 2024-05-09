import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


g_vals = [0, 0.5, 1, 5, 20]
data_arrays = []

for i in range(len(g_vals)):
    data_arrays.append(np.genfromtxt(f'g={g_vals[i]}_plane_wave_evol.txt', delimiter='\t')[:, 1:])

L = 20
xs = np.linspace(-L/2, L/2, data_arrays[0].shape[1])

fig, ax = plt.subplots()
every = 10
frames = np.arange(0, data_arrays[0].shape[0], every)
length = 5
fps = len(frames) / length

limit = np.max(np.array(data_arrays).flatten())

plots = [0, 0, 0, 0, 0]
for j in range(len(g_vals)):
    plots[j] = ax.plot(xs, data_arrays[j][0, :], label=f'$g={g_vals[j]}$')
ax.set(ylim=(0, limit))
ax.legend(loc='upper right')

def animate(i):
    for j in range(len(g_vals)):
        plots[j][0].set_data(xs, data_arrays[j][i, :])
    return [fig, ax]
    
ani = animation.FuncAnimation(fig, animate, frames=frames)
ani.save(f"animation.gif", writer='pillow', fps=fps)