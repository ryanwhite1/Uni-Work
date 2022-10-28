#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <string>
#include <complex>
#include <stdexcept>

typedef std::complex<double> complex;

void tridag(std::vector<complex> &a, std::vector<complex> &b, std::vector<complex> &c, std::vector<complex> &r, std::vector<complex> &u){
    // r is state vector, u is solution vector
    // a, b, c are diagonals of the tridiag matrix
	complex bet;
    std::vector<complex> gam(r.size(), 0);

	// Make sure the system is well formed
	if (b[0].real() == 0 && b[0].imag() == 0){
		std::cout << "tridag: rewrite equations" << std::endl;
		exit(1);
	}

	// Solve
	bet = b[0];
	u[0] = r[0] / bet;
	// Decompose and forward substitute
	// Alex Stilgoe: This loop may work despite being in the dangerzone!
	for (int k = 1; k < r.size(); k++){
        gam[k] = c[k-1] / bet;
        bet = b[k] - a[k] * gam[k];
        if (bet.real() == 0 && bet.imag() == 0){
          std::cout << "tridag failed" << std::endl;
          exit(1);
        }
        u[k] = (r[k] - a[k] * u[k-1]) / bet;
	}
	// Backsubstitute
	for (int k = r.size()-2; k >= 0; k--){
        u[k] = u[k] - gam[k+1] * u[k+1];
    }
}

std::vector<double> linspace(double start, double end, int steps){
    // this returns a linearly space vector from the start to end number, with desired number of steps
    double dx = (end - start) / (steps - 1);
    std::vector<double> vals(steps, 0);
    vals[0] = start;
    for (int i = 1; i < steps; i++){
        vals[i] = vals[i-1] + dx;
    }
    return vals;
}

std::vector<complex> g0initialstate(std::vector<double> x){
    // this is a gaussian initial state function (in the reals) for the wave function, psi(x, 0) = e^(-x^2)
    int xsize = x.size();
    std::vector<complex> initialstate(xsize, 0);
    double N = 0.893244; // normalisation constant, calculated via wolfram alpha integration over all the reals
    for (int i = 0; i < xsize; i++){
        initialstate[i] = {N * exp(-pow(x[i], 2)), 0};
    }
    return initialstate;
}

double potential(double x, double hbar, double m){
    // this is a quadratic potential for the wave function
    double V = 2 * hbar * hbar * x * x / m;
    return V;
}

