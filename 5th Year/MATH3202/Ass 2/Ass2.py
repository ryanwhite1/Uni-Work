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
years = ["Year5", "Year10"]
for year in years:
    for n in N:
        demand[n, year] = nodes[year][n]

S = {20: 458, 27: 897, 36: 912, 45: 685}      # supplying nodes. Format is node: MW

# Each upgrade option for each supplying node. Format is (node, option): [MW, $$$]
Upgrades = {(20, 0): [0, 0], (27, 0): [0, 0], (36, 0): [0, 0], (45, 0): [0, 0],
    (20, 1): [90, 9058000], (27, 1): [180, 17838000], (36, 1): [185, 18352000], (45, 1): [133, 13603000],
    (20, 2): [224, 22582000], (27, 2): [440, 42746000], (36, 2): [454, 42306000], (45, 2): [345, 42306000],
    (20, 3): [445, 41362000], (27, 3): [895, 81954000], (36, 3): [906, 83778000], (45, 3): [681, 63024000]}
    
Pmax = 358 # MJ, maximum pipeline capacity
Pcost = 200000 # $/km, upgrade cost of pipeline per km
CMult = [1, 0.7]

m = Model("Upgrades")

# Variables
X = {(n, t): m.addVar() for n in N for t in T}
Y = {(e, t): m.addVar() for e in E for t in T}
W = {(o, s, t): m.addVar(vtype=GRB.BINARY) for o in O for s in S for t in T}
P = {(e, t): m.addVar(vtype=GRB.BINARY) for e in E for t in T}

# Objective
m.setObjective(quicksum(CMult[t] * W[o, s, t] * Upgrades[s, o][1] for o in O for s in S for t in T) 
               + quicksum(CMult[t] * P[e, t] * E[e] * Pcost for e in E for t in T),
               GRB.MINIMIZE)

# Constraints
for t in T:
    for n in N:
        ## Supply constraints
        if n in S:
            s = n
            # below reads as:   node output <= max_supply + all of the upgrades done so far * the upgrade capacity
            m.addConstr(X[s, t] <= S[s] + quicksum(W[o, s, j] * Upgrades[s, o][0] for o in O for j in T[:t+1]))
        else:
            m.addConstr(X[n, t] <= 0)
            
        # Flow constraint:
        m.addConstr(X[n, t] + quicksum(Y[e, t] for e in E if e[1] == n) == 
                    quicksum(Y[e, t] for e in E if e[0] == n) + demand[n, years[t]])

## Unique upgrade constraint
for s in S:
    m.addConstr(quicksum(W[o, s, t] for o in O for t in T) == 1)

## Pipeline upgrade constraint
for t in T:
    for e in E:
        # below reads as:   pipeflow at this time <= max pipeflow + sum of the pipeflow upgrades done so far
        m.addConstr(Y[e, t] <= Pmax * (1 + quicksum(P[e, j] for j in T[:t+1])))

for e in E:
    m.addConstr(quicksum(P[e, t] for t in T) <= 1)


# Optimise!
m.optimize()

print(m.objVal)