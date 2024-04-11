# pragma once
#include <cmath>
#include <iostream>
#include <vector>
#include <string>
# include <iostream>
# include <fstream>
#include "matrix.hpp"

std::vector<double> ODEs_vector(Matrix particles, std::vector<double> masses, int index){
    // particles is a Nx5 matrix for x, y, vx, vy, t params for N particles
    std::vector<double> X_deriv(4, 0);
    // the X_deriv is a 1x4 vector corresponding to vx, vy, ax, ay

    for (int i = 0; i < 2; i++){
        X_deriv[i] = particles(index, i + 2);
    }

    // now calculate gravitational acceleration
    for (int i = 0; i < (int)masses.size(); i++){
        if (i != index){
            double r_norm = 0.;
            for (int j = 0; j < 2; j++){r_norm += (particles(i, j) - particles(index, j)) * (particles(i, j) - particles(index, j));}
            r_norm = sqrt(r_norm);

            for (int j = 0; j < 2; j++){
                X_deriv[j+2] += masses[i] * (particles(i, j) - particles(index, j)) / (r_norm * r_norm * r_norm);
            }
        }
    }
    return X_deriv;
}

void Nbody_step(Matrix &particles, std::vector<double> masses, double dt){
    Matrix particles_temp = particles;
    // double ti = particles(0, 4) + dt;
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

void grav_Nbody(Matrix &particles, std::vector<double> masses, double dt, double total_t, std::string filename){
    std::ofstream output_file;
    output_file.open(filename);

    output_orbits(particles, output_file);
    
    int n_steps = std::ceil(total_t / dt);
    for (int i = 0; i < n_steps; i++){
        Nbody_step(particles, masses, dt);
        output_orbits(particles, output_file);
    }
    output_file.close();
}

double nbody_energy(Matrix particles, std::vector<double> masses){
    double energy = 0.,temp_vel = 0., dist_temp = 0., dx = 0., dy = 0.;

    for (int i = 0; i < (int)particles.rows(); i++){
        temp_vel = sqrt(particles(i, 2)*particles(i, 2) + particles(i, 3)*particles(i, 3));
        energy += 0.5 * masses[i] * temp_vel*temp_vel;
        for (int j = 0; j < (int)particles.rows(); j++){
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