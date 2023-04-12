from gurobipy import *

# Sets
Quarters = ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8"]
Juices = ["Orange","Orange and Mango", "Breakfast", "Tropical", "Guava Delight", "Orchard Medley", "Strawberry Surpise" ]
Fruits = ["Orange","Apple","Mango", "Pineapple", "Passionfruit", "Guava", "Strawberry"]


T = range(len(Quarters)) 
J = range(len(Juices))
G = J[-3:]
F = range(len(Fruits))

# Data

# Maximum demand (kL) [Q][J]
Demand = [
        [538,174,370,243,244,1098,662],
        [895,373,780,531,479,622,744],
        [1412,538,1096,846,576,652,541],
        [1102,407,900,624,309,860,432],
        [576,229,447,376,246,1168,543],
        [1005,409,924,622,420,640,720],
        [1330,569,1146,833,497,585,516],
        [1160,400,793,679,306,870,478]
         ]

# Cost of fruit ($/kL) [F]
Cost = [946,620,1300,800,1500,710,1370]

# Quantity of fruit needed for juice [J][F]
Blend = [
     [1,0,0,0,0,0,0],
     [0.9,0,0.1,0,0,0,0],
     [0.15,0.55,0.02,0.28,0,0,0],
     [0.04,0.65,0,0.3,0.01,0,0],
     [0,0.8,0,0.1,0,0.1,0],
     [0.45,0.5,0.05,0,0,0,0],
     [0,0.9,0,0,0,0.02,0.08]
      ]
      
# Orange juice availability (kL) [Q]
FCOJ = [1000,2000,2600,2500,1300,2200,2650,2300]

# Selling price ($/kL)
Price = 1500


m = Model("Juices")

# Variables
X = {(j, t): m.addVar() for j in J for t in T}
Y = {(f, t): m.addVar(vtype=GRB.INTEGER) for f in F for t in T}
Z = {(g, t): m.addVar(vtype=GRB.BINARY) for g in G for t in T}


# Objective
m.setObjective(quicksum(Price * X[j, t] for j in J for t in T) - 
               quicksum(Cost[0] * Blend[j][0] * X[j, t] for j in J for t in T) - 
               quicksum(Cost[f] * 10 * Y[f, t] for f in F if f > 0 for t in T),
               GRB.MAXIMIZE)


# Constraints

# Limit on Demand
for j in J:
    for t in T:
        m.addConstr(X[j, t] <= Demand[t][j])
for g in G:
    for t in T:
        m.addConstr(X[g, t] <= Demand[t][g] * Z[g, t])
# Gourmet constraint
for t in T:
    m.addConstr(quicksum(Z[g, t] for g in G) <= 2)

# Limit on FCOJ
for t in T:
    m.addConstr(quicksum(Blend[j][0] * X[j, t] for j in J) <= FCOJ[t])
    
# Limit on fruit used
for f in F[1:]:
    for t in T:
        m.addConstr(quicksum(Blend[j][f] * X[j, t] for j in J) <= 10 * Y[f, t])
    
m.optimize()

print("Max profit is:", m.objVal)
print("Sales")
for t in T:
    print([round(X[j, t].x, 1) for j in J])
print("FCOJ")
for t in T:
    print(FCOJ[t], sum(Blend[j][0] * X[j, t].x for j in J))






