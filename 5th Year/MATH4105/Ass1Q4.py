# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 13:30:19 2023

@author: ryanw
"""

import sympy as sym
from sympy import sin, cos

u = sym.Symbol('u')
v = sym.Symbol('v')
thet = sym.Symbol('thet')

X = sym.Matrix([[v * cos(thet) / (u**2 + v**2), v * sin(thet) / (u**2 + v**2), u / (u**2 + v**2)],
                [u * cos(thet) / (u**2 + v**2), u * sin(thet) / (u**2 + v**2), -v / (u**2 + v**2)],
                [-sin(thet) / (u * v), cos(thet) / (u * v), 0]])

T = sym.Matrix([[1, 0.5, -4],
                [0.5, 2, 0],
                [3, -6, 7]])

a = X * T * X.T
b = sym.simplify(a)
print(b)