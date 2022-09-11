# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 12:55:13 2022

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(3020)
# k = 1.38 * 10**-23

plt.rcParams['font.family'] = 'Serif'

def gen_init_Ising(N):
    initState = np.random.uniform(0, 1, N)
    s = [1 if initState[i] >= 0.5 else -1 for i in range(N)]
    return s

def plot_1d_Ising(states, rows, name=None):
    if len(states) == 1:
        img = []
        for i in range(rows):
            img.append(states)
        img = np.array(img)
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.set_xlabel("Dipole")
    else:              
        from matplotlib import gridspec
        fig = plt.figure(figsize=(7, 2)) 

        gs = gridspec.GridSpec(len(states), 1,
                 wspace=0.0, hspace=0.0, top=1.-0.5/(len(states)+1), bottom=0.5/(len(states)+1), 
                 left=0.5/(1+1), right=1-0.5/(1+1)) 
        
        for k in range(len(states)):
            ax = plt.subplot(gs[k])
            img = []
            for i in range(rows):
                img.append(states[k])
            img = np.array(img)
            ax.imshow(img)
            # ax.set_ylabel(f"State {k}"); 
            ax.get_yaxis().set_ticks([])
            if k == len(states) - 1:
                ax.set_ylabel("Final")
                ax.set_xlabel("Dipole")
            else:
                if k == 0:
                    ax.set_ylabel("Initial")
                ax.get_xaxis().set_ticks([])
            
    if name != None:
        fig.savefig(name + ".png", dpi=400, bbox_inches='tight')
        fig.savefig(name + ".pdf", dpi=400, bbox_inches='tight')
    
def metropolis(states, iters, temperature):
    beta = 1 / temperature
    RVs = np.random.uniform(0, len(states) - 1, iters)
    RVs = [int(x) for x in RVs]
    for i in range(iters):
        if RVs[i] == len(states) - 1:
            Ldipole = states[RVs[i] - 1]
            Rdipole = states[0]
        elif RVs[i] == 0:
            Ldipole = states[len(states) - 1]
            Rdipole = states[1]
        else:
            Ldipole = states[RVs[i] - 1]
            Rdipole = states[RVs[i] + 1]
        energy = lambda D : -1 * ((Ldipole * D) + (Rdipole * D))
        dipole = states[RVs[i]]
        initEnergy = energy(dipole)
        flipEnergy = energy(-1 * dipole)
        deltaEnergy = flipEnergy - initEnergy
        if deltaEnergy <= 0:
            dipole *= -1
        else:
            flipProb = np.exp(-beta * deltaEnergy)
            evaluation = np.random.uniform(0, 1)
            if evaluation <= flipProb:
                dipole *= -1
        states[RVs[i]] = dipole
    return states

def Q1a():
    temps = [0.5, 1, 2, 5]
    for temp in temps:
        a = gen_init_Ising(100)
        a1 = a.copy()
        
        b = metropolis(a1, 100000, temp)
        plot_1d_Ising([a, b], 10, name=f"Q1a-Temp={temp}")

