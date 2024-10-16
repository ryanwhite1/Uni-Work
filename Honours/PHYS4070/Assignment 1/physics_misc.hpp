# pragma once
# include <vector>
# include <cmath>
# include <iostream>
# include <cassert> // for assert(), used in matrix example
# include "bspline.hpp"
# include "matrix.hpp"
# include "linalgSolvers.hpp"
# include "integrate.hpp"
# include "calculateYK.hpp"
# include "plot_misc.hpp"

double hydrogen_like_potential(double r, int l, double Z){
    // potential for our Hydrogen-like atoms
    return -Z/r + l * (l + 1.) / (2. * r*r);
}
double hydrogen_potential(double r, int l){return hydrogen_like_potential(r, l, 1.);}
double lithium_potential(double r, int l){return hydrogen_like_potential(r, l, 3.);}

double green_potential(double r, double Z, double h, double d){
    return ((Z - 1.) * h * (exp(r / d) - 1.)) / (r * (1. + h * (exp(r / d) - 1.)));
}
double gr_hydrogen_like_potential(double r, int l, double Z, double h, double d){
    return hydrogen_like_potential(r, l, Z) + green_potential(r, Z, h, d);
}
double gr_lithium_potential(double r, int l){return gr_hydrogen_like_potential(r, l, 3., 1., 0.2);}
double li_hartree_potential(double r, int l, double ykab){
    return lithium_potential(r, l) + 2. * ykab;
}

void populate_Hamiltonian(Matrix &mat, std::vector<double> r, BSpline bspline, int l, double (*potential)(double, int)){
    int N = mat.cols();
    int r_N = r.size();
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            std::vector<double> int1(r_N), int2(r_N);   // first and second integration region grid points
            for (int k = 0; k < r_N; k++){
                int1[k] = Bspl_deriv(bspline, i+2, r[k]) * Bspl_deriv(bspline, j+2, r[k]);  // b'_i * b'_j
                int2[k] = bspline.b(i+2, r[k]) * potential(r[k], l) * bspline.b(j+2, r[k]); // b_i * V(r) * b_j
            }
            mat.at(i, j) = 0.5 * trapezoid_integration(r, int1) + trapezoid_integration(r, int2); 
        }
    }
}
void populate_Hamiltonian_hartree(Matrix &mat, std::vector<double> r, BSpline bspline, int l, std::vector<double> ykab){
    int N_red = mat.cols();
    int r_N = r.size();
    for (int i = 0; i < N_red; i++){
        for (int j = 0; j < N_red; j++){
            std::vector<double> int1(r_N), int2(r_N);   // first and second integration region grid points
            for (int k = 0; k < r_N; k++){
                int1[k] = Bspl_deriv(bspline, i+2, r[k]) * Bspl_deriv(bspline, j+2, r[k]);  // b'_i * b'_j
                int2[k] = bspline.b(i+2, r[k]) * li_hartree_potential(r[k], l, ykab[k]) * bspline.b(j+2, r[k]); // b_i * V(r) * b_j
            }
            mat.at(i, j) = 0.5 * trapezoid_integration(r, int1) + trapezoid_integration(r, int2); 
        }
    }
}
void populate_Hamiltonian_hartree_fock(Matrix &mat, std::vector<double> r, BSpline bspline, int l, int k, std::vector<double> Pr_s1){
    double Lambda = 0.5;
    if (l == 1){
        Lambda = 1./6.;
    }
    std::vector<double> ys1s1 = YK::ykab(0, Pr_s1, Pr_s1, r);
    int N_red = mat.cols();
    int r_N = r.size();
    for (int i = 0; i < N_red; i++){
        for (int j = 0; j < N_red; j++){
            std::vector<double> int1(r_N), int2(r_N), int3(r_N);   // first and second integration region grid points
            std::vector<double> bj(r_N);
            for (int k = 0; k < r_N; k++){
                bj[k] = bspline.b(j+2, r[k]);
            }
            std::vector<double> ys1bj = YK::ykab(k, Pr_s1, bj, r);
            for (int k = 0; k < r_N; k++){
                int1[k] = Bspl_deriv(bspline, i+2, r[k]) * Bspl_deriv(bspline, j+2, r[k]);  // b'_i * b'_j
                int2[k] = bspline.b(i+2, r[k]) * li_hartree_potential(r[k], l, ys1s1[k]) * bspline.b(j+2, r[k]); // b_i * V(r) * b_j
                int3[k] = bspline.b(i+2, r[k]) * -2. * Lambda * ys1bj[k] * Pr_s1[k];
            }
            mat.at(i, j) = 0.5 * trapezoid_integration(r, int1) + trapezoid_integration(r, int2) + trapezoid_integration(r, int3);
        }
    }
}

void populate_B_Matrix(Matrix &mat, std::vector<double> r, BSpline bspline){
    int N = mat.cols();
    int r_N = r.size();
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            std::vector<double> int1(r_N);
            for (int k = 0; k < r_N; k++){
                int1[k] = bspline.b(i+2, r[k]) * bspline.b(j+2, r[k]);
            }
            mat.at(i, j) = trapezoid_integration(r, int1);
        }
    }
}

