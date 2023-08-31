# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 12:01:14 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

A = np.array([[1, 0, 0, 0, 0],
             [0, 0.75, 0, 0.15, 0],
             [0, 0, 1, 0, 0],
             [0, 0.15, 0, 0.75, 0],
             [0, 0.1, 0, 0.1, 1]])
B = np.array([[0, 20, 0, 0, 0],
             [0.1, 0.1, 0, 0, 0],
             [0, 0, 0, 10, 0],
             [0, 0, 0.1, 0.1, 0],
             [0, 0, 0, 0, 0.1]])

n0 = np.array([10, 5, 4, 8, 0]).T
C1 = (A@B) @ n0
C2 = (B@A) @ n0

M = B @ np.linalg.matrix_power(A, 10)

def maturation(n):
    '''Mature the population by one step'''
    return M @ n

times = np.arange(0, 15+1, 1)
n_times = np.zeros((len(n0), len(times)))
n_times[:, 0] = n0

for t in range(1, len(times)):
    n_times[:, t] = maturation(n_times[:, t - 1])
    
pops = ['Crop1Larvae', 'Crop1Adults', 'Crop2Larvae', 'Crop2Adults', 'Trapped']
mtype = ['o', '^', 'o', '^', '^']
ltype = ['-', '-', '--', '--', ':']

fig, ax = plt.subplots()
for i in range(len(n0)):
    ax.plot(times, n_times[i, :], ls=ltype[i], marker=mtype[i], label=pops[i])
    
ax.set_xlabel("Time")
ax.set_ylabel("Population")
ax.legend()

eig = np.linalg.eig(M)
dom_arg = np.argmax(np.abs(eig[0]))
dom_eigval = eig[0][dom_arg]
dom_eigvec = eig[1][:, dom_arg]

n = 200
attracts, Retents = np.linspace(0, 0.25, n), np.linspace(0, 1, n)
aR_mesh = np.zeros((len(attracts), len(Retents)))
for i, a in enumerate(attracts):
    for j, R in enumerate(Retents):
        A_aR = np.array([[1, 0, 0, 0, 0],
                     [0, 0.75, 0, 0.25 - a, (1 - R) / 2],
                     [0, 0, 1, 0, 0],
                     [0, 0.25 - a, 0, 0.75, (1 - R) / 2],
                     [0, a, 0, a, R]])
        M_aR = B @ np.linalg.matrix_power(A_aR, 10)
        eig_aR = np.linalg.eig(M_aR)
        dom_arg_aR = np.argmax(np.abs(eig_aR[0]))
        dom_eigval_aR = eig_aR[0][dom_arg_aR]
        dom_eigvec_aR = eig_aR[1][:, dom_arg_aR]
        
        # choose 0 if crop1/2 both negative => both crops decreasing in populations
        # choose 1 if either crop 1/2 negative => one crop is increasing, one is decreasing
        # choose 2 if neither crop 1/2 negative => populations increasing
        
        # if dom_eigvec_aR[0] < 0 or dom_eigvec_aR[2] < 0:
        #     if dom_eigvec_aR[2] < 0 and dom_eigvec_aR[0] < 0:
        #         aR_mesh[i, j] = 0 
        #     else:
        #         aR_mesh[i, j] = 1
        # else:
        #     aR_mesh[i, j] = 2
        
        aR_mesh[i, j] = np.mean([dom_eigvec_aR[k] for k in [1, 3]])

fig, ax = plt.subplots()
# ax.matshow(aR_mesh)
img = ax.pcolormesh(attracts, Retents, aR_mesh)
ax.set_xlabel("Trap Attraction $a$")
ax.set_ylabel("Trap Retention $R$")
fig.colorbar(img)
        