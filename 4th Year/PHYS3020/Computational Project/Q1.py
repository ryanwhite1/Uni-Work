# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 12:55:13 2022

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt
from time import time

np.random.seed(3020)

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
        ax.imshow(states[0])
        # ax.set_xlabel("Dipole")
        ax.get_yaxis().set_ticks([])
        ax.get_xaxis().set_ticks([])
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

def DeltaU2d(LD, RD, UD, DD, D):
    return -1 * ((LD * D) + (RD * D) + (UD * D) + (DD * D))

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
    N = states.shape[0] # assume square lattice
    
    RVhoriz = np.random.uniform(0, N, iters) # generate some random positions along horizontal axis
    RVvert = np.random.uniform(0, N, iters) # as above but along vertical axis
    RVhoriz = [int(x) for x in RVhoriz] # make them correspond to an index 
    RVvert = [int(x) for x in RVvert]

    evaluations = np.random.uniform(0, 1, iters)
    for i in range(iters):
        
        dipole = states[RVhoriz[i], RVvert[i]]
        Ldipole = states[RVhoriz[i]-1, RVvert[i]] if RVhoriz[i] != 0 else states[N-1, RVvert[i]] # value of the left dipole
        Rdipole = states[RVhoriz[i]+1, RVvert[i]] if RVhoriz[i] != N-1 else states[0, RVvert[i]] # right dipole
        Udipole = states[RVhoriz[i], RVvert[i]-1] if RVvert[i] != 0 else states[RVhoriz[i], N-1] # upper dipole
        Ddipole = states[RVhoriz[i], RVvert[i]+1] if RVvert[i] != N-1 else states[RVhoriz[i], 0] # lower dipole
        
        initEnergy = DeltaU2d(Ldipole, Rdipole, Udipole, Ddipole, dipole)
        flipEnergy = DeltaU2d(Ldipole, Rdipole, Udipole, Ddipole, -1*dipole)
        
        deltaEnergy = flipEnergy - initEnergy
        if deltaEnergy <= 0:
            states[RVhoriz[i], RVvert[i]] *= -1
        else:
            flipProb = np.exp(-beta * deltaEnergy)
            if evaluations[i] <= flipProb:
                states[RVhoriz[i], RVvert[i]] *= -1
    return states

def Q2a():
    temps = [1, 2, 3]
    for temp in temps:
        a = gen_init_Ising2d(100)
        
        b = metropolis2d(a.copy(), 1000000, temp)
        plot_2d_Ising([a, b], name=f"Q2a-Temp={temp}")
        
