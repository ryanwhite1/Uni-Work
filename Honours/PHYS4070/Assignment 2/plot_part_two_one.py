import numpy as np
import matplotlib.pyplot as plt

# set LaTeX font for our figures
plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'

data = np.genfromtxt('Ising_Datasets/Part2_1_run_1.txt')

temperatures = np.unique(data[:, 0])[:-1]

energies = np.zeros(len(temperatures))
energy_err = np.zeros(len(temperatures))
magnetisations = np.zeros(len(temperatures))
mag_errs = np.zeros(len(temperatures))
spec_heat = np.zeros(len(temperatures))
mag_sus = np.zeros(len(temperatures))

N_s = 20 * 20

for i, temp in enumerate(temperatures):
    subdata = data[np.where(data[:, 0] == temp), :][0, :, :]
    sub_energies = subdata[:, 1] / N_s
    energies[i] = np.mean(sub_energies)
    energy_err[i] = np.sqrt(np.var(sub_energies) / len(sub_energies))
    
    sub_mags = subdata[:, 2]
    magnetisations[i] = np.mean(sub_mags)
    mag_errs[i] = np.sqrt(np.var(sub_mags) / len(sub_mags))
    
    spec_heat[i] = np.var(sub_energies) * N_s / (temp**2)
    mag_sus[i] = np.var(np.abs(sub_mags)) * N_s / temp
    
fig, ax = plt.subplots()
ax.errorbar(temperatures, energies, yerr=energy_err, fmt='.')
ax.set(xlabel='Temperature, $T$', ylabel=r'Mean Energy per spin, $\langle E \rangle$')

fig, ax = plt.subplots()
ax.errorbar(temperatures, np.abs(magnetisations), yerr=mag_errs, fmt='.', label='Experimental')

t_crit = (2 / np.log(1 + 2**0.5))
true_temps = np.linspace(min(temperatures), max(temperatures), 100)
true_mag = np.array([(1 - np.sinh(2 / temp)**-4)**(1/8) if temp < t_crit else 0 for temp in true_temps])
ax.plot(true_temps, true_mag, label='Theoretical')
ax.set(xlabel='Temperature, $T$', ylabel=r'Absolute Mean Magnetisation per spin, $\langle M \rangle$')
ax.legend()

fig, ax = plt.subplots()
ax.scatter(temperatures, spec_heat)
ax.axvline(t_crit, c='tab:red', ls='--')
ax.set(xlabel='Temperature, $T$', ylabel=r'Specific Heat per spin')

fig, ax = plt.subplots()
ax.scatter(temperatures, mag_sus)
ax.set(xlabel='Temperature, $T$', ylabel=r'Magnetic Susceptibility per spin')
