# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 15:25:43 2023

@author: ryanw
"""

from gurobipy import *
import pandas as pd
import math

nodes = pd.read_csv("nodes.csv")
pipes = pd.read_csv("pipelines.csv")



N = range(len(nodes['Node']))

### --- INITIAL COMMUNICATIONS --- ###
demand = [nodes['Demand'][j] for j in N]

# supply and cost for each supplier node
supply = {20: 458, 27: 897, 36: 912, 45: 685} # MJ
cost = {20: 79, 27: 63, 36: 71, 45: 81} # $/MJ

# E[i,j] gives the distance (km) from node i to node j
E = {}
for j in range(len(pipes['Pipeline'])):
    n1 = pipes['Node1'][j]
    n2 = pipes['Node2'][j]
    distance = math.hypot(nodes['X'][n1] - nodes['X'][n2], nodes['Y'][n1] - nodes['Y'][n2])
    E[n1,n2] = distance
    
m = Model("GasPipes")

# Variables
Y = {} # production in each node
for n in N:
    Y[n] = m.addVar()
    
X = {}
for e in E:
    X[e] = m.addVar()
    
m.setObjective(quicksum(cost[n] * Y[n] for n in N if n in cost) + 
               quicksum(0.01 * X[e] * E[e] for n in N for e in E if e[0] == n)
               , GRB.MINIMIZE)

# Constraints
## Supply Constraint
for n in N:
    if n in supply:
        m.addConstr(Y[n] <= supply[n])
    else:
        m.addConstr(Y[n] <= 0)
## Balance Constraint
for n in N:
    m.addConstr(Y[n] + quicksum(X[e] for e in E if e[1] == n) == 
                quicksum(X[e] for e in E if e[0] == n) + demand[n])
## Pipeline Capacity Constraint
for e in E:
    m.addConstr(X[e] <= 489)

m.optimize()

for n in N:
    if Y[n].x > 0:
        print("Generator", n, "=", Y[n].x)
        
        
        
        
        
### --- THIRD COMMUNICATION --- ###
import numpy as np

nodes2 = pd.read_csv("nodes2.csv")

# supply and cost for each supplier node
supply = {20: 458, 27: 897, 36: 912, 45: 685} # MJ
cost = {20: 79, 27: 63, 36: 71, 45: 81} # $/MJ

# E[i,j] gives the distance (km) from node i to node j
E = {}
for j in range(len(pipes['Pipeline'])):
    n1 = pipes['Node1'][j]
    n2 = pipes['Node2'][j]
    distance = math.hypot(nodes['X'][n1] - nodes['X'][n2], nodes['Y'][n1] - nodes['Y'][n2])
    E[n1,n2] = distance

costs = np.zeros(14)

for i in range(14):
    demand = [nodes2[f'D{i}'][j] for j in N]
    
    m = Model("GasPipes")
    
    # Variables
    Y = {} # production in each node
    for n in N:
        Y[n] = m.addVar()
        
    X = {}
    for e in E:
        X[e] = m.addVar()
        
    m.setObjective(quicksum(cost[n] * Y[n] for n in N if n in cost) + 
                   quicksum(0.01 * X[e] * E[e] for n in N for e in E if e[0] == n)
                   , GRB.MINIMIZE)
    
    # Constraints
    ## Supply Constraint
    for n in N:
        if n in supply:
            m.addConstr(Y[n] <= supply[n])
        else:
            m.addConstr(Y[n] <= 0)
    ## Balance Constraint
    for n in N:
        m.addConstr(Y[n] + quicksum(X[e] for e in E if e[1] == n) == 
                    quicksum(X[e] for e in E if e[0] == n) + demand[n])
    ## Pipeline Capacity Constraint
    for e in E:
        m.addConstr(X[e] <= 489)
    
    m.optimize()
    
    costs[i] = m.objVal
    
    # for n in N:
    #     if Y[n].x > 0:
    #         print("Generator", n, "=", Y[n].x)
    
print(f"Total two week cost:", sum(costs))