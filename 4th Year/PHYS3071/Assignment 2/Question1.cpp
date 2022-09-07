#include <array>
#include <cmath>
#include <fstream>
#include <iostream>
#include "SimpsonsRule.cpp"
#include <vector>

// Below are the 0 to 3 order Schrodinger equation solutions in terms of x
double Schrodinger0(double x){
    // Solution for the schrodinger equation with 0 degree Hermite polynomial
    double omega = 1, mass = 9.11e-31, hbar = 1.055e-34, alpha = omega * mass / hbar;
    double result = 1 * exp(-alpha * pow(x, 2) / 2);
    return result;
}
double Schrodinger1(double x){
    // Solution for the schrodinger equation with 1 degree Hermite polynomial
    double omega = 1, mass = 9.11e-31, hbar = 1.055e-34, alpha = omega * mass / hbar;
    double result = (2 * x * pow(alpha, 0.5)) * exp(-alpha * pow(x, 2) / 2);
    return result;
}
double Schrodinger2(double x){
    // Solution for the schrodinger equation with 2 degree Hermite polynomial
    double omega = 1, mass = 9.11e-31, hbar = 1.055e-34, alpha = omega * mass / hbar;
    double result = (4 * pow(x * pow(alpha, 0.5), 2) - 2) * exp(-alpha * pow(x, 2) / 2);
    return result;
}
double Schrodinger3(double x){
    // Solution for the schrodinger equation with 3 degree Hermite polynomial
    double omega = 1, mass = 9.11e-31, hbar = 1.055e-34, alpha = omega * mass / hbar;
    double result = (8 * pow(x * pow(alpha, 0.5), 3) - 12 * x * pow(alpha, 0.5)) * exp(-alpha * pow(x, 2) / 2);
    return result;
}

// Below are the 0 to 3 order paraxial wave equation solutions in terms of x
double Parax0(double x){
    return 1 * exp(-1 * pow(x, 2));
}
double Parax1(double x){
    return 2 * sqrt(2) * x * exp(-1 * pow(x, 2));
}
double Parax2(double x){
    return (8 * pow(x, 2) - 2) * exp(-1 * pow(x, 2));
}
double Parax3(double x){
    return (16 * sqrt(2) * pow(x, 3) - 12 * sqrt(2) * x) * exp(-1 * pow(x, 2));
}

double question1a(int steps, double lower, double upper, int order){
    // initialise constant values
    double omega = 1, mass = 9.11e-31, hbar = 1.055e-34, alpha = omega * mass / hbar;
    double val = 0;
    // the below statements choose which equation to look at based off of the desired hermite polynomial order
    if (order == 0){
        val = simpsons(steps, lower, upper, Schrodinger0);
    } else if (order == 1){
        val = simpsons(steps, lower, upper, Schrodinger1);
    } else if (order == 2){
        val = simpsons(steps, lower, upper, Schrodinger2);
    } else {    // must be of order 3
        val = simpsons(steps, lower, upper, Schrodinger3);
    }
    return val;
}

double question1b(int m, int n){
    // functionally identical to function question1a(), except in terms of the paraxial equations and accounting for two orders m and n
    double xint = 0, yint = 0;
    if (m == 0){
        xint = simpsons(1e6, -10, 10, Parax0);
    } else if (m == 1){
        xint = simpsons(1e6, -10, 10, Parax1);
    } else if (m == 2){
        xint = simpsons(1e6, -10, 10, Parax2);
    } else {    // m must be 3
        xint = simpsons(1e6, -10, 10, Parax3);
    }
    if (n == 0){
        yint = simpsons(1e6, -10, 10, Parax0);
    } else if (n == 1){
        yint = simpsons(1e6, -10, 10, Parax1);
    } else if (n == 2){
        yint = simpsons(1e6, -10, 10, Parax2);
    } else {    // n must be 3
        yint = simpsons(1e6, -10, 10, Parax3);
    }
    return xint * yint;
}


void question1(){
    // generate and store data for the solution to the schrodinger equation over ranges of step sizes, integral bounds, and hermite polynomial order
    double value = 0, error = 0, actual = 0;
    std::ofstream outputFile;
    outputFile.open("Q1a-Results.txt");
    outputFile << "Order | Stepsize (1eX) | Bounds (1eX) | Integral | Error | NormConst " << std::endl;
    for (int i = 0; i <= 3; i++){ // one solution for each x of order 0 to 3
        if (i == 0){
            actual = 0.0269747; // analytic solution
        } else if (i == 1){
            actual = 0; // analytic solution
        } else if (i == 2){
            actual = 0.0539494; // analytic solution
        } else {        // 3rd order
            actual = 0; // analytic solution
        }
        for (int steppow = 3; steppow < 7; steppow++){      // goes from 1e3 to 1e6 steps
            for (int boundpow = -6; boundpow < 11; boundpow++){         // goes from bounds of -1e-6 <= x <= 1e-6 up to -1e10 <= x <= 1e10
                value = question1a(pow(10, steppow), -1 * pow(10, boundpow), pow(10, boundpow), i);
                error = value - actual;
                outputFile << i << " | " << steppow << " | " << boundpow << " | " << value << " | " << error << " | " << 1 / value << std::endl;
            }
        }
    }
    outputFile.close();

    // now to generate and store data about the results of the 2d paraxial wave equation solutions
    outputFile.open("Q1b-Results.txt");
    outputFile << " m | n | NormConst" << std::endl;
    for (int m = 0; m <= 3; m++){ // one solution for each x of order 0 to 3
        for (int n = 0; n <= 3; n++){ // one solution for each y of order 0 to 3
            outputFile << m << " | " << n << " | " << 1 / question1b(m, n) << std::endl;
        }
    }
    outputFile.close();
}