std::vector<double> get_expansion_coeffs(Matrix eigenvectors, int i){
    std::vector<double> c(eigenvectors.cols());
    for (int j = 0; j < (int)c.size(); j++){
        c[j] = eigenvectors.at(i, j);
    }
    return c;
}

double radial_wavefunction(std::vector<double> exp_coeffs, BSpline bspl, double r){
    double P = 0.;
    for (int i = 0; i < (int)exp_coeffs.size(); i++){
        P += exp_coeffs[i] * bspl(i+2, r);
    }
    return P;
}
std::vector<double> vec_radial_wavefunction(std::vector<double> exp_coeffs, BSpline bspl, std::vector<double> r){
    std::vector<double> Pr(r.size());
    for (int i = 0; i < (int)r.size(); i++){
        Pr[i] = radial_wavefunction(exp_coeffs, bspl, r[i]);
    }
    return Pr;
}

MatrixAndVector solve_schrodinger(BSpline bspl, int l, int N_red, std::vector<double> r){
    // l = orbital state
    // N_red = reduced number of b_splines (i.e. ignoring first 2 and last 1)
    // r = integration grid of radii

    Matrix matrix_H(N_red, N_red);
    Matrix matrix_B(N_red, N_red);
    populate_Hamiltonian(matrix_H, r, bspl, l, &lithium_potential);
    populate_B_Matrix(matrix_B, r, bspl);
    
    MatrixAndVector matandvec = solveEigenSystem_AveBv(matrix_H, matrix_B, N_red);
    return matandvec;
}
MatrixAndVector solve_schrodinger_gr(BSpline bspl, int l, int N_red, std::vector<double> r){
    // l = orbital state
    // N_red = reduced number of b_splines (i.e. ignoring first 2 and last 1)
    // r = integration grid of radii

    Matrix matrix_H(N_red, N_red);
    Matrix matrix_B(N_red, N_red);
    populate_Hamiltonian(matrix_H, r, bspl, l, &gr_lithium_potential);
    populate_B_Matrix(matrix_B, r, bspl);
    
    MatrixAndVector matandvec = solveEigenSystem_AveBv(matrix_H, matrix_B, N_red);
    return matandvec;
}
MatrixAndVector solve_schrodinger_hartree(BSpline bspl, int l, int N_red, std::vector<double> r, std::vector<double> P_s1){
    // l = orbital state
    // N_red = reduced number of b_splines (i.e. ignoring first 2 and last 1)
    // r = integration grid of radii
    std::vector<double> ykab = YK::ykab(0, P_s1, P_s1, r);
    Matrix matrix_H(N_red, N_red);
    Matrix matrix_B(N_red, N_red);
    populate_Hamiltonian_hartree(matrix_H, r, bspl, l, ykab);
    populate_B_Matrix(matrix_B, r, bspl);
    
    MatrixAndVector matandvec = solveEigenSystem_AveBv(matrix_H, matrix_B, N_red);
    return matandvec;
}
MatrixAndVector solve_schrodinger_hartree_fock(BSpline bspl, int l, int k, int N_red, std::vector<double> r, std::vector<double> P_s1){
    // l = orbital state
    // N_red = reduced number of b_splines (i.e. ignoring first 2 and last 1)
    // r = integration grid of radii
    Matrix matrix_H(N_red, N_red);
    Matrix matrix_B(N_red, N_red);
    populate_Hamiltonian_hartree_fock(matrix_H, r, bspl, l, k, P_s1);
    populate_B_Matrix(matrix_B, r, bspl);
    
    MatrixAndVector matandvec = solveEigenSystem_AveBv(matrix_H, matrix_B, N_red);
    return matandvec;
}


double expectation_value(std::vector<double> A1, std::vector<double> r, std::vector<double> A2){
    // this assumes r = x for integration (i.e. that we're taking the position expectation val.)
    std::vector<double> y(r.size());
    for (int i = 0; i < (int)r.size(); i++){
        y[i] = A1[i] * r[i] * A2[i];
    }
    return trapezoid_integration(r, y);
}

double state_lifetime(std::vector<double> A1, std::vector<double> r, std::vector<double> A2){
    double Rab = expectation_value(A1, r, A2);
    double freq = 0.06791;                      // experimental frequency
    double gamma = 2./3. * Rab*Rab * freq*freq*freq * 1.071e10;     // decay rate in s
    double lifetime = 1 / gamma;
    return lifetime * 1.e9;     // return lifetime in ns
}

double green_correction(std::vector<double> Pa, std::vector<double> r){
    // green correction for ***lithium***
    std::vector<double> Vgr(r.size());
    for (int i = 0; i < (int)r.size(); i++){ Vgr[i] = green_potential(r[i], 3., 1., 0.2); }
    std::vector<double> y = Pa * Pa;
    y = y * Vgr;
    return trapezoid_integration(r, y);
}