def Q2c(trials=5):
    colours = ['r', "tab:purple", "tab:green", "tab:blue"]
    # temps = [0.02, 0.5, 1, 2.27, 5]
    temps = [5, 4, 3, 2.27, 1.5, 1, 0.5, 0.02]
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
    
    lowest20, lowest50, lowest100 = np.ndarray((20, 20)), np.ndarray((50, 50)), np.ndarray((100, 100))
    
    for t, temp in enumerate(temps):
        
        intEnergy = np.zeros(trials)
        intEnergy2 = np.zeros(trials)
        S = np.zeros(trials)
        f = np.zeros(trials)
        c = np.zeros(trials)
        m = np.zeros(trials)
        numbers = [20, 50, 100]
        flips = [5 * 10**4, 5 * 10**5, 5 * 10**6]
        for n, N in enumerate(numbers):
            for i in range(trials):
                if N == 100:
                    lowest = lowest100
                elif N == 50:
                    lowest = lowest50
                else:
                    lowest = lowest20
                a = gen_init_Ising2d(N) if t==0 else lowest
                
                b = metropolis2d(a.copy(), flips[n], temp)
                
                NUp = np.ndarray(shape=(N, N))
                for j in range(N):
                    right = 0 if j == N - 1 else j + 1
                    for x in range(N):
                        down = 0 if x == N - 1 else x + 1
                        dU = (b[j, x] * b[right, x]) + (b[j, x] * b[j, down])
                        intEnergy[i] += dU
                        intEnergy2[i] += dU**2
                        
                    NUp[j, :] = [1 if x == 1 else 0 for x in b[j, :]]
                intEnergy[i] *= -1 / N**2 # internal energy per dipole
                intEnergy2[i] /= N**2
                
                NUp = np.sum(NUp) # number of up spin-up dipoles
                if NUp == 0 or N**2 - NUp == 0:
                    S[i] = 0
                else:
                    S[i] = (1 / N**2) * (N**2 * np.log(N**2) - NUp * np.log(NUp) - (N**2 - NUp) * np.log(N**2 - NUp)) # entropy per dipole
                
                f[i] = intEnergy[i] - temp * S[i]
                
                m[i] = abs(np.mean(b)) # reduced magnetisation per dipole
                
                c[i] = (1 / temp)**2 * (intEnergy2[i] - intEnergy[i]**2)
            
            if N == 100:
                lowest100 = b
            elif N == 50:
                lowest50 = b
            else:
                lowest20 = b
            colour = colours[n]
            lab = f"N={N}" if t == 1 else None
            
            plottemp = temp + 0.05 * (n - len(numbers) / 2)
            
            uax.errorbar(plottemp, np.mean(intEnergy), yerr=np.std(intEnergy), c=colour, fmt='.', label=lab)
            fax.errorbar(plottemp, np.mean(f), yerr=np.std(f), c=colour, fmt='.', label=lab)
            Sax.errorbar(plottemp, np.mean(S), yerr=np.std(S), c=colour, fmt='.', label=lab)
            Max.errorbar(plottemp, np.mean(m), yerr=np.std(m), c=colour, fmt='.', label=lab)
            # cax.errorbar(plottemp, np.mean(c), yerr=np.std(c), c=colour, fmt='.', label=lab)
            if t != len(temps)-1:
                cax.errorbar(plottemp, np.mean(c), yerr=np.std(c), c=colour, fmt='.', label=lab)
    
    uax.legend(); fax.legend(); Sax.legend(loc="lower right"); cax.legend(); Max.legend();
    
    for extension in [".png", ".pdf"]:
        ufig.savefig("Q2c-InternalEnergy" + extension, dpi=400, bbox_inches="tight")
        ffig.savefig("Q2c-FreeEnergy" + extension, dpi=400, bbox_inches="tight")
        Sfig.savefig("Q2c-Entropy" + extension, dpi=400, bbox_inches="tight")
        cfig.savefig("Q2c-HeatCapacity" + extension, dpi=400, bbox_inches="tight")
        Mfig.savefig("Q2c-ReducedMagnet" + extension, dpi=400, bbox_inches="tight")
        
