# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 14:32:35 2024

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

def energy(position, velocity, params):
    return params['m'] * 9.8 * position + 0.5 * params['m'] * velocity**2

def rk2_step(x, xdash, accel, params, dt):
    x_k1 = dt * xdash
    xdash_k1 = dt * accel(x, xdash, params)
    x_k2 = dt * (xdash + xdash_k1 / 2)
    xdash_k2 = dt * accel(x + x_k1 / 2, xdash + xdash_k1 / 2, params)
    
    new_x = x + x_k2
    new_xdash = xdash + xdash_k2
    
    return new_x, new_xdash

def leapfrog_step(x, xdash, accel, params, dt):
    new_x = x + dt * xdash + dt**2 / 2 * accel(x, xdash, params)
    new_xdash = xdash + dt * accel(x, xdash, params)
    
    return new_x, new_xdash

def problem_eq(x, xdash, params):
    return (-params['beta'] * xdash - params['k'] * x) / params['m']

def integrate(initial_state, times, accel, params, mode='rk2'):
    
    if mode == 'rk2':
        function = rk2_step 
    elif mode == 'leapfrog':
        function = leapfrog_step
    
    x0, xdash0 = initial_state
    
    solution = np.zeros((2, len(times)))
    solution[:, 0] = initial_state
    
    dt = times[1] - times[0]
    
    for i in range(1, len(times)):
        solution[:, i] = function(solution[0, i-1], solution[1, i-1], accel, params, dt)
    
    return solution

dt = 1e-6
times = np.arange(0, 1+dt, dt)
r0 = 1e-5
v0 = 0
beta = 0
k = 1e-6
m = 1

params = {'beta':beta, 'k':k, 'm':m}

solution = integrate([r0, v0], times, problem_eq, params, mode='rk2')
energies = energy(solution[0, :], solution[1, :], params)








