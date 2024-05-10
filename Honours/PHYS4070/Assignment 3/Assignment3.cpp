#pragma once
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <complex>
#include "RK4.hpp"


void part_one(){
    int N = 128;
    double L = 20., dt = 0.01, t = 30., delta_x = L / ((double)N - 1.);

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
    
    
}

int main(){
    part_one();
    return 0;
}