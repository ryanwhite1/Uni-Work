# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 22:41:35 2023

@author: ryanw
"""
import numpy as np
import matplotlib.pyplot as plt

G = 6.67 * 10**-11
c = 299792458
def cot(x):
    return 1 / np.tan(x)

def ddt(r, dt, dr):
    return - (2 * M / r**2) * (1 - 2 * M / r)**-1 * dt * dr

def ddphi(r, theta, dr, dtheta, dphi):
    return - 1 / r * dphi * dr - 2 * cot(theta) * dtheta * dphi

def ddtheta(r, theta, dr, dtheta, dphi):
    return r * dphi**2 * np.sin(theta) * np.cos(theta) - 1 / r * dr * dtheta

def ddr(r, theta, dt, dr, dtheta, dphi):
    X = 1 - 2 * M / r
    a = -(2 * M / r) * dt**2 
    # b = (2 * M / r**2) * X**-2 * dr**2
    b = 0 
    c = r * dtheta**2
    d = r * (np.sin(theta))**2 * dphi**2
    return X * (a + b + c + d)

def dtstep(dt, h, r, dr):
    return dt + h * ddt(r, dt, dr)
def dphistep(dphi, h, r, theta, dr, dtheta):
    return dphi + h * ddphi(r, theta, dr, dtheta, dphi)
def dthetastep(dtheta, h, r, theta, dr, dphi):
    return dtheta + h * ddtheta(r, theta, dr, dtheta, dphi)
def drstep(dr, h, r, theta, dt, dtheta, dphi):
    return dr + h * ddr(r, theta, dt, dr, dtheta, dphi)

def ddrNewt(r, theta, dtheta, dphi):
    # return r * dtheta**2 + r * (np.sin(theta))**2 * dphi**2
    return - M / r
def ddthetaNewt(r, theta, dr, dtheta, dphi):
    return dphi**2 * np.sin(theta) * np.cos(theta) - 1/r * dr * dtheta
def ddphiNewt(r, theta, dr, dtheta, dphi):
    return - 1 / r * dphi * dr - 2 * cot(theta) * dtheta * dphi

# def ddrNewt(r, theta, dtheta, dphi):
#     return - M / r**2 + dtheta + dphi

def dphistepNewt(dphi, h, r, theta, dr, dtheta):
    return dphi + h * ddphiNewt(r, theta, dr, dtheta, dphi)
def dthetastepNewt(dtheta, h, r, theta, dr, dphi):
    return dtheta + h * ddthetaNewt(r, theta, dr, dtheta, dphi)
def drstepNewt(dr, h, r, theta, dt, dtheta, dphi):
    return dr + h * ddrNewt(r, theta, dtheta, dphi)

M = 1 / 40
steps = int(1e5)
h = 0.01

t = np.ones(steps); dt = np.ones(steps);
r = np.ones(steps); dr = np.ones(steps);
theta = np.ones(steps); dtheta = np.ones(steps);
phi = np.ones(steps); dphi = np.ones(steps);

## interesting trajectory:
dr *= 0; dtheta *= 0; dphi *= 0.09274
r *= 100 * M; theta *= np.pi / 2; phi *= - np.pi / 2

# circular light orbit
# dr *= 0; dtheta *= 0; dphi *= 5.6011203361120383
# r *= 3 * M; theta *= np.pi / 2; phi *= - np.pi / 2

dt = (1 - 2 * M / r)**(-1/2) * np.sqrt(1 + (1 - 2 * M / r)**-1 * dr**2 + r**2 * dtheta**2 + r**2 * (np.sin(theta))**2 * dphi**2)

# drNewt = np.copy(dr); dthetaNewt = np.copy(dtheta); dphiNewt = 0.001 * np.copy(dphi); #dtNewt = np.ones(steps)
# rNewt = np.copy(r); thetaNewt = np.copy(theta); phiNewt = np.copy(phi); tNewt = np.copy(t)

for i in range(1, steps):
    t[i] = t[i - 1] + h * dt[i - 1]
    r[i] = r[i - 1] + h * dr[i - 1]
    theta[i] = theta[i - 1] + h * dtheta[i - 1]
    phi[i] = phi[i - 1] + h * dphi[i - 1]
    dt[i] = dtstep(dt[i - 1], h, r[i - 1], dr[i - 1])
    dr[i] = drstep(dr[i - 1], h, r[i - 1], theta[i - 1], dt[i - 1], dtheta[i - 1], dphi[i - 1])
    dtheta[i] = dthetastep(dtheta[i - 1], h, r[i - 1], theta[i - 1], dr[i - 1], dphi[i - 1])
    dphi[i] = dphistep(dphi[i - 1], h, r[i - 1], theta[i - 1], dr[i - 1], dtheta[i - 1])
    
    # tNewt[i] = tNewt[i - 1] + h
    # rNewt[i] = rNewt[i - 1] + h * drNewt[i - 1]
    # thetaNewt[i] = thetaNewt[i - 1] + h * dthetaNewt[i - 1]
    # phiNewt[i] = phiNewt[i - 1] + h * dphiNewt[i - 1]
    # drNewt[i] = drstepNewt(drNewt[i - 1], h, rNewt[i - 1], thetaNewt[i - 1], 1, dthetaNewt[i - 1], dphiNewt[i - 1])
    # dthetaNewt[i] = dthetastepNewt(dthetaNewt[i - 1], h, rNewt[i - 1], thetaNewt[i - 1], drNewt[i - 1], dphiNewt[i - 1])
    # dphiNewt[i] = dphistepNewt(dphiNewt[i - 1], h, rNewt[i - 1], thetaNewt[i - 1], drNewt[i - 1], dthetaNewt[i - 1])
    
    if r[i] <= 2 * M:
        r[i:] = 0
        break
    if phi[i] > 2 * np.pi:
        phi[i] += - 2 * np.pi 

x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)

# xNewt = rNewt * np.sin(thetaNewt) * np.cos(phiNewt)
# yNewt = rNewt * np.sin(thetaNewt) * np.sin(phiNewt)
# zNewt = rNewt * np.cos(thetaNewt)

x /= M; y /= M; z /= M 
# xNewt /= M; yNewt /= M; zNewt /= M 

fig, ax = plt.subplots()
ax.plot(x, y, c='tab:blue', label="GR")
# ax.plot(xNewt, yNewt, c='tab:orange', label="Newt")
ax.scatter(0, 0, c='k')
ax.set_aspect('equal')
ax.legend()