# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 12:22:50 2022

@author: ryanw
"""

from scipy.stats import binom

i = 0
c = 0
while i < 0.99:
    i = binom.cdf(c, 50, 0.4)
    if i < 0.99:
        c += 1
print(c)



print(1 - binom.cdf(27, 50, 0.5))

from scipy.stats import binom
power = 0
n = 1
while power < 0.9:
    c = 0
    i = 0
    while i < 0.99:
        i = binom.cdf(c, n, 0.4)
        if i < 0.99:
            c += 1
    power = 1 - binom.cdf(c, n, 0.5)
    n += 1
print(power, " at n = ", n)
    
