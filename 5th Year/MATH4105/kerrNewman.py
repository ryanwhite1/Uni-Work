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
    if abs(round(x, 2)) in [0, round(np.pi, 2)]:
        print("j")
        return 0
    return np.cos(x) / np.sin(x)

class Body(object):
    def __init__(self, r, dr, M, a, Q, q):
        self.r = r
        self.dr = dr
        self.M = M
        self.a = a
        self.Q = Q
        self.q = q
        self.horizon = 1 + np.sqrt(1 - a**2 - Q**2)
        
        self.angMom = self.Lz()
        self.E = self.energy()
        self.C = self.carter()
        
        # self.angMom = self.r[1]**2 * (np.sin(self.r[2]))**2 * self.dr[3]
        # self.epsilon = 0.5 * self.dr[1]**2 + self.Veff()
        # self.rest_energy = np.sqrt(2 * self.epsilon + 1)
        
        v = self.velMag()
        self.pathv = np.array([v])
        
        self.pathr = np.array([self.r])
        self.pathdr = np.array([self.dr])
        self.borked = False
        
    def Lz(self):
        Sigma = self.rhosquare()
        a = self.dr[3] * self.chi() * (np.sin(self.r[2]))**2 / Sigma
        b = - self.dr[0] * self.a * (np.sin(self.r[2]))**2 * (2 * self.r[1] - self.Q**2) / Sigma
        c = self.a * self.r[1] * self.Q * self.q * (np.sin(self.r[2]))**2 / Sigma 
        return a + b + c
    def energy(self):
        Sigma = self.rhosquare() 
        a = self.dr[0] * (1 - (2 * self.r[1] - self.Q**2) / Sigma)
        b = - self.dr[3] * self.a * (np.sin(self.r[2]))**2 * (2 * self.r[1] - self.Q**2) / Sigma
        c = self.a * self.r[1] * self.Q * self.q * (np.sin(self.r[2]))**2 / Sigma
        return a + b + c
    def carter(self):
        return (self.dr[2] * self.rhosquare())**2 + np.cos(self.r[2])**2 * (self.a**2 * (1 - self.E**2) + self.angMom**2 / np.sin(self.r[2])**2)
        
    
    def rhosquare(self):
        return self.r[1]**2 + self.a**2 * (np.cos(self.r[2]))**2
    def delta(self):
        return self.r[1]**2 - 2 * self.M * self.r[1] + self.a**2 + self.Q**2 / (4 * np.pi)
    def chi(self):
        return (self.a**2 + self.r[1])**2 - self.a**2 * (np.sin(self.r[2]))**2 * self.delta()
    def RadGyr(self):
        return np.sqrt(self.chi() / self.rhosquare()) * np.sin(self.r[2])
    def gravTimeDil(self):
        return self.chi() / (self.delta() * self.rhosquare())
    def velocity(self):
        return np.sqrt()
    def velMag(self):
        return self.dr[1] + self.r[1] * self.dr[2] * np.sin(self.r[3]) + self.r[1] * self.dr[3]
    
    def ddtddtau(self):
        Sigma = self.rhosquare() 
        a = - (self.a**2 * self.dr[2] * np.sin(2 * self.r[2]) * (self.q * self.Q * self.r[1] + (self.Q**2 - 2 * self.r[1]) * self.dr[0]) - 2 * self.a * (np.sin(self.r[2]))**3 * np.cos(self.r[2]) * (self.Q**2 - 2 * self.r[1]) * self.dr[3]) 
        b = (self.dr[1] * (((self.a**2 + self.r[1]**2) * ((self.a * np.cos(self.r[2]))**2 * (self.q * self.Q - 2 * self.dr[0]) + self.r[1] * (2 * (self.r[1] - self.Q**2) * self.dr[0] - self.q * self.Q * self.r[1]))) + self.a * (np.sin(self.r[2]))**2 * self.dr[3] * (2 * (self.a**2 * np.cos(self.r[2]))**2 + self.a**2 * (self.Q**2 * self.r[1] - self.r[1]**2) * (np.cos(2 * self.r[2]) + 3) + 4 * self.Q**2 * self.r[1]**3 - 6 * self.r[1]**4)) / (self.a**2 + self.r[1] * (self.r[1] - 2) + self.Q**2)) / (Sigma**2)
        return a + b
    def ddrddtau(self):
        Sigma = self.rhosquare() 
        a = (self.a**2 * self.dr[2] * np.sin(2 * self.r[2]) * self.dr[1]) / Sigma
        b = self.dr[1]**2 * ((self.r[1] - 1) / (self.a**2 + (self.r[1] - 2) * self.r[1] + self.Q**2) - self.r[1] / Sigma)
        c = ((self.a**2 + (self.r[1] - 2) * self.r[1] + self.Q**2) * (8 * self.a * np.sin(self.r[2])**2 * self.dr[3] * (self.a**2 * np.cos(self.r[2])**2 * (self.q * self.Q - 2 * self.dr[0]) + self.r[1] * (2 * (self.r[1] - self.Q**2) * self.dr[0] - self.q * self.Q * self.r[1])) + 8 * self.dr[0] * (self.a**2 * np.cos(self.r[2])**2 * (self.dr[0] - self.q * self.Q) + self.r[1] * (self.q * self.Q * self.r[1] + (self.Q**2 - self.r[1]) * self.dr[0])) + 8 * self.r[1] * self.dr[2]**2 * Sigma**2 + np.sin(self.r[2])**2 * self.dr[3]**2 * (2 * self.a**4 * np.sin(2 * self.r[2])**2 + self.r[1] * (self.a**2 * (self.a**2 * np.cos(4 * self.r[2]) + 3 * self.a**3 + 4 * (self.a - self.Q) * (self.a + self.Q) * np.cos(2 * self.r[2]) + 4 * self.Q**2) + 8 * self.r[1] * (-self.a**2 * np.sin(self.r[2])**2 + 2 * self.a**2 * self.r[1] * np.cos(self.r[2])**2 + self.r[1]**3))))) / (8 * Sigma**3)
        return a + b + c
    def ddthetaddtau(self):
        Sigma = self.rhosquare() 
        a = - (2 * self.r[1] * self.dr[2] * self.dr[1]) / Sigma
        b = - (self.a**2 * np.sin(self.r[2]) * np.cos(self.r[2]) * self.dr[1]**2) / ((self.a**2 + (self.r[1] - 2) * self.r[1] + self.Q**2) * Sigma)
        c = (np.sin(2 * self.r[2]) * (self.a**2 * (8 * self.dr[2]**2 * Sigma**2 - 8 * self.dr[0] * (2 * self.q * self.Q * self.r[1] + (self.Q**2 - 2 * self.r[1]) * self.dr[0])) + 16 * self.a * (self.a**2 + self.r[1]**2) * self.dr[3] * (self.q * self.Q * self.r[1] + (self.Q**2 - 2 * self.r[1]) * self.dr[0]) + self.dr[3]**2 * (3 * self.a**6 + 11 * self.a**4 * self.r[1]**2 + 10 * self.a**4 * self.r[1] - 5 * self.a**4 * self.Q**2 + 4 * self.a**2 * (self.a**2 + 2 * self.r[1]**2) * np.cos(2 * self.r[2]) * (self.a**2 + (self.r[1] - 2) * self.r[1] + self.Q**2) - 8 * self.a**2 * self.Q**2 * self.r[1]**2 + 16 * self.a**2 * self.r[1]**4 + self.a**4 * np.cos(4 * self.r[2]) * (self.a**2 + (self.r[1] - 2) * self.r[1] + self.Q**2) + 8 * self.r[1]**6))) / (16 * Sigma**3)
        return a + b + c
    def ddphiddtau(self):
        if abs(round(self.r[2], 1)) in [0, round(np.pi, 1)]:
            return 0
        Sigma = self.rhosquare() 
        a = - ((self.dr[1] * (4 * self.a * self.q * self.Q * (self.a**2 * np.cos(self.r[2])**2 - self.r[1]**2) - 8 * self.a * self.dr[0] * (self.a**2 * np.cos(self.r[2])**2 + self.r[1] * (self.Q**2 - self.r[1])) + self.dr[3] * (2 * self.a**4 * np.sin(2 * self.r[2])**2 + 8 * self.r[1]**3 * (self.a**2 * np.cos(2 * self.r[2]) + self.a**2 + self.Q**2) + self.a**2 * self.r[1] * (self.a**2 * (4 * np.cos(2 * self.r[2]) + np.cos(4 * self.r[2])) + 3 * self.a**2 + 8 * self.Q**2) - 4 * self.a**2 * self.r[1]**2 * (np.cos(2 * self.r[2]) + 3) + 8 * self.r[1]**5 - 16 * self.r[1]**4))) / (self.a**2 + (self.r[1] - 2) * self.r[1] + self.Q**2) + self.dr[2] * (self.dr[3] * (self.a**4 * (- np.sin(4 * self.r[2])) - 2 * self.a**2 * np.sin(2 * self.r[2]) * (3 * self.a**2 + 4 * (self.r[1] - 1) * self.r[1] + 2 * self.Q**2) + 8 * self.a * cot(self.r[2]) * (self.q * self.Q * self.r[1] + (self.Q**2 - 2 * self.r[1]) * self.dr[0])))) / (4 * Sigma**2)
        return a
        
    # def ddrddtau(self):
    #     ''' Eq (15) in https://arxiv.org/pdf/1706.05466.pdf
    #     '''
    #     a = self.M / self.r[1]**2
    #     b = - ((1 - self.epsilon**2) * self.a**2 + self.angMom**2 + self.Q**2) / self.r[1]**3
    #     c = 3 * self.M * (self.angMom - self.epsilon * self.a)**2 / self.r[1]**4 
    #     d = - 4 * Q**2 * (self.angMom - self.epsilon * self.a)**2 / self.r[1]**5
    #     return a + b + c + d
    
    # def ddrddtau(self):
    #     d = self.r[1]**2 - 2 * self.r[1] + self.a**2 + self.Q**2
    #     ddash = 2 * (self.r[1] - 1)
    #     p = self.E * (self.a**2 + self.r[1]**2) - self.a * self.angMom + self.q * self.r[1] * self.Q
    #     pdash = q * Q + 2 * self.E * self.r[1]
    #     return - ddash * ((self.angMom - self.a * self.E)**2 + self.C + self.r[1]**2) - 2 * self.r[1] * d + 2 * p * pdash
    # def ddthetaddtau(self):
    #     if abs(round(self.r[2], 1)) in [0, round(np.pi, 1)]:
    #         return 0
    #     return 2 * ((1 - self.E**2) * self.a**2 * np.sin(self.r[2]) * np.cos(self.r[2]) + self.angMom * cot(self.r[2]) * (1 + cot(self.r[2])**2))
    
    def update_pos(self, step):
        if self.borked:
            self.r = np.zeros(4)
            self.dr = np.zeros(4)
        else:
            self.r += step * self.dr
            if abs(self.r[1]) <= 1.2 * self.horizon:
                self.borked = True
                self.r = np.zeros(4)
                self.dr = np.zeros(4)
            else:
                self.update_vels(step)
            self.pathr = np.append(self.pathr, [self.r], axis=0)
            
    
    def update_vels(self, step):
        Dt = self.ddtddtau()
        Dr = self.ddrddtau()
        Dtheta = self.ddthetaddtau()
        Dphi = self.ddphiddtau()
        self.dr += step * np.array([Dt, Dr, Dtheta, Dphi])
        
        self.pathdr = np.append(self.pathdr, [self.dr], axis=0)
        v = self.velMag()
        self.pathv = np.append(self.pathv, v)
    
    
        