def Q1c(trials=3):
    # temps = [0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1, 1.5, 2, 3.5, 5]
    temps = np.linspace(0.02, 5, 15)
    ufig, uax = plt.subplots()
    ffig, fax = plt.subplots()
    Sfig, Sax = plt.subplots()
    cfig, cax = plt.subplots()
    Mfig, Max = plt.subplots()
    
    domain = np.linspace(min(temps), max(temps), 100)
    beta = 1 / domain
    uax.plot(domain, -1 * np.tanh(beta))
    fax.plot(domain, -1 - np.log(1 + np.exp(-2 * beta)) / beta)
    Sax.plot(domain, (1 / domain) * (1 - np.tanh(beta)) + np.log(1 + np.exp(-2 * beta)))
    cax.plot(domain, beta**2 / (np.cosh(beta))**2)
    
    uax.set_xlabel("Temperature ($\epsilon / k$)")
    fax.set_xlabel("Temperature ($\epsilon / k$)")
    Sax.set_xlabel("Temperature ($\epsilon / k$)")
    cax.set_xlabel("Temperature ($\epsilon / k$)")
    Max.set_xlabel("Temperature ($\epsilon / k$)")
    
    uax.set_ylabel("Internal Energy ($\epsilon$)")
    fax.set_ylabel("Free Energy ($\epsilon$)")
    Sax.set_ylabel("Entropy ($\epsilon / K$)")
    cax.set_ylabel("Specific Heat Capacity ($\epsilon / K$)")
    Max.set_ylabel("Reduced Magnetisation per Dipole")
    
    uax.grid(); fax.grid(); Sax.grid(); cax.grid(); Max.grid()
    
    for t, temp in enumerate(temps):
        intEnergy = np.zeros(trials)
        intEnergy2 = np.zeros(trials)
        S = np.zeros(trials)
        f = np.zeros(trials)
        c = np.zeros(trials)
        m = np.zeros(trials)
        for i in range(trials):
            N = 100
            a = gen_init_Ising(N)
            b = metropolis(a.copy(), 100000, temp)
            
            for j in range(N):
                right = 0 if j == N - 1 else j + 1
                intEnergy[i] += b[j] * b[right]
                intEnergy2[i] += (b[j] * b[right])**2
            intEnergy[i] *= -1 / N # internal energy per dipole
            intEnergy2[i] /= N
            
            NUp = [1 if x == 1 else 0 for x in b]; NUp = np.sum(NUp) # number of up spin-up dipoles
            if NUp == 0 or N - NUp == 0:
                S[i] = 0
            else:
                S[i] = (1 / N) * (N * np.log(N) - NUp * np.log(NUp) - (N - NUp) * np.log(N - NUp)) # entropy per dipole
            
            f[i] = intEnergy[i] - temp * S[i]
            
            m[i] = np.mean(b) # reduced magnetisation per dipole
            
            c[i] = (1 / temp)**2 * (intEnergy2[i] - intEnergy[i]**2)
        
        uax.errorbar(temp, np.mean(intEnergy), yerr=np.std(intEnergy), c='r', fmt='.')
        fax.errorbar(temp, np.mean(f), yerr=np.std(f), c='r', fmt='.')
        Sax.errorbar(temp, np.mean(S), yerr=np.std(S), c='r', fmt='.')
        Max.errorbar(temp, np.mean(m), yerr=np.std(m), c='r', fmt='.')
        if t != 0:
            cax.errorbar(temp, np.mean(c), yerr=np.std(c), c='r', fmt='.')
    
    for extension in [".png", ".pdf"]:
        ufig.savefig("Q1c-InternalEnergy" + extension, dpi=400, bbox_inches="tight")
        ffig.savefig("Q1c-FreeEnergy" + extension, dpi=400, bbox_inches="tight")
        Sfig.savefig("Q1c-Entropy" + extension, dpi=400, bbox_inches="tight")
        cfig.savefig("Q1c-HeatCapacity" + extension, dpi=400, bbox_inches="tight")
        Mfig.savefig("Q1c-ReducedMagnet" + extension, dpi=400, bbox_inches="tight")
        
def Q1e():
    temps = [0.5, 1, 2]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.subplots_adjust(hspace=0)

    ax2.set_xlabel("Reduced Magnetisation per Dipole")
    
    for temp in temps:
        for N in [100, 500]:
            ax = ax1 if N == 100 else ax2
            m = np.zeros(100)
            for i in range(100):
                a = gen_init_Ising(N)
                b = metropolis(a.copy(), 50000, temp)
                m[i] = np.mean(b)
            ax.hist(m, label=f"$T =$ {temp} $\epsilon / k$", alpha=0.7)
    ax1.set_ylabel("Freq. (N = 100)")
    ax2.set_ylabel("Freq. (N = 500)")
    ax1.legend(loc='upper left')
    ax1.grid(axis="x", linestyle='--', c='k', lw=0.5); ax2.grid(axis="x", linestyle='--', c='k', lw=0.5)
    ax1.set_xlim(xmax=1); ax2.set_xlim(xmax=1)
    fig.savefig("Q1e-Hist.png", dpi=400, bbox_inches="tight")
    fig.savefig("Q1e-Hist.pdf", dpi=400, bbox_inches="tight")

def gen_init_Ising2d(N):
    s = np.zeros((N, N))
    for i in range(N):
        initState = np.random.uniform(0, 1, N)
        s[i, :] = [1 if initState[i] >= 0.5 else -1 for i in range(N)]
    return s

