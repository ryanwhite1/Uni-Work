# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 12:01:44 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

r = 1.65
def bevHolt(rt, K):
    b = (r - 1) / K
    return r * rt / (1 + b * rt)

def log_noise_BH(zt, rt, K):
    return np.log(zt) + np.log(bevHolt(rt, K))

def log_prior(k):
    if 0 < k < 1e5:
        return 0 
    return -np.inf

def metropolis(n, p0, prop_width, x, y):
    
    # Step 1 : Initialise arrays and set first value to be initial estimate
    theta = np.zeros(int(n))
    theta[0] = p0
    
    burn_in = 5e2
    
    posterior_old = np.prod(norm.pdf(y, loc=np.log(bevHolt(x, p0)), scale=prop_width))
    # print(posterior_old)
    
    for i in range(1, int(n)):
        
        # Step 2: Sample new parameter estimate
        new_param = np.random.normal(theta[i - 1], 10)
        
        # Step 3: Calculate log likelihood ratio
        # Start with prior on k
        prior_new = log_prior(new_param)
        if np.isnan(prior_new):
            theta[i] = theta[i - 1]
            continue
        
        posterior_new = np.prod(norm.pdf(y, loc=np.log(bevHolt(x, new_param)), scale=prop_width))
        # print(posterior_new)
        
        ratio = posterior_new / posterior_old
        
        accept_prob = min(ratio, 1)
        
        if np.random.uniform() < accept_prob:
            posterior_old = posterior_new
            theta[i] = new_param
        else:
            theta[i] = theta[i - 1]
            
    posterior = theta[int(burn_in):]
    
    return posterior
        


data = np.genfromtxt("GovernmentData_L5.csv", delimiter=',')
years = data[:, 0]
biomass = data[:, 1]

fig, ax = plt.subplots()

ax.plot(years, biomass)
ax.set(xlabel="Year", ylabel="Population Biomass (Tonnes)")

n = len(biomass)
X = biomass[:n-1]
Y = np.log(biomass[1:])

p0 = max(biomass)

prop_width = np.std(Y - np.log(bevHolt(X, p0)))

n_samples = 2e4

posterior = metropolis(n_samples, p0, prop_width, X, Y)

fig, axes = plt.subplots(nrows=2, gridspec_kw={"hspace":1})

k_est = round(np.median(posterior), 1)
p1, p2 = np.percentile(posterior, [16, 84])
plus, minus = round(abs(k_est - p2), 1), round(abs(k_est - p1), 1)

axes[0].scatter(np.arange(0, len(posterior)), posterior, s=0.5)
axes[1].hist(posterior, bins=100)
axes[1].set(xlabel="Carrying Capacity", ylabel="Frequency",
            title=f"$k_{{est}} = {k_est}^{{+{plus}}}_{{-{minus}}}$")


fig, ax = plt.subplots()
ys = np.zeros(len(years[1:]))
for i in range(len(years[1:])):
    if i == 0:
        x = X[0]
    else:
        x = ys[i - 1]
    ys[i] = bevHolt(x, k_est)
ax.scatter(years, biomass)
ax.plot(years[1:], ys)
ax.set(xlabel="Year", ylabel="Population Biomass (Tonnes)")


### --- Week 13 Practical --- ###

nk = len(posterior)     # number of samples

nt = 100    # number of timesteps

nQ = 100    # number of quotas

Q = np.linspace(0, 25, nQ)  # range of quotas
# K = np.linspace(min(posterior), max(posterior), nk)

# Now we want to compute the yield given a quota q and carrying capacity k
Y = np.zeros((nQ, nk))

Ymean = np.zeros(nQ)    # initialise expected yield

k_hat = np.median(posterior)    # median value of samples

Ym = np.zeros(nQ)   # initialise vector for yield under mean k for each quota

B = np.zeros(nt)    # initialise the biomass vector
B[0] = biomass[-1]  # set initial biomass to our last data point as per question requirements

# Calculate the yield for each quota and k in the sample
for i in range(nQ):
    for j in range(nk): # begin k loop
        Yield = 0
        for t in range(1, nt):  # now loop over time
            B[t] = bevHolt(B[t - 1], posterior[j])  # calculate population at next time step
            harvest = min(Q[i], B[t])
            B[t] += - harvest
            Yield += harvest
            
        Y[i, j] = Yield     # now store yield in our matrix
        
    Ymean[i] = np.mean(Y[i, :])
    
import numpy as np
NUM = 100    # plot yield vs quota for first np samples in the posterior

fig, ax = plt.subplots()

for i in range(NUM):
    ax.plot(Q, Y[:, i])
    
ax.plot(Q, Ymean[:NUM], lw=3, c='k')

            
for i in range(nQ):
    Yield = 0
    for t in range(1, nt):  # now loop over time
        B[t] = bevHolt(B[t - 1], k_hat)  # calculate population at next time step
        harvest = min(Q[i], B[t])
        B[t] += - harvest
        Yield += harvest
        
    Ym[i] = Yield

ax.plot(Q, Ym, c='r', lw=3, ls='--')


print("The Quota which maximises the yield given the median carrying capacity is",
      Q[np.argwhere(Ym == max(Ym)).flatten()[0]])

print("The quota which maximises the expected yield given all k values is",
      Q[np.argwhere(Ymean == max(Ymean)).flatten()[0]])






