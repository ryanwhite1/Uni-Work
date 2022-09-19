# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 07:17:11 2022

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as sciop
import scipy.integrate as sciint
plt.rcParams['font.family'] = 'Serif'

def blackbody(x, temp, scale):
    '''Returns the radiant emittance (power per unit area) of a blackbody. x is given in units of meters
    '''
    h = 6.626 * 10**-34
    c = 299792458
    boltz = 1.38 * 10**-23
    rEmit = scale * (2 * np.pi * c**2 * h / x**5)  / (np.exp(c * h / (x * boltz * temp)) - 1)
    return rEmit

voltData = {}

# voltages = ["1Vb", "2Vb", "3Vb", "4Vb", "5V", "6Vb", "7V"]
voltages = ["2Vb", "3Vb", "4Vb", "5V", "6Vb", "7V"]
for voltage in voltages:
    with open(f'Data/{voltage}_Merge0.TXT', "r") as inputFile:
        i = 0
        wavs = []
        flux = []
        for line in inputFile:
            if i > 1 and len(line) > 2:
                string = line.split(';')
                if not (845 <= float(string[0]) <= 869):
                    wavs.append(float(string[0]))
                    flux.append(float(string[1]))
            i += 1
        voltData[f'{voltage[:1]}'] = np.array([wavs, flux])

bestTemps = np.zeros(len(voltages))
bestTempUnc = np.zeros(len(voltages))
scales = np.zeros(len(voltages))
for i, voltage in enumerate(voltData):
    x = voltData[f'{voltage}'][0] * 10**-9
    y = voltData[f'{voltage}'][1]
    popt, pcov = sciop.curve_fit(blackbody, xdata=x, ydata=y, p0=[2000, 1/50000])
    bestTemps[i] = popt[0]
    bestTempUnc[i] = pcov[0, 0]
    scales[i] = popt[1]
            

maxwave = 0
maxfluxes = np.zeros(len(voltages))
avefluxes = np.zeros(len(voltages))
peakwavelengths = np.zeros(len(voltages))
AUC = np.zeros(len(voltages))

fig, ax = plt.subplots(figsize=(10, 4))
fig2, ax2= plt.subplots(figsize=(10, 4))
colours = plt.rcParams['axes.prop_cycle'].by_key()['color']
colours = colours[:len(voltages)]

emiss = []

for i, voltage in enumerate(reversed(voltData)):
    wavelengths = voltData[f'{voltage}'][0]
    flux = voltData[f'{voltage}'][1]
    avefluxes[len(voltages)-1 - i] = np.mean(flux)
    maxwave = max(wavelengths) if max(wavelengths) > maxwave else maxwave
    peakwavelengths[len(voltages)-1 -i] = wavelengths[np.where(flux == max(flux))]
    maxfluxes[len(voltages)-1 - i] = max(flux)
    
    # AUC[i] = sciint.simpson(flux / 100, wavelengths*10**-9)
    
    ax.scatter(wavelengths, flux / 100, s=0.1, c=colours[i])
    ax.plot(wavelengths, blackbody(wavelengths*10**-9, bestTemps[len(voltages) - i-1], scales[len(voltages) - i-1]) / 100, 
            c=colours[i], label=f'{voltage}V', lw=1)
    
    indexes = []
    for l, w in enumerate(wavelengths):
        if w > 480:
            indexes.append(l)
    emiss.append(flux[indexes] / blackbody(wavelengths[indexes]*10**-9, bestTemps[len(voltages) - i-1], scales[-1]))
    print(np.mean(emiss[i]))
    ax2.plot(wavelengths[indexes], emiss[i], label=f'{voltage}V', lw=1, c=colours[i])
    
    # emiss.append(flux / blackbody(wavelengths*10**-9, bestTemps[len(voltages) - i-1], scales[-1]))
    # ax2.plot(wavelengths, emiss[i], label=f'{voltage}V', lw=0.5, c=colours[i])

meanemiss = np.array([np.mean(emiss[len(emiss)-1 - j]) for j in range(len(emiss))])

print(meanemiss)
print(bestTemps)

