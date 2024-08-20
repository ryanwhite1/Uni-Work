def int_orbit(a,v0,alpha):
   G = 9.81

   vx = v0*math.cos(alpha/180.0*math.pi)
   vy = v0*math.sin(alpha/180.0*math.pi)

   x = 0.0
   y = 0.0
   t = 0.0
   dt = 0.0001

   while (x<a):
     x  += dt*vx
     y  += 0.5*dt*vy   ### Using Leapfrog for the integration
     vy -= dt*G
     y  += 0.5*dt*vy
     t  += dt

   return y,t


import numpy as np
import math
import sys

# Ask user for a few numbers

a  = float(input("Enter distance to target (in m): "))
b  = float(input("Enter height of target (in m): "))
v0 = float(input("Enter muzzle velocity (in m/s): "))

alphal = 0.0
alphah = 70.0 

bfin = 0.0   # Initialize bfin 

nint = 1

while abs(bfin-b)>0.01:
   alpha = (alphal+alphah)/2.0
   bfin,tfin = int_orbit(a,v0,alpha)

   print("Nint =",'{:3d}'.format(nint)," alpha = ",'{:6.3f}'.format(alpha)," fin height = ",'{:7.3f}'.format(bfin))
 
   if bfin<b: 
     alphal=alpha
   else:
     alphah=alpha

   nint += 1

   if (nint>30):
     sys.exit("No solution found within 30 iterations !")
     


print("Correct angle: ",alpha," Time to hit target: ",tfin)