def Q2d(trials=100):
    # temps = np.linspace(0.02, 5, 8)
    temps = [5, 4, 3, 2.27, 1.5, 1, 0.5, 0.02]
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.subplots_adjust(hspace=0)
    # ax2 = ax.twinx()
    numbers = np.array([5, 10, 20])
    flips = numbers**2 * 5000
    colours = ['r', "tab:purple", "tab:green", "tab:blue", "tab:olive", "tab:brown"]
    # negColours = ["tab:blue", "tab:olive", "tab:brown"]
    
    ax2.set_xlabel("Temperature $(\epsilon / k)$")
    ax1.set_ylabel("Ave. Pos. Mag. ($s = 1$)")
    ax2.set_ylabel("Ave. Neg. Mag. ($s = -1$)")
    lowest5, lowest10, lowest20 = np.ndarray((trials, 5, 5)), np.ndarray((trials, 10, 10)), np.ndarray((trials, 20, 20))
    for t, temp in enumerate(temps):
        for n, N in enumerate(numbers):
            posMag = np.zeros(trials)
            negMag = np.zeros(trials)
            for i in range(trials):
                if N == 20:
                    lowest = lowest20[i, :, :]
                elif N == 10:
                    lowest = lowest10[i, :, :]
                else:
                    lowest = lowest5[i, :, :]
                a = gen_init_Ising2d(N) if t==0 else lowest
                b = metropolis2d(a.copy(), flips[n], temp)
                # runnPos, runnNeg = 0, 0
                
                # for q in range(N):
                #     for r in range(N):
                #         if b[q, r] == 1:
                #             runnPos += 1
                #         else:
                #             runnNeg += -1
                
                unique, counts = np.unique(b, return_counts=True)
                dic = dict(zip(unique, counts))
                # print(dic)
                try:
                    posMag[i] = dic[1] / N**2
                except:
                    posMag[i] = 0
                try:
                    negMag[i] = - dic[-1] / N**2
                except:
                    negMag[i] = 0
                
                # posMag[i] = np.sum([[1 if x == 1 else 0 for x in b[j, :]] for j in range(N)]) / N**2
                # negMag[i] = np.sum([[-1 if x == -1 else 0 for x in b[j, :]] for j in range(N)]) / N**2
                if N == 20:
                    lowest20[i, :, :] = b
                elif N == 10:
                    lowest10[i, :, :] = b
                else:
                    lowest5[i, :, :] = b
            plottemp = temp + 0.05 * (n - len(numbers) / 2)
            colour = colours[n]
            # negcolour = colours[n + 3]
            lab = f"N={N}" if t == 1 else None
            ax1.errorbar(plottemp, np.mean(posMag), yerr=np.std(posMag), fmt='.', label=lab, c=colour)
            ax2.errorbar(plottemp, np.mean(negMag), yerr=np.std(negMag), fmt='.', label=lab, c=colour)
            
                
    ax1.set_ylim(ymin=0); ax2.set_ylim(ymax=0)
    ax1.legend()
    ax1.grid(); ax2.grid()
    
    fig.savefig("Q2d-magnetisation.png", dpi=400, bbox_inches="tight")
    fig.savefig("Q2d-magnetisation.pdf", dpi=400, bbox_inches="tight")
    
def Q2e(N=20):
    N = 20
    temp = 1
    a = gen_init_Ising2d(N)
    b = metropolis2d(a, 2*10**5, temp)
    plot_2d_Ising([b], name="Q2e-T=1")
    for temp in np.arange(1, 3.1, 0.1):
        b = metropolis2d(b, int(10**5), temp)
    plot_2d_Ising([b], name="Q2e-T=3")  
    for temp in np.arange(3, 0.9, -0.1):
        b = metropolis2d(b, int(10**5), temp)
    plot_2d_Ising([b], name="Q2e-T=1 2")  
    
def gen_init_Ising3d(N):
    s = np.zeros((N, N, N))
    for i in range(N):
        for j in range(N):
            initState = np.random.uniform(0, 1, N)
            s[i, j, :] = [1 if initState[i] >= 0.5 else -1 for k in range(N)]
    return s
def DeltaU3d(LD, RD, UD, DD, FD, BD, D):
    return -1 * ((LD * D) + (RD * D) + (UD * D) + (DD * D) + (FD * D) + (BD * D))
