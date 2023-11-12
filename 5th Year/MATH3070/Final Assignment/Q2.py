# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 13:20:47 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family']='serif'
plt.rcParams['mathtext.fontset']='cm'

phi = 0.8
k = 100
def model(x, r):
    ''' This is the population dynamic model from Q1
    '''
    return x + (r - 1) * x * (1 - (x / k)**phi)

def log_prior(r):
    ''' Prior function to return a bad value if our growth rate escapes our `positive` growth rate bounds. 
    '''
    if 0 < r < 1e5:
        return 0 
    return -np.inf

def metropolis(n, p0, prop_width, x, y):
    ''' Implementation of the 1D Metroplis algorithm. 
    Parameters
    ----------
    n : int
        Number of iterations in the MCMC
    p0 : float
        Initial guess of our parameter
    prop_width : float
        Proposal distribution width (standard deviation) to calculate our log likelihoods with
    x : np.array
        Our x data
    y : np.array
        Our y data
    '''
    # Step 1 : Initialise arrays and set first value to be initial estimate
    theta = np.zeros(int(n))
    theta[0] = p0
    
    burn_in = 5e2
    
    # calculate the likelihood of our initial guess
    L_old = np.prod(norm.pdf(y, loc=np.log(model(x, p0)), scale=prop_width))
    
    for i in range(1, int(n)):
        
        # Step 2: Sample new parameter estimate
        new_param = np.random.normal(theta[i - 1], 0.1)
        
        # Step 3: Calculate log likelihood ratio
        # Start with prior on r
        prior_new = log_prior(new_param)
        if np.isnan(prior_new):     # if our new param doesn't fit the prior, skip this loop
            theta[i] = theta[i - 1]
            print("Param outside of prior bounds")
            continue
        
        # now calculate the likelihood of the new parameter estimate
        L_new = np.prod(norm.pdf(y, loc=np.log(model(x, new_param)), scale=prop_width))
        
        ratio = L_new / L_old
        
        accept_prob = min(ratio, 1)
        
        if np.random.uniform() < accept_prob:   # if we're choosing our new parameter
            L_old = L_new                       # set the old likelihood to our new one
            theta[i] = new_param                # update our samples with our new estimate
        else:
            theta[i] = theta[i - 1]             # if we reject this new estimate, set our current sample to our old one
            
    posterior = theta[int(burn_in):]    # get all samples after the burn in
    
    return posterior

def least_squares(xs):
    ''' This function computes the least squares estimate on data from equation (5) in the assignment
    '''
    numer = sum([(xs[i + 1] - xs[i] * (xs[i] / k)**phi) * xs[i] * (1 - (xs[i] / k)**phi) for i in range(len(xs) - 1)])
    denom = sum([xs[i]**2 * (1 - (xs[i] / k)**phi)**2 for i in range(len(xs) - 1)])
    return numer / denom
        
tankdata = np.genfromtxt('TankStudy.csv')[1:]   # load in the tank data numerical vals

# now to find the least squares estimate for each tank
LS_r_ests = np.zeros(len(tankdata))
for i in range(len(LS_r_ests)):
    LS_r_ests[i] = least_squares([2, tankdata[i]])  # our data is [2, {tank_value}]
    
p0 = np.mean(LS_r_ests)     # our initial guess in the MCMC will be the mean of the least squares values
print(f"Least Squares Est. from 10 data tanks is r = {round(p0, 2)}")

data = np.genfromtxt("GovernmentData.csv", delimiter=',')   # load in the government data
# now take time and biomass data for all but the first (header) rows
time = data[1:, 0] 
xdat = data[1:, 1]

# plot the data just to get a peek
fig, ax = plt.subplots()
ax.plot(time, xdat)
ax.set(xlabel="Year", ylabel="Population Biomass (Tonnes)")

n = len(xdat)   # our number of data points
X = xdat[:n-1]  # get our biomasses up to the last point
Y = np.log(xdat[1:])    # get our i+1 biomasses for each point and log it



# our proposal dist. width will be the standard deviation of the residuals in the logged model
prop_width = np.std(Y - np.log(model(X, p0)))

# want to perform 10^5 iterations
n_samples = 1e5

# now we run the MCMC and get the posterior distribution
posterior = metropolis(n_samples, p0, prop_width, X, Y)

# now to plot the samples and the histogram
fig, axes = plt.subplots(nrows=2, gridspec_kw={"hspace":0.4}, figsize=(8, 6))

