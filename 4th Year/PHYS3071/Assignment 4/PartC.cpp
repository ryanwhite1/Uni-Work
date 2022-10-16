#include <vector>
#include <cmath>
#include <iostream>
#include <fstream>
#include <stdexcept>
#include <math.h>

std::vector<double> rddtC(std::vector<double> r, double G, double m){
    // this is the acceleration on a body at some distance from a gravitational source (in arbitrary units)
    std::vector<double> ddt = {0,0}; // initialise vector
    double radius = sqrt(pow(r[0], 2) + pow(r[1], 2)); // find radius from grav source
    ddt[0] = - G * m * r[0] / pow(radius, 3); // x component of accel
    ddt[1] = - G * m * r[1] / pow(radius, 3); // y component of accel
    return ddt;
}
double IVPa(double sep, double rad1, double rad2, double aEst, double G, double m) {
    // calculates the time it would take to get to the position at rad2 (starting at rad1 and separated by sep) given a semi-major axis of aEst
    // first, initialise relevant variables
    double c = sep;
    double s = (c + rad2 + rad1) / 2;
    double alpha = 2 * asin(sqrt(s / (2 * aEst))), beta = 2 * asin(sqrt((s - c) / (2 * aEst)));
    double dt = sqrt(pow(aEst, 3) / (G * m)) * (alpha - beta - (sin(alpha) - sin(beta))); // now calculate time to rad2
    return dt;
}
double fitnessFunctionC(double sep, double rad1, double rad2, double aEst, double dt, double G, double m) {
    // evaluates the accuracy of some semi-major axis by finding how well it matches the delta-time we need
    double aTime = IVPa(sep, rad1, rad2, aEst, G, m); // find time to reach rad2, starting at rad1
    double fitness = aTime - dt; // find how well it fits the observations
    return fitness;
}
double SemiMajorShooting(double sep, double rad1, double rad2, double dt, double G, double m, double tol) {
    // find the optimal semi-major axis of the orbit with a shooting method on the BVP
    double previous = INFINITY, current = (sep + rad1 + rad2) / 4; // set initial guess "current" to the minimimum possible semi-major axis
    double upper, lower, CurrentFit;
    if (fitnessFunctionC(sep, rad1, rad2, current, dt, G, m) < 0){ // if initial guess gives a too small semi-major axis
        upper = rad1; // set the init radius as the upper bound
        while (fitnessFunctionC(sep, rad1, rad2, upper, dt, G, m) < 0) {
            upper *= 2; // make the upper bound bigger until it is too big
        }
        lower = current;
    } else{ // else if the initial guess gives a bigger than needed semi-major axis
        lower = rad1; // set lower bound to the initial radius
        while (fitnessFunctionC(sep, rad1, rad2, lower, dt, G, m) > 0) {
            lower /= 2; // half the lower bound until its too small 
        }
        upper = current;
    }
    while (std::abs(previous - current) > tol){ // now to perform bisection until we have a good semi-major axis
        previous = current;
        current = (lower + upper) / 2;
        CurrentFit = fitnessFunctionC(sep, rad1, rad2, current, dt, G, m); // evaluate fit of current guess
        if (CurrentFit == 0){
            return current; // good guess!
        } else if (CurrentFit * fitnessFunctionC(sep, rad1, rad2, upper, dt, G, m) > 0){ // i.e. if upper and current have same sign
            upper = current;
        } else { //(fitnessFunction(initRad, current, G, m) * fitnessFunction(initRad, lower, G, m) > 0) // if lower and current have same sign
            lower = current;
        }
    }
    return current;
}

double cot(double x){
    // just the cot(x) function, since it doesnt seem to be in <cmath>
    double y = cos(x) / sin(x);
    return y;
}

std::vector<double> initVel(double sep, double rad1, double rad2, std::vector<double> Pos1, std::vector<double> Pos2, double a, double G, double m){
    // this is used to find the velocity of the comet at the initial point, given the two positions and the semi-major axis
    double c = sep;
    // the below creates some needed unit vectors
    std::vector<double> u1 = {Pos1[0] / rad1, Pos1[1] / rad1}, u2 = {Pos2[0] / rad2, Pos2[1] / rad2}, uc = {(Pos2[0] - Pos1[0])/c, (Pos2[1] - Pos1[1])/c};
    // now calculate some required variables
    double s = (c + rad2 + rad1) / 2;
    double alpha = 2 * asin(sqrt(s / (2 * a))), beta = 2 * asin(sqrt((s - c) / (2 * a)));
    double A = sqrt(G * m / (4 * a)) * cot(alpha / 2), B = sqrt(G * m / (4 * a)) * cot(beta / 2);
    std::vector<double> vel = {(B + A)*uc[0] + (B - A)*u1[0], (B + A)*uc[1] + (B - A)*u1[1]}; // calculate velocity vector
    return vel;
}

void orbitStep(std::vector<double> &rad, std::vector<double> &vel, double dt, double G, double m) {
    // iterates the orbit of the comet to the next point in time (and its velocity vector too!)
    // r' = r + v dt
    rad[0] = rad[0] + vel[0] * dt;
    rad[1] = rad[1] + vel[1] * dt;
    // v = v + a dt
    std::vector<double> accel = rddtC(rad, G, m);
    vel[0] = vel[0] + accel[0] * dt;
    vel[1] = vel[1] + accel[1] * dt;
}

std::vector<double> orbitParams(std::vector<double> initPos, std::vector<double> initVel, int steps, double time, double G, double m){
    // this function saves the timeseries positions to a file, and also estimates some parameters about the orbit
    std::vector<double> position = {initPos[0], initPos[1]}, vel = {initVel[0], initVel[1]};
    double min = sqrt(pow(initPos[0], 2) + pow(initPos[1], 2)), max = sqrt(pow(initPos[0], 2) + pow(initPos[1], 2)); // initialise minimum and maximum variables based off of init pos
    double dt = time / steps, radius;
    std::ofstream outputFile; // initialise output file
    outputFile.open("Q1c.dat");
    for (int i=0; i < steps; i++){ // now to move the comet about its orbit
        outputFile << position[0] << " " << position[1] << std::endl;
        radius = sqrt(pow(position[0], 2) + pow(position[1], 2)); // calculate radius at current time
        if (radius < min){ 
            min = radius; // update minimum orbital radius
        } else if (radius > max){
            max = radius; // update maximum orbital radius
        }
        orbitStep(position, vel, dt, G, m); // iterate to the next step in the orbit
    }
    outputFile.close();
    std::vector<double> params = {min, max}; // put the perigee and apogee into a vector to output
    return params;
}

std::vector<double> Q1c(double sep, double rad1, double rad2, double dt, std::vector<double> Pos1, std::vector<double> Pos2, double G, double m, double tol){
    double a = SemiMajorShooting(sep, rad1, rad2, dt, G, m, tol); // estimate optimal value of semi-major axis for the orbit
    std::vector<double> vel = initVel(sep, rad1, rad2, Pos1, Pos2, a, G, m); // calculate initial velocity vector of comet at t_1
    std::vector<double> extrema = orbitParams(Pos1, vel, 100000, 100, G, m); // calculate perigee/apogee
    double eccentricity = (extrema[1] - extrema[0]) / (extrema[1] + extrema[0]); // calculate eccentricity of orbit based on apogee/perigee
    std::vector<double> params = {a, eccentricity, extrema[0], extrema[1]}; // a, eccentricity, min, max
    return params;
}
