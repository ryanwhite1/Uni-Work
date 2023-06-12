# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 23:16:23 2023

@author: ryanw
"""
import numpy as np
import matplotlib.pyplot as plt

class Body(object):
    def __init__(self, mass, r, dr, newt=False):
        self.mass = mass
        self.r = r
        self.dr = dr
        self.path_r = np.array(r[0])
        self.path_theta = np.array(r[1])
        self.path_phi = np.array(r[2])
        self.borked = False
        self.newt = newt
    
    def update_pos(self, step, M):
        if self.borked: 
            pass
        else:
            if self.r[0] > 2 * M:
                # self.r[0] = 0
                self.r = self.r + step * self.dr
            if self.r[0] <= 2 * M:
                self.borked = True
                self.r = np.array([0, 0, 0])
            self.path_r = np.append(self.path_r, self.r[0])
            self.path_theta = np.append(self.path_theta, self.r[1])
            self.path_phi = np.append(self.path_phi, self.r[2])
    
    def angular_momentum(self):
        self.l = self.r[0]**2 * (np.sin(self.r[1]))**2 * self.dr[2]
    
    def dVdr(self, M):
        return (self.r[0] - M) * (np.sin(self.r[1]))**4 * self.dr[2]**2 + M / self.r[0]**2
    def dVdt(self, M):
        return 2 * self.r[0] * (np.sin(self.r[1]))**3 * np.cos(self.r[1]) * (self.r[0] - 2 * M) * self.dr[2]**2
    def dVdp(self):
        return 0
    
    def update_velocity(self, step, M):
        if self.borked:
            pass
        else:
            self.angular_momentum()
            acc = - np.array([self.dVdr(M), 0, self.l / (self.r[0]**2 * (np.sin(self.r[1]))**2)])
            
            self.dr = self.dr + step * acc
        
    def cartesian(self, M):
        x = self.path_r * np.sin(self.path_theta) * np.cos(self.path_phi)
        y = self.path_r * np.sin(self.path_theta) * np.sin(self.path_phi)
        z = self.path_r * np.cos(self.path_theta)
        return x, y, z 
        
M = 30

b1 = Body(M, np.array([0, 0, 0]), np.array([0, 0, 0]))
b2 = Body(0, np.array([3 * M, np.pi / 2, 0]), np.array([100000, 0, 10000]))
#b3 = Body("Big", 10, 'g', np.array([2,5,0]), np.array([0,0,0]))
bodies = [b1, b2]

step = 0.00002
num_doops = 115000
for i in range(num_doops):
    b2.update_pos(step, M)
    b2.update_velocity(step, M)

x, y, z = b2.cartesian(M)

plt.plot(x, y)
