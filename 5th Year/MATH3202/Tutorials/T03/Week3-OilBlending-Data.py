from gurobipy import *

# Sets
Oils = ["Veg 1", "Veg 2", "Oil 1", "Oil 2", "Oil 3"]
O = range(len(Oils))
V = [i for i in O if Oils[i][0] == 'V']
N = [i for i in O if Oils[i][0] != 'V']
Months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
T = range(len(Months))

# Data
h = [8.8, 6.1, 2.0, 4.2, 5.0]
c = [[110, 130, 110, 120, 100,  90], 
     [120, 130, 140, 110, 120, 100],
     [130, 110, 130, 120, 150, 140], 
     [110,  90, 100, 120, 110,  80], 
     [115, 115,  95, 125, 105, 135]]
MaxV = 200
MaxN = 250
Sell = 150
MinH = 3
MaxH = 6
MaxStore = 1000
CStore = 5
Initial = 500

m = Model("Oils")

X = {(i, t): m.addVar() for i in O for t in T}
Y = {(i, t): m.addVar() for i in O for t in T}
S = {(i, t): m.addVar() for i in O for t in T}
    

m.setObjective(quicksum((Sell * X[i, t] - c[i][t] * Y[i, t] - CStore * S[i, t]) for i in O for t in T), GRB.MAXIMIZE)

m.addConstr(quicksum(X[i, t] * (MinH - h[i]) for i in O for t in T) <= 0)
m.addConstr(quicksum(X[i, t] * (h[i] - MaxH) for i in O for t in T) <= 0)

for t in T:
    m.addConstr(quicksum(X[i, t] for i in V) <= MaxV)
    m.addConstr(quicksum(X[i, t] for i in N) <= MaxN)

for i in O:
    for t in T:
        m.addConstr(S[i, t] <= MaxStore)
        if t > 0:
            m.addConstr(S[i, t] == S[i, t - 1] + Y[i, t] - X[i, t])
        else:
            m.addConstr(S[i, t] == Initial + Y[i, t] - X[i, t])
    m.addConstr(S[i, T[-1]] >= Initial)

m.optimize()

# for n in O:
#     print(f"{Oils[n]} = {X[n].x}")
