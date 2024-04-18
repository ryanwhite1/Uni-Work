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
    int Ndim = 25, Ntemps = 30, Nlattices = 5;
    double temp_min = 0., temp_max = 5.;
    std::vector<double> temps(Ntemps, 0);
    for (int i = 0; i < Ntemps; i++){temps[i] = temp_min + i * (temp_max - temp_min) / Ntemps;}
    std::string filename = "Ising_Datasets/Part2_1_run_X.txt";
    for (int n = 0; n < Nlattices; n++){
        filename[27] = '0' + n+1;
        IsingLattice h(Ndim, Ndim, temp_max, n, filename);
        h.initialise_lattice();
        h.output_params();
        for (int t = Ntemps - 1; t >= 0; t--){
            h.change_temperature(temps[t]);
            h.run_monte_carlo(1000*Ndim*Ndim);
            h.output_params();
        }
        h.close_file();
    }
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

