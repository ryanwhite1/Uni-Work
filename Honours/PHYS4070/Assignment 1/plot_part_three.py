import numpy as np
import matplotlib.pyplot as plt

one_s = np.loadtxt("B3_1s_states.txt", delimiter=',')
two_s = np.loadtxt("B3_2s_states.txt", delimiter=',')
two_p = np.loadtxt("B3_2p_states.txt", delimiter=',')

fig, ax = plt.subplots()
ax.plot(one_s[:, 0], one_s[:, 1], label='1s')
ax.plot(two_s[:, 0], two_s[:, 1], label='2s')
ax.plot(two_p[:, 0], two_p[:, 1], label='2p')

ax.legend()
ax.set(xlabel='Radius (au)', 
       ylabel=r'Probability Density $|P(r)|^2$', 
       xscale='log',
       xlim=(0.01, max(one_s[:, 0])))

fig.savefig("B3_14.png", dpi=400, bbox_inches='tight')

energies = np.loadtxt("B3_core_energies.txt", delimiter=',')

fig, ax = plt.subplots()
ax.plot(energies[:, 0], energies[:, 1])
ax.set(xlabel='Procedure Iteration', ylabel='Energy (au)')
fig.savefig("B3_12.png", dpi=400, bbox_inches='tight')
