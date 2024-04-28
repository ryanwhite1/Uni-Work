# pragma once
#include <cmath>
#include <iostream>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include "matrix.hpp"

std::vector<double> ODEs_vector(Matrix particles, std::vector<double> masses, int index){
    // calculates the velocities and accelerations on particles[index]

    // particles is a Nx5 matrix for x, y, vx, vy, t params for N particles
    std::vector<double> X_deriv(4, 0);
    // the X_deriv is a 1x4 vector corresponding to vx, vy, ax, ay

    for (int i = 0; i < 2; i++){
        X_deriv[i] = particles(index, i + 2);
    }

    double r_norm = 0., dx = 0., dy = 0.;
    // now calculate gravitational acceleration
    for (int i = 0; i < (int)masses.size(); i++){
        if (i != index){
            dx = particles(i, 0) - particles(index, 0);
            dy = particles(i, 1) - particles(index, 1);
            r_norm = sqrt(dx*dx + dy*dy);

            for (int j = 0; j < 2; j++){
                X_deriv[j+2] += masses[i] * (particles(i, j) - particles(index, j)) / (r_norm * r_norm * r_norm);
            }
        }
    }
    return X_deriv;
}

void Nbody_step(Matrix &particles, std::vector<double> masses, double dt){
    // performs RK4 integration on the positions/velocities of particles in the system
    Matrix particles_temp = particles;
    for (int i = 0; i < (int)particles.rows(); i++){
        std::vector<double> k1 = ODEs_vector(particles_temp, masses, i);
        
        Matrix k2_parts = particles_temp;
        for (int j = 0; j < 4; j++){
            k2_parts(i, j) += k1[i] * dt / 2.;
        }
        std::vector<double> k2 = ODEs_vector(k2_parts, masses, i);
        
        Matrix k3_parts = particles_temp;
        for (int j = 0; j < 4; j++){
            k3_parts(i, j) += k2[i] * dt / 2.;
        }
        std::vector<double> k3 = ODEs_vector(k3_parts, masses, i);

        Matrix k4_parts = particles_temp;
        for (int j = 0; j < 4; j++){
            k4_parts(i, j) += k3[i] * dt;
        }
        std::vector<double> k4 = ODEs_vector(k4_parts, masses, i);
        
        for (int j = 0; j < 4; j++){
            particles(i, j) += (k1[j] + 2.*k2[j] + 2.*k3[j] + k4[j]) * dt / 6.;
        }
        
        particles(i, 4) += dt;
    }
}

void output_orbits(Matrix &particles, std::ofstream &output_file){
    for (int i = 0; i < (int)particles.rows(); i++){
        for (int j = 0; j < (int)particles.cols(); j++){
            output_file << particles(i, j);
            if (j < (int)particles.cols() - 1){
                output_file << "\t";
            } else {
                output_file << "\n";
            }
        }
    }
}

void grav_Nbody(Matrix &particles, std::vector<double> masses, double dt, double total_t, std::string filename, int kick=0, double kick_time=0.){
    std::ofstream output_file;
    output_file.open(filename);
    output_orbits(particles, output_file); // output the initial positions of our orbiters
    int n_steps = std::ceil(total_t / dt);  // number of timesteps given our total time and timestep size
    int kicked = 0;         // this says whether or not the projectile has done its kick burn to enter a circular orbit around the moon; 0 for no, 1 for yes

    for (int i = 0; i < n_steps; i++){
        Nbody_step(particles, masses, dt);                  // calculate the movement of all bodies for one dt timestep
        for (int j = 0; j < 4; j++){particles(0, j) = 0.;}  // set the planet position/velocity to always be 0 as per the task sheet assumption
        output_orbits(particles, output_file);              // write the current positions to file

        // we only want to perform a kick at some time if the 'kick' parameter is not 0
        if ((kick > 0) && (kicked == 0)){
            double kick_dist = 0.5;     // circular orbit radius for the projectile-moon orbit, as per task sheet
            if (particles(0, 4) >= kick_time){  // if our elapsed time is equal to or past the desired kick time...
                double v_circ_moon = sqrt(masses[1] / kick_dist);    // calculate the orbital velocity around the moon at this radius
                // double theta = atan((particles(1, 1) - particles(2, 1)) / (particles(1, 0) - particles(2, 0)));     // calculate the projectile-moon angular separation
                // double theta = atan2((particles(1, 1) - particles(2, 1)), (particles(1, 0) - particles(2, 0))) + M_PI;     // calculate the projectile-moon angular separation
                double theta = atan2(-(particles(2, 1) - particles(1, 1)), -(particles(2, 0) - particles(1, 0))) - M_PI;     // calculate the projectile-moon angular separation
                std::cout << "Performing kick for v_circ = " << v_circ_moon << " given angular separation of "<< theta << " radians." << std::endl;
                // now update velocities
                particles(2, 2) += v_circ_moon * -sin(theta) - particles(2, 2) + particles(1, 2);      // vx = -v_circ sin(theta) - vx + vmoon
                particles(2, 3) += v_circ_moon * cos(theta) - particles(2, 3) + particles(1, 3);     // vy = v_circ cos(theta) - vy + vmoon
                kicked = 1; // set the kick counter to 1 so that we only kick once!
            }
        }
    }
    output_file.close();
}

double nbody_energy(Matrix particles, std::vector<double> masses){
    // calculates the orbital energy given particles positions and their masses
    double energy = 0.,temp_vel = 0., dist_temp = 0., dx = 0., dy = 0.; // initialise variables
    for (int i = 1; i < (int)particles.rows(); i++){
        temp_vel = sqrt(particles(i, 2)*particles(i, 2) + particles(i, 3)*particles(i, 3));
        energy += 0.5 * masses[i] * temp_vel*temp_vel;
        for (int j = 0; j < i; j++){
            if (j != i){
                dx = particles(i, 0) - particles(j, 0);
                dy = particles(i, 1) - particles(j, 1);
                dist_temp = sqrt(dx*dx + dy*dy);
                energy -= masses[i] * masses[j] / dist_temp;
            }
        }
    }
    return energy;
}





// std::vector<double> operator+(std::vector<double> &a, std::vector<double> &b) {
//     // overload matrix addition so we can easily add two matrices together
//     std::vector<double> sum = a;
//     for (int i = 0; i < (int)a.size(); i++) {
//         sum[i] += b[i];
//     }
//     return sum;
// }
// std::vector<double> operator*(std::vector<double> &a, std::vector<double> &b) {
//     // overload matrix addition so we can easily add two matrices together
//     std::vector<double> mult = a;
//     for (int i = 0; i < (int)a.size(); i++) {
//         mult[i] *= b[i];
//     }
//     return mult;
// }