double ee_corection(std::vector<double> Pa_1s, std::vector<double> Pa, std::vector<double> r){
    std::vector<double> y1s1s = YK::ykab(0, Pa_1s, Pa_1s, r);
    std::vector<double> y = Pa * Pa;
    y = y * y1s1s;
    return 2. * trapezoid_integration(r, y);
}

MatrixAndVector hartree_step(BSpline bspl, Matrix &matrix_H, Matrix &matrix_B, MatrixAndVector &matandvec, std::vector<double> r, std::vector<double> &s_Pr){
    std::vector<double> ykab = YK::ykab(0, s_Pr, s_Pr, r);
    int N_red = matrix_H.cols();
    populate_Hamiltonian_hartree(matrix_H, r, bspl, 0, ykab);
    matandvec = solveEigenSystem_AveBv(matrix_H, matrix_B, N_red);
    return matandvec;
}

std::vector<double> hartree_procedure(BSpline bspl, int N_red, std::vector<double> r){
    std::cout << "Running Hartree procedure to convergence..." << std::endl;
    Matrix matrix_H(N_red, N_red);
    Matrix matrix_B(N_red, N_red);
    populate_Hamiltonian(matrix_H, r, bspl, 0, &lithium_potential);
    populate_B_Matrix(matrix_B, r, bspl);
    
    MatrixAndVector matandvec = solveEigenSystem_AveBv(matrix_H, matrix_B, N_red);
    std::vector<double> s_coeffs = get_expansion_coeffs(matandvec.mat, 0); // get the expansion coefficients from the eigenvectors
    std::vector<double> s_Pr = vec_radial_wavefunction(s_coeffs, bspl, r);  // calculate the radial wavefunction on our grid
    double energy = matandvec.vec[0];
    double err = 1e10;

    std::vector<double> iters(1);
    std::vector<double> energies = {energy};
    while (fabs(err) > 2.e-6){
        // std::cout << "err = " << err << std::endl;
        matandvec = hartree_step(bspl, matrix_H, matrix_B, matandvec, r, s_Pr);
        s_coeffs = get_expansion_coeffs(matandvec.mat, 0); // get the expansion coefficients from the eigenvectors
        s_Pr = vec_radial_wavefunction(s_coeffs, bspl, r);  // calculate the radial wavefunction on our grid

        err = energy - matandvec.vec[0];
        energy = matandvec.vec[0];
        iters.push_back(iters.back() + 1);
        energies.push_back(energy);
    }

    output_1d_data(iters, energies, "B3_core_energies.txt");

    std::cout << "Hartree procedure converged!" << std::endl;

    return s_Pr;
}

MatrixAndVector hartree_fock_step(BSpline bspl, Matrix &matrix_H, Matrix &matrix_B, MatrixAndVector &matandvec, std::vector<double> r, std::vector<double> &Pr_s1, int l, int k){
    int N_red = matrix_H.cols();
    populate_Hamiltonian_hartree_fock(matrix_H, r, bspl, l, k, Pr_s1);
    matandvec = solveEigenSystem_AveBv(matrix_H, matrix_B, N_red);
    return matandvec;
}

std::vector<double> hartree_fock_procedure(BSpline bspl, int N_red, std::vector<double> r, std::vector<double> &Pr_s1){
    std::cout << "Running Hartree-Fock procedure to convergence..." << std::endl;
    int l = 0, k = 0;   // we only want to solve for Ps1
    Matrix matrix_H(N_red, N_red);
    Matrix matrix_B(N_red, N_red);
    std::vector<double> ys1s1 = YK::ykab(0, Pr_s1, Pr_s1, r);
    populate_Hamiltonian_hartree(matrix_H, r, bspl, l, ys1s1);
    populate_B_Matrix(matrix_B, r, bspl);
    
    MatrixAndVector matandvec = solveEigenSystem_AveBv(matrix_H, matrix_B, N_red);
    std::vector<double> s_coeffs = get_expansion_coeffs(matandvec.mat, 0); // get the expansion coefficients from the eigenvectors
    std::vector<double> s_Pr = vec_radial_wavefunction(s_coeffs, bspl, r);  // calculate the radial wavefunction on our grid
    double energy = matandvec.vec[0];
    double err = 1e10;

    std::vector<double> iters(1);
    std::vector<double> energies = {energy};
    while (fabs(err) > 2.e-6){
        // std::cout << "err = " << err << std::endl;
        matandvec = hartree_fock_step(bspl, matrix_H, matrix_B, matandvec, r, s_Pr, l, k);
        s_coeffs = get_expansion_coeffs(matandvec.mat, 0); // get the expansion coefficients from the eigenvectors
        s_Pr = vec_radial_wavefunction(s_coeffs, bspl, r);  // calculate the radial wavefunction on our grid

        err = energy - matandvec.vec[0];
        energy = matandvec.vec[0];
        iters.push_back(iters.back() + 1);
        energies.push_back(energy);
    }

    output_1d_data(iters, energies, "B4_core_energies.txt");

    std::cout << "Hartree-Fock procedure converged!" << std::endl;

    return s_Pr;
}

