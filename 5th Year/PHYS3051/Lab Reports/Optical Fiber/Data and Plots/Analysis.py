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
def cosSquare(x, A, S, B):
    return A * np.cos(x - S)**2 + B
def acceptance_angle(yvals):
    max_val = max(yvals)
    max_ind = np.argwhere(yvals == max_val)[0][0]
    
    a = 0
    currval = max_val
    
    while currval > max_val * 0.05:
        currval = yvals[max_ind + a]
        a += 1
    return a

def monte_carlo(x, y, xerr, yerr, iters, func, p0=None, method='fit'):
    '''
    '''
    if isinstance(x, np.float64):
        n2 = 1
    else:
        n2 = len(p0) if p0 != None else len(x)
    params = np.zeros((iters, n2))
    
    for i in range(iters):
        new_x = np.random.normal(x, xerr)
        
        if method == 'fit':
            new_y = np.random.normal(y, yerr)
            iter_params, covar = curve_fit(func, new_x, new_y, p0=p0, maxfev=1500)
        elif method == 'find':
            iter_params = func(new_x)
        params[i] = iter_params
    
    if method == 'fit':
        means = np.array([np.mean(params[:, j]) for j in range(n2)])
        stds =  np.array([np.std(params[:, j]) for j in range(n2)])
    elif method == 'find':
        means = np.mean(params)
        stds = np.std(params)
    return means, stds

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

# pol_params, pol_params_unc = monte_carlo(polarisation_angles, polarisation_means,
#                                          4 * np.pi/180, polarisation_stds, 
#                                          1000, sine, p0=[5.5, np.pi, 0, 5.5])
x = np.linspace(0, max(polarisation_angles), 100)
# fit_y = sine(x, pol_params[0], pol_params[1], pol_params[2], pol_params[3])

pol_params, pol_params_unc = monte_carlo(polarisation_angles, polarisation_means,
                                         4 * np.pi/180, polarisation_stds, 
                                         1000, cosSquare, p0=[12, 1, 0])
fit_y = cosSquare(x, pol_params[0], pol_params[1], pol_params[2])

ax.plot(x, fit_y, c='tab:blue')
ax.set_ylim(ymin=0)

ax.set_xlabel('Polarisation Filter Rotation (rad)')
ax.set_ylabel('Mean Voltage (mV)')
ax.grid()

fname = 'PolarisationFit'
fig.savefig(fname + '.png', bbox_inches='tight', dpi=300)
fig.savefig(fname + '.pdf', bbox_inches='tight', dpi=300)

# predicted = sine(polarisation_angles, pol_params[0], pol_params[1], pol_params[2], pol_params[3])
predicted = cosSquare(polarisation_angles, pol_params[0], pol_params[1], pol_params[2])
chi2_polarised = sum((polarisation_means - predicted)**2 / predicted)
chi2_dof_polarised = chi2_polarised / len(predicted)

