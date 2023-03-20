# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 08:10:25 2023

@author: ryanw
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.integrate as integ

P = lambda k, t, L: (np.cos(0.5 * k * L * np.cos(t)) - np.cos(0.5 * k * L)) / np.sin(t)

wavelen = 0.032 # meters
horn_len = 0.059 # meters
a_length = np.array([wavelen / 2, wavelen, 2 * wavelen])

far_field = 2 * (a_length + horn_len)**2 / wavelen

lengths = ["none", "2 inch", "4.5 inch"]
dists = [75, 130, 180]

time = np.zeros(len(lengths) * len(dists), dtype=object)
angles = np.zeros(len(time), dtype=object)
levels = np.zeros(len(time), dtype=object)
volts = np.zeros(len(time), dtype=object)
levels_a = np.zeros(len(time), dtype=object)



i = 0
for length in lengths:
    for dist in dists:
        data = pd.read_csv(f'{length} roof {dist}.csv')
        time[i] = data['Time t / min'].to_numpy()
        angles[i] = data['Angle &J / °'].to_numpy()
        levels[i] = data['Level A'].to_numpy()
        volts[i] = data['Voltage U / mV'].to_numpy()
        levels_a[i] = data['Level a / dB'].to_numpy()
        i += 1
        
        
        
directs = np.zeros(i, dtype=object)
for j in range(len(time)):
    directs[j] = 4 * integ.trapezoid((levels[j])**2, angles[j])**-1


half_beam = np.zeros(len(time))
for i in range(len(time)):
    max_val = max(levels_a[i])
    max_ind = np.argwhere(levels_a[i] == max_val)[0][0]
    
    try:
        a = 0
        currval = max_val
        while currval >= max_val - 3:
            currval = levels_a[i][max_ind + a]
            a += 1
    except IndexError:
        a = 0
        currval = max_val
        while currval >= max_val - 3:
            currval = levels_a[i][max_ind + a - 1]
            a += -1
    
    half_beam[i] = abs(angles[i][max_ind] - angles[i][max_ind + a])
    
    
    
    

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

for j in range(i):
    if j%3 == 0:
        ax.plot(angles[j][:] * np.pi / 180, levels_a[j][:], alpha=0.7)
     
        
     
        
a = 0
for i in range(3):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    
    for j in range(3):
        ax.plot(angles[a] * np.pi / 180, levels_a[a], alpha=0.7)
        a += 1
        
        
        
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
theta = np.arange(0, 2 * np.pi, 0.01)
pred = np.zeros(len(theta))
for i, t in enumerate(theta):
    k = 2 * np.pi / wavelen
    # pred[i] = P(1, t + np.pi / 2, a_length[2])
    pred[i] = P(k, t + np.pi / 2, a_length[2])
    if np.isnan(pred[i]):
        pred[i] = 0
pred *= max(levels[2]) / max(pred)
ax.plot(angles[2] * np.pi / 180, levels[2])
ax.plot(theta, abs(pred))




fig, ax = plt.subplots()
for j in range(len(lengths)):
    ax.plot(dists, directs[j*3:(j+1)*3], label=f'{lengths[j]}')

ax.legend()