r_est = round(np.median(posterior), 2)
p1, p2 = np.percentile(posterior, [16, 84])
plus, minus = round(abs(r_est - p2), 2), round(abs(r_est - p1), 2)

axes[0].scatter(np.arange(0, len(posterior)), posterior, s=0.5, alpha=0.6, rasterized=True)
axes[1].hist(posterior, bins=100, rasterized=True)
axes[0].set(xlabel="Walker Iteration", ylabel="$r$ Posterior Value")
axes[1].set(xlabel="Growth Rate $r$", ylabel="Frequency",
            title=f"$r_{{est}} = {r_est}^{{+{plus}}}_{{-{minus}}}$")

fig.savefig("MCMC.pdf", dpi=400, bbox_inches='tight')   # save the figure

# now to plot the median growth value in the model fit to the data
fig, ax = plt.subplots()
ys = np.zeros(len(time[1:]))
for i in range(len(time[1:])):
    if i == 0:
        x = X[0]
    else:
        x = ys[i - 1]
    ys[i] = model(x, r_est)
ax.scatter(time, xdat)
ax.plot(time[1:], ys)
ax.set(xlabel="Year", ylabel="Population Biomass (Tonnes)")

fig.savefig("Median Fit.pdf", dpi=400, bbox_inches='tight')     # save the figure

### --- Now on to calculating the optimal yield --- ###

yield_posterior = posterior[::10]   # get every 10th sample from the posterior, otherwise the calculation will take forever

nr = len(yield_posterior)     # number of samples

nt = 50    # number of timesteps (years) to look at

nQ = 100    # number of harvesting quotas to look at

Q = np.linspace(0, 25, nQ)  # range of quotas; i.e. checking for quotas between 0 and 25 tonnes/yr

# Now we want to compute the yield given a quota q and growth rate r
Y = np.zeros((nQ, nr))

Ymean = np.zeros(nQ)    # initialise expected yield

r_hat = round(np.median(posterior), 2)    # median value of samples

Ym = np.zeros(nQ)   # initialise vector for yield under mean r for each quota

B = np.zeros(nt)    # initialise the biomass vector
B[0] = xdat[-1]  # set initial biomass to our last data point (2023)

# Calculate the yield for each quota and r in the sample
for i in range(nQ):
    for j in range(nr): # begin loop of samples
        Yield = 0
        for t in range(1, nt):  # now loop over time
            B[t] = model(B[t - 1], yield_posterior[j])  # calculate population at next time step
            harvest = min(Q[i], B[t])   # we want to harvest the minimum of either the entire population or our quota
            B[t] += - harvest   # subtract the harvest from our biomass
            Yield += harvest    # add our harvest to our total yield
            
        Y[i, j] = Yield     # now store yield in our matrix
        
    Ymean[i] = np.mean(Y[i, :])     # calculate the mean for all of those growth values at this quota value
    
NUM = 100    # plot yield vs quota for first NUM samples in the posterior

fig, ax = plt.subplots()

for i in range(NUM):    # plot the first NUM yield curves
    ax.plot(Q, Y[:, i])
    
ax.plot(Q, Ymean, lw=3, c='k', label='Tot. Yield All Data')     # plot the mean yield curve

for i in range(nQ):
    Yield = 0
    for t in range(1, nt):  # now loop over time
        B[t] = model(B[t - 1], r_hat)  # calculate population at next time step
        harvest = min(Q[i], B[t])
        B[t] += - harvest
        Yield += harvest
        
    Ym[i] = Yield

ax.plot(Q, Ym, c='r', lw=3, ls='--', label=r'Tot. Yield at Median $\hat{r}$')   # plot the yield curve of the median
ax.legend()
ax.set(xlabel="Attempted Yearly Harvest (tonnes)", ylabel=f"Total Yield in {nt} year period (tonnes)")

fig.savefig("Yield.pdf", dpi=400, bbox_inches='tight')

# now print to the user the key values
print(f"The Quota which maximises the yield given the median growth rate r={round(r_hat, 2)} is",
      round(Q[np.argwhere(Ym == max(Ym)).flatten()[0]], 2), "tonnes/yr")

print("The quota which maximises the expected yield given all estimated r values is",
      round(Q[np.argwhere(Ymean == max(Ymean)).flatten()[0]], 2), "tonnes/yr")






