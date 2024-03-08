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

void part_one(){
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


void part_two(){
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
}


int main(){
    // part_one();
    part_two();
    return 0;
}