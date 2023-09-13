# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 07:42:09 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

# define params
a = 1.5
b = 0.5
n = 20
x0 = 0.01

def model(xt):
    # model for fish population: x_{t+1} = ax_t / (b + x_t)
    xt1 = a * xt / (b + xt)
    return xt1

def leastsquares(data):
    # least squares estimate for a_hat based on the equation derivation in question 2a
    numer = sum([2 * data[i] * data[i + 1] / (b + data[i]) for i in range(len(data) - 1)])
    denom = sum([2 * data[i]**2 / (b + data[i])**2 for i in range(len(data) - 1)])
    return numer / denom


times = np.arange(0, n, 1)  # set up times
pops = np.zeros(n)  # initialise array of zeros
pops[0] = x0    # set initial population

for i in range(1, n):   # iterate over each time
    pops[i] = model(pops[i-1])      # calculate population at this timestep
    
print(f'a_hat = {round(leastsquares(pops), 5)}')    # now calculate and print result of least squares estimate, to 5 decimal places