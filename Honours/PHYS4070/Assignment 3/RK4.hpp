#pragma once
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <complex>
#include <algorithm>

const std::complex<double> imag(0., 1.);

std::complex<double> plane_wave(double x, double L){
    std::complex<double> ans = 0.;
    if ((x > - L / 2.) && (x < L / 2.)){
        ans = std::cos(M_PI * x / L);
    }
    return ans;
}
std::complex<double> wave_packet(double x, double u, double L){
    std::complex<double> ans = 0.;
    if ((x > - L / 2.) && (x < L / 2.)){
        ans = sqrt(2.) * std::exp(imag * u * x) / cosh(x);
    }
    return ans;
}
std::complex<double> two_solitons(double x, double u, double phase, double L){
    std::complex<double> ans = 0.;
    if ((x > - L / 2.) && (x < L / 2.)){
        ans = std::exp(imag * u * x) / cosh(x + L / 4.);
        ans += std::exp(imag * (-u * x + phase)) / cosh(x - L / 4.);
        ans *= sqrt(2.);
    }
    return ans;
}


void output_wavefunction(std::vector<std::complex<double>> wavefunction, std::ofstream &output_file){
    // saves the orbital data to file in the format x y vx vy t, where each row is for a different particle at a different time
    int N = (int)wavefunction.size();
    for (int i = 0; i < N; i++){
        // output_file << wavefunction[i].real();
        output_file << std::norm(wavefunction[i]);
        if (i < N - 1){
            output_file << "\t";
        } else {
            output_file << "\n";
        }
    }
}
void output_timed_wavefunction(std::vector<std::complex<double>> wavefunction, std::ofstream &output_file, double t){
    output_file << t << "\t";
    output_wavefunction(wavefunction, output_file);
}

std::complex<double> second_deriv(std::vector<std::complex<double>> wavefunc, double index, double delta_x){
    // second derivative with the central difference method
    return (wavefunc[index + 1] - 2. * wavefunc[index] + wavefunc[index - 1]) / (delta_x * delta_x);
}
double second_deriv(std::vector<double> values, double index, double delta_x){
    // second derivative with the central difference method
    return (values[index + 1] - 2. * values[index] + values[index - 1]) / (delta_x * delta_x);
}
std::complex<double> ODE(std::vector<std::complex<double>> wavefunc, int index, double delta_x, double g){
    std::complex<double> X_deriv = -imag * (- second_deriv(wavefunc, index, delta_x) + g * std::norm(wavefunc[index]) * wavefunc[index]);
    return X_deriv;
}
// void RK4_step(std::vector<std::complex<double>> &wavefunc, double delta_x, double g, double dt){
//     // performs RK4 integration on the positions/velocities of particles in the system
//     std::vector<std::complex<double>> wavefunc_copy = wavefunc;
//     for (int i = 1; i < (int)wavefunc_copy.size() - 1; i++){
//         std::complex<double> k1 = ODE(wavefunc_copy, i, delta_x, g);
        
//         std::vector<std::complex<double>> k2_parts = wavefunc_copy;
//         k2_parts[i] += k1 * dt / 2.;
//         std::complex<double> k2 = ODE(k2_parts, i, delta_x, g);
        
//         std::vector<std::complex<double>> k3_parts = wavefunc_copy;
//         k3_parts[i] += k2 * dt / 2.;
//         std::complex<double> k3 = ODE(k3_parts, i, delta_x, g);

//         std::vector<std::complex<double>> k4_parts = wavefunc_copy;
//         k4_parts[i] += k3 * dt;
//         std::complex<double> k4 = ODE(k4_parts, i, delta_x, g);
        
