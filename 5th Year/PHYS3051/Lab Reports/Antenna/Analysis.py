# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 08:10:25 2023

@author: ryanw
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

for j in range(i):
    if j%3 == 0:
        ax.plot(angles[j][:] * np.pi / 180, levels[j][:], alpha=0.7)
# ax.set_rmax(max(levels[0][:]))

