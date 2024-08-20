import numpy as np
import matplotlib.pyplot as plt

# Ask user for a few numbers

a  = 500.0
b  = 100.0

G = 9.81

# Use 1000 teps for the solution
nstep = 1000

#tend = 1.4937 # for a=100
tend = 5.6099  # for a=500
dt = tend/nstep 

# in order to plot solution build x array
xint=np.linspace(0, (nstep - 1) * a/nstep, nstep)

avec = np.full(nstep-1, 1)
bvec = np.full(nstep, -2)
cvec = np.full(nstep-1, 1)
dvec = np.full(nstep,-dt*dt*G) 

# add final height to last element of rhs vector
dvec[-1]=dvec[-1]-b

mata = np.diag(avec, -1) + np.diag(bvec, 0) + np.diag(cvec, 1)
matinv = np.linalg.inv(mata)
yint = matinv @ dvec

xvel = a/tend
yvel = (yint[1]-yint[0])/dt 
v0 = np.sqrt(xvel*xvel++yvel*yvel)
print ("Initial velocity: ",v0)

plt.plot(xint,yint)
plt.xlabel("X [m]")
plt.ylabel("Y [m]")

plt.show()
