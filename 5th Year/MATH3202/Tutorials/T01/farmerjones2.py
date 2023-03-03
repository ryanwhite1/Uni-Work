# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 10:13:29 2023

@author: ryanw
"""

from gurobipy import *

# Sets
cakes = ['chocolate', 'plain']
ingredients = ['time', 'eggs', 'milk']

C = range(len(cakes))
I = range(len(ingredients))

# Data
revenue = [4, 2]
usage = [[20, 4, 250], 
         [50, 1, 200]]

availability = [480, 30, 5000]

m = Model("Farmer Jones")

# Variables
X = {}
for c in C:
    X[c] = m.addVar()

# Objective
m.setObjective(quicksum(revenue[c] * X[c] for c in C), GRB.MAXIMIZE)

# Constraints
for i in I:
    m.addConstr(quicksum(usage[c][i] * X[c] for c in C) <= availability[i])
    
m.optimize()

print("Revenue is", m.objval)
for c in C:
    print("Make", X[c].x, cakes[c], "cakes")