# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:50:11 2023

@author: ryanw
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

G = 6.6743 * 10**-11
c = 299792458

def cot(x):
    return np.cos(x) / np.sin(x)

class Body(object):
    def __init__(self, r, dr, M):
        self.r = r
        self.dr = dr
        self.M = M
        self.angMom = self.r[1]**2 * (np.sin(self.r[2]))**2 * self.dr[3]
        self.epsilon = 0.5 * self.dr[1]**2 + self.Veff()
        self.rest_energy = np.sqrt(2 * self.epsilon + 1)
        v = self.velMag()
        self.pathv = np.array([v])
        
        self.pathr = np.array([self.r])
        self.pathdr = np.array([self.dr])
        self.borked = False
    
    def Veff(self):
        return (- self.M / self.r[1]) + self.angMom**2 * (1 / (2 * self.r[1]**2) - self.M / self.r[1]**3)
    
    def dtdtau(self):
        # based on conservation of energy
        return self.rest_energy / (1 -  2 * self.M / self.r[1])
    def dphidtau(self):
        return self.angMom / (self.r[1]**2 * (np.sin(self.r[2]))**2)
    def drdtau(self):
        return np.sqrt(2 * (self.epsilon - self.Veff()))
    
    def ddrddtau(self):
        # X = (1 - 2 * self.M / self.r[1])
        # a = (2 * self.M / self.r[1]) * X * self.dtdtau()**2
        # b = - (2 * self.M / self.r[1]**2) * X**-1 * self.dr[1]**2
        # # b = 0
        # c = - self.r[1] * X * self.dr[2]**2
        # d = - self.r[1] * X * (np.sin(self.r[2]))**2 * self.dr[3]**2
        # return a + b + c + d
        # return - (self.M / self.r[1]**2 + self.dr[3]**2 * (np.sin(self.r[2]))**4 * (self.r[1] - self.M))
        
        # below func found by differentiating the effective potential wrt to r
        return -(self.angMom**2 * (3 * self.M - self.r[1]) + self.M * self.r[1]**2) / self.r[1]**4
    def ddthetaddtau(self):
        # below found by geodesic equation
        return  self.r[1] * self.dr[3]**2 * np.sin(self.r[2]) * np.cos(self.r[2]) - self.r[1]**-1 * self.dr[1] * self.dr[2]
    def ddphiddtau(self):
        # below found by geodesic equation
        return - 2 / self.r[1] * self.dr[1] * self.dr[3] - 2 * cot(self.r[2]) * self.dr[2] * self.dr[3]
    
    def velMag(self):
        # b = (-(1 - 2 * self.M / self.r[1]) * self.dr[0])**2
        # print(b)
        # return np.sqrt(1 - 1/b)
        return self.dr[1] + self.r[1] * self.dr[2] * np.sin(self.r[3]) + self.r[1] * self.dr[3]
    
    def update_pos(self, step):
        if self.borked:
            self.r = np.zeros(4)
            self.dr = np.zeros(4)
        else:
            self.r += step * self.dr
            if abs(self.r[1]) <= 2 * self.M:
                self.borked = True
                self.r = np.zeros(4)
                self.dr = np.zeros(4)
            else:
                self.update_vels(step)
            self.pathr = np.append(self.pathr, [self.r], axis=0)
            
    
    def update_vels(self, step):
        Dr = self.ddrddtau()
        Dtheta = self.ddthetaddtau()
        Dphi = self.ddphiddtau()
        self.dr += step * np.array([0, Dr, Dtheta, Dphi])
        # self.dr += step * np.array([0, 0, Dtheta, Dphi])
        self.dr[0] = self.dtdtau()
        # self.dr[1] = self.drdtau()
        # self.dr[3] = self.dphidtau()
        
        self.pathdr = np.append(self.pathdr, [self.dr], axis=0)
        v = self.velMag()
        self.pathv = np.append(self.pathv, v)
        
M = 1
r = np.array([0, 4 * M, np.pi / 2, 0])
dr = 0
dtheta = 0
dl_M = 4 
dphi = dl_M * M / (r[1]**2 * (np.sin(r[2]))**2)
# dphi = 1
dt = np.sqrt(2 * (0.5 * dr**2 + (- M / r[1]) + (r[1]**2 * (np.sin(r[2]))**2 * dphi)**2 * (1 / (2 * r[1]**2) - M / r[1]**3)) + 1) / (1 -  2 * M / r[1])
v = np.array([dt, dr, dtheta, dphi])

b1 = Body(r, v, M)
step = 0.1
iters = int(2e4)
for i in range(iters):
    b1.update_pos(step)


x = b1.pathr[:, 1] * np.sin(b1.pathr[:, 2]) * np.cos(b1.pathr[:, 3])
y = b1.pathr[:, 1] * np.sin(b1.pathr[:, 2]) * np.sin(b1.pathr[:, 3])
z = b1.pathr[:, 1] * np.cos(b1.pathr[:, 2])
x /= M; y /= M; z /= M 

maximum = max(max(x), max(y), max(z))

ax = plt.figure().add_subplot(projection='3d')

def plot_bh(ax):
    N=10
    u = np.linspace(0, 2 * np.pi, N)
    v = np.linspace(0, np.pi, N)
    X = 2 * M * np.outer(np.cos(u), np.sin(v))
    Y = 2 * M * np.outer(np.sin(u), np.sin(v))
    Z = 2 * M * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(X, Y, Z)
def plot_circle(ax, r):
    N = 50
    theta = np.linspace(0, 2 * np.pi, N)
    X = r * np.cos(theta)
    Y = r * np.sin(theta)
    ax.plot(X, Y, linestyle='--', c='k')

ax.plot(x, y, z)
plot_circle(ax, b1.pathr[0, 1])
plot_bh(ax)
ax.scatter(0, 0, 0, c='k')
ax.set_xlim(-maximum, maximum)
ax.set_ylim(-maximum, maximum)
ax.set_zlim(-maximum, maximum)
a = b1.pathv
        

anim = False
if anim:
    
    fig = plt.figure(figsize=(12, 12))
    ax = plt.axes(projection='3d')
    
    def animate(i):
        ax.clear()
        ax.set_xlim(-maximum, maximum)
        ax.set_ylim(-maximum, maximum)
        ax.set_zlim(-maximum, maximum)
        plot_bh(ax)
        plot_circle(ax, b1.pathr[0, 1])
        
        
        X = b1.pathr[:i, 1] * np.sin(b1.pathr[:i, 2]) * np.cos(b1.pathr[:i, 3])
        Y = b1.pathr[:i, 1] * np.sin(b1.pathr[:i, 2]) * np.sin(b1.pathr[:i, 3])
        Z = b1.pathr[:i, 1] * np.cos(b1.pathr[:i, 2])
        X /= M; Y /= M; Z /= M 
        
        ax.plot(X, Y, Z, c='tab:blue', linestyle='-', marker='')
        if i > 0:
            ax.plot(X[-1], Y[-1], Z[-1], color='tab:blue', linestyle='-', marker='o')
        
        return fig,
            
    ani = FuncAnimation(fig, animate, interval=100, repeat=True, frames=range(0, iters, 80))
    ani.save("bleepslonger.gif", dpi=50, writer=PillowWriter(fps=40))
        
        