//         wavefunc[i] += (k1 + 2.*k2 + 2.*k3 + k4) * dt / 6.;
//     }
// }
void RK4_step(std::vector<std::complex<double>> &wavefunc, double delta_x, double g, double dt){
    int N = (int)wavefunc.size();
    // performs RK4 integration on the positions/velocities of particles in the system
    std::vector<std::complex<double>> wavefunc_copy = wavefunc;
    std::vector<std::complex<double>> k2_parts = wavefunc_copy;
    std::vector<std::complex<double>> k3_parts = wavefunc_copy;
    std::vector<std::complex<double>> k4_parts = wavefunc_copy;
    std::vector<std::complex<double>> k1(N, 0.), k2(N, 0.), k3(N, 0.), k4(N, 0.);
    for (int i = 1; i < N - 1; i++){
        k1[i] = ODE(wavefunc_copy, i, delta_x, g);
        k2_parts[i] += k1[i] * dt / 2.;
    }
    for (int i = 1; i < N - 1; i++){
        k2[i] = ODE(k2_parts, i, delta_x, g);
        k3_parts[i] += k2[i] * dt / 2.;
    }
    for (int i = 1; i < N - 1; i++){
        k3[i] = ODE(k3_parts, i, delta_x, g);
        k4_parts[i] += k3[i] * dt;
    }
    for (int i = 1; i < N - 1; i++){
        k4[i] = ODE(k4_parts, i, delta_x, g);
        wavefunc[i] += (k1[i] + 2.*k2[i] + 2.*k3[i] + k4[i]) * dt / 6.;
    }
}

void RK4_method(std::vector<std::complex<double>> &wavefunc, double delta_x, double g, double dt, double total_t, std::string filename){
    double t = 0.;
    std::ofstream output_file;
    output_file.open(filename);
    output_timed_wavefunction(wavefunc, output_file, t); // output the initial wavefunction
    int n_steps = std::ceil(total_t / dt);  // number of timesteps given our total time and timestep size
    for (int i = 0; i < n_steps; i++){
        RK4_step(wavefunc, delta_x, g, dt);
        t += dt;
        output_timed_wavefunction(wavefunc, output_file, t);              // write the current positions to file
    }
    output_file.close();
}
void RK4_method_with_peak(std::vector<std::complex<double>> &wavefunc, std::vector<double> &peaks, std::vector<double> xs, double delta_x, double g, double dt, double total_t, std::string filename){
    double t = 0.;
    std::ofstream output_file;
    output_file.open(filename);
    output_timed_wavefunction(wavefunc, output_file, t); // output the initial wavefunction
    int n_steps = std::ceil(total_t / dt);  // number of timesteps given our total time and timestep size
    for (int i = 0; i < n_steps; i++){
        RK4_step(wavefunc, delta_x, g, dt);
        t += dt;
        output_timed_wavefunction(wavefunc, output_file, t);              // write the current positions to file

        std::vector<double> norm_wavefunc((int)wavefunc.size(), 0.);
        for (int z = 0; z < (int)wavefunc.size(); z++){norm_wavefunc[z] = std::norm(wavefunc[z]);}
        
        // get the peak position
        int peak_index = std::max_element(norm_wavefunc.begin(), norm_wavefunc.end()) - norm_wavefunc.begin();
        peaks[i] = xs[peak_index];
    }
    output_file.close();
}
void RK4_method_with_two_peaks(std::vector<std::complex<double>> &wavefunc, std::vector<std::vector<double>> &peaks, std::vector<double> xs, double delta_x, double g, double dt, double total_t, std::string filename){
    double t = 0.;
    std::ofstream output_file;
    output_file.open(filename);
    output_timed_wavefunction(wavefunc, output_file, t); // output the initial wavefunction
    int n_steps = std::ceil(total_t / dt);  // number of timesteps given our total time and timestep size
    int wavefunc_len = (int)wavefunc.size();
    for (int i = 0; i < n_steps; i++){
        RK4_step(wavefunc, delta_x, g, dt);
        t += dt;
        output_timed_wavefunction(wavefunc, output_file, t);              // write the current positions to file

        std::vector<double> norm_wavefunc((int)wavefunc.size(), 0.);
        for (int z = 0; z < (int)wavefunc.size(); z++){norm_wavefunc[z] = std::norm(wavefunc[z]);}
        // get the peak position
        std::vector<double> first_vec = std::vector<double>(norm_wavefunc.begin(), norm_wavefunc.end() - wavefunc_len/2);
        std::vector<double> second_vec = std::vector<double>(norm_wavefunc.begin() + wavefunc_len/2, norm_wavefunc.end());
        int first_peak_index = std::max_element(first_vec.begin(), first_vec.end()) - first_vec.begin();
        int second_peak_index = std::max_element(second_vec.begin(), second_vec.end()) - second_vec.begin() + wavefunc_len/2;
        peaks[i][0] = xs[first_peak_index];
        peaks[i][1] = xs[second_peak_index];
    }
    output_file.close();
}