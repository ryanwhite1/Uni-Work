#include <vector>
#include <cmath>
#include <iostream>
#include <fstream>
#include <stdexcept>
#include <math.h>

std::vector<double> rddt(std::vector<double> r, double G, double m){
    // this is the acceleration on a body at some distance from a gravitational source (in arbitrary units)
    std::vector<double> ddt = {0,0}; // initialise vector
    double radius = sqrt(pow(r[0], 2) + pow(r[1], 2)); // find radius from grav source
    ddt[0] = - G * m * r[0] / pow(radius, 3); // x component of accel
    ddt[1] = - G * m * r[1] / pow(radius, 3); // y component of accel
    return ddt;
}

void systemOfEquations(std::vector<double> &rad, std::vector<double> &vel, double dt, double G, double m) {
    // this is the iteration step on our position and velocity
    // r' = r + v dt 
    rad[0] = rad[0] + vel[0] * dt;
    rad[1] = rad[1] + vel[1] * dt;
    // v = v + a dt
    std::vector<double> accel = rddt(rad, G, m);
    vel[0] = vel[0] + accel[0] * dt;
    vel[1] = vel[1] + accel[1] * dt;
}
std::vector<double> IVPSolver(double velMag, double radius, int steps, double G, double m) {
    // this iterates the system of equations over the required time for a circular orbit at the input velocity and radius
    double t = 2 * M_PI * radius / velMag; // calculate the required time for a circular orbit at this radius and velocity
    double dt = t / steps; // the time step required
    std::vector<double> position = {radius, 0}; // initalise position vector. Arbitrarily set to (rad, 0) (i.e. init pos at positive x)
    std::vector<double> velocity = {0, velMag}; // initalise velocity vector. Arbitrarily set to (0, vel) (i.e. motion strictly in y direction)
    for (int i = 0; i < steps; i++){ // now let's iterate the system
        systemOfEquations(position, velocity, dt, G, m);
    }
    return position;
}
double fitnessFunction(double radius, double vel, double G, double m) {
    // function that evaluates how good the estimate is. Values close to 0 are good!
    std::vector<double> position = IVPSolver(vel, radius, 100000, G, m); // get position of particle after appropriate time
    double fitness = sqrt(pow(position[0], 2) + pow(position[1], 2)) - radius; // subtract particle radius from ideal radius
    return fitness;
}
double BVPShooting(double initRad, double initVel, double tol, double G, double m) {
    // shooting method for this BVP. Take desired radius, initial guess of velocity, and a tolerance
    double previous = INFINITY, current = initVel;
    double temp = 0;
    double upper, lower, CurrentFit;
    // first estimate some suitable upper/lower bounds for the bisection
    if (fitnessFunction(initRad, initVel, G, m) < 0){ // if initial guess gives a smaller than needed velocity
        upper = sqrt(2 * G * m / initRad); // set to a known positive, large number - escape velocity
        lower = current;
    } else{ // else if the initial guess gives a bigger than needed velocity
        lower = 0.0001; // set to a really small velocity
        upper = current;
    }
    // now perform bisection to find correct velocity
    while (std::abs(previous - current) > tol){
        previous = current;
        current = (lower + upper) / 2; // bisection step
        CurrentFit = fitnessFunction(initRad, current, G, m); // evaluate how good the current guess is
        if (CurrentFit == 0){ // we have a perfect fit!
            return current; 
        } else if (CurrentFit * fitnessFunction(initRad, upper, G, m) > 0){ // i.e. if upper and current have same sign
            upper = current; // set current guess as upper bound
        } else { // CurrentFit * fitnessFunction(initRad, lower, G, m) > 0) // if lower and current have same sign
            lower = current; // set current guess as lower bound
        }
    }
    return current;
}

void plotOrbit(double radius, double velMag, int steps, double G, double m){
    // plots the circular orbit of radius and velocity
    std::vector<double> position = {0, radius}, vel = {velMag, 0}; // initialise vectors
    double time = 2 * M_PI * radius / velMag; // calculate time needed for orbit
    double dt = time / steps; // size of time steps
    std::ofstream outputFile; // initialise output file
    outputFile.open("Q1b.dat");
    for (int i=0; i < steps; i++){
        outputFile << position[0] << " " << position[1] << std::endl; // write position of particle to file
        systemOfEquations(position, vel, dt, G, m); // calculate next position
    }
    outputFile.close();
}

double Q1b(double radius, double velGuess, double G, double m, double tol){
    double velocity = BVPShooting(radius, velGuess, tol, G, m); // find the velocity needed for a circular orbit given radius and init guess
    plotOrbit(radius, velocity, 10000, G, m); // plot the orbit once we've found velocity
    return velocity;
}
