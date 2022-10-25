# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 13:51:33 2022

@author: ryanw
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

data = pd.read_csv("likes.csv", delimiter=',')

print('mean = ', np.mean(data['rating']), ' sd = ', np.std(data['rating']), ' median = ', np.median(data['rating']), 
      ' mode = ', stats.mode(data['rating']))
# plt.hist(data['rating'])