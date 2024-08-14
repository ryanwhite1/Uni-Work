# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 09:27:13 2024

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

##### exercise 1
t12 = 7e8
lamb = np.log(2) / t12

def analytic(t, N0):
    return N0 * np.exp(-lamb * t)

def deriv(N):
    return - lamb * N
def euler_step(deriv, y, x, dx):
    '''1D euler method'''
    dydx = deriv(y)
    return y + dydx * dx
def euler_1d(deriv, y0, x):
    dx = x[1] - x[0]
    y = np.zeros(len(x))
    y[0] = y0
    for i in range(1, len(x)):
        y[i] = euler_step(deriv, y[i-1], x[i], dx)
    return y

N0 = 6.022e23
n = int(1e3)
x = np.linspace(0, 5e9, n)
y = euler_1d(deriv, N0, x)

fig, ax = plt.subplots()
ax.plot(x, y, label='numerical')
ax.plot(x, analytic(x, N0), label='analytic')
ax.legend()
ax.set(xlabel='Time (years)', ylabel='$^{235}U$ Atoms Remaining')


##### exercise 2
gamma = 0.05
omega = 0.1

def analytic(t, y0):
    Omega = np.sqrt(4 * omega**2 - gamma**2)
    return y0 * np.exp(-gamma * t / 2) * (np.cos(0.5 * Omega * t) + (gamma / Omega) * np.sin(0.5 * Omega * t))

def fdash(dydt, y):
    return - gamma * dydt - omega**2 * y

def euler_step_2nd_order(fdash, ydash, y, dt):
    ddyddt = fdash(ydash, y)
    ydash_next = ydash + dt * ddyddt
    y_next = y + dt * ydash
    return ydash_next, y_next

def euler_2nd_order(fdash, ydash0, y0, t):
    dt = t[1] - t[0]
    y = np.zeros(len(t))
    dydt = np.zeros(len(t))
    y[0] = y0; dydt[0] = ydash0
    
    for i in range(1, len(t)):
        ydash_next, y_next = euler_step_2nd_order(fdash, dydt[i-1], y[i-1], dt)
        dydt[i] = ydash_next 
        y[i] = y_next
        
    return dydt, y 


n = int(1e3)
t = np.linspace(0, 50, n)

y0 = 2 

dydt, y = euler_2nd_order(fdash, 0, y0, t)

fig, ax = plt.subplots()
ax.plot(t, y, label='numerical')
ax.plot(t, y0 * np.cos(omega * t), label='check')
ax.plot(t, analytic(t, y0), label='analytic')
ax.legend()

fig, ax = plt.subplots()
ax.plot(dydt, y)
ax.set(xlabel='dy/dt', ylabel='y')



###### exercise 3
wd = 1 
w0 = 1
def analytic(t):
    return (np.exp(-w0 * t) / (w0**2 + wd**2)) * (w0**2 + wd**2 + wd + w0 * np.exp(w0 * t) * np.sin(wd * t) - wd * np.exp(w0 * t) * np.cos(wd * t))
def deriv(y, t):
    return np.sin(wd * t) - w0 * y
def euler_step(deriv, y, t, dt):
    '''1D euler method'''
    dydt = deriv(y, t)
    return y + dydt * dt
def euler_1d(deriv, y0, t):
    dt = t[1] - t[0]
    y = np.zeros(len(t))
    y[0] = y0
    for i in range(1, len(t)):
        y[i] = euler_step(deriv, y[i-1], t[i], dt)
    return y

n = int(1e3)
t = np.linspace(0, 10, n)
y0 = 1

y = euler_1d(deriv, y0, t)

fig, ax = plt.subplots()
ax.plot(t, y, label='numerical')
ax.plot(t, analytic(t), label='analytic')
ax.legend()

fig, ax = plt.subplots()
dydt = deriv(y, t)
ax.plot(dydt, y)
ax.set(xlabel='dy/dt', ylabel='y')


    