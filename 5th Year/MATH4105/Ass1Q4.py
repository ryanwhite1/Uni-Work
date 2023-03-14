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

X = sym.Matrix([[v * cos(thet) / (u**2 + v**2), v * sin(thet) / (u**2 + v**2), u / (u**2 + v**2)]])

print(X.T)