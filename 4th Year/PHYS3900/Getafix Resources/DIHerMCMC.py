import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
import starry
import pymc3 as pm
import pymc3_ext as pmx
import exoplanet
import theano.tensor as tt
import arviz as az


plt.rcParams['font.family'] = 'Serif'

starry.config.quiet = True
starry.config.lazy = True

print("Import good.")

time = []; flux = []; ferr = []
with open("timedata.txt", 'r') as timedata:
    for t in timedata:
        time.append(float(t))
with open("fluxdata.txt", 'r') as fluxdata:
    for f in fluxdata:
        flux.append(float(f))
with open("ferrdata.txt", 'r') as ferrdata:
    for err in ferrdata:
        ferr.append(float(err))

time = np.array(time); flux = np.array(flux); ferr = np.array(ferr)

print("Data read good.")

#primary limb darkening
u1_m = 0.124
u1_e = 0.1
u2_m = 0.262 
u2_e = 0.1


#primary mass and radius
A_m_m = 5.1
A_m_e = 0.2
A_r_m = 2.4
A_r_e = 0.3

#primary rot period and tpole
A_prot_m =  1.07 #in days
A_omega = 0.225 #dimensionless
A_prot_e = 0.1

A_tpole_m = 17300
A_tpole_e = 800

#secondary luminosity ratio
B_amp_l = 0.6
B_amp_u = 0.8
#secondary mass and radius
B_m_m = 4.4
B_m_e = 0.2
B_r_m = 2.5
B_r_e = 0.3

#secondary tpole
B_tpole_m = 15400
B_tpole_e = 800

#secondary vsini
B_vsini_m = 100
B_vsini_e = 30

#orbital parameters
orb_inc_m = 88.90036698
orb_inc_e = 1.0
orb_period = 10.54980498
orb_ecc = 0.50002396
long_periastron = 327.28588277
long_ascend = 90 #106


G_mks = 6.67e-11
Msun = 1.989e+30
Rsun = 6.95700e8

map_soln = {'A_M_lowerbound__': np.array(1.62944291),
 'A_R_lowerbound__': np.array(0.98037289),
 'A inc_periodic__': np.array([ 2.64709232, -3.60451579]),
 'A_prot_lowerbound__': np.array(0.07237746),
 'u1_lowerbound__': np.array(-2.24535639),
 'u2_lowerbound__': np.array(-1.84569244),
 'B_R_lowerbound__': np.array(0.90174968),
 'period_lowerbound__': np.array(2.35610737),
 'inc orb_interval__': np.array(-7.80442223),
 'ecc_interval__': np.array(-6.03156992),
 'long periastron_interval__': np.array(0.70180696),
 't0_interval__': np.array(0.10218496),
 'A_M': np.array(5.10103218),
 'A_R': np.array(2.66544997),
 'A inc': np.array(1.41243868),
 'A inc deg': np.array(80.92677536),
 'A_prot': np.array(1.07506106),
 'u1': np.array(0.1058898),
 'u2': np.array(0.15791594),
 'B_R': np.array(2.4639104),
 'period': np.array(10.54980498),
 'inc orb': np.array(88.90036698),
 'ecc': np.array(0.50002396),
 'long periastron': np.array(327.28588277),
 't0': np.array(2018.67830961)}
    
with open('MAPSoln.txt', 'w') as MAPfile:
     MAPfile.write(str(map_soln))

print("Save MAP good.")


with pm.Model() as model:

    # These are the variables we're solving for;
    # here we're placing wide Gaussian priors on them.
    BoundedNormal = pm.Bound(pm.Normal, lower=0)
    
    # fix these 
    # A_m = map_soln["A_M"] #
    A_m = BoundedNormal("A_M", mu=A_m_m, sd=A_m_e, testval=A_m_m) # fix to MAP
    # A_r = map_soln["A_R"] #
    A_r = BoundedNormal("A_R", mu=A_r_m, sd=A_r_e, testval=A_r_m) # fix to MAP
    A_inc_rad = pmx.Periodic("A inc", lower=0, upper=np.pi/2) # fix to paper val
    A_inc = pm.Deterministic("A inc deg", A_inc_rad*180/np.pi) 
#     A_inc = 89.02 # from Liang et al
#     A_inc_rad = A_inc * np.pi / 180
#     A_prot = map_soln["A_prot"]
    A_prot = BoundedNormal("A_prot",mu=1.07,sd=0.1,testval=1.07)
    
    pm.Potential("isotropy", tt.log(tt.sin(A_inc_rad)))
    
    u1 = map_soln["u1"]
    u2 = map_soln["u2"]
    
    
    pri_map = starry.Map(udeg=2,ydeg=4) #ydeg = 2*order_approx udeg=2
    pri_map[1] = u1
    pri_map[2] = u2
    pri_map.inc= A_inc
    
    primary = starry.Primary(pri_map, m=A_m, r=A_r,prot=A_prot)

 
    B_r = map_soln["B_R"] #BoundedNormal("B_R",mu=B_r_m,sd=B_r_e,testval=B_r_m) # set to MAP value

    sec_map = starry.Map(udeg=2,ydeg=1)
    sec_map[1] = u1
    sec_map[2] = u2
    secondary = starry.kepler.Secondary(map=sec_map,
        m=4.4,  # mass in solar masses
        r=B_r,  # radius in solar radii
        porb = orb_period, # orbital period in days
        inc = orb_inc_m,
        Omega = long_ascend,  # longitude of ascending node in degrees
        ecc = orb_ecc,  # eccentricity
        # ecc = pm.Uniform("ecc", lower=0.50, upper=0.51, testval=0.505),
        w = long_periastron,  # longitude of pericenter in degrees
        # w = pm.Uniform("long periastron", lower=320.6, upper=330.6, testval=326.5),
        t0 = map_soln["t0"],  # set to MAP 
    )
    
    system = starry.System(primary, secondary)

print("Init model good.")

with model:
    system.set_data(flux, C=ferr**2)

    # Prior on primary
    pri_mu = np.zeros(primary.map.Ny)
    pri_mu[0] = 1
    pri_L = np.zeros(primary.map.Ny)
    pri_L[0] = 1e-2
    pri_L[1:] = 1e-2
    primary.map.set_prior(mu=pri_mu, L=pri_L)
    
    # Prior on secondary
    sec_mu = np.zeros(secondary.map.Ny)
    sec_mu[0] = 0.9
    sec_L = np.zeros(secondary.map.Ny)
    sec_L[0] = 1e-4
    sec_L[1:] = 1e-4
    secondary.map.set_prior(mu=sec_mu, L=sec_L)


    pm.Potential("marginal", system.lnlike(t=time))

print("Set data good.")

keys = ["A inc_periodic__", 
"A inc", 
"A inc deg", 
"A_prot_lowerbound__", 
"A_prot", 
'A_M_lowerbound__', 
'A_R_lowerbound__', 
'A_M',
'A_R']
# 'ecc_interval__', 
# 'long periastron_interval__', 
# 'ecc', 
# 'long periastron'
# ]

start_state = {}
for key in keys:
    start_state[key] = map_soln[key]

print("Starting MCMC.")
with model:
    trace = pmx.sample(tune=50, draws=1000, start=start_state, chains=None, cores=None, initial_accept = 0.5, target_accept=0.9)

print("MCMC Good.")


trace.to_netcdf("DIHerMCMCFull.h5")
# to load from a .h5 file, use:
# samples = az.from_netcdf("DIHerMCMC.h5")
print("Saved file!")
display(pm.summary(trace))