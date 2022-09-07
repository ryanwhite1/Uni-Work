# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 17:49:37 2022

@author: ryanw
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Serif'

# data has columns of "Temperature, Delta Temp, Real VBE, VBE, IC uA, Delta IC"
data = pd.read_csv('BoltzmannData.csv', delimiter=',')

temps = np.array([221, 293, 333, 363, 374])
gradients, intercepts, interceptsErr, saturats = np.ones(len(temps)), np.ones(len(temps)), np.ones(len(temps)), np.ones(len(temps))

colours = plt.rcParams['axes.prop_cycle'].by_key()['color']
colours = colours[:len(temps)]

fig, ax = plt.subplots(figsize=(10, 5))
ax.grid()
grad_old, sing_vals_old = 0, 0
outputFile = open("AnalysisResults.txt", "w")
outputFile.write("IC vs Vbe \n")
for num, temp in enumerate(temps):
    indexes = [i for i, x in enumerate(data["Temperature"]) if x == temp]
    temp_voltage = data["Real VBE"][indexes].to_numpy()
    temp_current = data["IC uA"][indexes].to_numpy()
    temp_currentErr = data["Delta IC"][indexes].to_numpy()
    real_indexes = [i for i, x in enumerate(temp_current) if x > 0]
    temp_voltage = temp_voltage[real_indexes]
    temp_current = temp_current[real_indexes]
    temp_currentErr = temp_currentErr[real_indexes]
    temp_lnCurrent = np.log(temp_current)
    
    R2 = np.zeros(len(real_indexes))
    for i in range(5, len(real_indexes)):
        grad, residuals, rank, sing_vals, rcond = np.polyfit(temp_voltage[:i], temp_lnCurrent[:i], 
                                                                  full = True, deg=1, cov=True)
        R2[i] = 1 - sum(residuals) / sum([(temp_lnCurrent[j] - np.mean(temp_lnCurrent))**2 for j in range(0, i + 1)])
        if R2[i] < R2[i - 1]:
            ax.plot([temp_voltage[0], temp_voltage[i-1]], [temp_lnCurrent[0], temp_lnCurrent[i-1]], c=colours[num], lw=1)
            outputFile.write(f"{temp} -- Est. Sat. Point = {temp_current[i]} \n")
            outputFile.write(f"{temp} -- m = {grad_old[0]}, dm = {sing_vals_old[0]} \n")
            outputFile.write(f"{temp} -- c = {grad_old[1]}, dc = {sing_vals_old[1]} \n \n")
            gradients[num] = grad_old[0]
            intercepts[num] = grad_old[1]
            interceptsErr[num] = sing_vals_old[1]
            saturats[num] = temp_current[i]
            break
        else:
            grad_old, sing_vals_old = grad, sing_vals
    
    ax.scatter(temp_voltage, temp_lnCurrent, label=f"{temp}K", c = colours[num], s = 15)
    ax.errorbar(temp_voltage, temp_lnCurrent, yerr = 10 * temp_currentErr / temp_current, fmt='none', c = colours[num], lw=1)

ax.legend(title="Temperature")

ax.set_ylabel("Log Collector Current     ln$(I_C)$ ($\mu$A)")
ax.set_xlabel("Voltage     $V_{BE}$ (V)")

fig.savefig("ln(IC) vs Vbe.png", dpi = 400, bbox_inches='tight')
fig.savefig("ln(IC) vs Vbe.pdf", dpi = 400, bbox_inches='tight')
plt.close()


# now part 2 -- finding the band gap


plt.rc('font', size=13.5) 

tempErr = np.zeros(len(temps))
for num, temp in enumerate(temps):
    indexes = [i for i, x in enumerate(data["Temperature"]) if x == temp]
    tempErr[num] = data["Delta Temp"][indexes].to_numpy()[0]

ColCurrTemps = intercepts - np.log(temps**(3/2))
invTemps = 1 / temps
invTempsErr = invTemps * tempErr / temps

ColCurrTempsErr = np.sqrt(interceptsErr**2 + ((3/2) * np.sqrt(temps) * tempErr / temps)**2)

fig, ax = plt.subplots()
ax.scatter(invTemps, ColCurrTemps, s=10)
ax.errorbar(invTemps, ColCurrTemps, xerr = invTempsErr, yerr=ColCurrTempsErr, fmt='none')

phi_grad, residuals, rank, sing_vals, rcond = np.polyfit(invTemps, ColCurrTemps, deg=1, full=True)
trendY = [phi_grad[0] * x + phi_grad[1] for x in [invTemps[0], invTemps[-1]]]
ax.plot([invTemps[0], invTemps[-1]], trendY)

ax.grid()
ax.set_ylabel("Log Current over Temperature     ln($I_0 T^{-3/2}$)")
ax.set_xlabel("Inverse Temperature     (K$^{-1}$)")
ax.ticklabel_format(axis='x', style='sci', useMathText=True, scilimits=(-2, 2))



fig.savefig("ln(I0T) vs T.png", dpi = 400, bbox_inches='tight')
fig.savefig("ln(I0T) vs T.pdf", dpi = 400, bbox_inches='tight')
plt.close()

outputFile.write("ln(I0T) vs 1/T \n")
outputFile.write(f"phi / k = {phi_grad[0]} \pm {sing_vals[0]}\n")


# part 3 - saturation
fig, ax = plt.subplots()

sat_volts = np.array([0.765, 0.633, 0.535, 0.486, 0.442])
sat_voltsErr = np.array([0.03, 0.03, 0.02, 0.02, 0.02])
ax.scatter(temps, sat_volts, s = 10)
ax.errorbar(temps, sat_volts, xerr=tempErr, yerr=sat_voltsErr, fmt='none')

mc, residuals, rank, sing_vals, rcond = np.polyfit(temps, sat_volts, deg=1, full=True)
m, c = mc
trendY = [m * x + c for x in [temps[0], temps[-1]]]
ax.plot([temps[0], temps[-1]], trendY)

ax.grid()

ax.set_xlabel("Temperature  (K)")
ax.set_ylabel("Saturation Voltage Difference   $V_{BE}$ (V)")


fig.savefig("Sat. Vbe vs T.png", dpi = 400, bbox_inches='tight')
fig.savefig("Sat. Vbe vs T.pdf", dpi = 400, bbox_inches='tight')
plt.close()

outputFile.close()