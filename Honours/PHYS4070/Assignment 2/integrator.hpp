# pragma once
#include <cmath>
#include <iostream>
#include <vector>
#include "matrix.hpp"

Matrix ODEs_vector(Matrix particles, std::vector<double> masses, int index){
    // particles is a Nx5 matrix for x, y, vx, vy, t params for N particles
    Matrix X_deriv(2, 2);

    for (int i = 0; i < 2; i++){
        X_deriv(0, i) = particles(index, i + 2);
    }

    // now calculate gravitational acceleration
    for (int i = 0; i < masses.size(); i++){
        if (i != index){
            double r_norm = 0.;
            for (int j = 0; j < 2; j++){r_norm += (particles(i, j) - particles(index, j)) * (particles(i, j) - particles(index, j));}
            r_norm = sqrt(r_norm);

            for (int j = 0; j < 2; j++){
                X_deriv(1, j) += masses[i] * (particles(i, j) - particles(index, j)) / (r_norm * r_norm * r_norm);
            }
        }
    }
    return X_deriv;
}

void Nbody_step(Matrix &particles, std::vector<double> masses, double dt){
    Matrix particles_temp = particles;
    double ti = particles(0, 4) + dt;
    for (int i = 0; i < (int)particles.rows(); i++){
        Matrix k1 = ODEs_vector(particles_temp, masses, i);

        Matrix k2_parts = particles_temp;
        for (int j = 0; j < 4; j++){
            k2_parts(i, j) += k1(i, j) * dt / 2.;
        }
        Matrix k2 = ODEs_vector(k2_parts, masses, i);

        Matrix k3_parts = particles_temp;
        for (int j = 0; j < 4; j++){
            k3_parts(i, j) += k2(i, j) * dt / 2.;
        }
        Matrix k3 = ODEs_vector(k3_parts, masses, i);

        Matrix k4_parts = particles_temp;
        for (int j = 0; j < 4; j++){
            k4_parts(i, j) += k3(i, j) * dt;
        }
        Matrix k4 = ODEs_vector(k4_parts, masses, i);

        for (int j = 0; j < 2; j++){
            particles(i, j) += (k1(j, 0) + 2.*k2(j, 0) + 2.*k3(j, 0) + k4(j, 0)) * dt / 6.;
            particles(i, j+2) += (k1(j, 1) + 2.*k2(j, 1) + 2.*k3(j, 1) + k4(j, 1)) * dt / 6.;
        }
    }
}





std::vector<double> operator+(std::vector<double> &a, std::vector<double> &b) {
    // overload matrix addition so we can easily add two matrices together
    std::vector<double> sum = a;
    for (int i = 0; i < (int)a.size(); i++) {
        sum[i] += b[i];
    }
    return sum;
}
std::vector<double> operator*(std::vector<double> &a, std::vector<double> &b) {
    // overload matrix addition so we can easily add two matrices together
    std::vector<double> mult = a;
    for (int i = 0; i < (int)a.size(); i++) {
        mult[i] *= b[i];
    }
    return mult;
}