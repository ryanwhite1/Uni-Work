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

    int r_N = 3000;
    std::vector<double> r(r_N);
    double step_size = (rmax - r0) / r_N;
    for (int i = 0; i < r_N; i++){
        r[i] = r0 + i * step_size;
    }

    BSpline bspl(k_spline, N, r0, rmax);

    int N_red = N - 3;
    int s = 0, p = 1;   // values of l for the different orbital states
    MatrixAndVector s_eval = solve_schrodinger(bspl, s, N_red, r);
    MatrixAndVector p_eval = solve_schrodinger(bspl, p, N_red, r);

    std::cout << "First 10 's' eigenstates:" << std::endl;
    s_eval.print_vector(10); // print first 10 elements in vector
    std::cout << "First 10 'p' eigenstates:" << std::endl;
    p_eval.print_vector(9); // print first 10 elements in vector

    std::cout << "Expectation for the s states:" << std::endl;
    for (int i = 0; i < 10; i++){
        std::vector<double> s_coeffs = get_expansion_coeffs(s_eval.mat, i);
        std::vector<double> s_Pr = vec_radial_wavefunction(s_coeffs, bspl, r);
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



int main(){
    part_one();
    return 0;
}