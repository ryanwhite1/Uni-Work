#include <vector>
#include <iostream>
#include "PartA.cpp"
#include "PartB.cpp"
#include "PartC.cpp"

int main(){
    // start by doing part A
    Q1a(1); // this tests the root finding over the range of parameters given in the report to make sure that it works
    Q1a(0); // this finds the roots and outputs a useful statement
    // now for part B of the question
    double initRad = 1;
    double vel = Q1b(1, 0.4, 1, 1, 0.00001);
    std::cout << "For a radius of " << initRad << ", we obtain a circular velocity of approx. " << vel << " units/time." << std::endl;
    // now for part C. We use the given initial position, and the calculated final position of the comet. 
    std::vector<double> initPos = {0, 1}, finPos = {0.4416, 0.2345};
    std::vector<double> CometParams = Q1c(0.884, 1, 0.5, 1, initPos, finPos, 1, 1, 0.001); // calculate a possible orbit and output the parameters.
    std::cout << "Found semi-major axis is = " << CometParams[0] << " units." << std::endl;
    std::cout << "Orbit has eccentricity of e = " << CometParams[1] << " with a perigee of " << std::endl;
    std::cout << CometParams[2] << " units, and apogee of " << CometParams[3] << " units." << std::endl;
    return 0;
}