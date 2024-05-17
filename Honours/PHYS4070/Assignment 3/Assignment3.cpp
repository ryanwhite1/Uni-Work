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
    int N = 128;
    double L = 20., dt = 0.01, t = 30., delta_x = L / ((double)N - 1.);
    int t_steps = std::ceil(t / dt);

    // PART b)
    std::cout << "Evolving plane wave for different interaction terms..." << std::endl;
    std::vector<double> xs(N, 0.);
    std::vector<std::complex<double>> plane_wave_wavefunc(N, 0.);
    for (int i = 0; i < N; i++){
        xs[i] = -L/2 + i * delta_x;
        plane_wave_wavefunc[i] = plane_wave(xs[i], L);
    }
    std::string planewave_file = "plane_wave_evol.txt";
    std::vector<double> g_vals = {0., 0.5, 1., 5., 20.};
    std::vector<std::string> plane_wave_files = {"g=0_plane_wave_evol.txt", "g=0.5_plane_wave_evol.txt", "g=1_plane_wave_evol.txt", "g=5_plane_wave_evol.txt", "g=20_plane_wave_evol.txt"};
    for (int i = 0; i < (int)g_vals.size(); i++){
        std::vector<std::complex<double>> plane_wavefunc_copy = plane_wave_wavefunc;
        RK4_method(plane_wavefunc_copy, delta_x, g_vals[i], dt, t, plane_wave_files[i]);
    }

    // PART c)
    std::cout << "Evolving solitons for different values of u..." << std::endl;
    std::vector<double> us = {-5., -1., 0., 1., 5.};
    std::vector<std::string> soliton_files = {"u=-5_soliton.txt", "u=-1_soliton.txt", "u=0_soliton.txt", "u=1_soliton.txt","u=5_soliton.txt"};
    std::vector<std::vector<std::complex<double>>> u_solitons((int)us.size(), std::vector<std::complex<double>>(N));
    std::vector<std::vector<double>> soliton_peak((int)us.size(), std::vector<double>(t_steps));
    for (int i = 0; i < (int)us.size(); i++){
        for (int j = 0; j < N; j++){
            u_solitons[i][j] = wave_packet(xs[j], us[i], L);
        }
        RK4_method_with_peak(u_solitons[i], soliton_peak[i], xs, delta_x, -1., dt, t, soliton_files[i]);
    }
    std::ofstream part_c_file;
    part_c_file.open("Part1c_peak_pos.txt");
    for (int i = 0; i < t_steps; i++){
        part_c_file << (i+1) * 0.01 << "\t";
        for (int j = 0; j < (int)us.size(); j++){
            part_c_file << soliton_peak[j][i];
            if (j == (int)us.size() - 1){
                part_c_file << std::endl;
            } else {
                part_c_file << "\t";
            }
        }
    }
    
    // PART d)
    std::cout << "Evolving two solitons for different values of phase..." << std::endl;
    double u = 0.1;
    std::vector<double> phases = {0., M_PI/10., M_PI/7., M_PI/4., M_PI/3., M_PI/2., M_PI};
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
    // PART a)
    std::cout << "Timing Hamiltonian construction w.r.t atom number..." << std::endl;
    std::ofstream part_a_file;
    part_a_file.open("Part2a_run_times.txt");
    std::vector<int> atom_nums = {2, 3, 4, 5, 6, 7, 8};
    for (int i = 0; i < (int)atom_nums.size(); i++){
        part_a_file << atom_nums[i] << "\t";
        for (int j = 0; j < 10; j++){ // run for 10 iterations to get some idea of the variance
            auto start = std::chrono::steady_clock::now();
            Matrix hamiltonian = hamiltonian_matrix(atom_nums[i], 10.);
            MatrixAndVector sols = solveEigenSystem(hamiltonian, hamiltonian.rows());
            auto end = std::chrono::steady_clock::now();
            double time = std::chrono::duration<double>(end - start).count();
            part_a_file << time << "\t";
        }
        part_a_file << std::endl;
    }
    part_a_file.close();

    // PART b)
    // construct array of g values
    std::cout << "Testing ground state behaviour vs interaction term..." << std::endl;
    int num_g = 50, N = 8, M = 2000; // no. of g vals, atom number of our system, integration steps for analytic result
    double max_g = 8., min_g = 0., dg = (max_g - min_g) / (double)(num_g - 1); // stop, start, step
    std::vector<double> gs(num_g, 0), ground_states(num_g, 0), ground_state_deriv(num_g, 0), thermo_limit(num_g, 0), thermo_limit_deriv(num_g, 0);
    for (int i = 0; i < num_g; i++){gs[i] = min_g + (double)i * dg;}
    for (int i = 0; i < num_g; i++){
        Matrix hamiltonian = hamiltonian_matrix(N, gs[i]);
        MatrixAndVector sols = solveEigenSystem(hamiltonian, hamiltonian.rows());
        ground_states[i] = sols.vec[0];

        // now calculate the analytic expression for this value of g
        double x = 8. * gs[i] / ((2. + gs[i])*(2. + gs[i]));
        for (int k = 0; k < M; k++){
            thermo_limit[i] += sqrt(1. - x * pow(sin(M_PI * (double)k / (2. * (double)M)), 2));
        }
        thermo_limit[i] *= -(0.5/M_PI) * (2. + gs[i]) * (M_PI / (2. * (double)M));
    }

    for (int i = 1; i < num_g - 1; i++){
        ground_state_deriv[i] = second_deriv(ground_states, i, dg);
        thermo_limit_deriv[i] = second_deriv(thermo_limit, i, dg);
    }
    std::ofstream part_b_file;
    part_b_file.open("Part2b_ground_states.txt");
    for (int i = 0; i < num_g; i++){
        part_b_file << gs[i] << "\t" << ground_states[i] / (double)N << "\t" << ground_state_deriv[i] / (double)N << "\t" << thermo_limit[i] << "\t" << thermo_limit_deriv[i] << std::endl;
    }
    part_b_file.close();


    // PART c)
}

int main(){
    part_one();
    // part_two();
    return 0;
}