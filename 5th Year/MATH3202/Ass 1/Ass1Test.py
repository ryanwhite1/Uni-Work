# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 15:25:43 2023

@author: ryanw
"""

from gurobipy import *
import pandas as pd
import math

# Sets / Data
nodes = pd.read_csv("nodes.csv")
nodes2 = pd.read_csv("nodes2.csv")
pipes = pd.read_csv("pipelines.csv")

N = range(len(nodes['Node']))
T = range(14) # number of days we're looking at

# supply and cost for each supplier node
supply = {20: 458, 27: 897, 36: 912, 45: 685} # MJ
cost = {20: 79, 27: 63, 36: 71, 45: 81} # $/MJ
distC = 0.01 # $/MJ/km
MaxF = 489 # MJ/day
MaxS = 11265 # MJ over 2 weeks
imCost = 0.1 # $/MJ due to imbalance in each pipe

# mickey's data
supply = { 1: 313, 5: 754, 11: 750, 42: 557 }
cost = { 1: 71, 5: 85, 11: 65, 42: 75 }
MaxF = 348
MaxS = 9378
nodes2 = pd.read_csv("mickey_nodes2.csv")
pipes = pd.read_csv("mickey_pipelines.csv")
nodes = nodes2[['Node', 'X', 'Y']].copy()

# E[i,j] gives the distance (km) from node i to node j
E = {}
for j in range(len(pipes['Pipeline'])):
    n1 = pipes['Node1'][j]
    n2 = pipes['Node2'][j]
    distance = math.hypot(nodes['X'][n1] - nodes['X'][n2], nodes['Y'][n1] - nodes['Y'][n2])
    E[n1,n2] = distance

demand = {}
for t in T:
    demand[t] = [nodes2[f'D{t}'][j] for j in N]

m = Model("GasPipes")

# Variables
Y = {(n, t): m.addVar() for n in N for t in T} # production in each node
X = {(e, t): m.addVar() for e in E for t in T} # net gas transmission on edge between nodes
I = {(e, t): m.addVar(lb = -GRB.INFINITY) for e in E for t in T} # imbalance in each pipe for each day
AI = {(e, t): m.addVar() for e in E for t in T} # absolute value of imbalance for each day
    
# Objective
m.setObjective(quicksum(cost[n] * Y[n, t] for n in N if n in cost for t in T) + 
               quicksum(distC * X[e, t] * E[e] for n in N for e in E if e[0] == n for t in T) + 
               quicksum(imCost * AI[e, t] for e in E for t in T)
               , GRB.MINIMIZE)

# Constraints
## Capacity Constraint
for t in T:
    for n in N:
        if n in supply:
            m.addConstr(Y[n, t] <= supply[n])
        else:
            m.addConstr(Y[n, t] <= 0)
## Balance Constraint
for t in T:
    for n in N:
        if t > 0:
            m.addConstr(Y[n, t] + quicksum(X[e, t] + I[e, t] for e in E if e[1] == n) == 
                        quicksum(X[e, t] for e in E if e[0] == n) + demand[t][n])
        else:
            m.addConstr(Y[n, t] + quicksum(X[e, t] + I[e, t] for e in E if e[1] == n) == 
                        quicksum(X[e, t] for e in E if e[0] == n) + demand[t][n])
    
## Pipeline Capacity Constraint
for t in T:
    for e in E:
        m.addConstr(X[e, t] <= MaxF)
        
## Supplier Constraint
for n in N:
    if n in supply:
        m.addConstr(quicksum(Y[n, t] for t in T) <= MaxS)

## Imbalance Constraints
for e in E:
    m.addConstr(I[e, T[0]] == 0)
    m.addConstr(I[e, T[-1]] == 0)
    m.addConstr(quicksum(I[e, t] for t in T) == 0)

## Abs Value Constraint
for e in E:
    for t in T:
        m.addConstr(AI[e, t] >= I[e, t])
        m.addConstr(AI[e, t] >= -I[e, t])
        m.addConstr(AI[e, t] >= 0)

m.optimize()

# for e in E:
#     print(I[e, 5].x)