def plot_2d_Ising(states, name=None):
    if len(states) == 1:
        fig, ax = plt.subplots()
        ax.imshow(states)
        ax.set_xlabel("Dipole")
    else:              
        fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        fig.subplots_adjust(wspace=0.02)
        
        for k in range(len(states)):
            ax = ax2 if k == 1 else ax1
            ax.imshow(states[k])
            ax.get_yaxis().set_ticks([])
            ax.get_xaxis().set_ticks([])
            if k == len(states) - 1:
                ax.set_title("Final")
            else:
                if k == 0:
                    ax.set_title("Initial")
                ax.get_yaxis().set_ticks([])
            
    if name != None:
        fig.savefig(name + ".png", dpi=400, bbox_inches='tight')
        fig.savefig(name + ".pdf", dpi=400, bbox_inches='tight')

def metropolis2d(states, iters, temperature):
    '''
    Parameters
    ----------
    states : np.array
        and NxN array composed only of -1 and 1, corresponding to the spin of each dipole
    iters : int
        The number of iterations (different states) to simulate
    temperature : float
        The temperature (in units of epsilon / k) of the reservoir
    '''
    beta = 1 / temperature
    RVhoriz = np.random.uniform(0, states.shape[0] - 1, iters) # generate some random positions along horizontal axis
    RVhoriz = [int(x) for x in RVhoriz] # make them correspond to an index 
    RVvert = np.random.uniform(0, states.shape[1] - 1, iters) # as above but along vertical axis
    RVvert = [int(x) for x in RVvert]
    for i in range(iters):
        if RVhoriz[i] == states.shape[0] - 1: # if the index is on the right border
            left = RVhoriz[i] - 1
            right = 0
        elif RVhoriz[i] == 0: # if the index is on the left border
            left = states.shape[0] - 1
            right = 1
        else: 
            left = RVhoriz[i] - 1
            right = RVhoriz[i] + 1
            
        if RVvert[i] == states.shape[1] - 1: # if the index is on the bottom border
            up = RVvert[i] - 1
            down = 0
        elif RVvert[i] == 0: # if the index is on the top border
            up = states.shape[1] - 1
            down = RVvert[i] + 1
        else:
            up = RVvert[i] - 1
            down = RVvert[i] + 1
        dipole = states[RVhoriz[i], RVvert[i]] # this is the value of the randomly chosen dipole
        Ldipole = states[left, RVvert[i]]   # value of the left dipole
        Rdipole = states[right, RVvert[i]] # right dipole
        Udipole = states[RVhoriz[i], up] # upper dipole
        Ddipole = states[RVhoriz[i], down] # lower dipole
        # below is a lambda function to calculate the internal energy due to the dipole (according to eq (1) in notes)
        energy = lambda D : -1 * ((Ldipole * D) + (Rdipole * D) + (Udipole * D) + (Ddipole * D))
        initEnergy = energy(dipole)
        flipEnergy = energy(-1 * dipole)
        deltaEnergy = flipEnergy - initEnergy
        if deltaEnergy <= 0:
            states[RVhoriz[i], RVvert[i]] *= -1
        else:
            flipProb = np.exp(-beta * deltaEnergy)
            evaluation = np.random.uniform(0, 1)
            if evaluation <= flipProb:
                states[RVhoriz[i], RVvert[i]] *= -1
    return states

def Q2a():
    temps = [1, 2, 3]
    for temp in temps:
        a = gen_init_Ising2d(100)
        
        b = metropolis2d(a.copy(), 1000000, temp)
        plot_2d_Ising([a, b], name=f"Q2a-Temp={temp}")
        
