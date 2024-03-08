import numpy as np
import matplotlib.pyplot as plt

one_s = np.loadtxt("B2_1s_states.txt", delimiter=',')
two_s = np.loadtxt("B2_2s_states.txt", delimiter=',')
two_p = np.loadtxt("B2_2p_states.txt", delimiter=',')

fig, ax = plt.subplots()
ax.plot(one_s[:, 0], one_s[:, 1], label='1s')
ax.plot(two_s[:, 0], two_s[:, 1], label='2s')
ax.plot(two_p[:, 0], two_p[:, 1], label='2p')

ax.legend()
ax.set(xlabel='Radius (au)', ylabel=r'Probability $|P(r)|^2$', xscale='log')

fig.savefig("B2_7.png", dpi=400, bbox_inches='tight')

