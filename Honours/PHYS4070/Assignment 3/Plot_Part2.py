# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:13:27 2024

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

run_times = np.genfromtxt('Part2a_run_times.txt', delimiter='\t')[:, :-1]

def linear(x, m, c):
    return m * x + c

fig, ax = plt.subplots()

yvals = np.mean(run_times[:, 1:], axis=1)

[k, t0], pcov = curve_fit(linear, run_times[1:, 0], np.log10(yvals[1:]), p0=(3, 1e-5))

ax.errorbar(run_times[:, 0], yvals, yerr=np.std(run_times[:, 1:], axis=1), fmt='.', label='Simulation Time')
ax.plot(run_times[:, 0], yvals[3] / 2**(2 * run_times[3, 0]) * 2**(2 * run_times[:, 0]), label='$t = t_0 2^{2N}$') # plot the 2^2N slope
ax.plot(run_times[:, 0], 10**linear(run_times[:, 0], k, t0), label=rf'$t = 10^{{{t0:.2f}}} \times 2^{{{10**k:.2f}N}}$')
ax.set(yscale='log', xlabel='Atom Number', ylabel='Compute Time (s)')
ax.legend()
fig.savefig('Part2a_run_times.png', bbox_inches='tight')
fig.savefig('Part2a_run_times.pdf', bbox_inches='tight')



ground_states = np.genfromtxt('Part2b_ground_states.txt')

fig, axes = plt.subplots(nrows=3, sharex=True, gridspec_kw={'hspace':0}, figsize=(10, 10))

axes[0].plot(ground_states[:, 0], ground_states[:, 1], label='Numerical Result')
axes[0].plot(ground_states[:, 0], ground_states[:, 3], label='Analytic Result')
axes[0].plot(ground_states[:, 0], -ground_states[:, 0] / 4, label=r'$\varepsilon / N = -g/4$', c='tab:purple', ls='--')
axes[0].axhline(-0.5, label=r'$\varepsilon / N = -0.5$', ls='--', c='k')
axes[1].plot(ground_states[:, 0], ground_states[:, 3] - ground_states[:, 1], label='Residuals')
axes[1].axhline(0, c='k', ls=':')
axes[2].plot(ground_states[1:-1, 0], ground_states[1:-1, 2], label='Numerical Second Derivative')
axes[2].plot(ground_states[1:-1, 0], ground_states[1:-1, 4], label='Analytic Second Derivative')
axes[2].plot()
axes[2].axhline(0, c='k', ls=':')
axes[0].set(ylabel=r'Ground State Energy, $\varepsilon / N$', ylim=(-2.1, -0.4))
axes[1].set(ylabel='Energy Residuals')
axes[2].set(xlabel='$g$', ylabel=r'Second Derivative, $1/N \times \partial^2 \varepsilon / \partial g^2$')
for i, ax in enumerate(axes):
    loc = 'lower right' if i == 2 else None
    ax.legend(loc=loc)
    ax.grid(axis='x')
fig.savefig('Part2b_ground_states.png', bbox_inches='tight')
fig.savefig('Part2b_ground_states.pdf', bbox_inches='tight')


filenames = ['Part2c_g=1_evolution.txt', 'Part2c_g=4_evolution.txt', 'Part2c_g=20_evolution.txt']
gvals = [1, 4, 20]
fig, axes = plt.subplots(figsize=(10, 12), nrows=3, gridspec_kw={'hspace':0}, sharex=True)
for i, g in enumerate(gvals):
    time_evolution = np.genfromtxt(filenames[i], delimiter='\t')
    times = time_evolution[:, 0]
    
    axes[i].plot(times, time_evolution[:, 1], label='$S_z$')
    axes[i].plot(times, time_evolution[:, 2], label='$S_x$')
    axes[i].plot(times, time_evolution[:, 3], label='$C_{xx}$')
    if i == 0:
        axes[i].legend()
    else:
        axes[i].axhline(2, ls=':', c='k', alpha=0.7)
    xlabel = 'Time' if i == len(gvals) - 1 else ''
    axes[i].set(xlabel=xlabel, ylabel='Observable Value')
    axes[i].text(18, 3.5, fr'$g = {gvals[i]}$', fontsize=14)
fig.savefig('Part2c_time_evolution.png', bbox_inches='tight')
fig.savefig('Part2c_time_evolution.pdf', bbox_inches='tight')