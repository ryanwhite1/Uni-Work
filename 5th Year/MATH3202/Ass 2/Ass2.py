# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 15:54:13 2023

@author: ryanw
"""

from gurobipy import *
import pandas as pd
import math

# Sets / Data
nodes = pd.read_csv("nodes3.csv")
pipes = pd.read_csv("pipelines.csv")

N = range(len(nodes['Node']))
T = range(2) # number of days we're looking at
O = range(4) # number of options we have to upgrade (0th option is no upgrade)


# E[i,j] gives the distance (km) from node i to node j
E = {}
for j in range(len(pipes['Pipeline'])):
    n1 = pipes['Node1'][j]
    n2 = pipes['Node2'][j]
    distance = math.hypot(nodes['X'][n1] - nodes['X'][n2], nodes['Y'][n1] - nodes['Y'][n2])
    E[n1, n2] = distance

demand = {}
for year in ["Year5", "Year10"]:
    for n in N:
        demand[n, year] = nodes[year][n]

S = {20: 458, 27: 897, 36: 912, 45: 685}      # supplying nodes. Format is node: MW

# Each upgrade option for each supplying node. Format is (node, option): [MW, $$$]
Upgrades = {(20, 0): [0, 0], (27, 0): [0, 0], (36, 0): [0, 0], (45, 0): [0, 0],
    (20, 1): [90, 9058000], (27, 1): [180, 17838000], (36, 1): [185, 18352000], (45, 1): [133, 13603000],
    (20, 2): [224, 22582000], (27, 2): [440, 42746000], (36, 2): [454, 42306000], (45, 2): [345, 42306000],
    (20, 3): [445, 41362000], (27, 3): [895, 81954000], (36, 3): [906, 83778000], (45, 3): [681, 63024000]}
    
m = Model("Upgrades")

# Variables
X = {(n, t): m.addVar() for n in N for t in T}
Y = {(e, t): m.addVar() for e in E for t in T}
W = {(o, s): m.addVar(vtype=GRB.BINARY) for o in O for s in S}

# Objective
m.setObjective(quicksum(W[o, s] * Upgrades[s, o][1] for o in O for s in S),
               GRB.MINIMIZE)

# Constraints
for t in T:
    for n in N:
        if n in S:
            s = n
            m.addConstr(X[s, t] <= S[s] + quicksum(W[o, s] * Upgrades[s, o][0] for o in O))
        else:
            m.addConstr(X[n, t] <= 0)
            
        # Flow constraint:
        m.addConstr(X[n, t] + quicksum(Y[e, t] for e in E if e[1] == n) == 
                    quicksum(Y[e, t] for e in E if e[0] == n) + demand[n, "Year10"])

for s in S:
    m.addConstr(quicksum(W[o, s] for o in O) == 1)

# Optimise!
m.optimize()