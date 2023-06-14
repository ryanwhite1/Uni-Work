''' Question 2 Formulation
## -- Sets -- ##
N               -       customer nodes


## -- Data -- ##
demand_n        -       the demand of cylinders by customer n in N
dist_{n1, n2}   -       travel time between nodes n1 and n2         n1, n2 in N
maxtime         -       the time since t=0 that the driver must return to the depot by


## -- Stages -- ##
t               -       current time

## -- States -- ##
l_t               -       previously visited customers (nodes) of delivery driver

## -- Actions -- ##
a_t             -       next location (customer node) to move to


## -- Value Function -- ##
V(t, l_t)   =   maximum number of gas cylinders we can deliver before we need to return to the depot if we start at
                time t and location l_t 
            =   max_[a_t in N\l_t if t + dist[l_t][a_t] + dist[a_t][0] <= maxtime] {demand_{l_t} + V(t + dist_{l_t, a_t}, l_t + a_t)}

Terminating case:
      V(t, l_t) = 0 if   
We seek V(0, [0])
'''



N = range(10)
depot = 0
demand = [0, 3, 1, 2, 1, 2, 2, 2, 3, 2]
maxtime = 6 * 60

# dist[i][j] gives the travel time (mins) between i and j
dist = [
	[0, 30, 50, 120, 140, 180, 120, 210, 160, 100],
	[30, 0, 50, 100, 110, 160, 120, 190, 140, 70],
	[50, 50, 0, 70, 100, 130, 70, 160, 110, 60],
	[120, 100, 70, 0, 60, 60, 60, 90, 40, 30],
	[140, 110, 100, 60, 0, 120, 120, 150, 100, 40],
	[180, 160, 130, 60, 120, 0, 100, 30, 50, 90],
	[120, 120, 70, 60, 120, 100, 0, 130, 50, 90],
	[210, 190, 160, 90, 150, 30, 130, 0, 80, 120],
	[160, 140, 110, 40, 100, 50, 50, 80, 0, 70],
	[100, 70, 60, 30, 40, 90, 90, 120, 70, 0]
]

def V(t, l):
    for n in N:     # let's check what nodes we can viably go to. 
        if n not in [l]:
            A = [j for j, T in enumerate(dist[n]) if T + t + dist[j][0] <= maxtime]
    if not A:
        return (0, 0)
    else:
        return max([(demand[a] + V(t + dist[l[-1]][a], l + [a])[0], a) for a in N if a not in l])

print(f"Optimal number of cylinders delivered is {V(0, [0])[0]}")
print(f"Start at node 0.")
currtime, currlocs = 0, [0]
while currtime <= maxtime:
    print(f"Deliver {demand[currlocs[-1]]} cylinders at this location.")
    deliv, nextn = V(currtime, currlocs)
    print(f"Next, start going to node {nextn} at time {currtime}.")
    currtime += dist[currlocs[-1]][nextn]
    currlocs += [nextn]

