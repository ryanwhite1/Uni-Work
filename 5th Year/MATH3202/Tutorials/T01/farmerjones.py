# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 09:51:49 2023

@author: ryanw
"""

from gurobipy import *

m = Model("Farmer Jones")

x1 = m.addVar()
x2 = m.addVar()

m.setObjective(4 * x1 + 2 * x2, GRB.MAXIMIZE)

m.addConstr(20 * x1 + 50 * x2 <= 480)
m.addConstr(4 * x1 + x2 <= 30)
m.addConstr(250 * x1 + 200 * x2 <= 5000)

m.optimize()

print("Maximum revenuse=", m.objval)
print("Make", x1.x, "chocolate cakes, and", x2.x, "plain cakes.")