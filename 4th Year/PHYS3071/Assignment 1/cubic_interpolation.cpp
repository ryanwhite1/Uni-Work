//Cubic spline interpolation code roughly following Numerical Recipes.
//Pat Scott Aug 5 2021. Material made for PHYS3071/PHYS7073.

//Salted by Alex Stilgoe 2022 to remove functionality to make it a bug fixing task.
//This is an example of using C-style arrays which I do NOT recommend! -A.S. 2022

#include <iostream>
#include <array>
#include <cstdlib>


// Precompute a couple of constants to help compiler with optimisation
const double third = 1.0/3.0;
const double sixth = 1.0/6.0;

// Tridiagonal matrix solver helper function definition
template <size_t n>
void tridag(std::array<double, n> &a, std::array<double, n> &b, std::array<double, n> &c, std::array<double, n> &r, std::array<double, n> &u){
	double bet;
    std::array<double, n> gam = {0};

	// Make sure the system is well formed
	if (b[0] == 0){
		std::cout << "tridag: rewrite equations" << std::endl;
		exit(1);
	}

	// Solve
	bet = b[0];
	u[0] = r[0] / bet;
	// Decompose and forward substitute
	// Alex Stilgoe: This loop may work despite being in the dangerzone!
	for (int j = 1; j < n; j++){
        gam[j] = c[j-1] / bet;
        bet = b[j] - a[j] * gam[j];
        if (bet == 0){
          std::cout << "tridag failed" << std::endl;
          exit(1);
        }
        u[j] = (r[j] - a[j] * u[j-1]) / bet;
	}
	// Backsubstitute
	for (int j = n-2; j >= 0; j--){
        u[j] = u[j] - gam[j+1] * u[j+1];
    }
}

// Cubic spline initialisation function (natural spline boundary conditions only)
// Input:
//  x        = abcissae/independent values (must be monotonically increasing)
//  y        = dependent values
//  n        = dimension of x and y arrays
// Output:
//  d2y      = second derivatives d^2y/dx^2
template <size_t n>
void cspline_init(std::array<double, n> x, std::array<double, n> y, std::array<double, n> &d2y){
	// Internal temporary variables
    std::array<double, n> a={0}, b={0}, c={0}, F={0};

	//These should never be required, but we'll initialise them just in case.
    a.at(0) = 0.0;
    c.at(n-1) = 0.0;

	//Implement boundary conditions for natural splines
	b[0] = 1;
	c[0] = 0;
	F[0] = 0;
	a[n-1] = 0;
	b[n-1] = 1;
	F[n-1] = 0;

	// Set the tridiagonal matix and solution vector entries for the interior points.
	// Remember that array indices start at 0 in C/C++, so we
	// need to use index 0 for j=1 in the lectures/assignment, and so on.
	for (int j = 1; j < n-1; j++){
		a[j] = sixth * (x[j]   - x[j-1]);
		b[j] = third * (x[j+1] - x[j-1]);
		c[j] = sixth * (x[j+1] - x[j]);
		F[j] = (y[j+1] - y[j]) / (x[j+1] - x[j]) - (y[j] - y[j-1]) / (x[j] - x[j-1]);
	}

	// Invert the matrix and find the second derivatives
	tridag(a, b, c, F, d2y);
}

// Cubic spline evaluation function
//Input:
// x                  = abcissae/independent values (as in call to cspline_init)
// y                  = dependent values (as in call to cspline_init)
// n                  = dimension of x and y arrays (as in call to cspline_init)
// d2y                = second derivatives d^2y/dx^2 (as output by cspline_init)
// xval               = value of abcissa at which the function is to be evaluated
//Output:
// cspline_interp     = interpolated value of the function at xval
template <size_t n>
double cspline_interp(std::array<double, n> &x, std::array<double, n> &y, std::array<double, n> &d2y, double xval){
    //Find the correct interval to work with, between indices j and j+1, using bisection
    int jlow = 0;
    int jhigh = n - 1;
    int j;
    while (jhigh - jlow > 1){
		j = (jhigh + jlow) >> 1;
		if (x[j] > xval) jhigh = j;
		else jlow = j;
    }
    double xj = x[jlow];
    double xjplus1 = x[jhigh];

    //Calculate the coefficients
    double diff = xjplus1 - xj;
    if (diff == 0){
		std::cout << "Error in cspline_interp: abcissa must be strictly increasing" << std::endl;
		exit(1);
    }
    double A = (xjplus1 - xval) / diff;
    double B = 1 - A;
    double Cprime = A * (A * A - 1);
    double Dprime = B * (B * B - 1);

    //Calculate the function value
    return A * y[jlow] + B * y[jhigh] + sixth * diff * diff * (Cprime * d2y[jlow] + Dprime * d2y[jhigh]);
}

