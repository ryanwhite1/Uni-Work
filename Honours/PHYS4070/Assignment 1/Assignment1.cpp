# include <vector>
# include <cmath>
# include <iostream>
# include <string>
# include "bspline.hpp"
# include "matrix.hpp"
# include "linalgSolvers.hpp"
# include "physics_misc.hpp"
# include "integrate.hpp"
# include "plot_misc.hpp"

void part_one(BSpline bspl, int N_red, std::vector<double> r){
    int s = 0, p = 1;   // values of l for the different orbital states
    // solve our system to get the energy eigenstates and eigenvectors (expansion coefficients)
    MatrixAndVector s_eval = solve_schrodinger(bspl, s, N_red, r);
    MatrixAndVector p_eval = solve_schrodinger(bspl, p, N_red, r);

    // Print the eigenstates for the 2nd part
    std::cout << "First 10 's' eigenstates:" << std::endl;
    s_eval.print_vector(10); // print first 10 elements in vector
    std::cout << "First 10 'p' eigenstates:" << std::endl;
    p_eval.print_vector(9); // print first 10 elements in vector

    // Now print the position expectation values for the third part
    std::cout << "Expectation for the s states:" << std::endl;
    for (int i = 0; i < 10; i++){
        std::vector<double> s_coeffs = get_expansion_coeffs(s_eval.mat, i); // get the expansion coefficients from the eigenvectors
        std::vector<double> s_Pr = vec_radial_wavefunction(s_coeffs, bspl, r);  // calculate the radial wavefunction on our grid
        double s_expectation = expectation_value(s_Pr, r, s_Pr);   
        std::cout << i+1 << "s state: " << s_expectation << "\t";

        if (i == 0 || i == 1){
            std::string filename("B1_ns_states.txt");
            filename.replace(3, 1, std::to_string(i+1));
            output_1d_data(r, s_Pr*s_Pr, filename);
        }
    } std::cout << std::endl;

    std::cout << "Expectation for the p states:" << std::endl;
    for (int i = 0; i < 9; i++){
        std::vector<double> p_coeffs = get_expansion_coeffs(p_eval.mat, i);
        std::vector<double> p_Pr = vec_radial_wavefunction(p_coeffs, bspl, r);
        double p_expectation = expectation_value(p_Pr, r, p_Pr);
        std::cout << i+2 << "p state: " << p_expectation << "\t";

        if (i == 0){
            output_1d_data(r, p_Pr*p_Pr, "B1_2p_states.txt");
        }
    } std::cout << std::endl;
}


void part_two(BSpline bspl, int N_red, std::vector<double> r){
    int s = 0, p = 1;   // values of l for the different orbital states
    // solve our system to get the energy eigenstates and eigenvectors (expansion coefficients)
    MatrixAndVector s_eval = solve_schrodinger_gr(bspl, s, N_red, r);
    MatrixAndVector p_eval = solve_schrodinger_gr(bspl, p, N_red, r);

    // Print the eigenstates for the 2nd part
    std::cout << "2s eigenstate:" << s_eval.vec[1] << std::endl;
    std::cout << "2p eigenstate:" << p_eval.vec[0] << std::endl;

    // Now print the position expectation values for the second part
    for (int i = 0; i < 2; i++){
        std::vector<double> s_coeffs = get_expansion_coeffs(s_eval.mat, i); // get the expansion coefficients from the eigenvectors
        std::vector<double> s_Pr = vec_radial_wavefunction(s_coeffs, bspl, r);  // calculate the radial wavefunction on our grid
        std::string filename("B2_ns_states.txt");
        filename.replace(3, 1, std::to_string(i+1));
        output_1d_data(r, s_Pr*s_Pr, filename);
    }
    
    std::vector<double> p_coeffs = get_expansion_coeffs(p_eval.mat, 0);
    std::vector<double> p_Pr = vec_radial_wavefunction(p_coeffs, bspl, r);
    output_1d_data(r, p_Pr*p_Pr, "B2_2p_states.txt");

    std::vector<double> s2_coeffs = get_expansion_coeffs(s_eval.mat, 1); // get the expansion coefficients from the eigenvectors
    std::vector<double> s2_Pr = vec_radial_wavefunction(s2_coeffs, bspl, r);  // calculate the radial wavefunction on our grid
    double lifetime = state_lifetime(s2_Pr, r, p_Pr);
    std::cout << "2p lifetime (Green's): " << lifetime << "ns" << std::endl;

    std::vector<double> s1_coeffs = get_expansion_coeffs(s_eval.mat, 0); // get the expansion coefficients from the eigenvectors
    std::vector<double> s1_Pr = vec_radial_wavefunction(s1_coeffs, bspl, r);  // calculate the radial wavefunction on our grid

    double green_corr_2s = green_correction(s2_Pr, r);
    double ee_corr_2s = ee_corection(s1_Pr, s2_Pr, r);
    double corr_2s = ee_corr_2s - green_corr_2s;
    double green_corr_2p = green_correction(p_Pr, r);
    double ee_corr_2p = ee_corection(s1_Pr, p_Pr, r);
    double corr_2p = ee_corr_2p - green_corr_2p;
    std::cout << "2s energy correction: " << corr_2s << "\n2p energy correction: " << corr_2p << std::endl;
    // std::cout << green_corr_2s << " " << green_corr_2p << std::endl;
}

