import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

print("Generating animation for plane wave evolution...")
g_vals = [0, 0.5, 1, 5, 20]
data_arrays = []

for i in range(len(g_vals)):
    temp_array = np.genfromtxt(f'g={g_vals[i]}_plane_wave_evol.txt', delimiter='\t')
    data_arrays.append(temp_array[:, 1:])
times = temp_array[:, 0]

L = 20
xs = np.linspace(-L/2, L/2, data_arrays[0].shape[1])

fig, ax = plt.subplots()
every = 10
frames = np.arange(0, data_arrays[0].shape[0], every)
length = 5
fps = len(frames) / length

limit = 1.1 * np.max(np.array(data_arrays).flatten())

plots = [0, 0, 0, 0, 0]
for j in range(len(g_vals)):
    plots[j] = ax.plot(xs, data_arrays[j][0, :], label=f'$g={g_vals[j]}$')
ax.set(ylim=(0, limit), ylabel=r'$|\psi|^2$', xlabel='$x$')
ax.legend(loc='upper right')

def animate(i):
    for j in range(len(g_vals)):
        plots[j][0].set_data(xs, data_arrays[j][i, :])
    ax.set(title=f'Time = {times[i]:.2f}')
    return [fig, ax]
    
ani = animation.FuncAnimation(fig, animate, frames=frames)
ani.save(f"Part1b_Plane_Wave_Evolution.gif", writer='pillow', fps=fps)

