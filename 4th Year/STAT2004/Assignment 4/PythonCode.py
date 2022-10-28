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

print('mean = ', np.mean(data['rating']), ' sd = ', np.std(data['rating']), 
      ' median = ', np.median(data['rating']), 
      ' mode = ', stats.mode(data['rating']))

# q1b
InfAnswers = data[data['user'] == 'influencer']
RegAnswers = data[data['user'] == 'regular']
InfCounts, RegCounts = np.zeros(5), np.zeros(5)
for i in range(len(InfAnswers['rating'])):
    InfCounts[InfAnswers['rating'].to_numpy()[i] - 1] += 1
for i in range(len(RegAnswers['rating'])):
    RegCounts[RegAnswers['rating'].to_numpy()[i] - 1] += 1
print([RegCounts, InfCounts])
total = sum(RegCounts) + sum(InfCounts)
chi2 = 0
for i in range(len(RegCounts)):
    for col in [RegCounts, InfCounts]:
        Eij = (sum(col) * sum([RegCounts[i], InfCounts[i]])) / total
        chi2 += (col[i] - Eij)**2 / Eij
pval = 1 - stats.chi2.cdf(chi2, 4)
print(f"We get a value of {chi2 = }, and a corresponding {pval = }")

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

# q3a
col1 = np.array([298, 146, 119, 106, 29, 133, 29])
col2 = np.array([165, 264, 16, 328, 203, 165, 30])
total = sum(col1) + sum(col2)
chi2 = 0
for i in range(len(col1)):
    for col in [col1, col2]:
        Eij = (sum(col) * sum([col1[i], col2[i]])) / total
        chi2 += (col[i] - Eij)**2 / Eij
pval = 1 - stats.chi2.cdf(chi2, 6)
print(f"We get a value of {chi2 = }, and a corresponding {pval = }")

# q3b
col1 = np.array([12, 6, 5, 4, 2, 5, 2])
col2 = np.array([11, 6, 5, 4, 0, 6, 0])
col3 = np.array([12, 7, 5, 6, 0, 4, 2])
col4 = np.array([12, 6, 4, 2, 0, 5, 2])
col5 = np.array([13, 5, 5, 4, 2, 4, 0])
col6 = np.array([11, 8, 3, 2, 0, 4, 0])
col7 = np.array([13, 7, 4, 6, 2, 6, 0])
col8 = np.array([12, 5, 4, 6, 2, 5, 2])
total = np.sum([[col1, col2, col3, col4, col5, col6, col7, col8]])
chi2 = 0
for i in range(len(col1)):
    for col in [col1, col2, col3, col4, col5, col6, col7, col8]:
        Eij = (sum(col) * sum([col1[i], col2[i], col3[i], col4[i], 
                                col5[i], col6[i], col7[i], col8[i]])) / total
        chi2 += (col[i] - Eij)**2 / Eij
pval = 1 - stats.chi2.cdf(chi2, 42)
print(f"We get a value of {chi2 = }, and a corresponding {pval = }")