void part_three(BSpline bspl, int N_red, std::vector<double> r){
    int s = 0, p = 1;
    std::vector<double> Pr_1s = hartree_procedure(bspl, N_red, r);
    save_vector(Pr_1s, "Hartree-1s.txt");
    output_1d_data(r, Pr_1s*Pr_1s, "B3_1s_states.txt");

    // now we want to generate the 2s and 2p states and save them
    MatrixAndVector eval_2s = solve_schrodinger_hartree(bspl, s, N_red, r, Pr_1s);
    std::vector<double> eval_2s_coeffs = get_expansion_coeffs(eval_2s.mat, 1);
    std::vector<double> Pr_2s = vec_radial_wavefunction(eval_2s_coeffs, bspl, r);
    output_1d_data(r, Pr_2s*Pr_2s, "B3_2s_states.txt");
    std::cout << "Hartree 2s energy: " << eval_2s.vec[1] << "au" << std::endl;
    MatrixAndVector eval_2p = solve_schrodinger_hartree(bspl, p, N_red, r, Pr_1s);
    std::vector<double> eval_2p_coeffs = get_expansion_coeffs(eval_2p.mat, 0);
    std::vector<double> Pr_2p = vec_radial_wavefunction(eval_2p_coeffs, bspl, r);
    output_1d_data(r, Pr_2p*Pr_2p, "B3_2p_states.txt");
    std::cout << "Hartree 2p energy: " << eval_2p.vec[0] << "au" << std::endl;

    double lifetime = state_lifetime(Pr_2s, r, Pr_2p);
    std::cout << "2p lifetime (Hartree): " << lifetime << "ns" << std::endl;
}

void part_four(){
    std::vector<double> Pr_1s = load_vector("Hartree-1s.txt");

}


int main(){
    // define our constants
    int N = 50;             // no. of B-splines
    double r0 = 1.e-5;      // starting value of integration grid
    double rmax = 50.;      // max val of integration grid
    int k_spline = 7;       // order of bspline

    // now create our integration grid
    int r_N = 3000;         // number of grid points
    std::vector<double> r(r_N);
    double step_size = (rmax - r0) / r_N; // essentially make a linspace from r0 to rmax
    for (int i = 0; i < r_N; i++){
        r[i] = r0 + i * step_size;
    }

    // make our bspline object to call on later
    BSpline bspl(k_spline, N, r0, rmax);

    int N_red = N - 3;  // we ignore the first 2 and last 1 bspline, so our matrices will have dimension N_red


    // std::cout << "Beginning part one: " << std::endl;
    // part_one(bspl, N_red, r);
    // std::cout << "Beginning part two: " << std::endl;
    // part_two(bspl, N_red, r);
    // std::cout << "Beginning part three: " << std::endl;
    // part_three(bspl, N_red, r);
    std::cout << "Beginning part four: " << std::endl;
    part_four();
    return 0;
}