// #pragma once
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <complex>
#include <chrono>
#include "RK4.hpp"
#include "ising.hpp"


void part_one(){
    // this function runs the entirety of part 1 of the project, evolving all of the needed wavefunctions and saving the data
    int N = 128; // num of x grid partitions
    double L = 20., dt = 0.01, t = 30., delta_x = L / ((double)N - 1.); // define length scale, time step, max time, and length step
    int t_steps = std::ceil(t / dt);    // num of time steps

    // PART b)
    // start with a plane wave and evolve that for some time, varying the interaction strength
    std::cout << "Evolving plane wave for different interaction terms..." << std::endl;
    std::vector<double> xs(N, 0.); // initialise x vals vector
    std::vector<std::complex<double>> plane_wave_wavefunc(N, 0.); // initialise wave function vector
    for (int i = 0; i < N; i++){
        // now update the vectors to calculate x val and wavefunc val at that x
        xs[i] = -L/2 + i * delta_x;
        plane_wave_wavefunc[i] = plane_wave(xs[i], L);
    }
    std::vector<double> g_vals = {0., 0.5, 1., 5., 20.}; // interaction strength values for us to model the plane wave evolution for
    // now create a vector of filenames for the different interaction strengths so that we can just run the sims and save the data within 1 for loop
    std::vector<std::string> plane_wave_files = {"g=0_plane_wave_evol.txt", "g=0.5_plane_wave_evol.txt", "g=1_plane_wave_evol.txt", "g=5_plane_wave_evol.txt", "g=20_plane_wave_evol.txt"};
    for (int i = 0; i < (int)g_vals.size(); i++){
        std::vector<std::complex<double>> plane_wavefunc_copy = plane_wave_wavefunc; // make a copy of the initial wave function (t = 0)
        RK4_method(plane_wavefunc_copy, delta_x, g_vals[i], dt, t, plane_wave_files[i]);    // perform the rk4 method up to our max time, and save the data
    }

    // PART c)
    // much of the same code as above, but now for a solitary soliton as opposed to a plane wave
    std::cout << "Evolving solitons for different values of u..." << std::endl;
    std::vector<double> us = {-5., -1., 0., 1., 5.}; // modelling different soliton speeds now instead of interaction strengths (we now set g = -1)
    std::vector<std::string> soliton_files = {"u=-5_soliton.txt", "u=-1_soliton.txt", "u=0_soliton.txt", "u=1_soliton.txt","u=5_soliton.txt"};
    std::vector<std::vector<std::complex<double>>> u_solitons((int)us.size(), std::vector<std::complex<double>>(N)); // initialise 2d vector to store soliton data
    std::vector<std::vector<double>> soliton_peak((int)us.size(), std::vector<double>(t_steps)); // 2d vector to store peak positions of all solitons
    for (int i = 0; i < (int)us.size(); i++){
        // one iteration for each of our soliton speeds
        for (int j = 0; j < N; j++){
            // calculate initial state
            u_solitons[i][j] = wave_packet(xs[j], us[i], L);
        }
        RK4_method_with_peak(u_solitons[i], soliton_peak[i], xs, delta_x, -1., dt, t, soliton_files[i]); // run rk4 for this soliton
    }
    // now to output the data
    std::ofstream part_c_file;
    part_c_file.open("Part1c_peak_pos.txt"); // want to output the peak positions too
    for (int i = 0; i < t_steps; i++){ // for each time...
        part_c_file << (i+1) * 0.01 << "\t"; // output current time
        for (int j = 0; j < (int)us.size(); j++){  // for each soliton...
            part_c_file << soliton_peak[j][i]; // output soliton peak position
            if (j == (int)us.size() - 1){ // we're at the end of the line
                part_c_file << std::endl; 
            } else {
                part_c_file << "\t";
            }
        }
    }
    
    // PART d)
    // essentially the same as for part c), now keeping u = 0.1 and varying the relative phase of the solitons
    std::cout << "Evolving two solitons for different values of phase..." << std::endl;
    double u = 0.1;
    std::vector<double> phases = {0., M_PI/10., M_PI/7., M_PI/4., M_PI/3., M_PI/2., M_PI}; // these are our relative phases to test
    std::vector<std::string> phase_files = {"theta=0_solitons.txt", "theta=pi_10_solitons.txt", "theta=pi_7_solitons.txt", "theta=pi_4_solitons.txt", "theta=pi_3_solitons.txt", "theta=pi_2_solitons.txt", "theta=pi_solitons.txt"};
    std::vector<std::vector<std::complex<double>>> phase_solitons((int)phases.size(), std::vector<std::complex<double>>(N));
    std::vector<std::vector<std::vector<double>>> solitons_peaks((int)phases.size(), std::vector<std::vector<double>>(t_steps, std::vector<double>(2)));
    for (int i = 0; i < (int)phases.size(); i++){
        for (int j = 0; j < N; j++){
            phase_solitons[i][j] = two_solitons(xs[j], u, phases[i], L);
        }
        RK4_method_with_two_peaks(phase_solitons[i], solitons_peaks[i], xs, delta_x, -1., dt, t, phase_files[i]);
    }
    std::ofstream part_d_file;
    part_d_file.open("Part1d_peak_pos.txt");
    for (int i = 0; i < t_steps; i++){
        part_d_file << (i+1) * 0.01 << "\t";
        for (int j = 0; j < (int)phases.size(); j++){
            part_d_file << solitons_peaks[j][i][0] << "\t" << solitons_peaks[j][i][1];
            if (j == (int)phases.size() - 1){
                part_d_file << std::endl;
            } else {
                part_d_file << "\t";
            }
        }
    }
    
}