def metropolis3d(states, iters, temperature):
    '''
    Parameters
    ----------
    states : np.array
        and NxNxN array composed only of -1 and 1, corresponding to the spin of each dipole
    iters : int
        The number of iterations (different states) to simulate
    temperature : float
        The temperature (in units of epsilon / k) of the reservoir
    '''
    beta = 1 / temperature
    N = states.shape[0] # assume square lattice
    
    RVx = np.random.uniform(0, N, iters) # generate some random positions along x axis
    RVy = np.random.uniform(0, N, iters) # as above but along y axis
    RVz = np.random.uniform(0, N, iters)
    RVx = [int(x) for x in RVx] # make them correspond to an index 
    RVy = [int(x) for x in RVy]
    RVz = [int(x) for x in RVz]
    
    # RVhoriz = np.random.randint(0, high=N, size=iters)
    # RVvert = np.random.randint(0, high=N, size=iters)
    evaluations = np.random.uniform(0, 1, iters)
    for i in range(iters):
        dipole = states[RVx[i], RVy[i], RVz[i]]
        Ldipole = states[RVx[i]-1, RVy[i], RVz[i]] if RVx[i] != 0 else states[N-1, RVy[i], RVz[i]] # value of the -x dipole
        Rdipole = states[RVx[i]+1, RVy[i], RVz[i]] if RVx[i] != N-1 else states[0, RVy[i], RVz[i]] # +x dipole
        Udipole = states[RVx[i], RVy[i]-1, RVz[i]] if RVy[i] != 0 else states[RVx[i], N-1, RVz[i]] # +y dipole
        Ddipole = states[RVx[i], RVy[i]+1, RVz[i]] if RVy[i] != N-1 else states[RVx[i], 0, RVz[i]] # -y dipole
        Fdipole = states[RVx[i], RVy[i], RVz[i]-1] if RVz[i] != 0 else states[RVx[i], RVy[i], N-1] # -z dipole
        Bdipole = states[RVx[i], RVy[i], RVz[i]+1] if RVz[i] != N-1 else states[RVx[i], RVy[i], 0] # +z dipole
        
        initEnergy = DeltaU3d(Ldipole, Rdipole, Udipole, Ddipole, Fdipole, Bdipole, dipole)
        flipEnergy = DeltaU3d(Ldipole, Rdipole, Udipole, Ddipole, Fdipole, Bdipole, -1*dipole)

        deltaEnergy = flipEnergy - initEnergy
        if deltaEnergy <= 0:
            states[RVx[i], RVy[i], RVz[i]] *= -1
        else:
            flipProb = np.exp(-beta * deltaEnergy)
            if evaluations[i] <= flipProb:
                states[RVx[i], RVy[i], RVz[i]] *= -1
    return states
def plot_3d_Ising(states, name=None, style='colour'):
    lattice = states[0]
    N = lattice.shape[0]
    if style == '2d':
        z = np.ndarray((N, N))
        for i in range(N):
            for j in range(N):
                z[i, j] = np.sum(lattice[i, :, j]) / N
        fig, ax = plt.subplots()
        z = np.rot90(z) # for some reason, the 2d array needs to be rotated to match up with the 3d one
        c = ax.imshow(z, vmin=-1, vmax=1)
        ax.get_yaxis().set_ticks([])
        ax.get_xaxis().set_ticks([])
        ax.set_xlabel('$x$'); ax.set_ylabel('$z$')
        cax = plt.axes([0.83, 0.15, 0.04, 0.7])
        cbar = fig.colorbar(c, cax=cax)
        cbar.set_label('Average Spin Along $y$')
    else:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        x, y, z, alpha = np.zeros(N**3), np.zeros(N**3), np.zeros(N**3), np.zeros(N**3)
        colours = [None] * N**3
        index = 0
        Up, Down = 0, 0
        size = 2
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    x[index] = i; y[index] = j; z[index] = k
                    if lattice[i, j, k] == 1:
                        alpha[index] = 1
                        colours[index] = 'tab:blue'
                        if Up == 0:
                            ax.scatter(x[index], y[index], z[index], c=colours[index], s=size, label='Spin Up')
                            Up = 1
                    else:
                        alpha[index] = 0
                        colours[index] = 'tab:red'
                        if Down == 0:
                            ax.scatter(x[index], y[index], z[index], c=colours[index], s=size, label='Spin Down')
                            Down = 1
                    index += 1
        ax.legend()
        plt.tight_layout()
        ax.get_yaxis().set_ticks([])
        ax.get_xaxis().set_ticks([])
        ax.get_zaxis().set_ticks([])
        ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); ax.set_zlabel('$z$')
        if style == 'colour':
            ax.scatter(x, y, z, c=colours, s=size)
        else:
            ax.scatter(x, y, z, c='tab:blue', s=10, alpha=alpha)
        
    if name != None:
        fig.savefig(name + ".png", dpi=400, bbox_inches='tight')
        fig.savefig(name + ".pdf", dpi=400, bbox_inches='tight')
        
def plot_both_3d(states, name):
    for style in ['2d', 'colour']:
        name += f' {style}'
        plot_3d_Ising(states, name=name, style=style)
        
