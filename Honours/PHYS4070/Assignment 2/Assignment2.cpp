#include <cmath>
#include <iostream>
#include <vector>
#include "integrator.hpp"
#include "matrix.hpp"
#include "isingmodel.hpp"

void part1_1(){
    // start by shooting the projectile straight up at the moon!
    
    Matrix particles(3, 5); // 3 rows for 3 particles, 5 columns for x, y, vx, vy, t parameters
    std::vector<double> masses = {1., 0., 1e-24};  // planet, moon, projectile
    // set moon initial position and velocity
    double moon_orb = 19.;
    double moon_period = 2. * M_PI * sqrt(moon_orb*moon_orb*moon_orb);
    double moon_vc = 1. / sqrt(moon_orb);
    double pos_angle = (1. - 89.1 / moon_period) * 2. * M_PI;
    std::cout << moon_period << " " << moon_vc << " " << pos_angle << std::endl;
    particles(1, 0) = moon_orb * cos(pos_angle);    // x
    particles(1, 1) = moon_orb * sin(pos_angle);    // y
    particles(1, 2) = -moon_vc * sin(pos_angle);    // vx
    particles(1, 3) = moon_vc * cos(pos_angle);     // vy
    // set particle initial position and velocity
    particles(2, 0) = 1.;       // x
    particles(2, 2) = 1.376;    // vx

    std::string filename = "part1_1.txt";
    
    double dt = 0.0005, total_t = 100.;

    std::cout << "System energy before integration = " << nbody_energy(particles, masses) << std::endl;
    grav_Nbody(particles, masses, dt, total_t, filename);
    std::cout << "System energy after integration = " << nbody_energy(particles, masses) << std::endl;
}

void part1_2(){
    Matrix particles(3, 5); // 3 rows for 3 particles, 5 columns for x, y, vx, vy, t parameters
    std::vector<double> masses = {1., 0.1, 1e-24};  // planet, moon, projectile
    // set moon initial position and velocity
    double moon_orb = 19.;
    double moon_period = 2. * M_PI * sqrt(moon_orb*moon_orb*moon_orb);
    double moon_vc = 1. / sqrt(moon_orb);
    double pos_angle = (1. - 89.1 / moon_period) * 2. * M_PI;
    std::cout << moon_period << " " << moon_vc << " " << pos_angle << std::endl;
    double min_dist = 0.5;
    
    particles(1, 0) = moon_orb * cos(pos_angle);    // x
    particles(1, 1) = moon_orb * sin(pos_angle);    // y
    particles(1, 2) = -moon_vc * sin(pos_angle);    // vx
    particles(1, 3) = moon_vc * cos(pos_angle);     // vy
    // set particle initial position and velocity
    particles(2, 0) = 1.;       // x
    particles(2, 2) = 1.376;    // vx

    // now make copies of our initial system so that we can run the sim multiple times from the start
    Matrix part1_23_particles = particles;
    Matrix part1_26_particles = particles;
    double dt = 0.0005, total_t = 100.;     // integration timestep and total integration time

    std::string filename = "part1_23.txt";
    std::cout << "System energy before integration = " << nbody_energy(part1_23_particles, masses) << std::endl;
    grav_Nbody(part1_23_particles, masses, dt, total_t, filename);
    std::cout << "System energy after integration = " << nbody_energy(part1_23_particles, masses) << std::endl;

    std::cout << "Now performing integration including projectile velocity kick..." << std::endl;
    std::string kick_file = "part1_26.txt";
    double kick_time = 75.2;    // required time to perform kick (found from the previous integration)
    double full_orbit_time = moon_period + kick_time;    // have 2nd integration go for a full moon orbit once capture has happened.
    std::cout << "System energy before integration = " << nbody_energy(part1_26_particles, masses) << std::endl;
    grav_Nbody(part1_26_particles, masses, dt, full_orbit_time, kick_file, 1, kick_time);
    std::cout << "System energy after integration = " << nbody_energy(part1_26_particles, masses) << std::endl;
}

void part2_1(){
    IsingLattice h(20, 20, 2, 20, "test_file.txt");
    h.initialise_lattice();
    h.print_lattice();
    h.print_params();

    h.run_monte_carlo(100*10*10);
    h.print_lattice();
    h.print_params();
}

void part2_2(){

}

int main(){
    // std::cout << "Beginning part 1.1..." << std::endl;
    // part1_1();
    // std::cout << "Beginning part 1.2..." << std::endl;
    // part1_2();
    std::cout << "Beginning part 2.1..." << std::endl;
    part2_1();
    return 0;
}

