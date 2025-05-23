# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 08:36:43 2024

@author: ryanw
"""

import numpy as np
import jax.numpy as jnp
from jax import jit, vmap, grad
import jax
import jax.lax as lax
import jax.scipy.stats as stats
from jax.scipy.optimize import minimize
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.ndimage import gaussian_filter
import jax.scipy.signal as signal
from matplotlib import animation
import time
import emcee
# import jaxoplanet
import jaxopt

jax.config.update("jax_enable_x64", True)

M_odot = 1.98e30
G = 6.67e-11
c = 299792458
yr2day = 365.25
yr2s = yr2day * 24*60*60
kms2pcyr = 60*60*24*yr2day / (3.086e13) # km/s to pc/yr
AU2km = 1.496e8



def rotate_x(angle):
    arr = jnp.array([[1, 0, 0],
                     [0, jnp.cos(angle), jnp.sin(angle)],
                     [0, -jnp.sin(angle), jnp.cos(angle)]])
    return arr

def rotate_y(angle):
    arr = jnp.array([[jnp.cos(angle), 0, -jnp.sin(angle)],
                     [0, 1, 0],
                     [jnp.sin(angle), 0, jnp.cos(angle)]])
    return arr

def rotate_z(angle):
    arr = jnp.array([[jnp.cos(angle), jnp.sin(angle), 0],
                     [-jnp.sin(angle), jnp.cos(angle), 0],
                     [0, 0, 1]])
    return arr
def euler_angles(coords, Omega, i, w):
    return rotate_z(jnp.deg2rad(Omega)) @ (
            rotate_x(jnp.deg2rad(i)) @ (
            rotate_z(jnp.deg2rad(w)) @ coords))



# def kepler_solve_sub_sub(i, E0_ecc_mi):
#     '''
#     '''
#     E0, ecc, mi = E0_ecc_mi
#     return (E0 - (E0 - ecc * jnp.sin(E0) - mi) / (1 - ecc * jnp.cos(E0)), ecc, mi)
# def kepler_solve_sub(i, ecc, tol, M):
#     ''' This is the main kepler equation solving step. 
#     '''
#     E0 = M[i]
#     # Newton's formula to solve for eccentric anomaly
#     E0 = lax.fori_loop(0, 20, kepler_solve_sub_sub, (E0, ecc, M[i]))[0]
#     return E0
# def kepler_solve(t, P, ecc):
#     ''' Solver for Kepler's 2nd law giving the angle of an orbiter (rel. to origin) over time
#     '''
#     # follow the method in https://downloads.rene-schwarz.com/download/M001-Keplerian_Orbit_Elements_to_Cartesian_State_Vectors.pdf
#     # to get true anomaly
#     M = 2 * jnp.pi / P * t
#     tol = 1e-8

#     E = vmap(lambda i: kepler_solve_sub(i, ecc, tol, M))(jnp.arange(len(t)))
#     # now output true anomaly (rad)
#     return E, 2 * jnp.arctan2(jnp.sqrt(1 + ecc) * jnp.sin(E / 2), jnp.sqrt(1 - ecc) * jnp.cos(E / 2))


### the following kepler solver functions are from https://jax.exoplanet.codes/en/latest/tutorials/core-from-scratch/#core-from-scratch

def kepler_starter(mean_anom, ecc):
    ome = 1 - ecc
    M2 = jnp.square(mean_anom)
    alpha = 3 * jnp.pi / (jnp.pi - 6 / jnp.pi)
    alpha += 1.6 / (jnp.pi - 6 / jnp.pi) * (jnp.pi - mean_anom) / (1 + ecc)
    d = 3 * ome + alpha * ecc
    alphad = alpha * d
    r = (3 * alphad * (d - ome) + M2) * mean_anom
    q = 2 * alphad * ome - M2
    q2 = jnp.square(q)
    w = jnp.square(jnp.cbrt(jnp.abs(r) + jnp.sqrt(q2 * q + r * r)))
    return (2 * r * w / (jnp.square(w) + w * q + q2) + mean_anom) / d
def kepler_refiner(mean_anom, ecc, ecc_anom):
    ome = 1 - ecc
    sE = ecc_anom - jnp.sin(ecc_anom)
    cE = 1 - jnp.cos(ecc_anom)

    f_0 = ecc * sE + ecc_anom * ome - mean_anom
    f_1 = ecc * cE + ome
    f_2 = ecc * (ecc_anom - sE)
    f_3 = 1 - f_1
    d_3 = -f_0 / (f_1 - 0.5 * f_0 * f_2 / f_1)
    d_4 = -f_0 / (f_1 + 0.5 * d_3 * f_2 + (d_3 * d_3) * f_3 / 6)
    d_42 = d_4 * d_4
    dE = -f_0 / (f_1 + 0.5 * d_4 * f_2 + d_4 * d_4 * f_3 / 6 - d_42 * d_4 * f_2 / 24)

    return ecc_anom + dE
@jnp.vectorize
def kepler_solver_impl(mean_anom, ecc):
    mean_anom = mean_anom % (2 * jnp.pi)

    # We restrict to the range [0, pi)
    high = mean_anom > jnp.pi
    mean_anom = jnp.where(high, 2 * jnp.pi - mean_anom, mean_anom)

    # Solve
    ecc_anom = kepler_starter(mean_anom, ecc)
    ecc_anom = kepler_refiner(mean_anom, ecc, ecc_anom)

    # Re-wrap back into the full range
    ecc_anom = jnp.where(high, 2 * jnp.pi - ecc_anom, ecc_anom)

    return ecc_anom
def kepler(mean_anom, ecc):
    E = kepler_solver_impl(mean_anom, ecc)
    return E, 2 * jnp.arctan2(jnp.sqrt(1 + ecc) * jnp.sin(E / 2), jnp.sqrt(1 - ecc) * jnp.cos(E / 2))



def nonlinear_accel(x, t, rt, amax):
    xuse = x[0]
    sqrtx = jnp.sqrt(1 - rt/xuse) * jnp.heaviside(xuse - rt, 0)
    t_est = (xuse * sqrtx + rt * jnp.arctanh(sqrtx)) * AU2km / jnp.sqrt(2 * amax/yr2s * rt * AU2km)
    return jnp.abs(t_est - t)

def dust_circle(i_nu, stardata, theta, plume_direction, pos2, widths):
    '''
    '''
    i, nu = i_nu
    x = nu / (2 * jnp.pi)
    transf_nu = 2 * jnp.pi * (x + jnp.floor(0.5 - x))
    turn_on = jnp.deg2rad(stardata['turn_on'])
    turn_off = jnp.deg2rad(stardata['turn_off'])
    turned_on = jnp.heaviside(transf_nu - turn_on, 0)
    turned_on *= jnp.heaviside(widths[i] - stardata['nuc_dist'] * AU2km, 1)   # nucleation distance (no dust if less than nucleation dist), converted from AU to km
    turned_off = jnp.heaviside(turn_off - transf_nu, 0)
    direction = plume_direction[:, i] / jnp.linalg.norm(plume_direction[:, i])
    
    half_angle = jnp.deg2rad(stardata['open_angle']) / 2

    circle = jnp.array([jnp.ones(len(theta)) * jnp.cos(half_angle), 
                        jnp.sin(half_angle) * jnp.sin(theta), 
                        (1 - stardata['oblate']) * jnp.sin(half_angle) * jnp.cos(theta)])
    circle *= widths[i]
    ### below attempts to model latitude varying windspeed -- don't see this significantly in apep
    ### if you think about it, the CW shock occurs more or less around the equatorial winds so it shouldnt have a huge effect
    # latitude_speed_var = jnp.array([jnp.ones(len(theta)), 
    #                     jnp.ones(len(theta)), 
    #                     jnp.ones(len(theta)) * (1. + stardata['lat_v_var'] * jnp.cos(theta)**2)])
    # circle *= widths[i] * latitude_speed_var
    
    ### Below few lines handle acceleration of dust from radiation pressure -- only relevant when phase is tiny
    # https://physics.stackexchange.com/questions/15587/how-to-get-distance-when-acceleration-is-not-constant
    spiral_time = widths[i] / stardata['windspeed1']
    
    valid_dists = jnp.heaviside(stardata['opt_thin_dist'] - stardata['nuc_dist'], 1)
    t_noaccel = stardata['nuc_dist'] * AU2km / stardata['windspeed1']
    t_linear = 2 * jnp.sqrt(valid_dists * (stardata['opt_thin_dist'] - stardata['nuc_dist']) * AU2km / (2 * stardata['acc_max']/yr2s))
    accel_lin = jnp.heaviside(spiral_time - t_noaccel, 0)
    dist_accel_lin = accel_lin * 0.5 * stardata['acc_max']/yr2s * jnp.min(jnp.array([spiral_time, t_linear]))**2
    accel_r2 = jnp.heaviside(spiral_time - t_linear, 0)
    
    
    ### much more work needed for nonlinear acceleration
    # minim = minimize(nonlinear_accel, jnp.array([10*stardata['opt_thin_dist']]), args=(spiral_time - t_linear, stardata['opt_thin_dist'], stardata['acc_max']), method='BFGS', tol=1e-6)
    # # print(minim.x)
    # dist_accel_r2 = minim.x
    # dist_accel_r2 *= accel_r2
    # circle += valid_dists * (dist_accel_lin + dist_accel_r2)
    
    # solver = jaxopt.GradientDescent(fun=nonlinear_accel, maxiter=200)
    # res = solver.run(jnp.array([100*stardata['opt_thin_dist']]), t=spiral_time - t_linear, rt=stardata['opt_thin_dist'], amax=stardata['acc_max'])
    # dist_accel_r2 = res.params[0]
    # dist_accel_r2 *= accel_r2
    
    dist_accel_r2 = 0
    circle += valid_dists * (dist_accel_lin + dist_accel_r2)
    
    ### now rotate the circle to account for the star orbit direction
    angle_x = -jnp.arctan2(direction[1], direction[0]) + jnp.pi
    circle = rotate_z(angle_x) @ circle
    
    # circle *= turned_on * turned_off
    weights = jnp.ones(len(theta)) * turned_on * turned_off
    
    ### below accounts for the dust production not turning on instantaneously (probably negligible effect, so commented out)
    # weights = jnp.ones(len(theta))
    # sigma = jnp.deg2rad(10)
    # mult = 0.1
    # weights *= 1 - (1 - turned_on - mult * jnp.exp(-0.5 * ((transf_nu - turn_on) / sigma)**2))
    # weights *= 1 - (1 - turned_off - mult * jnp.exp(-0.5 * ((transf_nu - turn_off) / sigma)**2))
    
    
    alpha = jnp.deg2rad(stardata['comp_incl'])
    beta = jnp.deg2rad(stardata['comp_az'])
    comp_halftheta = jnp.deg2rad(stardata['comp_open'] / 2)
    x = circle[0, :]
    y = circle[1, :]
    z = circle[2, :]
    r = jnp.sqrt(x**2 + y**2 + z**2)
    particles_alpha = jnp.arccos(z / r)
    particles_beta = jnp.sign(y) * jnp.arccos(x / jnp.sqrt(x**2 + y**2))
    
    ### to get angular separation of the points on the sphere, I used the cos(alpha) = ... formula from
    # https://www.atnf.csiro.au/people/Tobias.Westmeier/tools_spherical.php#:~:text=The%20angular%20separation%20of%20two%20points%20on%20a%20shpere&text=cos(%CE%B1)%3Dcos(%CF%911)cos(,%CF%861%E2%88%92%CF%862).
    term1 = jnp.cos(alpha) * jnp.cos(particles_alpha)
    term2 = jnp.sin(alpha) * jnp.sin(particles_alpha) * jnp.cos(beta - particles_beta)
    angular_dist = jnp.arccos(term1 + term2)
    
    photodis_prop = 1   # how much of the plume is photodissociated by the companion. set to < 1 if you want a another plume generated
    ## linear scaling for companion photodissociation
    # companion_dissociate = jnp.where(angular_dist < comp_halftheta,
    #                                  (1 - stardata['comp_reduction'] * jnp.ones(len(weights))), jnp.ones(len(weights)))
    ## gaussian scaling for companion photodissociation
    comp_gaussian = 1 - stardata['comp_reduction'] * jnp.exp(-0.5 * (angular_dist / comp_halftheta)**2)
    comp_gaussian = jnp.maximum(comp_gaussian, jnp.zeros(len(comp_gaussian))) # need weight value to be between 0 and 1
    companion_dissociate = jnp.where(angular_dist < photodis_prop * comp_halftheta,
                                      comp_gaussian, jnp.ones(len(weights)))
    
    ### below code calculates another plume from the wind-companion interaction
    ### currently is commented out to save on computation
    # in_comp_plume = jnp.where((photodis_prop * comp_halftheta < angular_dist) & (angular_dist < comp_halftheta),
    #                           jnp.ones(len(x)), jnp.zeros(len(x)))
    
    # # now we need to generate angles around the plume edge that are inconsistent to the other rings so that it smooths out
    # # i.e. instead of doing linspace(0, 2*pi, len(x)), just do a large number multiplied by our ring number and convert that to [0, 2pi]
    # ring_theta = jnp.linspace(0, i * len(x), len(x))%(2*jnp.pi)
    
    # ## The coordinate transformations below are from user DougLitke from
    # ## https://math.stackexchange.com/questions/643130/circle-on-sphere?newreg=42e38786904e43a0a2805fa325e52b92
    # new_x = r * (jnp.sin(comp_halftheta) * jnp.cos(alpha) * jnp.cos(beta) * jnp.cos(ring_theta) - jnp.sin(comp_halftheta) * jnp.sin(beta) * jnp.sin(ring_theta) + jnp.cos(comp_halftheta) * jnp.sin(alpha) * jnp.cos(beta))
    # new_y = r * (jnp.sin(comp_halftheta) * jnp.cos(alpha) * jnp.sin(beta) * jnp.cos(ring_theta) + jnp.sin(comp_halftheta) * jnp.cos(beta) * jnp.sin(ring_theta) + jnp.cos(comp_halftheta) * jnp.sin(alpha) * jnp.sin(beta))
    # new_z = r * (-jnp.sin(comp_halftheta) * jnp.sin(alpha) * jnp.cos(ring_theta) + jnp.cos(comp_halftheta) * jnp.cos(alpha))
    
    # x = x + in_comp_plume * (-x + new_x)
    # y = y + in_comp_plume * (-y + new_y)
    # z = z + in_comp_plume * (-z + new_z)
    
    # circle = jnp.array([x, y, z])
    
    # weights *= (1 - in_comp_plume * (1 - stardata['comp_plume']))
    
    
    
    # now calculate the weights of each point according the their orbital variation
    prop_orb = 1 - (1 - stardata['orb_amp']) * jnp.exp(-0.5 * (((transf_nu*180/jnp.pi + 180) - stardata['orb_min']) / stardata['orb_sd'])**2) # weight proportion from orbital variation
    
    # now from azimuthal variation
    prop_az = 1 - (1 - stardata['az_amp']) * jnp.exp(-0.5 * ((theta * 180/jnp.pi - stardata['az_min']) / (stardata['az_sd']))**2)
    
    # we need our orbital proportion to be between 0 and 1
    prop_orb = jnp.min(jnp.array([prop_orb, 1]))
    prop_orb = jnp.max(jnp.array([prop_orb, 0]))
    # and the same for our azimuthal proportion
    prop_az = jnp.minimum(jnp.maximum(prop_az, jnp.zeros(len(prop_az))), jnp.ones(len(prop_az)))
    weights *= prop_orb * prop_az
    
    weights *= companion_dissociate
    
    # circle = circle.at[:, :].add(jnp.tile(pos2[:, i], (len(theta), 1)).T)
    
    circle = jnp.array([circle[0, :], 
                        circle[1, :], 
                        circle[2, :],
                        weights])
    
    return circle

def calculate_semi_major(period_s, m1, m2):
    '''
    '''
    m1_kg = m1 * M_odot                                 # mass of stars in kg
    m2_kg = m2 * M_odot
    M_kg = m1_kg + m2_kg                                # total mass in kg
    # M = m1 + m2                                         # total mass in solar masses
    mu = G * M_kg
    a = jnp.cbrt((period_s / (2 * jnp.pi))**2 * mu)/1000    # semi-major axis of the system (total separation)
    a1 = m2_kg / M_kg * a                                   # semi-major axis of first body (meters)
    a2 = a - a1                                             # semi-major axis of second body
    return a1, a2



def dust_plume_sub(theta, times, n_orbits, period_s, stardata):
    
    n_time = len(times)
    n_t = n_time / n_orbits
    ecc = stardata['eccentricity']
    # E, true_anomaly = kepler_solve(times, period_s, ecc)
    
    E, true_anomaly = kepler(2 * jnp.pi * times / period_s, jnp.array([ecc]))
    
    # true_times = period_s / (2*jnp.pi) * (E / 180 * jnp.pi - stardata["eccentricity"] * jnp.rad2deg(jnp.sin(E)));
    
    a1, a2 = calculate_semi_major(period_s, stardata['m1'], stardata['m2'])
    r1 = a1 * (1 - ecc * jnp.cos(E)) * 1e-3     # radius in km 
    r2 = a2 * (1 - ecc * jnp.cos(E)) * 1e-3
    # ws_ratio = stardata['windspeed1'] / stardata['windspeed2']
    
    positions1 = jnp.array([jnp.cos(true_anomaly), 
                            jnp.sin(true_anomaly), 
                            jnp.zeros(n_time)])
    positions2 = jnp.copy(positions1)
    positions1 *= r1      # position in the orbital frame
    positions2 *= -r2     # position in the orbital frame
    
    widths = stardata['windspeed1'] * period_s * (n_orbits - jnp.arange(n_time) / n_t)
    
    plume_direction = positions1 - positions2               # get the line of sight from first star to the second in the orbital frame
    
        
    particles = vmap(lambda i_nu: dust_circle(i_nu, stardata, theta, plume_direction, positions2, widths))((jnp.arange(n_time), true_anomaly))

    weights = particles[:, 3, :].flatten()
    particles = particles[:, :3, :]
    
    
    particles = jnp.array([jnp.ravel(particles[:, 0, :]),
                           jnp.ravel(particles[:, 1, :]),
                           jnp.ravel(particles[:, 2, :])])
    

    # shock_start = plume_direction * (stardata['nuc_dist'] * AU2km / jnp.max(jnp.abs(plume_direction)))# + positions2
    # shock_start = positions2
    
    ### the shock originates from the second star, not the WR, so we need to add its position to the spiral
    shock_start = positions2
    shock_start = jnp.repeat(shock_start, len(theta), axis=-1)
    particles += shock_start

    # particles = rotate_z(jnp.deg2rad(- stardata['asc_node'])) @ (
    #         rotate_x(jnp.deg2rad(- stardata['inclination'])) @ (
    #         rotate_z(jnp.deg2rad(- stardata['arg_peri'])) @ particles))
    particles = euler_angles(particles, stardata['asc_node'], stardata['inclination'], stardata['arg_peri'])

    return 60 * 60 * 180 / jnp.pi * jnp.arctan(particles / (stardata['distance'] * 3.086e13)), weights

@jit
def dust_plume(stardata):
    '''
    Parameters
    ----------
    stardata : dict
    '''
    phase = stardata['phase']%1
    
    period_s = stardata['period'] * 365.25 * 24 * 60 * 60
    
    n_orbits = 1
    n_t = 30       # circles per orbital period
    n_points = 40   # points per circle
    n_particles = n_points * n_t * n_orbits
    n_time = n_t * n_orbits
    theta = 2 * jnp.pi * jnp.linspace(0, 1, n_points)
    times = period_s * jnp.linspace(phase, n_orbits + phase, n_time)
    particles, weights = dust_plume_sub(theta, times, n_orbits, period_s, stardata)
    return particles, weights
@jit
def dust_plume_for_gif(stardata):
    '''
    Parameters
    ----------
    stardata : dict
    '''
    phase = stardata['phase']%1
    
    period_s = stardata['period'] * 365.25 * 24 * 60 * 60
    
    n_orbits = 1
    n_t = 1000       # circles per orbital period
    n_points = 400   # points per circle
    n_particles = n_points * n_t * n_orbits
    n_time = n_t * n_orbits
    theta = 2 * jnp.pi * jnp.linspace(0, 1, n_points)
    times = period_s * jnp.linspace(phase, n_orbits + phase, n_time)
    particles, weights = dust_plume_sub(theta, times, n_orbits, period_s, stardata)
    return particles, weights
  
    
gui_funcs = [lambda stardata, i=i: dust_plume_GUI_sub(stardata, i) for i in range(1, 20)]
gui_funcs = [jit(gui_funcs[i]) for i in range(len(gui_funcs))]
def dust_plume_GUI_sub(stardata, n_orb):
    phase = stardata['phase']%1
    
    period_s = stardata['period'] * 365.25 * 24 * 60 * 60
    
    n_orbits = n_orb
    n_t = 30       # circles per orbital period
    n_points = 40   # points per circle
    n_particles = n_points * n_t * n_orbits
    n_time = n_t * n_orbits
    theta = 2 * jnp.pi * jnp.linspace(0, 1, n_points)
    times = period_s * jnp.linspace(phase, n_orbits + phase, n_time)
    particles, weights = dust_plume_sub(theta, times, n_orbits, period_s, stardata)
    return particles, weights


@jit 
def smooth_histogram2d(particles, weights, stardata):
    '''
    '''
    
    im_size = 256
    
    x = particles[0, :]
    y = particles[1, :]
    
    weights = jnp.where((x != 0) & (y != 0), weights, 0)
    
    xbound, ybound = jnp.max(jnp.abs(x)), jnp.max(jnp.abs(y))
    bound = jnp.max(jnp.array([xbound, ybound]))
    _, xedges, yedges = jnp.histogram2d(x, y, bins=im_size, weights=weights, range=jnp.array([[-bound, bound], [-bound, bound]]))
    
    x_indices = jnp.digitize(x, xedges)
    y_indices = jnp.digitize(y, yedges)
    
    side_width = xedges[1] - xedges[0]
    
    alphas = x%side_width
    betas = y%side_width
    
    big_alphas = alphas + side_width / 2    # these alphas are in the right half of their respective bin
    big_betas = betas + side_width / 2      # these betas are in the top half of their respective bin
    
    a_s = jnp.minimum(alphas, big_alphas)
    b_s = jnp.minimum(betas, big_betas)
    
    one_minus_a_indices = x_indices - (1 + 2 * jnp.heaviside(alphas - side_width / 2, 0))
    one_minus_b_indices = y_indices - (1 + 2 * jnp.heaviside(betas - side_width / 2, 0))
    
    # now check the indices that are out of bounds
    x_edge_check = jnp.heaviside(one_minus_a_indices, 1) * jnp.heaviside(len(x_indices) - one_minus_a_indices, 0)
    y_edge_check = jnp.heaviside(one_minus_b_indices, 1) * jnp.heaviside(len(y_indices) - one_minus_b_indices, 0)
    
    x_edge_check = x_edge_check.astype(int)
    y_edge_check = y_edge_check.astype(int)
    
    main_quadrant = a_s * b_s * weights
    horizontal_quadrant = (side_width - a_s) * b_s * weights
    vertical_quadrant = a_s * (side_width - b_s) * weights
    corner_quadrant = (side_width - a_s) * (side_width - b_s) * weights
    
    # H = jnp.zeros((im_size, im_size))
    # H[x_indices, y_indices] += main_quadrant
    # H[x_indices * x_edge_check, y_indices] += x_edge_check * horizontal_quadrant
    # H[x_indices, y_indices * y_edge_check] += y_edge_check * vertical_quadrant
    # H[x_indices * x_edge_check, y_indices * y_edge_check] += x_edge_check * y_edge_check * corner_quadrant
    
    # The below few lines rely fundamentally on the following line sourced from https://jax.readthedocs.io/en/latest/_autosummary/jax.numpy.ndarray.at.html:
    # Unlike NumPy in-place operations such as x[idx] += y, if multiple indices refer to the same location, all updates will be applied (NumPy would only apply the last update, rather than applying all updates.)
    
    H = jnp.zeros((im_size, im_size))
    H = H.at[x_indices, y_indices].add(main_quadrant)
    H = H.at[x_indices * x_edge_check, y_indices].add(x_edge_check * horizontal_quadrant)
    H = H.at[x_indices, y_indices * y_edge_check].add(y_edge_check * vertical_quadrant)
    H = H.at[x_indices * x_edge_check, y_indices * y_edge_check].add(x_edge_check * y_edge_check * corner_quadrant)
    
    X, Y = jnp.meshgrid(xedges, yedges)
    # H = H.T
    H /= jnp.max(H)
    
    H = jnp.minimum(H, jnp.ones((im_size, im_size)) * stardata['histmax'])
    
    shape = 30 // 2  # choose just large enough grid for our gaussian
    gx, gy = jnp.meshgrid(jnp.arange(-shape, shape+1, 1), jnp.arange(-shape, shape+1, 1))
    gxy = jnp.exp(- (gx*gx + gy*gy) / (2 * stardata['sigma']**2))
    gxy /= gxy.sum()
    
    H = signal.convolve(H, gxy, mode='same', method='fft')
    
    H /= jnp.max(H)
    
    return X, Y, H
    

@jit
def spiral_grid(particles, weights, stardata):
    ''' Takes in the particle positions and weights and calculates the 2D histogram, ignoring those points at (0,0,0), and
        applying a Gaussian blur.
    Parameters
    ----------
    particles : ndarray (Ndim, Nparticles)
        Particle positions in cartesian coordinates
    weights : array (Nparticles)
        Weight of each particle in the histogram (for orbital/azimuthal variations)
    sigma : 
    '''
    im_size = 256
    
    x = particles[0, :]
    y = particles[1, :]
    
    weights = jnp.where((x != 0) & (y != 0), weights, 0)
    
    H, xedges, yedges = jnp.histogram2d(y, x, bins=im_size, weights=weights)
    X, Y = jnp.meshgrid(xedges, yedges)
    H = H.T
    H /= jnp.max(H)
    
    H = jnp.minimum(H, jnp.ones((im_size, im_size)) * stardata['histmax'])
    
    shape = 30 // 2  # choose just large enough grid for our gaussian
    gx, gy = jnp.meshgrid(jnp.arange(-shape, shape+1, 1), jnp.arange(-shape, shape+1, 1))
    gxy = jnp.exp(- (gx*gx + gy*gy) / (2 * stardata['sigma']**2))
    gxy /= gxy.sum()
    
    H = signal.convolve(H, gxy, mode='same', method='fft')
    
    H /= jnp.max(H)
    
    return X, Y, H

@jit
def spiral_grid_w_bins(particles, weights, stardata, xbins, ybins):
    ''' Takes in the particle positions and weights and calculates the 2D histogram, ignoring those points at (0,0,0), and
        applying a Gaussian blur.
    Parameters
    ----------
    particles : ndarray (Ndim, Nparticles)
        Particle positions in cartesian coordinates
    weights : array (Nparticles)
        Weight of each particle in the histogram (for orbital/azimuthal variations)
    sigma : 
    '''
    im_size = 256
    
    x = particles[0, :]
    y = particles[1, :]
    
    weights = jnp.where((x != 0) & (y != 0), weights, 0)
    
    H, xedges, yedges = jnp.histogram2d(x, y, bins=[xbins, ybins], weights=weights)
    X, Y = jnp.meshgrid(xedges, yedges)
    H = H.T
    H /= jnp.max(H)
    
    H = jnp.minimum(H, jnp.ones((im_size, im_size)) * stardata['histmax'])
    
    shape = 30 // 2  # choose just large enough grid for our gaussian
    gx, gy = jnp.meshgrid(jnp.arange(-shape, shape+1, 1), jnp.arange(-shape, shape+1, 1))
    gxy = jnp.exp(- (gx*gx + gy*gy) / (2 * stardata['sigma']**2))
    gxy /= gxy.sum()
    
    H = signal.convolve(H, gxy, mode='same', method='fft')
    
    H /= jnp.max(H)
    
    return X, Y, H

def plot_spiral(X, Y, H):
    ''' Plots the histogram given by X, Y edges and H densities
    '''
    fig, ax = plt.subplots()
    
    ax.pcolormesh(X, Y, H, cmap='hot')
    # import matplotlib.colors as cols
    # ax.pcolormesh(X, Y, H, norm=cols.LogNorm(vmin=1, vmax=H.max()))
    # ax.pcolormesh(X, Y, H, norm=cols.PowerNorm(gamma=1/2), cmap='hot')
    ax.set(aspect='equal', xlabel='', ylabel='',
           xticklabels=[], yticklabels=[])
    
    fig.savefig('TestSystemHist.png', dpi=400, bbox_inches='tight')


# @jit
def spiral_gif(stardata):
    '''
    '''
    starcopy = stardata.copy()
    fig, ax = plt.subplots()
    
    # im_size = 256
    # im = np.zeros((im_size, im_size))
    starcopy['phase'] = 0.01
    starcopy['sigma'] = 2
    particles, weights = dust_plume(stardata)
    X, Y, H = spiral_grid(particles, weights, starcopy)
    xmin, xmax = jnp.min(X), jnp.max(X)
    ymin, ymax = jnp.min(Y), jnp.max(Y)
    # border = [[xmin, xmax], [ymin, ymax]]
    # bins = [X, Y]
    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax), aspect='equal', 
           xlabel='Relative RA (")', ylabel='Relative Dec (")')
    
    starcopy['phase'] = 0.5
    particles, weights = dust_plume(starcopy)
    X, Y, H = spiral_grid(particles, weights, starcopy)
    # vmin, vmax = jnp.min(H), jnp.max(H)
    
    every = 1
    length = 10
    # now calculate some parameters for the animation frames and timing
    nt = int(stardata['period'])    # roughly one year per frame
    # nt = 10
    frames = jnp.arange(0, nt, every)    # iterable for the animation function. Chooses which frames (indices) to animate.
    fps = len(frames) // length  # fps for the final animation
    
    phases = jnp.linspace(0, 1, nt)
    
    # @jit
    def animate(i):
        if (i // every)%20 == 0:
            print(f"{i // every} / {len(frames)}")
        # print(i)
        starcopy['phase'] = phases[i] + 0.5
        particles, weights = dust_plume(starcopy)
        X, Y, H = spiral_grid(particles, weights, starcopy)
        # ax.imshow(H, extent=[0, 1, 0, 1], vmin=vmin, vmax=vmax, cmap='Greys')
        # ax.pcolormesh(xedges, yedges[::-1], H, vmax=vmax)
        ax.pcolormesh(X, Y, H, cmap='hot')
        return fig, 

    ani = animation.FuncAnimation(fig, animate, frames=frames, blit=True, repeat=False)
    ani.save(f"animation.gif", writer='pillow', fps=fps)
    
def plot_3d(particles, weights):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    n = 1
    ax.scatter(particles[0, ::n], particles[1, ::n], particles[2, ::n], marker='.', s=100, alpha=0.5)
    ax.view_init(elev=-90, azim=0)
    ax.set_box_aspect([1.0, 1.0, 1.0])
    ax.set(xlabel='', ylabel='', 
           xticklabels=[], yticklabels=[], zticklabels=[])
    fig.savefig('TestSystem3D.png', dpi=400, bbox_inches='tight')
    
def plot_orbit(stardata):
    ## plots orbits
    theta = np.linspace(0, 2 * np.pi, 100)
    r1 = stardata['p1'] / (1 + stardata['eccentricity'] * np.cos(theta))
    r2 = stardata['p2'] / (1 + stardata['eccentricity'] * np.cos(theta))

    x1, y1 = r1 * np.cos(theta), r1 * np.sin(theta)
    x2, y2 = -r2 * np.cos(theta), -r2 * np.sin(theta)

    fig, ax = plt.subplots()

    ax.plot(x1, y1)
    ax.plot(x2, y2)
    ax.set_aspect('equal')


test_system = {"m1":15.,                # solar masses
        "m2":10.,                # solar masses
        "eccentricity":0., 
        "inclination":23.8,       # degrees
        "asc_node":254.1,         # degrees
        "arg_peri":10.6,           # degrees
        "open_angle":125.,       # degrees (full opening angle)
        "period":125.,           # years
        "distance":2400.,        # pc
        "windspeed1":700.,       # km/s
        "windspeed2":2400.,      # km/s
        "turn_on":-180.,         # true anomaly (degrees)
        "turn_off":180.,         # true anomaly (degrees)
        "oblate":0.,
        "nuc_dist":1., "opt_thin_dist":2.,           # nucleation and optically thin distance (AU)
        "acc_max":0.1,                                 # maximum acceleration (km/s/yr)
        "orb_sd":0., "orb_amp":0., "orb_min":180., "az_sd":30., "az_amp":0., "az_min":270.,
        "comp_incl":127.1, "comp_az":116.5, "comp_open":0., "comp_reduction":0., "comp_plume":1.,
        "phase":0.6, 
        "sigma":5.,              # sigma for gaussian blur
        "histmax":1.}

# # # for i in range(10):
# t1 = time.time()
# particles, weights = dust_plume(test_system)
# X, Y, H = smooth_histogram2d(particles, weights, test_system)
# print(time.time() - t1)
# plot_spiral(X, Y, H)

# plot_3d(particles, weights)



# import numpy as np
# import matplotlib.pyplot as plt

# def rotate_x(angle):
#     arr = np.array([[1, 0, 0],
#                      [0, np.cos(angle), np.sin(angle)],
#                      [0, -np.sin(angle), np.cos(angle)]])
#     return arr

# def rotate_y(angle):
#     arr = np.array([[np.cos(angle), 0, -np.sin(angle)],
#                      [0, 1, 0],
#                      [np.sin(angle), 0, np.cos(angle)]])
#     return arr

# def rotate_z(angle):
#     arr = np.array([[np.cos(angle), np.sin(angle), 0],
#                      [-np.sin(angle), np.cos(angle), 0],
#                      [0, 0, 1]])
#     return arr


# theta = np.linspace(0, 2*np.pi, 30)
# phi = np.pi / 2
# r = 1

# z = r * np.cos(theta) * np.sin(phi)
# y = r * np.sin(theta) * np.sin(phi)
# x = r * np.cos(phi) + 1 * np.ones(len(theta))

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')

# ax.plot3D(x, y, z, marker='.', ls='')
# ax.set(xlabel='', ylabel='', zlabel='', 
#        xticklabels=[], yticklabels=[], zticklabels=[],
#        xlim=(0.5, 3))
# ax.set_box_aspect([1.0, 1.0, 1.0])
# ax.view_init(elev=30, azim=40)
# fig.savefig('RingStructure.png', dpi=400, bbox_inches='tight')




def orbital_positions(stardata):
    
    phase = stardata['phase']%1
    
    period_s = stardata['period'] * 365.25 * 24 * 60 * 60
    
    n_orbits = 1
    n_t = 100       # circles per orbital period
    n_points = 40   # points per circle
    n_particles = n_points * n_t * n_orbits
    n_time = n_t * n_orbits
    theta = 2 * jnp.pi * jnp.linspace(0, 1, n_points)
    times = period_s * jnp.linspace(phase, n_orbits + phase, n_time)
    n_time = len(times)
    n_t = n_time / n_orbits
    ecc = stardata['eccentricity']
    # E, true_anomaly = kepler_solve(times, period_s, ecc)
    
    E, true_anomaly = kepler(2 * jnp.pi * times / period_s, jnp.array([ecc]))
    
    a1, a2 = calculate_semi_major(period_s, stardata['m1'], stardata['m2'])
    r1 = a1 * (1 - ecc * jnp.cos(E)) * 1e-3     # radius in km 
    r2 = a2 * (1 - ecc * jnp.cos(E)) * 1e-3
    # ws_ratio = stardata['windspeed1'] / stardata['windspeed2']
    
    positions1 = jnp.array([jnp.cos(true_anomaly), 
                            jnp.sin(true_anomaly), 
                            jnp.zeros(n_time)])
    positions2 = jnp.copy(positions1)
    positions1 *= r1      # position in the orbital frame
    positions2 *= -r2     # position in the orbital frame
    
    return positions1, positions2

def transform_orbits(pos1, pos2, stardata):
    pos1 = euler_angles(pos1, stardata['asc_node'], stardata['inclination'], stardata['arg_peri'])
    pos2 = euler_angles(pos2, stardata['asc_node'], stardata['inclination'], stardata['arg_peri'])
    pos1 = 60 * 60 * 180 / jnp.pi * jnp.arctan(pos1 / (stardata['distance'] * 3.086e13))
    pos2 = 60 * 60 * 180 / jnp.pi * jnp.arctan(pos2 / (stardata['distance'] * 3.086e13))
    return pos1, pos2

# @jit
def orbit_spiral_gif(stardata):
    '''
    '''
    starcopy = stardata.copy()
    fig, ax = plt.subplots(figsize=(6, 6))
    
    every = 1
    length = 10
    # now calculate some parameters for the animation frames and timing
    # nt = int(stardata['period'])    # roughly one year per frame
    nt = 100
    # nt = 10
    frames = jnp.arange(0, nt, every)    # iterable for the animation function. Chooses which frames (indices) to animate.
    fps = len(frames) // length  # fps for the final animation
    
    phases = jnp.linspace(0, 1, nt)
    pos1, pos2 = orbital_positions(test_system)
    pos1, pos2 = transform_orbits(pos1, pos2, starcopy)
    
    
    lim = 2 * max(np.max(np.abs(pos1)), np.max(np.abs(pos2)))
    xbins = np.linspace(-lim, lim, 257)
    ybins = np.linspace(-lim, lim, 257)
    ax.set_aspect('equal')
    
    
    # @jit
    def animate(i):
        ax.cla()
        if i%20 == 0:
            print(i)
        starcopy['phase'] = phases[i] + 0.5
        particles, weights = dust_plume_for_gif(starcopy)
        
        pos1, pos2 = orbital_positions(starcopy)
        pos1, pos2 = transform_orbits(pos1, pos2, starcopy)

        X, Y, H = spiral_grid_w_bins(particles, weights, starcopy, xbins, ybins)
        ax.pcolormesh(X, Y, H, cmap='hot')
        
        
        ax.plot(pos1[0, :], pos1[1, :], c='w')
        ax.plot(pos2[0, :], pos2[1, :], c='w')
        ax.scatter([pos1[0, -1], pos2[0, -1]], [pos1[1, -1], pos2[1, -1]], c=['tab:cyan', 'w'], s=100)
        
        ax.set(xlim=(-lim, lim), ylim=(-lim, lim))
        ax.set_facecolor('k')
        ax.set_axis_off()
        ax.text(0.3 * lim, -0.8 * lim, f"Phase = {starcopy['phase']%1:.2f}", c='w', fontsize=14)
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        return fig, 

    ani = animation.FuncAnimation(fig, animate, frames=frames, blit=True, repeat=False)
    ani.save(f"orbit_spiral.gif", writer='pillow', fps=fps)

test_system = {"m1":22.,                # solar masses
        "m2":10.,                # solar masses
        "eccentricity":0.5, 
        "inclination":60.,       # degrees
        "asc_node":254.1,         # degrees
        "arg_peri":10.6,           # degrees
        "open_angle":40.,       # degrees (full opening angle)
        "period":1.,           # years
        "distance":10.,        # pc
        "windspeed1":0.1,       # km/s
        "windspeed2":2400.,      # km/s
        "turn_on":-180.,         # true anomaly (degrees)
        "turn_off":180.,         # true anomaly (degrees)
        "oblate":0.,
        "nuc_dist":0.0001, "opt_thin_dist":2.,           # nucleation and optically thin distance (AU)
        "acc_max":0.1,                                 # maximum acceleration (km/s/yr)
        "orb_sd":0., "orb_amp":0., "orb_min":180., "az_sd":30., "az_amp":0., "az_min":270.,
        "comp_incl":127.1, "comp_az":116.5, "comp_open":0., "comp_reduction":0., "comp_plume":1.,
        "phase":0.6, 
        "sigma":1.5,              # sigma for gaussian blur
        "histmax":1.}
orbit_spiral_gif(test_system)
    
    



















