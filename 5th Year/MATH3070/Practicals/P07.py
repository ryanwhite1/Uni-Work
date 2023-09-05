# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 11:56:52 2023

@author: ryanw
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# part a
def LS_rho(biomass):
    ''' Returns a least squares estimate of the parameter p, for R_{t+1} = p * R_t
    '''
    denom = sum([biomass[i]**2 for i in range(len(biomass) - 1)])
    numer = sum([biomass[i + 1] * biomass[i] for i in range(len(biomass) - 1)])
    return numer / denom

def discrete_exp(R, p):
    ''' This is the discrete time exponential model, with R_{t + 1} = p * R_t
    '''
    return p * R

# part b
data = pd.read_csv('LS.csv', sep=',')

# part c
fig, ax = plt.subplots()
ax.scatter(data['years'], data['biomass'])

# part d
data_rho_est = LS_rho(data['biomass'])

# part e
T = 10
times = np.linspace(0, T, T)
R = np.zeros(T)
R0 = 2
R[0] = R0
p = 1.5
for i in range(1, T):
    R[i] = discrete_exp(R[i - 1], p)

fig, ax = plt.subplots()
ax.plot(times, R)
rho_est = LS_rho(R)

# part f

time_rates = np.random.exponential(p, size=T)
R_rand = np.zeros(T)
R_rand[0] = R0
for i in range(1, T):
    R_rand[i] = discrete_exp(R_rand[i - 1], time_rates[i-1])

ax.scatter(times, R_rand)

# part g
N = 10000
time_rates = np.random.exponential(p, size=(T, N))
p_ests = np.zeros(N)
for i in range(N):
    R_rand = np.zeros(T)
    R_rand[0] = R0
    for j in range(1, T):
        R_rand[j] = discrete_exp(R_rand[j - 1], time_rates[j-1, i])
    p_ests[i] = LS_rho(R_rand)

fig, ax = plt.subplots()
ax.hist(p_ests, bins=20, label=r"$R_{t + 1} = \rho R_t$", alpha=0.5)
ax.set_xlabel(r"$\rho$ estimate")
ax.set_ylabel("Frequency")
# ax.set_title()

# part h

def discrete_exp_err(R, p, a):
    return a + p * R
def LS_err_exp(biomass):
    n = len(biomass) - 1
    sum_x = sum([biomass[i] for i in range(len(biomass) - 1)])
    sum_x_square = sum([biomass[i]**2 for i in range(len(biomass) - 1)])
    sum_y = sum([biomass[i] for i in range(1, len(biomass))])
    sum_xy = sum([biomass[i] * biomass[i - 1] for i in range(1, len(biomass))])
    a_est = (sum_x_square * sum_y - sum_x * sum_xy) / (n * sum_x_square - sum_x**2)
    p_est = (n * sum_xy - sum_x * sum_y) / (n * sum_x_square - sum_x**2)
    return a_est, p_est

N = 10000
time_rates = np.random.exponential(p, size=(T, N))
a_ests, p_ests = np.zeros(N), np.zeros(N)
for i in range(N):
    R_rand = np.zeros(T)
    R_rand[0] = R0
    for j in range(1, T):
        R_rand[j] = discrete_exp_err(R_rand[j - 1], time_rates[j-1, i], 1)
    a_ests[i], p_ests[i] = LS_err_exp(R_rand)

# fig, ax = plt.subplots()
ax.hist(p_ests, bins=20, label=r"$R_{t + 1} = a + \rho R_t$", alpha=0.5)
# ax.set_xlabel(r"$\rho$ estimate")
# ax.set_ylabel("Frequency")
# ax.set_title()
ax.legend()

fig, ax = plt.subplots()
ax.hist(a_ests[np.argwhere(abs(a_ests) <= 100)], bins=20)
ax.set_xlabel(r"$a$ estimate")
ax.set_ylabel("Frequency")


