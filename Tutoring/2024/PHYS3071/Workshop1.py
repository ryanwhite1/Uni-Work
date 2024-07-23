# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:52:50 2024

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

#### bisection

def bisection(func, a, b, tol=1e-6):
    new_a = a
    new_b = b
    midpoint = 0.5 * (new_a + new_b)
    err = 100
    i = 0
    while abs(err) > tol:
        fa = func(new_a)
        fb = func(new_b)
        new_midpoint = 0.5 * (new_a + new_b)
        fm = func(new_midpoint)
        if np.sign(fm) == np.sign(fa):
            new_a = new_midpoint
        else:
            new_b = new_midpoint
        if i > 0:
            err = midpoint - new_midpoint
            midpoint = new_midpoint
        i += 1
    return midpoint, i

q1_func = lambda x: x**2 - 5 * x - 3

print(bisection(q1_func, -2, 4))




#### newton's method

def newton(func, func_dash, init_guess, tol=1e-6):
    err = 100
    guess = init_guess
    while abs(err) > tol:
        new_guess = guess - func(guess) / func_dash(guess)
        err = new_guess - guess
        guess = new_guess
    return guess

q2_func = lambda x: np.cos(x) - 0.25 * x
q2_func_dash = lambda x: -np.sin(x) - 0.25

print(newton(q2_func, q2_func_dash, 2))



#### newton's method in 2d

def newton_2d(func1, func1_dash, func2, func2_dash, xs, tol=1e-6):
    guess = xs
    err = 100
    while abs(err) > tol:
        func_eval = np.array([func1(guess[0], guess[1]), func2(guess[0], guess[1])])
        a1, a2 = func1_dash(guess[0], guess[1])
        b1, b2 = func2_dash(guess[0], guess[1])
        jacob = np.array([[a1, a2], [b1, b2]])
        invert_jacob = np.linalg.inv(jacob)
        new_guess = guess - invert_jacob @ func_eval
        err = max(np.abs(guess - new_guess))
        guess = new_guess
    return guess

q3_func1 = lambda x1, x2: -x1 * x2 - 0.5 * x2**2 + 2 
q3_func2 = lambda x1, x2: -x1 + 2 * x2 - 1 

def q3_func1_dash(x1, x2):
    return -x2, -x1 - x2 
def q3_func2_dash(x1, x2):
    return -1, 2 

init_guess = np.array([2, 0])
print(newton_2d(q3_func1, q3_func1_dash, q3_func2, q3_func2_dash, init_guess))
    