from gurobipy import *

''' Part (a) Formulation

## -- Sets -- ##
T       -       Truck types
L       -       Lanes


## -- Data -- ##
LaneLength_l        -       length of lane l in L
Length_t            -       length of truck t in T
mass_t              -       mass of truck t in T
value_t             -       value of goods able to be carried by truck t in T
total_t             -       total number of trucks of type t in T
cap                 -       mass capacity of the ferry


## -- Variables -- ##
X_{tl}              -       number of trucks of type t in T being used in lane l in L


## -- Objective Value -- ##
max SUM_t (SUM_l value_t * X_{tl}))                 We want to maximise the value carried on the ferry overall from each truck


## -- Constraints -- ##
number constr:      SUM_l X_{tl} <= total_t                     for t in T          This is to ensure we don't use more trucks than we have
mass constr:        SUM_t (SUM_l X_{tl} * mass_t) <= cap                            This is to ensure we don't put too much mass on the ferry
length constr:      SUM_t (X_{tl} * length_t) <= LaneLength_l   for l in L          This is to ensure we don't have trucks spilling over the front/back of the ferry


'''
print("### --- Part A --- ### \n")
# Lanes
L = range(5)
LaneLength = [40, 40, 40, 40, 35]

# Truck types
Trucks = ["Van", "Small Truck", "Medium Truck", "Large Truck"]
T = range(len(Trucks))
Value = [450, 600, 1000, 1800]
Length = [4.5, 7, 10, 15] # metres
Mass = [1.5, 2.5, 5, 9] # tonnes
Total = [6, 8, 7, 9] # maximum number of truck type to load
Cap = 120           # maximum load of ferry. 

m = Model("Ferry")      # Initialise model

# Variable:
X = {(t, l): m.addVar(vtype=GRB.INTEGER) for t in T for l in L}

# Objective function:
m.setObjective(quicksum(X[t, l] * Value[t] for t in T for l in L), GRB.MAXIMIZE)

# Number constraint:
for t in T:
    m.addConstr(quicksum(X[t, l] for l in L) <= Total[t])
    
# Length constraint:
for l in L:
    m.addConstr(quicksum(X[t, l] * Length[t] for t in T) <= LaneLength[l])
    
# Mass constraint:
m.addConstr(quicksum(X[t, l] * Mass[t] for t in T for l in L) <= Cap)       
    
m.optimize()        # now optimize

for l in L:
    print(f"\nLane {l}:")
    print(f"Length used: {sum([X[t, l].x * Length[t] for t in T])} / {LaneLength[l]}m")
    for t in T:
        if X[t, l].x > 0:
            for i in range(int(X[t, l].x)):
                print(f"{Trucks[t]}")
print(f"\nTotal mass used is {sum([X[t, l].x * Mass[t] for l in L for t in T])}")
print(f"We expect to transport ${m.objVal} worth of goods in the first trip.")





# now onto part b
''' Part (b) Formulation
## -- New Set -- ##
Sides                   -       Two sides of the ferry, L and R with lanes [0, 1] and [3, 4] respectively 


## -- New Data -- ##
DistanceMult_l          -       distance multiplier for how far a lane l in L is away from the center of the ferry
side_s                  -       which lanes are in side s in S


## -- New Constr -- ##
Balance constr:     SUM_t (SUM_{l in side_0} X_{tl} * mass_t * DistanceMult_l - SUM_{l in side_1} X_{tl} * mass_t * DistanceMult_l) <= 0.05 * SUM_t (SUM_{l in side_s} X_{tl} * mass_t * DistanceMult_l)        for s in S

the above constraint ensures that the mass on one side is no more than 5% of the mass on the other side of the ferry

'''
print("\n\n\n### --- Part B --- ###\n")

S = range(2)        # side set
sides = [[0, 1], [3, 4]]        # lanes in each side
mult = [2, 1, 0, 1, 2]  # distance multipliers for mass calculation

# balance constraint:
for s in S:
    side = sides[s]
    m.addConstr(quicksum(X[t, l] * Mass[t] * mult[l] if l in sides[0] else -X[t, l] * Mass[t] * mult[l] for t in T for l in L) <= 0.05 * quicksum(X[t, l] * Mass[t] * mult[l] for t in T for l in side))


m.optimize() # now optimize!

for l in L:
    print(f"\nLane {l}:")
    print(f"Length used: {sum([X[t, l].x * Length[t] for t in T])} / {LaneLength[l]}m")
    print(f"Weighted mass in lane is {sum([X[t, l].x * Mass[t] * mult[l] for t in T])}kg")
    for t in T:
        if X[t, l].x > 0:
            for i in range(int(X[t, l].x)):
                print(f"{Trucks[t]}")
print(f"\nTotal mass used is {sum([X[t, l].x * Mass[t] for l in L for t in T])}")
print(f"We expect to transport ${m.objVal} worth of goods in the first trip.")