def Q3(N=15, trials=10):
    temps = [8, 7, 6, 5, 4, 3, 2.27, 1.5, 1, 0.5, 0.02]
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
    
    lowest = np.ndarray((trials, N, N, N))
    
    for t, temp in enumerate(temps):
        
        intEnergy = np.zeros(trials)
        intEnergy2 = np.zeros(trials)
        S = np.zeros(trials)
        f = np.zeros(trials)
        c = np.zeros(trials)
        m = np.zeros(trials)
        flips = N**3 * 1000
        for n in range(trials):
            a = gen_init_Ising3d(N) if t==0 else lowest[n, :, :, :]
            
            b = metropolis3d(a.copy(), flips, temp)
            
            NUp = np.ndarray(shape=(N, N, N))
            for i in range(N):
                right = 0 if i == N - 1 else i + 1
                for j in range(N):
                    down = 0 if j == N - 1 else j + 1
                    for k in range(N):
                        forward = 0 if k == N - 1 else k + 1
                        dU = (b[i, j, k] * b[right, j, k]) + (b[i, j, k] * b[i, down, k]) + (b[i, j, k] * b[i, j, forward])
                        intEnergy[n] += dU
                        intEnergy2[n] += dU**2
                    
                    NUp[i, j, :] = [1 if x == 1 else 0 for x in b[i, j, :]]
            intEnergy[n] *= -1 / N**3 # internal energy per dipole
            intEnergy2[n] /= N**3
            
            NUp = np.sum(NUp) # number of up spin-up dipoles
            if NUp == 0 or N**3 - NUp == 0:
                S[n] = 0
            else:
                S[n] = (1 / N**3) * (N**3 * np.log(N**3) - NUp * np.log(NUp) - (N**3 - NUp) * np.log(N**3 - NUp)) # entropy per dipole
            
            f[n] = intEnergy[n] - temp * S[n]
            
            m[n] = abs(np.mean(b)) # reduced magnetisation per dipole
            
            c[n] = (1 / temp)**2 * (intEnergy2[n] - intEnergy[n]**2)
        
            lowest[n, :, :, :] = b
        
        uax.errorbar(temp, np.mean(intEnergy), yerr=np.std(intEnergy), c='r', fmt='.')
        fax.errorbar(temp, np.mean(f), yerr=np.std(f), c='r', fmt='.')
        Sax.errorbar(temp, np.mean(S), yerr=np.std(S), c='r', fmt='.')
        Max.errorbar(temp, np.mean(m), yerr=np.std(m), c='r', fmt='.')
        if t != len(temps)-1:
            cax.errorbar(temp, np.mean(c), yerr=np.std(c), c='r', fmt='.')
    
    uax.legend(); fax.legend(); Sax.legend(loc="lower right"); cax.legend(); Max.legend();
    
    for extension in [".png", ".pdf"]:
        ufig.savefig("Q3-InternalEnergy" + extension, dpi=400, bbox_inches="tight")
        ffig.savefig("Q3-FreeEnergy" + extension, dpi=400, bbox_inches="tight")
        Sfig.savefig("Q3-Entropy" + extension, dpi=400, bbox_inches="tight")
        cfig.savefig("Q3-HeatCapacity" + extension, dpi=400, bbox_inches="tight")
        Mfig.savefig("Q3-ReducedMagnet" + extension, dpi=400, bbox_inches="tight")
# Q1a()
# Q1c(trials=20)
# Q1e()
# Q2a()
# Q2c(trials=10)
# Q2d(trials=100)
# Q2e()
Q3()

# t1 = time()
# a = gen_init_Ising2d(100)
# print(a.shape[0])
# print(time() - t1)

# b = metropolis2d(a, 5*10**6, 2)
# print(time() - t1)
# plot_2d_Ising([b])

# a = gen_init_Ising3d(20)
# b = metropolis3d(a, 10**5, 2)
# # print(b)
# # plot_3d_Ising([b], style='2d')
# plot_both_3d([b], '3D20')



