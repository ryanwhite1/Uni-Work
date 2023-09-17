# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 12:31:54 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

trials = 10000
N = 1000
t = 100
c = 200

pop_est = np.zeros(trials)

for trial in range(trials):
    labels = np.arange(1, N + 1, 1)
    
    # tagged = np.random.choice(labels, size=t, replace=False)
    # captured = np.random.choice(labels, size=c, replace=False)
    
    # resamples = len(np.intersect1d(tagged, captured))
    
    resamples = np.random.hypergeometric(t, N - t, c)
    pop_est[trial] = c * t / resamples
fig, ax = plt.subplots()
ax.hist(pop_est)
print(f"Mean={round(np.mean(pop_est), 2)}\nMedian={round(np.median(pop_est), 2)}",
      f"\nVariance={round(np.std(pop_est), 2)}")


trial_num = np.arange(100, 10000, 200)
seps = np.zeros(len(trial_num))

for i, trials in enumerate(trial_num):
    pop_est = np.zeros(trials)

    for trial in range(trials):
        labels = np.arange(1, N + 1, 1)
        
        tagged = np.random.choice(labels, size=t, replace=False)
        captured = np.random.choice(labels, size=c, replace=False)
        
        resamples = len(np.intersect1d(tagged, captured))
        pop_est[trial] = c * t / resamples
    
    seps[i] = np.mean(pop_est) - N
fig, ax = plt.subplots()
# ax.hist(seps)
ax.plot(trial_num, seps)
print(f"Mean={round(np.mean(seps), 2)}\nMedian={round(np.median(seps), 2)}",
      f"\nVariance={round(np.std(seps)**2, 2)}")


trials = 100000
N = 1000
t = 100
c = 200

pop_est = np.zeros((trials, 2))

for trial in range(trials):
    labels = np.arange(1, N + 1, 1)
    
    tagged = np.random.choice(labels, size=t, replace=False)
    captured = np.random.choice(labels, size=c, replace=False)
    
    resamples = len(np.intersect1d(tagged, captured))
    
    hyper_resamp = np.random.hypergeometric(t, N - t, c)
    pop_est[trial, 0] = c * t / resamples
    pop_est[trial, 1] = c * t / hyper_resamp
fig, ax = plt.subplots()
ax.hist(pop_est[:, 0], bins=30, alpha=0.5, color='tab:blue')
ax.hist(pop_est[:, 1], bins=30, alpha=0.5, color='tab:red')
print(f"Mean={round(np.mean(pop_est), 2)}\nMedian={round(np.median(pop_est), 2)}",
      f"\nVariance={round(np.std(pop_est), 2)}")