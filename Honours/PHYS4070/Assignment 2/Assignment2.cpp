#include <cmath>
#include <iostream>
#include <vector>
#include "integrator.hpp"
#include "matrix.hpp"

void part1_1(){
    // start by shooting the projectile straight up at the moon!
    
    Matrix particles(3, 5);
    std::vector<double> masses = {1., 0., 1e-24};
    // set moon initial position and velocity
    double moon_orb = 19.;
    double moon_period = 2. * M_PI * sqrt(moon_orb*moon_orb*moon_orb);
    double moon_vc = 1. / sqrt(moon_orb);
    double pos_angle = (1. - 89.1 / moon_period) * 2. * M_PI;
    std::cout << moon_period << " " << moon_vc << " " << pos_angle << std::endl;
    particles(1, 0) = moon_orb * cos(pos_angle);   // x
    particles(1, 1) = moon_orb * sin(pos_angle); // y
    particles(1, 2) = -moon_vc * sin(pos_angle);   // vx
    particles(1, 3) = moon_vc * cos(pos_angle);   // vy
    // set particle initial position and velocity
    particles(2, 0) = 1.;       // x
    particles(2, 2) = 1.376;    // vx

    std::string filename = "part1_1.txt";
    
    double dt = 0.0005, total_t = 100.;
    grav_Nbody(particles, masses, dt, total_t, filename);
}

int main(){
    part1_1();
    return 0;
}