fig, ax = plt.subplots()
for i in range(len(g_vals)):
    ax.plot(xs, data_arrays[i][data_arrays[0].shape[0]//2, :], label=f'$g={g_vals[i]}$')
ax.set(ylim=(0, limit), ylabel=r'$|\psi|^2$', xlabel='$x$')
ax.legend(loc='upper right')
fig.savefig('Part1b_PlaneWave_snapshot.png', bbox_inches = 'tight')
fig.savefig('Part1b_PlaneWave_snapshot.pdf', bbox_inches = 'tight')





print("Generating animation and peak plot for single soliton evolution...")

u_vals = [-5, -1, 0, 1, 5]
data_arrays = []
for i in range(len(u_vals)):
    temp_array = np.genfromtxt(f'u={u_vals[i]}_soliton.txt', delimiter='\t')
    data_arrays.append(temp_array[:, 1:])
data_arrays = np.array(data_arrays)
times = temp_array[:, 0]

L = 20
xs = np.linspace(-L/2, L/2, data_arrays.shape[2])

fig, ax = plt.subplots()
every = 10
frames = np.arange(0, data_arrays[0].shape[0], every)
length = 5
fps = len(frames) / length

limit = 1.1 * np.max(np.array(data_arrays).flatten())

plots = [0, 0, 0, 0, 0]
for j in range(len(u_vals)):
    plots[j] = ax.plot(xs, data_arrays[j, 0, :], label=f'$u={u_vals[j]}$')
ax.set(ylim=(0, limit), ylabel=r'$|\psi|^2$', xlabel='$x$')
ax.legend(loc='upper right')

def animate(i):
    for j in range(len(u_vals)):
        plots[j][0].set_data(xs, data_arrays[j, i, :])
    ax.set(title=f'Time = {times[i]:.2f}')
    return [fig, ax]
ani = animation.FuncAnimation(fig, animate, frames=frames)
ani.save(f"Part1c_Soliton_Evolution.gif", writer='pillow', fps=fps)

fig, ax = plt.subplots()
for i in range(len(u_vals)):
    ax.plot(xs, data_arrays[i, data_arrays.shape[1]//2, :], label=f'$u={u_vals[i]}$')
ax.set(ylim=(0, limit), ylabel=r'$|\psi|^2$', xlabel='$x$')
ax.legend(loc='upper right')
fig.savefig('Part1c_soliton_snapshot.png', bbox_inches = 'tight')
fig.savefig('Part1c_soliton_snapshot.pdf', bbox_inches = 'tight')

peak_positions = np.genfromtxt('Part1c_peak_pos.txt', delimiter='\t')
fig, ax = plt.subplots()
for i in range(len(u_vals)):
    ax.plot(peak_positions[:, 0], peak_positions[:, i+1], label=f'$u={u_vals[i]}$')
ax.legend()
ax.set(xlabel='Time ($t$)', ylabel=r'Soliton $|\psi|^2$ Peak Position ($x$)')
fig.savefig('Part1c_Peak_Positions.png', bbox_inches = 'tight')
fig.savefig('Part1c_Peak_Positions.pdf', bbox_inches = 'tight')






print("Generating animation and peak plot for double soliton evolution...")

phase_vals = [0, np.pi/10, np.pi/7, np.pi / 4, np.pi / 3, np.pi / 2, np.pi]
phase_vals_symbolic = ['0', '\pi/10', '\pi/7', '\pi/4', '\pi/3', '\pi/2', '\pi']
colours = ['tab:blue', 'tab:green', 'tab:orange', 'tab:red', 'tab:purple', 'tab:brown', 'tab:olive']
phase_filenames = ["theta=0_solitons.txt", "theta=pi_10_solitons.txt", "theta=pi_7_solitons.txt", "theta=pi_4_solitons.txt", 
                   "theta=pi_3_solitons.txt", "theta=pi_2_solitons.txt", "theta=pi_solitons.txt"]
data_arrays = []
for i in range(len(phase_vals)):
    temp_array = np.genfromtxt(phase_filenames[i], delimiter='\t')
    data_arrays.append(temp_array[:, 1:])
data_arrays = np.array(data_arrays)
times = temp_array[:, 0]

L = 20
xs = np.linspace(-L/2, L/2, data_arrays.shape[2])

fig, ax = plt.subplots()
every = 10
frames = np.arange(0, data_arrays[0].shape[0], every)
length = 5
fps = len(frames) / length

limit = 1.1 * np.max(np.array(data_arrays).flatten())

plots = [0, 0, 0, 0, 0, 0, 0]
for j in range(len(phase_vals)):
    plots[j] = ax.plot(xs, data_arrays[j, 0, :], label=rf'$\theta={phase_vals_symbolic[j]}$')
ax.set(ylim=(0, limit), ylabel=r'$|\psi|^2$', xlabel='$x$')
ax.legend(loc='upper right')

def animate(i):
    for j in range(len(phase_vals)):
        plots[j][0].set_data(xs, data_arrays[j, i, :])
    ax.set(title=f'Time = {times[i]:.2f}')
    return [fig, ax]
ani = animation.FuncAnimation(fig, animate, frames=frames)
ani.save(f"Part1d_Solitons_Evolution.gif", writer='pillow', fps=fps)

fig, ax = plt.subplots()
for i in range(len(phase_vals)):
    ax.plot(xs, data_arrays[i, data_arrays.shape[1]//2, :], label=rf'$\theta={phase_vals_symbolic[i]}$')
ax.set(ylim=(0, limit), ylabel=r'$|\psi|^2$', xlabel='$x$')
ax.legend(loc='upper right')
fig.savefig('Part1d_solitons_snapshot.png', bbox_inches = 'tight')
fig.savefig('Part1d_solitons_snapshot.pdf', bbox_inches = 'tight')


peak_positions = np.genfromtxt('Part1d_peak_pos.txt', delimiter='\t')

fig, ax = plt.subplots()
for i in range(len(phase_vals)):
    peak_index = (i * 2) + 1
    ax.plot(peak_positions[:, 0], peak_positions[:, peak_index], c=colours[i], label=rf'$\theta={phase_vals_symbolic[i]}$')
    ax.plot(peak_positions[:, 0], peak_positions[:, peak_index+1], c=colours[i])
ax.legend()
ax.set(xlabel='Time ($t$)', ylabel=r'Soliton $|\psi|^2$ Peak Position ($x$)')
fig.savefig('Part1d_Peak_Positions.png', bbox_inches = 'tight')
fig.savefig('Part1d_Peak_Positions.pdf', bbox_inches = 'tight')


fig, ax = plt.subplots()
for i in range(len(phase_vals)):
    peak_index = (i * 2) + 1
    ax.plot(peak_positions[:, 0], np.abs(peak_positions[:, peak_index] - peak_positions[:, peak_index+1]), c=colours[i], label=rf'$\theta={phase_vals_symbolic[i]}$')
ax.legend()
ax.set(xlabel='Time ($t$)', ylabel=r'Soliton $|\psi|^2$ Peak Separation ($x$)')
fig.savefig('Part1d_Peak_Separations.png', bbox_inches = 'tight')
fig.savefig('Part1d_Peak_Separations.pdf', bbox_inches = 'tight')


close_approach = np.zeros(len(phase_vals))
for i in range(len(phase_vals)):
    peak_index = (i * 2) + 1
    close_approach[i] = np.min(np.abs(peak_positions[:, peak_index] - peak_positions[:, peak_index+1]))
fig, ax = plt.subplots()
ax.scatter(phase_vals, close_approach)
ax.set(xlabel='Relative Phase', ylabel='Closest Approach of Peaks')
ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 5))
ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 10))
from matplotlib.ticker import FuncFormatter, MultipleLocator
ax.xaxis.set_major_formatter(FuncFormatter(lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else '0'))
ax.xaxis.set_major_locator(MultipleLocator(base=np.pi/5))
fig.savefig('Part1d_Peak_CloseApproach.png', bbox_inches = 'tight')
fig.savefig('Part1d_Peak_CloseApproach.pdf', bbox_inches = 'tight')




