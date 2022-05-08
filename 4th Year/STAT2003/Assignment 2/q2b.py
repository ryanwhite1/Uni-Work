# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 20:20:19 2022

@author: ryanw
"""

from numpy.random import uniform, seed
from numpy import arange
import matplotlib.pyplot as plt


def inverse_function(sample):
    '''This is the inverse function from question 2, part a. 
    '''
    b = 3
    a = 2
    output = (b * ((1 / (1 - sample)) - 1))**(1/a)
    return output

def prob_dens_func(x):
    '''This is the probability density function as per the question description.
    '''
    b = 3
    a = 2
    output = a * b * (x**(a-1)) / (b + x**a)**2
    return output


seed(58268)         #this is a nice seed :)
values = uniform(0, 1, 10**5)       #values is an array of 10^5 uniform random variables, with min=0 and max=1 

variables = inverse_function(values)    #calculates the inverse-transform variables 
X = arange(0, max(variables), 0.1)      #this is the range of the pdf function line

fig, ax = plt.subplots()

ax.hist(variables, bins=500)
plt.xlim(0, 20)
ax.set_xlabel("Random Variable")
ax.set_ylabel("Number of Instances")

ax2 = ax.twinx()

ax2.plot(X, prob_dens_func(X), 'r-')
plt.ylim(0, 0.4)
ax2.set_ylabel("Probability")

fig.savefig('histogram.pdf', dpi=200, bbox_inches='tight', pad_inches = 0.01)