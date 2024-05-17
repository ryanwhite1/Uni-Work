# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:13:27 2024

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

run_times = np.genfromtxt('Part2a_run_times.txt', delimiter='\t')[:, :-1]

fig, ax = plt.subplots()

# ax.scatter(run_times[:, 0], run_times[:, 1])
ax.errorbar(run_times[:, 0], np.mean(run_times[:, 1:], axis=1), yerr=np.std(run_times[:, 1:], axis=1), fmt='.')
ax.set(yscale='log', xlabel='Atom Number', ylabel='Compute Time (s)')
fig.savefig('Part2a_run_times.png', bbox_inches='tight')
fig.savefig('Part2a_run_times.pdf', bbox_inches='tight')



ground_states = np.genfromtxt('Part2b_ground_states.txt')

fig, axes = plt.subplots(nrows=3, sharex=True, gridspec_kw={'hspace':0}, figsize=(10, 10))

axes[0].plot(ground_states[:, 0], ground_states[:, 1], label='Numerical Result')
axes[0].plot(ground_states[:, 0], ground_states[:, 3], label='Analytic Result')
axes[1].plot(ground_states[:, 0], ground_states[:, 3] - ground_states[:, 1], label='Residuals')
axes[1].axhline(0, c='k', ls='--')
axes[2].plot(ground_states[1:-1, 0], ground_states[1:-1, 2], label='Numerical Second Derivative')
axes[2].plot(ground_states[1:-1, 0], ground_states[1:-1, 4], label='Analytic Second Derivative')
axes[2].plot()
axes[2].axhline(0, c='k', ls='--')
axes[0].set(ylabel=r'Ground State Energy, $\varepsilon / N$')
axes[1].set(ylabel='Energy Residuals')
axes[2].set(xlabel='$g$', ylabel=r'Second Derivative, $1/N \times \partial^2 \varepsilon / \partial g^2$')
for i, ax in enumerate(axes):
    loc = 'lower right' if i == 2 else None
    ax.legend(loc=loc)
    ax.grid(axis='x')
fig.savefig('Part2b_ground_states.png', bbox_inches='tight')
fig.savefig('Part2b_ground_states.pdf', bbox_inches='tight')