ax.set_ylim(ymin=0)
ax.set_xlim(xmax = maxwave)
ax.grid(); ax.legend()
ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Relative Irradiance (prop. of 7V)")
fig.savefig('Blackbody Curves.png', dpi=400, bbox_inches='tight')
fig.savefig('Blackbody Curves.pdf', dpi=400, bbox_inches='tight')

ax2.set_ylabel("Emissivity (prop. of 7V $\epsilon$)")
ax2.set_xlabel("Wavelength (nm)")
ax2.set_ylim(0, 1.5)
ax2.set_xlim(xmax = maxwave)
ax2.grid(); ax2.legend()
fig2.savefig("Emissivity Curves.png", dpi=400, bbox_inches='tight')
fig2.savefig("Emissivity Curves.pdf", dpi=400, bbox_inches='tight')

fig, ax = plt.subplots()
ax.scatter(bestTemps, np.log((1 / 0.329814) - meanemiss))
ax.set_xlabel("Temperature (K)")
ax.set_ylabel("Log Emissivity Difference")
ax.grid()
fig.savefig("Log Emiss.png", dpi=400, bbox_inches='tight')
fig.savefig("Log Emiss.pdf", dpi=400, bbox_inches='tight')

def meanemissCurve(temp, metal, c):
    return c * (1 - np.exp(-metal * temp))

# fig, ax = plt.subplots()
# ax.scatter(bestTemps, meanemiss)
# tungsten, tungUnc = sciop.curve_fit(meanemissCurve, xdata=bestTemps, ydata=meanemiss, p0=[1.5*10**-4, 0.5])
# tungUnc = np.sqrt(tungUnc)
# print(tungsten)
# ax.plot(bestTemps, meanemissCurve(bestTemps, tungsten[0], tungsten[1]))

# fig, ax = plt.subplots()
# ax.scatter(bestTemps, avefluxes)
# meanBlackbods = [np.mean(blackbody(wavelengths, bestTemps[i], scales[i])) for i in range(len(voltages))]
# emissivity = avefluxes / meanBlackbods

# for i, voltage in enumerate(voltData):
# def emissCurve(temp, const):
#     return 1 - np.exp(-const * temp)
# popt, pcov = sciop.curve_fit(emissCurve, xdata=bestTemps, ydata=AUC, p0=[1.5*10**-4])
    
# ax.scatter(bestTemps, AUC)
# ax.plot(bestTemps, emissCurve(bestTemps, popt))
# fig, ax = plt.subplots()
# ax.scatter(bestTemps[:-1], np.log((1 / 0.329814) - avefluxes[:-1] / 100))
# ax.scatter(bestTemps[:-1], np.log((1 / 0.329814) - AUC[:-1]))
    


def wienslaw(temp, boltzmann):
    h = 6.626 * 10**-34
    c = 299792458
    peak = 0.2014 * h * c / (boltzmann * temp)
    return peak

popt, pcov = sciop.curve_fit(wienslaw, xdata=bestTemps[1:]*10**-9, ydata=peakwavelengths[1:], p0=1.28*10**-23)
boltz = popt
boltzUnc = np.sqrt(pcov)
fig, ax = plt.subplots()

ax.errorbar(1 / bestTemps[1:], peakwavelengths[1:], xerr=bestTempUnc[1:] / bestTemps[1:], c='r', fmt='.')
# the error in the above might need to be Unc / T**2 ??
ax.plot(1 / bestTemps[1:], wienslaw(bestTemps[1:], popt)*10**9)
ax.set_xlabel("Inverse Temperature (K$^{-1}$)")
ax.set_ylabel("Peak Wavelength (nm)")
ax.grid()
fig.savefig("Peak Wavelength vs Temp.png", dpi=400, bbox_inches='tight')
fig.savefig("Peak Wavelength vs Temp.pdf", dpi=400, bbox_inches='tight')

with open('Results.txt', "w") as output:
    output.write(f"Boltzmann Constant = {boltz} \pm {boltzUnc} \n")
    output.write("Best Temps/Mean emissivities: \n")
    for i, emis in enumerate(meanemiss):
        output.write(f"V = {voltages[i]};  T = {bestTemps[i]}K;  Scale = {1 / scales[i]};  meanemiss = {emis}\n")
    
    