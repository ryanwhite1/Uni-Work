# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 08:47:42 2022

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

def binomCDF(p):
    n = 50
    return 1 - (binom.cdf(26, n, p) - binom.cdf(15, n, p))

x = np.linspace(0, 1, 100)
power = binomCDF(x)

fig, ax = plt.subplots()
ax.plot(x, power)
ax.set_xlabel('Probability $p$'); ax.set_ylabel('Power')

fig.savefig('PowerCurve.png', dpi=400, bbox_inches='tight')
fig.savefig('PowerCurve.pdf', dpi=400, bbox_inches='tight')
