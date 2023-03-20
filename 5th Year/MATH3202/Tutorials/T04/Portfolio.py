# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 07:31:49 2023

@author: ryanw
"""

from gurobipy import *

P = {"Cars Ger": 0.103, 
           "Cars Jap": 0.101, 
           "Comp USA": 0.118, 
           "Comp Sing": 0.114, 
           "App Eur": 0.127, 
           "App Asia": 0.122, 
           "Ins Ger": 0.095, 
           "Ins USA": 0.099, 
           "Short Bonds": 0.036, 
           "Medium Bonds": 0.042}

# P = range(len(returns))

m = Model("Portfolio")

X = {p: m.addVar() for p in P}

m.setObjective(quicksum(P[p] * X[p] for p in P), GRB.MAXIMIZE)

## Constraints
C = {"Tot": m.addConstr(quicksum(X[p] for p in P) == 100000),
     "Cars": m.addConstr(quicksum(X[p] for p in P if "Cars" in p) <= 30000),
     "Comp": m.addConstr(quicksum(X[p] for p in P if "Comp" in p) <= 30000),
     "App": m.addConstr(quicksum(X[p] for p in P if "App" in p) <= 20000),
     "Ins": m.addConstr(quicksum(X[p] for p in P if "Ins" in p) >= 20000),
     "Bonds": m.addConstr(quicksum(X[p] for p in P if "Bonds" in p) >= 25000),
     "Short/Med": m.addConstr(X["Short Bonds"] >= 0.4 * X["Medium Bonds"]),
     "Ger": m.addConstr(quicksum(X[p] for p in P if "Ger" in p) <= 50000),
     "USA": m.addConstr(quicksum(X[p] for p in P if "USA" in p) <= 40000)}

m.optimize()

print("Earnings =", m.objVal)
print("Average Earnings =", m.objVal / 100000 * 100)

print("### Portfolio ###")
for p in P:
    print(p, X[p].x)
    
print("### Duals ###")
for k in C:
    print(k, C[k].pi, C[k].Slack, C[k].SARHSLow, C[k].RHS, C[k].SARHSUp)
    
print("### Variable Sensitivity ###")
for p in P:
    print(p,  X[p].rc, X[p].SAObjLow, X[p].obj, X[p].SAObjUp)