ext = lambda x: (x[0] + x[1]) / x[0]
extinction, extinction_unc = monte_carlo(np.array([pol_params[2], pol_params[0]]), None,
                         np.array([pol_params_unc[2], pol_params_unc[0]]), None,
                         1000, ext, method='find')




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
M, M_unc = np.zeros(len(names)), np.zeros(len(names))
V, V_unc = np.zeros(len(names)), np.zeros(len(names))
NA_vals, NA_unc = np.zeros(len(names)), np.zeros(len(names))
accept_angle, accept_angle_unc = np.zeros(len(names)), np.zeros(len(names))
chi2, chi2_dof = np.zeros(len(names)), np.zeros(len(names))

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
    
    red_level = abs(intensity - np.median(intensity))
    # c = intensity[0]
    # m = (intensity[-1] - intensity[0]) / image.shape[1]
    # red_level = abs(intensity - (m * x + c))
    
    # show the red pixel values across the chosen row
    fig, ax = plt.subplots(figsize=(fs, .7*fs))
    
    ax.scatter(x, red_level, c='tab:green', s=1)
    ax.set_ylabel("Red Pixel Value")
    ax.set_xlabel("Horizontal Pixel")
    
    
    params, stds = monte_carlo(x, red_level, 3, np.sqrt(red_level), 2000, gaussian, p0=[150, 500, 10])
    
    
    gauss_fit = gaussian(x, params[0], params[1], params[2])
    val1 = round(params[1] - 2 * params[2])
    val2 = round(params[1] + 2 * params[2])
    chi2[i] = sum((red_level[val1:val2] - gauss_fit[val1:val2])**2 / gauss_fit[val1:val2])
    chi2_dof[i] = chi2[i] / len(x[val1:val2])
    
    n = 2000
    accept_angles = np.zeros(n)
    for j in range(n):
        a = np.random.normal(params[0], stds[0])
        b = np.random.normal(params[1], stds[1])
        c = np.random.normal(params[2], stds[2])
        gauss_fit = gaussian(x, a, b, c)
        accept_angles[j] = acceptance_angle(gauss_fit) # pixels
        
    accept_angle[i] = min(np.mean(accept_angles), 2 * params[2])
    accept_angle_unc[i] = np.std(accept_angles)
    
    ax.plot(x, gauss_fit, lw=2, c='tab:blue')
    for sign in [1, -1]:
        ax.axvline(params[1] + sign * accept_angle[i], c='r', ls='--')
        
    ax.set_ylim(ymin=0)
    ax.set_xlim(0, image.shape[1])
    ax.grid()
    fig.savefig(im_name + '-fit.png', bbox_inches='tight', dpi=300)
    fig.savefig(im_name + '-fit.pdf', bbox_inches='tight', dpi=300)
    
    if 'single' in im_name:
        adjacent = float(im_name.replace('single', ''))
        opposite = accept_angle[i] / single_ppcm
        opposite_err = accept_angle_unc[i] / single_ppcm
        a = 4.3 * 10e-6 / 2
    elif 'multi' in im_name:
        adjacent = float(im_name.replace('multi', ''))
        opposite = accept_angle[i] / multi_ppcm
        opposite_err = accept_angle_unc[i] / multi_ppcm
        a = 100 * 10e-6 / 2
    adjacent_err = 1.5
    na = lambda x: np.sin(np.arctan(x[0] / x[1]))
    
    NA_vals[i], NA_unc[i] = monte_carlo(np.array([opposite, adjacent]), None, 
                                   np.array([opposite_err, adjacent_err]), None, 
                                   1000, na, method='find')
    
    
    wavelen = 633 * 10e-9 
    k = 2 * np.pi / wavelen
    Vfunc = lambda x: k * a * x
    V[i], V_unc[i] = monte_carlo(NA_vals[i], None,
                                 NA_unc[i], None,
                                 1000, Vfunc, method='find')
    Mfunc = lambda x: x**2 / 2
    M[i], M_unc[i] = monte_carlo(V[i], None,
                                 V_unc[i], None,
                                 1000, Mfunc, method='find')
    
    
    
    # now show the image along with the chosen row
    fig, ax = plt.subplots(figsize=(fs, 72/96 * fs))
    ax.set_aspect('equal')
    ax.imshow(image)
    ax.axhline(row)
    ax.set_xlabel("Horizontal Pixel")
    ax.set_ylabel("Vertical Pixel")
    
    fig.savefig(im_name + '-row.png', bbox_inches='tight', dpi=300)
    fig.savefig(im_name + '-row.pdf', bbox_inches='tight', dpi=300)


plt.close('all')

ave = lambda x: sum(x) / len(x)
V_single, V_single_unc = monte_carlo(V[:len(single_dists)], None,
                                     V_unc[:len(single_dists)], None,
                                     1000, ave, method='find')
V_multi, V_multi_unc = monte_carlo(V[len(single_dists):], None,
                                     V_unc[len(single_dists):], None,
                                     1000, ave, method='find')
NA_single, NA_single_unc = monte_carlo(NA_vals[:len(single_dists)], None,
                                     NA_unc[:len(single_dists)], None,
                                     1000, ave, method='find')
NA_multi, NA_multi_unc = monte_carlo(NA_vals[len(single_dists):], None,
                                     NA_unc[len(single_dists):], None,
                                     1000, ave, method='find')
M_single, M_single_unc = monte_carlo(M[:len(single_dists)], None,
                                     M_unc[:len(single_dists)], None,
                                     1000, ave, method='find')
M_multi, M_multi_unc = monte_carlo(M[len(single_dists):], None,
                                     M_unc[len(single_dists):], None,
                                     1000, ave, method='find')