void part_two(){
    // this function runs the entirety of part 2 of the project
    // PART a)
    // here we want to construct the hamiltonian and solve for its eigenvectors/values for systems with varying number of particles, timing it in each case
    std::cout << "Timing Hamiltonian construction w.r.t atom number..." << std::endl;
    std::ofstream part_a_file; // create file to store our data
    part_a_file.open("Part2a_run_times.txt");
    std::vector<int> atom_nums = {2, 3, 4, 5, 6, 7, 8}; // the number of particles per system that we want to test
    for (int i = 0; i < (int)atom_nums.size(); i++){
        part_a_file << atom_nums[i] << "\t"; // output to file the number of particles in this system
        for (int j = 0; j < 20; j++){ // run for 20 iterations to get some idea of the variance
            auto start = std::chrono::steady_clock::now(); // get time before calculations
            Matrix hamiltonian = hamiltonian_matrix(atom_nums[i], 10.); // construct our hamiltonian with g = 10 (chosen arbitrarily since we're only timing the code speed)
            MatrixAndVector sols = solveEigenSystem(hamiltonian, hamiltonian.rows()); // solve for the eigenvectors/values
            auto end = std::chrono::steady_clock::now(); // get time after calculations
            double time = std::chrono::duration<double>(end - start).count(); // convert the time to a value in seconds
            part_a_file << time << "\t"; // output the time taken to file
        }
        part_a_file << std::endl;
    }
    part_a_file.close();

    // PART b)
    // in this part we construct several systems with N = 8 and vary the interaction strength, seeing how the ground state energy changes as a result
    std::cout << "Testing ground state behaviour vs interaction term..." << std::endl;
    // want to start by constructing vector of g values
    int num_g = 50, N = 8, M = 2000; // no. of g vals, atom number of our system, integration steps for analytic result
    double max_g = 8., min_g = 0., dg = (max_g - min_g) / (double)(num_g - 1); // stop, start, step of our g value vector
    std::vector<double> gs(num_g, 0), ground_states(num_g, 0), ground_state_deriv(num_g, 0), thermo_limit(num_g, 0), thermo_limit_deriv(num_g, 0); // initialise all vectors
    for (int i = 0; i < num_g; i++){gs[i] = min_g + (double)i * dg;} // populate g array with linearly spaced values
    for (int i = 0; i < num_g; i++){ // for each g value...
        Matrix hamiltonian = hamiltonian_matrix(N, gs[i]); // construct hamiltonian at this g
        MatrixAndVector sols = solveEigenSystem(hamiltonian, hamiltonian.rows()); // solve for eigenvalues/vectors
        ground_states[i] = sols.vec[0]; // get ground state eigenvalue (eigenvalues are stored in the vector, ground state is the 0th element)

        // now calculate the analytic expression for the ground state energy at this value of g (in the thermodynamic limit) using riemann sum formula from task sheet
        double x = 8. * gs[i] / ((2. + gs[i])*(2. + gs[i]));
        for (int k = 0; k < M; k++){ // this is the approximate integral
            thermo_limit[i] += sqrt(1. - x * pow(sin(M_PI * (double)k / (2. * (double)M)), 2));
        }
        thermo_limit[i] *= -(0.5/M_PI) * (2. + gs[i]) * (M_PI / (2. * (double)M));
    }
    // now we want to numerically estimate the second derivative at each point (except the boundaries) in our numerical and analytic (thermo_limit) ground state energy vectors
    for (int i = 1; i < num_g - 1; i++){
        ground_state_deriv[i] = second_deriv(ground_states, i, dg);
        thermo_limit_deriv[i] = second_deriv(thermo_limit, i, dg);
    }
    // finally, we want to output all of this data to file
    std::ofstream part_b_file;
    part_b_file.open("Part2b_ground_states.txt");
    for (int i = 0; i < num_g; i++){
        // output in format: g value -- numerical ground state energy / N -- 2nd deriv of this / N -- analytic ground state energy / N -- 2nd deriv of this
        part_b_file << gs[i] << "\t" << ground_states[i] / (double)N << "\t" << ground_state_deriv[i] / (double)N << "\t" << thermo_limit[i] << "\t" << thermo_limit_deriv[i] << std::endl;
    }
    part_b_file.close();


    // PART c)
    // in this final section we want to construct a system at g=0, then evolve it in a g=4 state
    double dt = 0.01, time = 20., t = 0.; // time step, max time, initial time
    int nsteps = time / dt;
    std::cout << "Evolving N=8 system in time..." << std::endl;
    Matrix hamiltonian = hamiltonian_matrix(8, 0.); // construct N = 8 system at g = 0
    MatrixAndVector initial_sol = solveEigenSystem(hamiltonian, hamiltonian.rows()); // get initial eigenvectors/values
    Matrix hamiltonian_g4 = hamiltonian_matrix(8, 4.); // now construct our hamiltonian for the g = 4 case
    MatrixAndVector quench_sol = solveEigenSystem(hamiltonian_g4, hamiltonian_g4.rows()); // get the eigenvectors/values for the g = 4 case
    std::vector<double> eigenvalues = quench_sol.vec; // eigenvalues of g = 4 hamiltonian
    std::vector<std::complex<double>> ground_state_wavefunc(initial_sol.mat.rows(), 0.); // initialise vector to store our initial wavefunction at the ground state of g=0
    for (int i = 0; i < initial_sol.mat.rows(); i++){ground_state_wavefunc[i] = initial_sol.mat(0, i);} // get the ground state eigenvector
    std::vector<std::complex<double>> wavefunc = ground_state_wavefunc; // treat the exponential diagonal matrix as just a vector
    quench_sol.mat = transpose(quench_sol.mat); // transpose our g=4 matrix because of the way dsyev does things

    // now create 2d complex vector to store our matrices
    std::vector<std::vector<std::complex<double>>> energy_matrix((int)eigenvalues.size(), std::vector<std::complex<double>> ((int)eigenvalues.size(), 0.));
    for (int i = 0; i < (int)eigenvalues.size(); i++){energy_matrix[i][i] = exp(-imag * eigenvalues[i] * dt);} // populate the diagonal with the complex exponential terms

    // now calculate the pauli spin matrices once for our N = 8 system
    Matrix Sx = pauli_x(N, 0), Sz = pauli_z(N, 0), Cxx = pauli_x(N, 0) * pauli_x(N, 1);
    for (int m = 1; m < N; m++){
        Sx = Sx + pauli_x(N, m);
        Sz = Sz + pauli_z(N, m);
        for (int n = 0; n < N; n++){
            if (n != m){
                Cxx = Cxx + pauli_x(N, m) * pauli_x(N, n);
            }
        }
    }
    // now calculate our time evolution matrix just once: U * e^(-iD dt) * U^dagger
    std::vector<std::vector<std::complex<double>>> time_evolution = quench_sol.mat * energy_matrix * transpose(quench_sol.mat);
    
    std::ofstream part_c_file;
    part_c_file.open("Part2c_g=4_evolution.txt");
    // initialise our Sz, Sx, and Cxx observables with the current state, and save them to file
    double temp_Sz = dot_product(wavefunc, Sz * wavefunc); 
    double temp_Sx = dot_product(wavefunc, Sx * wavefunc); 
    double temp_Cxx = dot_product(wavefunc, Cxx * wavefunc); 
    part_c_file << t << "\t" << temp_Sz << "\t" << temp_Sx << "\t" << temp_Cxx << std::endl;
    for (int i = 0; i < nsteps; i++){ // for each step in our time evolution...
        wavefunc = time_evolution * wavefunc; // evolve the wave function, and...
        double temp_Sz = dot_product(wavefunc, Sz * wavefunc); // compute the observables:
        double temp_Sx = dot_product(wavefunc, Sx * wavefunc); 
        double temp_Cxx = dot_product(wavefunc, Cxx * wavefunc); 
        t += dt;
        // now output observables to file
        part_c_file << t << "\t" << temp_Sz << "\t" << temp_Sx << "\t" << temp_Cxx << std::endl;
    }
    part_c_file.close();
    // done!
}

int main(){
    std::cout << "Beginning Part I..." << std::endl;
    part_one();
    std::cout << "Beginning Part II..." << std::endl;
    part_two();
    return 0;
}