# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 15:40:34 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import leastsq

def gaussian(x, a, b, c):
    return a * np.exp(-(x - b)**2 / (2 * c**2))
def sine(x, A, P, S, E):
    return A * np.sin((2 * np.pi / P) * (x - S)) + E

plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family']='serif'
plt.rcParams['mathtext.fontset']='cm'

fs = 3.568 # figure size, inches




polarisation_baseline = 3.15 # mV
polarisation_angles = np.arange(0, 360, 30) # deg 
# for each polarisation angle, we have three data points of the voltage (mV) through the polarising lens. 
polarisation_data = np.array([[9.54, 9.24, 10], [13.9, 14, 12.6], [12.7, 12.5, 13.4], [11.3, 10.6, 11.8], [5.19, 5.37, 5.26],
                              [4.93, 4.87, 5.01], [11.4, 11.9, 12], [14.7, 15.2, 14.3], [14.8, 14.6, 13.9], [12.6, 11.7, 11.8],
                              [4.91, 4.55, 4.61], [4.2, 4.44, 4.51]])

fig, ax = plt.subplots(figsize=(fs, .7*fs))
polarisation_angles = polarisation_angles * np.pi / 180
polarisation_means = np.array([np.mean(polarisation_data[i, :]) for i in range(len(polarisation_angles))]) - polarisation_baseline
polarisation_stds = np.array([np.std(polarisation_data[i, :]) for i in range(len(polarisation_angles))])
# ax.plot(polarisation_angles, polarisation_means)
ax.errorbar(polarisation_angles, polarisation_means, 
            xerr=4 * np.pi/180, 
            yerr=polarisation_stds,
            fmt='.', elinewidth=0.75, markersize=1.5,
            c='tab:red')

pol_params, covar = curve_fit(sine, polarisation_angles, polarisation_means, p0=[5.5, np.pi, 0, 5.5])
x = np.linspace(0, max(polarisation_angles), 100)
fit_y = sine(x, pol_params[0], pol_params[1], pol_params[2], pol_params[3])
ax.plot(x, fit_y, c='tab:blue')
ax.set_ylim(ymin=0)

ax.set_xlabel('Polarisation Filter Rotation (rad)')
ax.set_ylabel('Mean Voltage (mV)')
ax.grid()

fname = 'PolarisationFit'
fig.savefig(fname + '.png', bbox_inches='tight', dpi=300)
fig.savefig(fname + '.pdf', bbox_inches='tight', dpi=300)

predicted = sine(polarisation_angles, pol_params[0], pol_params[1], pol_params[2], pol_params[3])
chi2_polarised = sum((polarisation_means - predicted)**2 / predicted)
chi2_dof_polarised = chi2_polarised / len(predicted)





single_dists = [5.5, 16.5, 25.5] # cm
multi_dists = [6, 10, 14, 20] # cm

# the single and multi mode images were taken with a slightly different setup, so we will expect some difference in their pixel counts per dist
# lets get the pixels per centimer in the single-mode images
single_ppcm = [42, 45, 43, 48, 47, 46] # pixels between the cm increments
single_ppcm_unc = np.std(single_ppcm)
single_ppcm = np.mean(single_ppcm)

# now lets get the pixels per centimeter in the multi-mode images
multi_ppcm = [44, 44, 42, 44, 45, 46] # pixels between the cm increments
multi_ppcm_unc = np.std(multi_ppcm)
multi_ppcm = np.mean(multi_ppcm)

# now normalise the uncertainties against each other, as they are based on the same grid markings
single_ppcm_unc, multi_ppcm_unc = max([multi_ppcm_unc, single_ppcm_unc]) * np.array([single_ppcm, multi_ppcm]) / max([single_ppcm, multi_ppcm])



names = ['single' + str(dist) for dist in single_dists] + ['multi' + str(dist) for dist in multi_dists]
NA, V, M = np.zeros(len(names)), np.zeros(len(names)), np.zeros(len(names))
for i, im_name in enumerate(names):
    # read in the image
    # im_name = 'multi10'
    image = plt.imread(im_name + '.jpg') # the read image is a numpy ndarray with dimensions (vertical, horizontal, RGB)
    
    # # find the row with the brightest red pixel
    # row = np.unravel_index(np.argmax(image[:, :, 0]), image[:, :, 0].shape)[0]
    
    # find the row with the largest sum of the red pixel values
    row = image[:, :, 0].sum(axis=1).argmax()
    
    # create x data point for each column (pixel)
    x = np.arange(0, image.shape[1], 1)
    intensity = image[row, :, 0]
    
    
    # show the red pixel values across the chosen row
    fig, ax = plt.subplots(figsize=(fs, .7*fs))
    ax.scatter(x, abs(intensity - np.median(intensity)), c='tab:green', s=1)
    ax.set_ylabel("Red Pixel Value")
    ax.set_xlabel("Horizontal Pixel")
    
    
    params, covar = curve_fit(gaussian, x, abs(intensity - np.median(intensity)))
    gauss_fit = gaussian(x, params[0], params[1], params[2])
    
    
    max_val = max(gauss_fit)
    max_ind = np.argwhere(gauss_fit == max_val)[0][0]
    
    a = 0
    currval = max_val
    while currval > max_val / 2:
        currval = gauss_fit[max_ind + a]
        a += 1
    
    accept_angle = a # pixels
    
    ax.plot(x, gauss_fit, lw=2, c='tab:blue')
    for sign in [1, -1]:
        ax.axvline(max_ind + sign * a, c='r', ls='--')
        
    ax.set_ylim(ymin=0)
    ax.set_xlim(0, image.shape[1])
    ax.grid()
    fig.savefig(im_name + '-fit.png', bbox_inches='tight', dpi=300)
    fig.savefig(im_name + '-fit.pdf', bbox_inches='tight', dpi=300)
    
    if 'single' in im_name:
        adjacent = float(im_name.replace('single', ''))
        opposite = accept_angle / single_ppcm
        a = 4.3 * 10e-6 
    elif 'multi' in im_name:
        adjacent = float(im_name.replace('multi', ''))
        opposite = accept_angle / multi_ppcm
        a = 100 * 10e-6 
    theta = np.arctan(opposite / adjacent)
    NA[i] = np.sin(theta)
    
    wavelen = 633 * 10e-9 
    k = 2 * np.pi / wavelen
    V[i] = k * a * NA[i]
    M[i] = V[i]**2 / 2
    
    
    
    # now show the image along with the chosen row
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.axhline(row)
    ax.set_xlabel("Horizontal Pixel")
    ax.set_ylabel("Vertical Pixel")
    
    fig.savefig(im_name + '-row.png', bbox_inches='tight', dpi=300)
    fig.savefig(im_name + '-row.pdf', bbox_inches='tight', dpi=300)


plt.close('all')