void crank(std::vector<double> x, std::vector<double> t, std::vector<complex> statevec, std::string filename, double g){
    // start by initialising variables needed for the simulation
    double hbar = 1, m = 0.5, Bbound = 1e-5;
    double dx = x[1] - x[0], dx2 = pow(dx, 2);
    double dt = t[1] - t[0];
    int xsteps = x.size(), timesteps = t.size(); // this is the resolution of the parameter space
    complex a{0, hbar * dt / (2 * m * dx2)}, b{0, dt / hbar}; // these are the constant coefficients for the Schrodinger Crank-Nicholson scheme
    std::vector<complex> B(xsteps, {0, 0}), A(xsteps, -a), C(xsteps, -a); // initialise the coefficients in the tridiag matrix, one for each diagonal

    // now, populate the middle diagonal (B), and set the boundary conditions for all of the diagonals
    for (int i = 0; i < xsteps; i++){
        B[i] = 2. * a + b * (potential(x[i], hbar, m) + g * std::norm(statevec[i]));
    }
    A[0] = {0, 0}; A[xsteps-1] = {0, 0}; 
    // B[0] = {Bbound, Bbound}; B[xsteps - 1] = {Bbound, Bbound};
    C[0] = {0, 0}; C[xsteps-1] = {0, 0};

    // now, create vectors vVec = (I + dt/2 * M), and diag = (1 - dt/2 * M)
    std::vector<complex> vVec(xsteps, {0, 0});
    std::vector<complex> vVecA(xsteps, {0, 0}), vVecB(xsteps, {0, 0}), vVecC(xsteps, {0, 0});
    std::vector<complex> diagA(xsteps, {0, 0}), diagB(xsteps, {0, 0}), diagC(xsteps, {0, 0});
    for (int i = 0; i < xsteps; i++){
        vVecA[i] = (dt / 2) * A[i]; diagA[i] = - (dt / 2) * A[i];
        vVecB[i] = 1. + (dt / 2) * B[i]; diagB[i] = 1. - (dt / 2) * B[i];
        vVecC[i] = (dt / 2) * C[i]; diagC[i] = - (dt / 2) * C[i];
    }

    // now, open the data file and check if it opened correctly. 
    std::ofstream outputFile;
    outputFile.open(filename);
    if (!outputFile){
        throw std::runtime_error("Data output file not opened correctly. Check that the file exists.");
    }
    
    // finally, we're ready for the crank nicholson over the time space
    for (int i = 0; i < timesteps; i++){
        if (g != 0 && i != 0){  // now change the value of B if g =/= 0, and we're not on the first iteration of the loop
            for (int k = 0; k < xsteps; k++){
                if (k == 0 || k == xsteps - 1) {
                    // B[k] = {Bbound, Bbound};
                    B[k] = 2. * a + b * (potential(x[k], hbar, m) + g * std::norm(statevec[k]));
                } else {
                    B[k] = 2. * a + b * (potential(x[k], hbar, m) + g * std::norm(statevec[k]));
                }
                vVecB[k] = 1. + (dt / 2) * B[k]; diagB[k] = 1. - (dt / 2) * B[k];
            }
        }
        for (int j = 0; j < xsteps; j++){
            outputFile << t[i] << " " << x[j] << " " << std::norm(statevec[j]) << std::endl; // output time/x/probability data to file
            // now perform matrix multiplication, for V = (I + dt/2 * M) * U_i
            if (j == 0){
                vVec[j] = vVecB[j] * statevec[j] + vVecC[j] * statevec[j+1];
            } else if (j == xsteps - 1){
                vVec[j] = vVecA[j] * statevec[j-1] + vVecB[j] * statevec[j];
            } else {
                vVec[j] = vVecA[j] * statevec[j-1] + vVecB[j] * statevec[j] + vVecC[j] * statevec[j+1];
            }
        }
        tridag(diagA, diagB, diagC, vVec, statevec); // now the tridiag, which solves U_(i+1) = (I - dt/2 * M) * V
    }
    outputFile.close();
}

void partA(int xsteps, int timesteps){
    // start by initialising the parameter space
    std::vector<double> x = linspace(-4, 4, xsteps), t = linspace(0, M_PI / 2, timesteps);
    std::vector<complex> statevec = g0initialstate(x); // now initialise the initial state (all along x at t=0)
    std::string filename = "PartA.dat"; // this is the file to save data to
    crank(x, t, statevec, filename, 0.); // now perform crank nicholson over the duration
}

void partB(int xsteps, int timesteps){
    // start by initialising the parameter space
    std::vector<double> x = linspace(-4, 4, xsteps), t = linspace(0, M_PI / 2, timesteps);
    std::vector<complex> statevec(xsteps, 0);
    double hbar = 1, p = 2 * hbar, N = 0.76017; // our momentum and normalisation constant
    complex j{0, 0};
    // now initialise the initial state (all along x at t=0)
    for (int i = 0; i < xsteps; i++){
        j = {cos(p * x[i] / hbar), sin(p * x[i] / hbar)}; // this is the x + iy version of e^(-x^2 + ipx / hbar)
        statevec[i] = exp(- pow(x[i], 2)) * j * N;
    }
    std::string filename = "PartB.dat"; // this is the file to save data to
    crank(x, t, statevec, filename, 0); // now perform crank nicholson over the duration
}

void partC(int xsteps, int timesteps){
    // start by initialising the parameter space
    std::vector<double> x = linspace(-4, 4, xsteps), t = linspace(0, M_PI / 2, timesteps);
    std::vector<complex> statevec = g0initialstate(x); // now initialise the initial state (all along x at t=0)
    std::string filename = "PartC.dat"; // this is the file to save data to
    crank(x, t, statevec, filename, 30.); // now perform crank nicholson over the duration
}

int main(){
    // this will run all of parts A through C for the same parameter space and steps
    int xsteps = 100, timesteps = 1000;
    partA(xsteps, timesteps);
    partB(xsteps, timesteps);
    partC(xsteps, timesteps);
    return 0;
}