M = 1
a = 0
Q = 0
q = 0

r = np.array([0, 4 * M, np.pi / 2, 0])
dr = 0
dtheta = 0
dl_M = 6
if round(r[2], 4) == 0:
    dphi = 0
else:
    dphi = dl_M * M / (r[1]**2 * (np.sin(r[2]))**2)
# dphi = 1
dt = np.sqrt(2 * (0.5 * dr**2 + (- M / r[1]) + (r[1]**2 * (np.sin(r[2]))**2 * dphi)**2 * (1 / (2 * r[1]**2) - M / r[1]**3)) + 1) / (1 -  2 * M / r[1])
v = np.array([dt, dr, dtheta, dphi])

b1 = Body(r, v, M, a, Q, q)
step = 0.01
iters = int(1e4)
for i in range(iters):
    b1.update_pos(step)


x = b1.pathr[:, 1] * np.sin(b1.pathr[:, 2]) * np.cos(b1.pathr[:, 3])
y = b1.pathr[:, 1] * np.sin(b1.pathr[:, 2]) * np.sin(b1.pathr[:, 3])
z = b1.pathr[:, 1] * np.cos(b1.pathr[:, 2])
x /= M; y /= M; z /= M 

maximum = max(max(x), max(y), max(z))

ax = plt.figure().add_subplot(projection='3d')

