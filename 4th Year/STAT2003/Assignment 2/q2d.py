# -*- coding: utf-8 -*-
"""
Created on Sun May  1 16:58:32 2022

@author: ryanw
"""

from numpy.random import uniform, seed
from numpy import arange, pi, zeros, sqrt
import matplotlib.pyplot as plt


def inverse_function(sample):
    '''This is the inverse function from question 2, part a. 
    '''
    b = 1 / sqrt(3)
    a = 1 / 2
    output = (b * ((1 / (1 - sample)) - 1))**(1/a)
    return output

def prob_dens_funcG(x):
    '''This is the probability density function of g(x).
    '''
    b = 1 / sqrt(3)
    a = 1 / 2
    output = a * b * (x**(a - 1)) / (b + x**a)**2
    return output

def prob_dens_funcF(x):
    '''This is the probability density function of f(x).
    '''
    output = (x**(-1/2)) / ((pi / 2) * (x + 1)**2)
    return output

seed(4)         #this is a nice seed :)

n = 10**5       #how many rand. vars. we want. 
z = zeros(n)
C = 3 * sqrt(3) / pi        
for i in range(n):
    found = False
    while not found:
        x = inverse_function(uniform(0, 1))     #X ~ g  as per q2b
        y = uniform(0, C * prob_dens_funcG(x))  #Y ~ U(0, Cg(x))
        if (y <= prob_dens_funcF(x)):
            found = True
            z[i] = x

xmax = 2
X = arange(0, xmax+1, 0.01)

fig, ax = plt.subplots()
#now to plot the histogram of random variables and their frequencies
ax.hist(z, bins=40, range=(0, xmax))
plt.xlim(0, xmax)
ax.set_xlabel("Random Variable")
ax.set_ylabel("Number of Instances")

ax2 = ax.twinx()
#now to plot the pdf overlaid on top of the histogram
ax2.plot(X, prob_dens_funcF(X), 'r-')
plt.ylim(bottom=0)
ax2.set_ylabel("Probability")

fig.savefig('histogram2d.pdf', dpi=200, bbox_inches='tight', pad_inches = 0.01)