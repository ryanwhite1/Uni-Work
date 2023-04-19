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

N = range(len(nodes['Node'])) # number of nodes in the pipeline system
T = range(2) # number of time periods we're looking at
O = range(4) # number of options we have to upgrade (0th option is no upgrade)
F = range(3) # number of possible demand scenarios in 10 years


# E[i,j] gives the distance (km) from node i to node j
E = {}
for j in range(len(pipes['Pipeline'])):
    n1 = pipes['Node1'][j]
    n2 = pipes['Node2'][j]
    distance = math.hypot(nodes['X'][n1] - nodes['X'][n2], nodes['Y'][n1] - nodes['Y'][n2])
    E[n1, n2] = distance

demand = {}
years = ["Year5", "Year10"] # each time period we're looking at
for year in years:
    for n in N:
        demand[n, year] = nodes[year][n] # get the demand in a specific year at the specific node

S = {20: 458, 27: 897, 36: 912, 45: 685}      # supplying nodes. Format is node: MW

# Each upgrade option for each supplying node. Format is (node, option): [MW, $$$]
Upgrades = {(20, 0): [0, 0], (27, 0): [0, 0], (36, 0): [0, 0], (45, 0): [0, 0],
    (20, 1): [90, 9058000], (27, 1): [180, 17838000], (36, 1): [185, 18352000], (45, 1): [133, 13603000],
    (20, 2): [224, 22582000], (27, 2): [440, 42746000], (36, 2): [454, 42306000], (45, 2): [345, 42306000],
    (20, 3): [445, 41362000], (27, 3): [895, 81954000], (36, 3): [906, 83778000], (45, 3): [681, 63024000]}
    
Pmax = 358 # MJ, maximum pipeline capacity
Pcost = 200000 # $/km, upgrade cost of pipeline per km
CMult = [1, 0.7] # Cost multiplier for upgrading things now vs in 5 years; CMult[T]
DMult = [[1, 1, 1], [0.8, 1, 1.2]] # Demand multipliers for forecast demand in 10 years; DMult[T][F]

m = Model("Upgrades") # initialise model

# Variables
X = {(n, t, f): m.addVar() for n in N for t in T for f in F}
Y = {(e, t, f): m.addVar() for e in E for t in T for f in F}
W = {(o, s, t, f): m.addVar(vtype=GRB.BINARY) for o in O for s in S for t in T for f in F}
P = {(e, t, f): m.addVar(vtype=GRB.BINARY) for e in E for t in T for f in F}

# Objective
m.setObjective(quicksum(1/3 * (quicksum(CMult[t] * W[o, s, t, f] * Upgrades[s, o][1] for o in O for s in S for t in T) 
               + quicksum(CMult[t] * P[e, t, f] * E[e] * Pcost for e in E for t in T)) for f in F),
               GRB.MINIMIZE)

# Constraints
for f in F:
    for t in T:
        for n in N:
            ## Supply constraints
            if n in S:
                s = n
                # below reads as:   node output <= max_supply + all of the upgrades done so far * the upgrade capacity
                m.addConstr(X[s, t, f] <= S[s] + quicksum(W[o, s, j, f] * Upgrades[s, o][0] for o in O for j in T[:t+1]))
            else:
                m.addConstr(X[n, t, f] <= 0)
                
            # Flow constraint:
            m.addConstr(X[n, t, f] + quicksum(Y[e, t, f] for e in E if e[1] == n) == 
                        quicksum(Y[e, t, f] for e in E if e[0] == n) + DMult[t][f] * demand[n, years[t]])

## Unique upgrade constraint
for f in F:
    for s in S:
        m.addConstr(quicksum(W[o, s, t, f] for o in O for t in T) == 1)

## Pipeline upgrade constraints
for f in F:
    for t in T:
        for e in E:
            # below reads as:   pipeflow at this time <= max pipeflow + sum of the pipeflow upgrades done so far
            m.addConstr(Y[e, t, f] <= Pmax * (1 + quicksum(P[e, j, f] for j in T[:t+1])))
    for e in E: # max one upgrade!
        m.addConstr(quicksum(P[e, t, f] for t in T) <= 1)

## 5-Year Upgrade Constraints
for e in E:
    m.addConstr(quicksum(P[e, 0, f] for f in F) == len(F) * P[e, 0, 0])
for s in S:
    m.addConstr(quicksum(W[o, s, 0, f] for f in F for o in O) == len(F) * quicksum(W[o, s, 0, 0] for o in O))

## 10 vs 5 Year Upgrade Constraint
C = {}
for f in F:
    C[f] = m.addConstr(quicksum(W[o, s, 1, f] * Upgrades[s, o][1] for o in O for s in S) + quicksum(P[e, 1, f] * E[e] * Pcost for e in E)
                <= 2 * quicksum(W[o, s, 0, f] * Upgrades[s, o][1] for o in O for s in S) + quicksum(P[e, 0, f] * E[e] * Pcost for e in E))

# Optimise!
m.optimize()

print("Optimal solution:", round(m.objval, 0))

# Upgrade values
for f in F: 
    print("Scenario:", f)
    for t in T:
        print(years[t])
        for s in S:
            print([W[o, s, t, f].x for o in O])
        for e in E:
            if P[e, t, f].x == 1:
                print("Upgraded pipe linking:", e, "for cost:", E[e] * Pcost * CMult[t])
    print("")
    
for f in F:
    print(f"Slack in scenario {f} is ${round(C[f].slack, 0)}")