def plot_bh(ax, r):
    N=10
    if r == None:
        r = 2 * M
    u = np.linspace(0, 2 * np.pi, N)
    v = np.linspace(0, np.pi, N)
    X = r * np.outer(np.cos(u), np.sin(v))
    Y = r * np.outer(np.sin(u), np.sin(v))
    Z = r * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(X, Y, Z)
def plot_circle(ax, r):
    N = 50
    theta = np.linspace(0, 2 * np.pi, N)
    X = r * np.cos(theta)
    Y = r * np.sin(theta)
    ax.plot(X, Y, linestyle='--', c='k')

ax.plot(x, y, z)
plot_circle(ax, b1.pathr[0, 1])
plot_bh(ax, b1.horizon)
ax.scatter(0, 0, 0, c='k')
# ax.set_xlim(-maximum, maximum)
# ax.set_ylim(-maximum, maximum)
# ax.set_zlim(-maximum, maximum)
a = b1.pathv

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
        

anim = True
if anim:
    
    fig = plt.figure(figsize=(12, 12))
    ax = plt.axes(projection='3d')
    
    def animate(i):
        ax.clear()
        ax.set_xlim(-maximum, maximum)
        ax.set_ylim(-maximum, maximum)
        ax.set_zlim(-maximum, maximum)
        plot_circle(ax, b1.pathr[0, 1])
        plot_bh(ax, b1.horizon)
        
        
        X = b1.pathr[:i, 1] * np.sin(b1.pathr[:i, 2]) * np.cos(b1.pathr[:i, 3])
        Y = b1.pathr[:i, 1] * np.sin(b1.pathr[:i, 2]) * np.sin(b1.pathr[:i, 3])
        Z = b1.pathr[:i, 1] * np.cos(b1.pathr[:i, 2])
        X /= M; Y /= M; Z /= M 
        
        ax.plot(X, Y, Z, c='tab:blue', linestyle='-', marker='')
        if i > 0:
            ax.plot(X[-1], Y[-1], Z[-1], color='tab:blue', linestyle='-', marker='o')
        
        return fig,
            
    ani = FuncAnimation(fig, animate, interval=100, repeat=True, frames=range(0, iters, 80))
    ani.save("KerrNewman.gif", dpi=50, writer=PillowWriter(fps=40))
        
        