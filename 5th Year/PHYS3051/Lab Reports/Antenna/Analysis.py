# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 08:10:25 2023

@author: ryanw
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.integrate as integ

plt.rcParams['font.family'] = 'Serif'

# formula for theoretical normalised radiation pattern, in terms of theta (t)
P = lambda k, t, L: (np.cos(0.5 * k * L * np.cos(t)) - np.cos(0.5 * k * L)) / np.sin(t)


def directivity(levels, angles, levels_unc, iters):
    ''' Monte carlo analysis and directivity calculation
    levels : np.array
        LevelA data
    angles : np.array
        Each angle in *radians*
    '''
    norm_levels = levels / max(levels)
    iter_direct = np.zeros(iters)
    for i in range(iters):
        iter_level = np.zeros(len(levels))
        for j in range(len(levels)):
            iter_level[j] = np.random.normal(norm_levels[j], levels_unc[j])
            
        iter_direct[i] = 4 * integ.trapezoid((iter_level)**2 * abs(np.sin(angles)), angles)**-1
    
    av_direct = np.mean(iter_direct)
    sd_direct = np.std(iter_direct)
        
    return av_direct, sd_direct

def one_directivity(levels, angles):
    return 4 * integ.trapezoid((levels)**2 * abs(np.sin(angles)), angles)**-1

# define 
fs = 8 # fig size, inches
wavelen = 0.032 # meters
horn_len = 0.059 # meters
a_length = np.array([wavelen / 2, 1.5 * wavelen, 4 * wavelen])

far_field = 2 * (a_length + horn_len)**2 / wavelen

lengths = ["none", "2 inch", "4.5 inch"]
dists = [75, 130, 180]

# initialise arrays
time = np.zeros(len(lengths) * len(dists), dtype=object)
angles = np.zeros(len(time), dtype=object)
levels = np.zeros(len(time), dtype=object)
volts = np.zeros(len(time), dtype=object)
levels_a = np.zeros(len(time), dtype=object)



# load in data
i = 0
for length in lengths:
    for dist in dists:
        data = pd.read_csv(f'{length} roof {dist}.csv')
        time[i] = data['Time t / min'].to_numpy()
        angles[i] = data['Angle &J / °'].to_numpy()
        levels[i] = data['Level A'].to_numpy()
        volts[i] = data['Voltage U / mV'].to_numpy()
        levels_a[i] = data['Level a / dB'].to_numpy()
        i += 1
        
# print(levels[0])
# convert angles from degrees to radians, and add pi/2 to make this the position of maximum lobe (as per lab manual)
rad_angles = angles * np.pi / 180 + np.pi / 2       

rad_angles[5] += 5 * np.pi / 180 # clean up data




half_beam = np.zeros(len(time))
for i in range(len(time)):
    max_val = max(levels_a[i])
    max_ind = np.argwhere(levels_a[i] == max_val)[0][0]
    
    try:
        a = 0
        currval = max_val
        while currval >= max_val - 3:
            currval = levels_a[i][max_ind + a]
            a += 1
    except IndexError:
        a = 0
        currval = max_val
        while currval >= max_val - 3:
            currval = levels_a[i][max_ind + a - 1]
            a += -1
    
    half_beam[i] = abs(angles[i][max_ind] - angles[i][max_ind + a])
    

# theory half beam width and directivity
pred_patterns = np.zeros((len(a_length), len(rad_angles[0])))
for i in range(len(a_length)):
    theta = rad_angles[0]
    for j, t in enumerate(theta):
        k = 2 * np.pi / wavelen  # wavenumber calculation
        pred_patterns[i, j] = abs(P(k, t,  a_length[i]))   # calculate predicted values here
        if np.isnan(pred_patterns[i, j]):
            pred_patterns[i, j] = 0
for i in range(len(a_length)):
    pred_patterns[i, :] /= max(pred_patterns[i, :])
pred_HBW = np.zeros(len(a_length))
pred_direct = np.zeros(len(a_length))
pred_a = 20 * np.log(pred_patterns)
for i in range(len(a_length)):
    max_val = max(pred_a[i, :])
    max_ind = np.argwhere(pred_a[i, :] == max_val)[0][0]
    
    try:
        a = 0
        currval = max_val
        while currval >= max_val - 3:
            currval = pred_a[i, :][max_ind + a]
            a += 1
    except IndexError:
        a = 0
        currval = max_val
        while currval >= max_val - 3:
            currval = pred_a[i, :][max_ind + a - 1]
            a += -1
    
    pred_HBW[i] = abs(angles[0][max_ind] - angles[0][max_ind + a])
    
for i in range(len(a_length)):
    pred_direct[i] = one_directivity(pred_patterns[i, :], rad_angles[0])
    
    
## calculate uncertainties in pattern
averages = np.zeros((len(lengths), len(levels[0])))
sds = np.zeros((len(lengths), len(levels[0])))
fignames = ["0.5Lambda Pattern with Unc.png", "1.5Lambda Pattern with Unc.png", "4Lambda Pattern with Unc.png"]
for i in range(3):
    start = i * 3; end = i * 3 + 2
    for k in range(len(levels[0])):
        averages[i, k] = np.mean([levels[j][k] / max(levels[j]) for j in range(start, end + 1)])
        sds[i, k] = np.std([levels[j][k] / max(levels[j]) for j in range(start, end + 1)])
        
    # fig, ax = plt.subplots(figsize=(fs, fs), subplot_kw={'projection': 'polar'})
    
    



# fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# for j in range(len(time)):
#     if j%3 == 0:
#         ax.plot(angles[j][:] * np.pi / 180, levels_a[j][:], alpha=0.7)
     
        
     
# now plot the change in levelA vs distance away
fignames = ["0.5Lambda Pattern vs Distance", "1.5Lambda Pattern vs Distance", "4Lambda Pattern vs Distance"]
a = 0
for i in range(3):
    fig, ax = plt.subplots(figsize=(fs, fs), subplot_kw={'projection': 'polar'})
    
    for j in range(3):
        ax.plot(rad_angles[a], levels[a], alpha=0.7, label=str(dists[j] / 100) + "m")
        a += 1
    ax.legend(loc='upper right')
    fig.savefig(fignames[i] + ".pdf", bbox_inches='tight')
    fig.savefig(fignames[i] + ".png", bbox_inches='tight')


# now plot the observed vs predicted pattern for each antenna length
        
chi2 = np.zeros(len(a_length))
chi2dof = np.zeros(len(a_length))
names = ["0.5Lambda Obs vs Pred, 180cm", "1.5Lambda Obs vs Pred, 180cm", "4Lambda Obs vs Pred, 180cm"]
# Calculate predicted pattern for each antenna length
for i, ind in [(0, 2), (1, 5), (2, 8)]:
    # matches predicted for 1/2 lambda, 3/2 lambda, and 4 lambda
    
    theta = np.arange(-np.pi, np.pi, 2 * np.pi / len(rad_angles[i]))
    pred = np.zeros(len(theta))
    
    for j, t in enumerate(theta):
        k = 2 * np.pi / wavelen  # wavenumber calculation
        pred[j] = P(k, t,  a_length[i])   # calculate predicted values here
        if np.isnan(pred[j]):
            pred[j] = 0
    pred = abs(pred)
    pred *= max(averages[i, :]) / max(pred) # normalise prediction
    
    fig, ax = plt.subplots(figsize=(fs, fs), subplot_kw={'projection': 'polar'})
    # ax.plot(angles[ind] * np.pi / 180, levels[ind])
    # ax.plot(rad_angles[ind], levels[ind], label="Observed Values")
    ax.fill_between(rad_angles[i], averages[i, :] + sds[i, :], averages[i, :] - sds[i, :],
                    alpha = 0.3, color='r')
    ax.plot(rad_angles[i], averages[i, :], c='r', label='Observed')
    
    # fig.savefig(fignames[i])
    ax.plot(theta, pred, label="Prediction")
    ax.legend(loc='upper right')
    fig.savefig(names[i] + ".pdf", bbox_inches='tight')
    fig.savefig(names[i] + ".png", bbox_inches='tight')
    
    chi2[i] = sum((averages[i, :][j] - pred[j])**2 / pred[j] if pred[j] != 0 else 0 for j in range(len(pred)))
    chi2dof[i] = chi2[i] / len(pred)




# calculate directivity for 
# directs = np.array([directivity(levels[i], rad_angles[i]) for i in range(len(levels))])

directs, directs_unc = np.zeros(len(averages[:, 0])), np.zeros(len(averages[:, 0]))
for i in range(len(averages[:, 0])):
    directs[i], directs_unc[i] = directivity(averages[i, :], rad_angles[i], sds[i, :], 1000)



# labels = ["$1/2~\lambda$", "$3/2~\lambda$", "$4~\lambda$"]
# fig, ax = plt.subplots()
# for j in range(len(lengths)):
#     ax.plot(dists, directs[j*3:(j+1)*3], label=fr'{labels[j]}')

# ax.set_ylabel("Directivity")
# ax.set_xlabel("Transmitter-Antenna Distance (cm)")
# ax.legend(loc='upper right')
# fig.savefig("Directivity vs Dist.png", bbox_inches='tight')



# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(fs, fs), subplot_kw={'projection': 'polar'})

test_angles = np.linspace(0, 2*np.pi, 500)
test_lengths = np.linspace(wavelen / 2, 4 * wavelen, 10)

import matplotlib.cm as cm
import matplotlib.colors
colours = cm.plasma(np.linspace(0, 1, len(test_lengths)))

for j, length in enumerate(test_lengths):
    pred = np.zeros(len(test_angles))
    for i, angle in enumerate(test_angles):
        pred[i] = P(k, angle, length)
        if np.isnan(pred[i]):
            pred[i] = 0
    pred = abs(pred)
    
    figure = ax.plot(test_angles, pred, c=colours[j], alpha=0.7)

fig.colorbar(cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=0.5, vmax=4), cmap='plasma'),
             label=r'Antenna Length (frac. of $\lambda$)',
             shrink=0.8, pad=0.08)
fig.savefig("predictionMap.pdf", bbox_inches='tight')
fig.savefig("predictionMap.png", bbox_inches='tight')



plt.close('all')