def Q2c(trials=3):
    colours = ['r', "tab:purple", "tab:green", "tab:blue"]
    temps = [0.02, 0.5, 1, 2.27, 5]
    # temps = np.linspace(0.02, 5, 15)
    ufig, uax = plt.subplots()
    ffig, fax = plt.subplots()
    Sfig, Sax = plt.subplots()
    cfig, cax = plt.subplots()
    Mfig, Max = plt.subplots()
    
    uax.set_xlabel("Temperature ($\epsilon / k$)")
    fax.set_xlabel("Temperature ($\epsilon / k$)")
    Sax.set_xlabel("Temperature ($\epsilon / k$)")
    cax.set_xlabel("Temperature ($\epsilon / k$)")
    Max.set_xlabel("Temperature ($\epsilon / k$)")
    
    uax.set_ylabel("Internal Energy ($\epsilon$)")
    fax.set_ylabel("Free Energy ($\epsilon$)")
    Sax.set_ylabel("Entropy per Dipole ($\epsilon / K$)")
    cax.set_ylabel("Specific Heat Capacity ($\epsilon / K$)")
    Max.set_ylabel("Abs. Reduced Magnetisation per Dipole")
    
    uax.grid(); fax.grid(); Sax.grid(); cax.grid(); Max.grid()
    
    for t, temp in enumerate(temps):
        intEnergy = np.zeros(trials)
        intEnergy2 = np.zeros(trials)
        S = np.zeros(trials)
        f = np.zeros(trials)
        c = np.zeros(trials)
        m = np.zeros(trials)
        numbers = [20, 50, 100]
        flips = [2 * 10**4, 2 * 10**5, 2 * 10**6]
        for n, N in enumerate(numbers):
            for i in range(trials):
                a = gen_init_Ising2d(N)
                b = metropolis2d(a.copy(), flips[n], temp)
                
                for j in range(N):
                    right = 0 if j == N - 1 else j + 1
                    for x in range(N):
                        down = 0 if x == N - 1 else x + 1
                        dU = (b[j, x] * b[right, x]) + (b[j, x] * b[j, down])
                        intEnergy[i] += dU
                        intEnergy2[i] += dU**2
                intEnergy[i] *= -1 / N**2 # internal energy per dipole
                intEnergy2[i] /= N**2
                
                NUp = [[1 if x == 1 else 0 for x in b[i, :]] for i in range(N)]; NUp = np.sum(NUp) # number of up spin-up dipoles
                if NUp == 0 or N**2 - NUp == 0:
                    S[i] = 0
                else:
                    S[i] = (1 / N**2) * (N**2 * np.log(N**2) - NUp * np.log(NUp) - (N**2 - NUp) * np.log(N**2 - NUp)) # entropy per dipole
                
                f[i] = intEnergy[i] - temp * S[i]
                
                m[i] = abs(np.mean(b)) # reduced magnetisation per dipole
                
                c[i] = (1 / temp)**2 * (intEnergy2[i] - intEnergy[i]**2)
            
            colour = colours[n]
            lab = f"N={N}" if t == 1 else None
            
            plottemp = temp + 0.05 * (n - len(numbers) / 2)
            
            uax.errorbar(plottemp, np.mean(intEnergy), yerr=np.std(intEnergy), c=colour, fmt='.', label=lab)
            fax.errorbar(plottemp, np.mean(f), yerr=np.std(f), c=colour, fmt='.', label=lab)
            Sax.errorbar(plottemp, np.mean(S), yerr=np.std(S), c=colour, fmt='.', label=lab)
            Max.errorbar(plottemp, np.mean(m), yerr=np.std(m), c=colour, fmt='.', label=lab)
            # cax.errorbar(plottemp, np.mean(c), yerr=np.std(c), c=colour, fmt='.', label=lab)
            if t != 0:
                cax.errorbar(plottemp, np.mean(c), yerr=np.std(c), c=colour, fmt='.', label=lab)
    
    uax.legend(); fax.legend(); Sax.legend(loc="lower right"); cax.legend(); Max.legend();
    
    for extension in [".png", ".pdf"]:
        ufig.savefig("Q2c-InternalEnergy" + extension, dpi=400, bbox_inches="tight")
        ffig.savefig("Q2c-FreeEnergy" + extension, dpi=400, bbox_inches="tight")
        Sfig.savefig("Q2c-Entropy" + extension, dpi=400, bbox_inches="tight")
        cfig.savefig("Q2c-HeatCapacity" + extension, dpi=400, bbox_inches="tight")
        Mfig.savefig("Q2c-ReducedMagnet" + extension, dpi=400, bbox_inches="tight")

# Q1a()
# Q1c(trials=20)
# Q1e()
# Q2a()
Q2c(trials=6)