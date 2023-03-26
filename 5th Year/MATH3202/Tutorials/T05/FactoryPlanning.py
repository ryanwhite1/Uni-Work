from gurobipy import *

# Data
profit = [10, 6, 8, 4, 11, 9, 3]
P = range(len(profit))

Machines = ["Grinding","VDrilling","HDrilling","Boring","Planing"]
n = [4, 2, 3, 1, 1]
M = range(len(n))

# usage[P][M]
usage = [
    [0.5, 0.1, 0.2, 0.05, 0.00],
    [0.7, 0.2, 0.0, 0.03, 0.00],
    [0.0, 0.0, 0.8, 0.00, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.00],
    [0.3, 0.0, 0.0, 0.10, 0.05],
    [0.2, 0.6, 0.0, 0.00, 0.00],
    [0.5, 0.0, 0.6, 0.08, 0.05]
    ]

# months
T = range(6)

# maintenance[T][M]
maint = [
    [1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1]
    ]

# market[P][T]
market = [
    [ 500, 600, 300, 200,   0, 500],
    [1000, 500, 600, 300, 100, 500],
    [ 300, 200,   0, 400, 500, 100],
    [ 300,   0,   0, 500, 100, 300],
    [ 800, 400, 500, 200,1000,1100],
    [ 200, 300, 400,   0, 300, 500],
    [ 100, 150, 100, 100,   0,  60]
    ]

maxstore = 100
storecost = 0.5
endstore = 50
monthhours = 16*24

fp = Model("Factory Planning")

## VARIABLES
X = {(p, t): fp.addVar(vtype=GRB.INTEGER) for p in P for t in T} # produce
S = {(p, t): fp.addVar(vtype=GRB.INTEGER) for p in P for t in T} # stock
Y = {(p, t): fp.addVar(vtype=GRB.INTEGER) for p in P for t in T} # sold
Z = {(t, m): fp.addVar(vtype=GRB.INTEGER) for t in T for m in M} # number of machine m to maintain in month P

## OBJECTIVE
fp.setObjective(quicksum(quicksum(profit[p] * Y[p, t] - storecost * S[p, t] for t in T) for p in P), GRB.MAXIMIZE)

## CONSTRAINTS
# Machine constraint
for t in T:
    for m in M:
        fp.addConstr(quicksum(usage[p][m] * X[p, t] for p in P) <= monthhours * (n[m] - Z[t, m]))

# Market constraint
for p in P:
    for t in T:
        fp.addConstr(Y[p, t] <= market[p][t])

# Storage flow constraint
for p in P:
    for t in T:
        if t > 0:
            fp.addConstr(S[p, t] == S[p, t - 1] + X[p, t] - Y[p, t])
        else:
            fp.addConstr(S[p, t] == X[p, t] - Y[p, t])

# Max Storage Constraint
for p in P:
    for t in T:
        fp.addConstr(S[p, t] <= maxstore)

# Final Storage Constraint
for p in P:
    fp.addConstr(S[p, T[-1]] >= endstore)

# Non-negativity constraints
for p in P:
    for t in T:
        fp.addConstr(X[p, t] >= 0)
        fp.addConstr(S[p, t] >= 0)
        fp.addConstr(Y[p, t] >= 0)
        
# Maintenance constraint
for m in M:
    fp.addConstr(quicksum(Z[t, m] for t in T) == sum(maint[t][m] for t in T))

# Total maintenance constraint
for t in T:
    fp.addConstr(quicksum(Z[t, m] for m in M) <= 3)
        
fp.optimize()

for m in M:
    print([abs(Z[t, m].x) for t in T], Machines[m])



