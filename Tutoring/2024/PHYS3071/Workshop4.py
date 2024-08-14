# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 08:53:45 2024

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt


##### QUESTION 1

def RK4_step_FO(deriv, yi, t, dt, params):
    '''First order equation RK4 step'''
    
    y0 = deriv(params, yi, t)
    y1 = deriv(params, yi + 0.5 * dt * y0, t + 0.5 * dt)
    y2 = deriv(params, yi + 0.5 * dt * y1, t + 0.5 * dt)
    y3 = deriv(params, yi + dt * y2, t + dt)
    
    return yi + dt * (y0 + 2 * y2 + 2 * y2 + y3) / 6

def RK4_FO(deriv, y0, t0, dt, params, n):
    '''First order RK4 solver.'''
    ys = np.zeros(n)
    ys[0] = y0
    ts = np.zeros(n)
    ts[0] = t0
    
    for i in range(1, n):
        ys[i] = RK4_step_FO(deriv, ys[i-1], ts[i-1], dt, params)
        ts[i] = ts[i-1] + dt

    return ts, ys 

def simple_ODE(params, yi, t):
    return params["a0"] * np.cos(t) - yi
def simple_ODE_solution(t, y0, params):
    return 0.5 * (2 * y0 * np.exp(-t) - params["a0"] * np.exp(-t) + params["a0"] * np.sin(t) + params["a0"] * np.cos(t))

n = 5000

t_init = 0
t_final = 100 * np.pi 
dt = (t_final - t_init) / n

y_init = 0

params = {"a0":1}

ts, ys = RK4_FO(simple_ODE, y_init, t_init, dt, params, n)

fig, ax = plt.subplots()

ax.plot(ts, ys)
ax.plot(ts, simple_ODE_solution(ts, y_init, params))



t_init = 0
t_final = 100 * np.pi 
dt = (t_final - t_init) / n
ts, ys = RK4_FO(simple_ODE, y_init, t_init, dt, params, n)
solution = simple_ODE_solution(ts, y_init, params)

fig, axes = plt.subplots(nrows=2)

axes[0].plot(ts, ys)
axes[0].plot(ts, solution)

axes[1].plot(ts, abs(ys - solution))
axes[1].set(yscale='log')



#### QUESTION 2

def RK4_step_SO(deriv, yi, t, dt, params):
    first_deriv, second_deriv = deriv
    
    y0 = first_deriv(params, yi, t)
    y0_dash = second_deriv(params, yi, t)
    
    y1 = first_deriv(params, yi + 0.5 * dt * np.array([y0, y0_dash]), t + 0.5 * dt)
    y1_dash = second_deriv(params, yi + 0.5 * dt * np.array([y0, y0_dash]), t + 0.5 * dt)
    
    y2 = first_deriv(params, yi + 0.5 * dt * np.array([y1, y1_dash]), t + 0.5 * dt)
    y2_dash = second_deriv(params, yi + 0.5 * dt * np.array([y1, y1_dash]), t + 0.5 * dt)
    
    y3 = first_deriv(params, yi + dt * np.array([y2, y2_dash]), t + dt)
    y3_dash = second_deriv(params, yi + dt * np.array([y2, y2_dash]), t + dt)
    
    y_final = yi[0] + dt * (y0 + 2 * y2 + 2 * y2 + y3) / 6
    y_dash_final = yi[1] + dt * (y0_dash + 2 * y1_dash + 2 * y2_dash + y3_dash) / 6
    
    return y_final, y_dash_final

def RK4_SO(deriv, y0, t0, dt, params, n):
    
    ys = np.zeros(n)
    ys[0] = y0[0]
    y_dashes = np.zeros(n)
    y_dashes[0] = y0[1]
    ts = np.zeros(n)
    ts[0] = t0
    
    for i in range(1, n):
        yi, yi_dash = RK4_step_SO(deriv, [ys[i-1], y_dashes[i-1]], ts[i-1], dt, params)
        ys[i] = yi; y_dashes[i] = yi_dash
        ts[i] = ts[i-1] + dt

    return ts, ys, y_dashes

def first_deriv(params, yi, t):
    return yi[1]

def second_deriv(params, yi, t):
    return - params["g"] / params["l"] * np.sin(yi[0])

params = {"g":9.8, "l":10}
n = int(1e4)

y_init = np.array([np.pi / 2, 0.])
t_init = 0.
t_final = 10
dt = (t_final - t_init) / n


ts, ys, y_dashes = RK4_SO([first_deriv, second_deriv], y_init, t_init, dt, params, n)

# plot the pendulum motion
fig, ax = plt.subplots()
x = np.sin(ys)
y = -np.cos(ys)
ax.plot(x, y)
ax.set(aspect='equal')

# plot the phase space
fig, ax = plt.subplots()
ax.plot(ys, y_dashes)


ms = np.arange(1., 5.)
fig, ax = plt.subplots()
for m in ms:
    y_init = np.array([(1. - 10.**-m) * np.pi, 0.])
    t_init = 0.
    t_final = 30
    dt = (t_final - t_init) / n


    ts, ys, y_dashes = RK4_SO([first_deriv, second_deriv], y_init, t_init, dt, params, n)
    
    ax.plot(ys, y_dashes, label=str(m))
ax.legend()



    