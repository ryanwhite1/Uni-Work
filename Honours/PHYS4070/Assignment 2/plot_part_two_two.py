import numpy as np
import matplotlib.pyplot as plt

# set LaTeX font for our figures
plt.rcParams.update({"text.usetex": True})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'

t_crit = (2 / np.log(1 + 2**0.5))

dimensions = [10, 20, 40, 80]

shfig, shax = plt.subplots()    ### specific heat figure
msfig, msax = plt.subplots()    ### magnetic susceptibility figure

re_shfig, re_shax = plt.subplots()    ### rescaled specific heat figure
re_msfig, re_msax = plt.subplots()    ### rescaled magnetic susceptibility figure


for i, dim in enumerate(dimensions):
    

    data = np.genfromtxt(f'Ising_Datasets/Part2_2_ndim={dim}.txt')
    
    temperatures = np.unique(data[:, 0])[:-1]
    
    energies = np.zeros(len(temperatures))
    energy_err = np.zeros(len(temperatures))
    magnetisations = np.zeros(len(temperatures))
    mag_errs = np.zeros(len(temperatures))
    spec_heat = np.zeros(len(temperatures))
    mag_sus = np.zeros(len(temperatures))

    N_s = dim*dim

    for i, temp in enumerate(temperatures):
        subdata = data[np.where(data[:, 0] == temp), :][0, :, :]
        sub_energies = subdata[:, 1]
        energies[i] = np.mean(sub_energies)
        energy_err[i] = np.sqrt(np.var(sub_energies) / len(sub_energies))
        
        sub_mags = subdata[:, 2]
        magnetisations[i] = np.mean(sub_mags)
        mag_errs[i] = np.sqrt(np.var(sub_mags) / len(sub_mags))
        
        spec_heat[i] = np.var(sub_energies) * N_s / (temp**2)
        mag_sus[i] = np.var(np.abs(sub_mags)) * N_s / temp
    
    shax.scatter(temperatures, spec_heat, label=fr'${dim}\times{dim}$')
    msax.scatter(temperatures, mag_sus, label=fr'${dim}\times{dim}$')
    
    rescaled_temps = ((temperatures - t_crit) / t_crit) * dim
    rescaled_spec_heat = spec_heat / np.log(dim)
    rescaled_mag_sus = mag_sus / (dim**(7/4))
    
    re_shax.scatter(rescaled_temps, rescaled_spec_heat, label=fr'${dim}\times{dim}$')
    re_msax.scatter(rescaled_temps, rescaled_mag_sus, label=fr'${dim}\times{dim}$')
    
    

shax.axvline(t_crit, c='tab:red', ls='--')
shax.set(xlabel='Temperature, $T$', ylabel=r'Specific Heat per spin')
re_shax.set(xlabel='Rescaled Temperature, $t$', ylabel=r'Finite Size Specific Heat per spin')
msax.set(xlabel='Temperature, $T$', ylabel=r'Magnetic Susceptibility per spin', yscale='log')
re_msax.set(xlabel='Rescaled Temperature, $t$', ylabel=r'Finite Size Magnetic Susceptibility per spin', xlim=(-10, 20))

for ax in [shax, msax, re_shax, re_msax]:
    ax.legend()
    
shfig.savefig('Part_2_21_SpecHeat-Temp.png', dpi=400, bbox_inches='tight')
shfig.savefig('Part_2_21_SpecHeat-Temp.pdf', dpi=400, bbox_inches='tight')
msfig.savefig('Part_2_21_MagSus-Temp.png', dpi=400, bbox_inches='tight')
msfig.savefig('Part_2_21_MagSus-Temp.pdf', dpi=400, bbox_inches='tight')
re_shfig.savefig('Part_2_22_SpecHeat-Temp.png', dpi=400, bbox_inches='tight')
re_shfig.savefig('Part_2_22_SpecHeat-Temp.pdf', dpi=400, bbox_inches='tight')
re_msfig.savefig('Part_2_22_MagSus-Temp.png', dpi=400, bbox_inches='tight')
re_msfig.savefig('Part_2_22_MagSus-Temp.pdf', dpi=400, bbox_inches='tight')
    
    
    
    
    
    
data = np.genfromtxt(f'Ising_Datasets/Part2_2_Power.txt')
temperatures = np.unique(data[:, 0])[:-1]

energies = np.zeros(len(temperatures))
energy_err = np.zeros(len(temperatures))
magnetisations = np.zeros(len(temperatures))
mag_errs = np.zeros(len(temperatures))
spec_heat = np.zeros(len(temperatures))
mag_sus = np.zeros(len(temperatures))

N_s = dim*dim

for i, temp in enumerate(temperatures):
    subdata = data[np.where(data[:, 0] == temp), :][0, :, :]
    sub_energies = subdata[:, 1]
    energies[i] = np.mean(sub_energies)
    energy_err[i] = np.sqrt(np.var(sub_energies) / len(sub_energies))
    
    sub_mags = subdata[:, 2]
    magnetisations[i] = np.mean(sub_mags)
    mag_errs[i] = np.sqrt(np.var(sub_mags) / len(sub_mags))
    
    spec_heat[i] = np.var(sub_energies) * N_s / (temp**2)
    mag_sus[i] = np.var(np.abs(sub_mags)) * N_s / temp
    
### now calculate the vertical shifts required 
import scipy.optimize as opt
## define our fitting functions
def vert_shift(c, x, y):
    return c * x - y
def log_vert_shift(c, x, y):
    return np.log10(c * x) - np.log10(y)
# now do a least squares regression to get our vertical shift multiplier for each plot
mag_shift = opt.least_squares(vert_shift, 1., args=(np.abs(temperatures - t_crit)**(1/8), np.abs(magnetisations))).x
magsus_shift = opt.least_squares(log_vert_shift, 1., args=(np.abs(temperatures - t_crit)**(-7/4), mag_sus)).x


fig, ax = plt.subplots()
ax.errorbar(np.abs(temperatures - t_crit), np.abs(magnetisations), yerr=mag_errs, fmt='.', label='Experiment')
ax.plot(np.abs(temperatures - t_crit), np.abs(temperatures - t_crit)**(1/8) * mag_shift, label='Power Law')
ax.set(xscale='log', yscale='log', xlabel='Rescaled Temperature, $|T - T_c|$', ylabel='Magnetisation per spin')
ax.legend()
fig.savefig('Part_2_23_Mag-Temp.png', dpi=400, bbox_inches='tight')
fig.savefig('Part_2_23_Mag-Temp.pdf', dpi=400, bbox_inches='tight')

fig, ax = plt.subplots()
ax.scatter(np.abs(temperatures - t_crit), mag_sus, label='Experiment')
ax.plot(np.abs(temperatures - t_crit), np.abs(temperatures - t_crit)**(-7/4) * magsus_shift, label='Power Law')
ax.set(xscale='log', yscale='log', xlabel='Rescaled Temperature, $|T - T_c|$', ylabel='Magnetic Susceptibility per spin')
ax.legend()
fig.savefig('Part_2_23_MagSus-Temp.png', dpi=400, bbox_inches='tight')
fig.savefig('Part_2_23_MagSus-Temp.pdf', dpi=400, bbox_inches='tight')





