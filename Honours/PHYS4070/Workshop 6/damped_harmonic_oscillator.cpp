#include <cmath>
#include <iostream>
#include <vector>

//--------------------------------------------------------------------------
// You can define function "declarations" (essentially "placeholders") at the
// top of the code, and then put the full definitions for those functions
// after "main()". 
// Equivalently, you can just put your main() function at the end, but this
// can look a bit messier.
//--------------------------------------------------------------------------

// Placeholder - operator overloading
std::ostream& operator<<(std::ostream& ostr, const std::vector<double>& vect);
//std::vector<double> operator*(double a, const std::vector<double> &b) ;
std::vector<double> operator*(double a, std::vector<double> b) ;
//std::vector<double> operator+(const std::vector<double> &a, const std::vector<double> &b);
std::vector<double> operator+(const std::vector<double> &a, const std::vector<double> &b);

// Placholder - ODE function
void ODE(std::vector<double> old_coords, std::vector<double> &kn); //outputs the result of the coupled system of ODEs

int main()
{
	//set up memory for gradient vector k1
	std::vector<double> k1(2,0);

	// Simulation parameters: step size, simulation length
	double dt = 0.1;
	int    N  = 1000;

	// Initial conditions of the simulation: position and velocity
	std::vector<double> coords(2,0); // x0, vx0
	coords.at(0) = 10; //x0
	coords.at(1) = 0;  //vx0

	// Output initial (time, position, velocity) to the console using the overloading of operator<< for std::vectors
	std::cout << 0.0 << '\t' << coords << std::endl;

	// Loop over timesteps
	for (int i=0; i<N; i++)
	{
        // Integration step - Euler method
		ODE(coords,k1);          // Calculate vector of gradients k1 using the system of ODEs ("f(X,t)" function)
		coords = coords + dt*k1; // Update the coordinates using the gradient k1

        // Print out: time, position, velocity
		std::cout << i*dt << '\t' << coords << std::endl;
	}

	return 0;

}

//Computes the derivative of the system of ODEs from old_coords and puts the result in kn.
void ODE(std::vector<double> old_coords, std::vector<double> &kn)
{
	//Set working values
	double x  = old_coords.at(0); // Previous x position
	double vx = old_coords.at(1); // Previous x velocity

    // Solve a damped harmonic oscillator:
    // m*dx^2/dt^2 + b*dx/dt + k*x = 0
    // with:
    // mass m=1.0
    // damping strength b=0.05
    // spring constant k=0.1

	// Coupled ODE equations:
	kn.at(0) = vx;
	kn.at(1) = (-0.1*x - 0.05*vx)/1.0;
}

// Takes the current output stream, ostr, and appends the content of a vector, vect, onto the end.
// Notice that if has the '&' at the front. This means it will CHANGE ostr at the
// memory level, i.e. it can't be undone.
std::ostream& operator<<(std::ostream& ostr, const std::vector<double> &vect)
{
	ostr << vect.at(0); // Output 0th element
	for (int i = 1; i < vect.size(); ++i) // Loop from 1 to size(vect)
	{
		ostr << '\t' << vect.at(i); // Output 1st, 2nd, 3rd, ... elements, with tab separators
 	}

	return ostr;
}

// Double * vector multiplication
// Makes a copy of the vector b, multiplies each element by a and then returns it back.
std::vector<double> operator*(const double a, std::vector<double> b) 
{
    // Loop over vector b
    for (double &bref_i : b) // Loop from 1 to size(b)
	{
		bref_i*=a;
	}

    return b;
}

// Makes a copy of vector b, adds each element of a to the copy of b and returns it back.
std::vector<double> operator+(const std::vector<double> &a, const std::vector<double> &b)
{
    // Initiate a new vector c
	std::vector<double> c(b);
    for (int i = 0; i < b.size(); ++i) // Loop from 1 to size(a)
	{
        // Add element-by-element
        c.at(i) = a.at(i) + b.at(i);
	}

	return c;
}