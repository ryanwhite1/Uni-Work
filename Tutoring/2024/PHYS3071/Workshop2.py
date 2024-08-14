# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 12:04:27 2024

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

def trapezoid(func, a, b, n):
    tot = 0
    dx = (b - a) / n
    x1 = a 
    x2 = a + dx
    for i in range(n):
        tot += 0.5 * (func(x1) + func(x2)) * dx
        x1 += dx
        x2 += dx
    return tot

def simpson(func, a, b, n):
    tot = 0
    dx = (b - a) / n
    x1 = a 
    x2 = a + dx
    for i in range(n):
        tot += (dx/6) * (func(x1) + 4 * func((x1 + x2)/2) + func(x2))
        x1 += dx
        x2 += dx
    return tot

def monte_carlo(func, a, b, n):
    points = np.random.uniform(0, 1, n)
    x = np.random.uniform(a, b, n)
    fx = func(np.linspace(a, b, n))
    points *= max(fx)
    counter = 0
    for i in range(n):
        if points[i] <= func(x[i]):
            counter += 1 
    return (b - a) * max(fx) * counter / n
    

func_1 = lambda x: np.sin(1 * np.sqrt(x))

# print(trapezoid(func_1, 0, np.pi, 1000))
# print(simpson(func_1, 0, np.pi, 1000))
# print(monte_carlo(func_1, 0, np.pi, 1000))

x_values = np.arange(0.1, 10.1, 0.1)

int_values = np.zeros(len(x_values))

# for i, x_val in enumerate(x_values):
#     function = lambda x: np.sin(x_val * np.sqrt(x))
#     int_values[i] = trapezoid(function, 0, np.pi, 1000)
count = 0
for x_val in x_values:
    function = lambda x: np.sin(x_val * np.sqrt(x))
    int_values[count] = trapezoid(function, 0, np.pi, 1000)
    count = count + 1
    
fig, ax = plt.subplots()
ax.plot(x_values, int_values)
