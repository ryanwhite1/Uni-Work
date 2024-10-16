#include <cmath>
#include <iostream>
#include <vector>
#include <omp.h>
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
    double pos_angle = (1. - 88.75 / moon_period) * 2. * M_PI;
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
    double pos_angle = (1. - 88.75 / moon_period) * 2. * M_PI;
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
    double kick_time = 74.9;    // required time to perform kick (found from the previous integration)
    double full_orbit_time = moon_period + kick_time;    // have 2nd integration go for a full moon orbit once capture has happened.
    std::cout << "System energy before integration = " << nbody_energy(part1_26_particles, masses) << std::endl;
    grav_Nbody(part1_26_particles, masses, dt, full_orbit_time, kick_file, 1, kick_time);
    std::cout << "System energy after integration = " << nbody_energy(part1_26_particles, masses) << std::endl;
}

void part2_1(){
    // run over a 20x20 lattice, with 30 temperature samples, and 1 lattice (can change to more if wanted)
    int Ndim = 20, Ntemps = 30, Nlattices = 1;
    double temp_min = 0., temp_max = 5.;
    std::vector<double> temps(Ntemps, 0);
    for (int i = 0; i < Ntemps; i++){temps[i] = temp_min + i * (temp_max - temp_min) / Ntemps;} // fill out our temperature array
    std::string filename = "Ising_Datasets/Part2_1_run_X.txt"; // initialise filename to save data to, where "X" can be changed based on the number of lattices we're doing
    int sweep_mult = 1;
    for (int n = 0; n < Nlattices; n++){
        filename[27] = '0' + n+1; // update our filename to save to
        IsingLattice lattice(Ndim, Ndim, temp_max, n, filename);
        lattice.initialise_lattice();
        lattice.output_params();
        for (int t = Ntemps - 1; t >= 0; t--){
            sweep_mult = (int)(1 + 19 * exp(-pow(((temps[t] - 2.269) / 0.3), 2))); // do 20x as many sweeps at the critical temperature, and do f(x) as many near it, where f(x) is a gaussian with STD 0.3
            lattice.change_temperature(temps[t]); // update our lattice bath temperature 
            lattice.run_monte_carlo(1000 * sweep_mult, 1); // run for 1000*mult sweeps, and output the data on each sweep
            std::cout << "Temperature = " << temps[t] << std::endl;
            lattice.print_lattice();
        }
        lattice.close_file();
    }
}

void part2_2(){
    std::vector<int> dims = {8, 16, 32, 64};
    std::vector<int> first_num = {1, 2, 4, 8}; // numbers for the output filenames
    
    double temp_min = 0.1, temp_max = 4.9;
    
    std::string filename = "Ising_Datasets/Part2_2_ndim=X0.txt";
    int sweep_mult = 1;
    for (int n = 0; n < 4; n++){
        std::cout << "Running sim on lattice of size " << dims[n] << std::endl;
        filename[28] = '0' + first_num[n];
        IsingLattice lattice(dims[n], dims[n], temp_max, n, filename);
        lattice.initialise_lattice();
        lattice.output_params();

        int Ntemps = (int) (20 + pow(dims[n], 0.8));
        std::vector<double> temps(Ntemps, 0);
        for (int i = 0; i < Ntemps; i++){temps[i] = temp_min + i * (temp_max - temp_min) / Ntemps;}

        for (int t = Ntemps - 1; t >= 0; t--){
            sweep_mult = (int)(1 + 19 * exp(-pow(((temps[t] - 2.269) / 0.3), 2))); // do 20x as many sweeps at the critical temperature, and do f(x) as many near it, where f(x) is a gaussian with STD 0.3
            lattice.change_temperature(temps[t]); // update our lattice bath temperature 
            lattice.run_monte_carlo(1000 * sweep_mult, 1); // run for 1000*mult sweeps, and output the data on each sweep
            std::cout << "Temperature = " << temps[t] << std::endl;
            // h.print_lattice();
        }
        lattice.close_file();
    }

    // now we want to run a lattice for some temperatures just near the critical temp to fit power models to
    std::cout << "Running sim on lattice near critical temperature" << std::endl;
    int near_crit_num = 10, near_crit_dim = 40; // number of temperatures and dimension of lattice
    std::vector<double> near_crit_temps(near_crit_num, 0);
    for (int i = 0; i < 10; i++){near_crit_temps[i] = 2 + i * (2.27 - 2) / near_crit_num;}
    IsingLattice lattice(near_crit_dim, near_crit_dim, temp_max, 0, "Ising_Datasets/Part2_2_Power.txt");
    lattice.initialise_lattice();
    lattice.output_params();
    for (int t = near_crit_num - 1; t >= 0; t--){
        lattice.change_temperature(near_crit_temps[t]); // update our lattice bath temperature 
        lattice.run_monte_carlo(10000, 1); // run for 10000 sweeps, and output the data on each sweep
        std::cout << "Temperature = " << near_crit_temps[t] << std::endl;
        // h.print_lattice();
    }
    lattice.close_file();
}

void part2_3(){
    // want to test the OpenMP code with a 64x64 lattice at one temperature and a variety of thread counts.
    int Ndim = 64;
    double temp = 4;
    std::vector<int> num_threads = {1, 2, 4, 8};
    double t1 = 0., t2 = 0.; // initialise our time variables to see how long the code takes
    int nsweeps = 1;    // only performing one sweep
    std::string filename = "Ising_Datasets/Part2_3_runs.txt"; // this is where we'll save our times
    std::ofstream output_file;
    output_file.open(filename);

    IsingLattice lattice(Ndim, Ndim, temp, 0, "");
    lattice.initialise_lattice();
    int num_runs = 20;  // we'll do this many runs for each of our thread counts to get a good idea of the averaged behaviour
    for (int i = 0; i < (int)num_threads.size(); i++){  // iterate over our thread counts
        output_file << num_threads[i] << "\t";
        for (int r = 0; r < num_runs; r++){     // iterate over our runs
            t1 = omp_get_wtime();
            lattice.run_monte_carlo_parallel(nsweeps, num_threads[i]); // run for one sweep with our specified number of threads
            t2 = omp_get_wtime();
            std::cout << num_threads[i] << " threads completed " << nsweeps << " sweeps in " << t2 - t1 << " s" << std::endl;
            output_file << t2 - t1 << "\t";
        }
        output_file << std::endl;
    }
    lattice.close_file();
}

int main(){
    // runs each assignment part on its own
    std::cout << "Beginning part 1.1..." << std::endl;
    part1_1();
    std::cout << "Beginning part 1.2..." << std::endl;
    part1_2();
    std::cout << "Beginning part 2.1..." << std::endl;
    part2_1();
    std::cout << "Beginning part 2.2..." << std::endl;
    part2_2();
    std::cout << "Beginning part 2.3..." << std::endl;
    part2_3();
    return 0;
}

