# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 13:51:33 2022

@author: ryanw
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# q1a
data = pd.read_csv("likes.csv", delimiter=',')

print('mean = ', np.mean(data['rating']), ' sd = ', np.std(data['rating']), ' median = ', np.median(data['rating']), 
      ' mode = ', stats.mode(data['rating']))
# plt.hist(data['rating'])

# q2h
print(1 - stats.chi2.cdf(6.368, 1))

#q2i
row1 = 52; row2 = 30
col1 = 41; col2 = 41
iters = 10**6
counts = 0

for i in range(iters):
    x1 = np.random.randint(0, min(row1 + 1, col1))
    x2 = row1 - x1
    x3 = col1 - x1
    x4 = col2 - x2
    if (x2 - x3)**2 / (x2 + x3) >= 6.368:
        counts += 1

print(f"p-value from {iters} trials is ", counts / iters)

