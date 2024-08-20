# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 08:23:30 2024

@author: ryanw
"""

import matplotlib.pyplot as plt
import numpy as np

### Question 1 -- Shooting method

def exact(x, alpha, v0):
    return x * np.tan(alpha) - 0.5 * 9.8 * x**2 / (v0 * np.cos(alpha))**2

def euler(v0, alpha, a, n):
    x_vel = v0 * np.cos(alpha)
    y_vel = v0 * np.sin(alpha)
    
    dt = a / (x_vel * n)
    
    ys = np.zeros(n)
    xs = np.zeros(n)
    
    for i in range(1, n):
        ys[i] = ys[i-1] + dt * y_vel 
        xs[i] = xs[i-1] + dt * x_vel
        
        y_vel += dt * -9.8 
        
    return xs, ys
    

def shooting(a, b, v0, alpha_range):
    boundary_err = lambda alpha: b - euler(v0, alpha, a, 1000)[1][-1]
    left, right = alpha_range
    
    error = 10
    i = 0 
    max_iter = 30
    EXIT_SUCCESS = 1
    while abs(error) > 1e-2:
        midpoint = (left + right) / 2
        midpoint_err = boundary_err(midpoint)
        if np.sign(boundary_err(left)) == np.sign(midpoint_err):
            left = midpoint
        else:
            right = midpoint
        
        error = midpoint_err
        i += 1
        
        print(f"Iteration = {i}. Angle range = [{left:.4f}, {right:.4f}]. Final height = {- midpoint_err + b:.2f}")
        if i > max_iter:
            print("Did not converge!")
            EXIT_SUCCESS = 0
            break
        
    if EXIT_SUCCESS:
        fig, ax = plt.subplots()
        xs = np.linspace(0, 1.1 * a, 1000)
        ax.plot(xs, exact(xs, midpoint, v0))
        ax.scatter(a, b)
        x, y = euler(v0, midpoint, a, 1000)
        ax.plot(x, y)
    return midpoint 

# print(euler(100, 0.5, 100, 1000))
# print(shooting(1000, 100, 100, [0.1, 3]))


# fig, ax = plt.subplots()
# # exact = lambda x, alpha, v0: 
# xs = np.linspace(0, 1000, 100)

# ax.plot(xs, exact(xs, np.sin(np.deg2rad(45)), 100))

### Finite difference method

fA = 0 
fB = 100

max_x = 500

alpha = shooting(max_x, fB, 100, [0.1, 2])
x_vel = 100 * np.cos(alpha)

N = 1000

t = max_x / x_vel
h = t / N 



ai = 1 * np.ones(N - 1)
bi = -2 * np.ones(N)
ci = 1 * np.ones(N - 1)
A = np.diag(ai, -1) + np.diag(bi, 0) + np.diag(ci, 1)
A_inv = np.linalg.inv(A)
    
d = np.ones(N) * h**2 * -9.8
d[-1] += -1 * fB

f = A_inv @ d

xs = np.linspace(0, max_x, N)
fig, ax = plt.subplots()
ax.plot(xs, f)
ax.scatter(max_x, fB)
    
    
    
    