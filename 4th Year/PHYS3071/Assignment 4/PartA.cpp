#include <vector>
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <math.h>

double RootHybridOffset(double (*fun)(double, double), double (*deriv)(double), double init, double tol, double offset){
    // this root finder takes a function, its derivative, and initial guess of the root, a tolerance and a vertical offset of the function
    double previous = INFINITY, current = init; // set current best guess to the initial guess, and the previous guess to infinity so that the while loop always starts
    double temp; // temp variable
    while (std::abs(previous - current) > tol){ // while the difference between previous and current guess is greater than some tolerance...
        previous = current;
        temp = current;
        try { // try newton's method of root finding
            current = current - (fun(current, offset) / deriv(current));
            if ((std::abs(current) == INFINITY) || (std::isnan(std::abs(current)))) { // if the guess escapes to infinity...
                std::cout << "Estimate escaped to infinity. Trying to solve..." << std::endl; // say that we've got a problem
                throw std::runtime_error("Escaped to infinity."); // throw an error and try to solve it with the catching method
            }
        } catch(std::runtime_error) { // if newton's method escaped to infinity, try with bisection
            int n = 0;
            double bisectBound = 0;
            while (n < 10){ // we want to bisect 10 times (arbitrarily) to get a better guess than we started with
                bisectBound = 0; // arbitrarily set the initial lower bound to 0
                while (fun(bisectBound, offset) * fun(temp, offset) > 0) { // if the function at the bisect bound and temp variable have the same sign...
                    if (bisectBound < 0){bisectBound -= 0.01;} // first get the bisect bound further away from 0
                    else {bisectBound += 0.01;}
                    bisectBound *= -1; // and then flip the sign
                }
                temp = (bisectBound + temp) / 2; // perform bisection step
                n += 1; // and increment the counter
            }
            current = temp; // we've found a better guess, now try the loop again with newton's method
        }
    }
    return current;
}

double func1(double x, double a){
    // this is the function y = sin(x)/x - a
    return (sin(x) / x) - a;
}
double func1dx(double x){
    return (cos(x) / x) + (- sin(x) / (x * x));
}
double func2(double x, double a){
    // this is the function y = (x - 1)*e^(-x^2) - a
    return (x - 1) * exp(- x * x) - a;
}
double func2dx(double x){
    return exp(-x * x) * (-2 * x*x + 2 * x + 1);
}
double func3(double x, double a){
    // this is the function y = 1/x - a
    return (1 / x) - a;
}
double func3dx(double x){
    return - 1 / (x * x);
}
double func4(double x, double a){
    // this is the function y = x^2 - a
    return x * x - a;
}
double func4dx(double x){
    return 2 * x;
}


void Q1a(int test){
    // parameter 'test' is 1 if testing the root finding over a range of init guesses, and 0 if root finding for one guess with useful output
    double a14 = 0.5, a2 = 0, a3 = 1; // these are the offsets we apply to each function 
    double root1, root2, root3, root4;
    if (test == 1){ // testing the functions
        std::cout << "Beginning testing of functions over range of possible initial guesses..." << std::endl;
        for (int i=-200; i <= 200; i++){ // test over the range of init guess from -200 to 200 in increments of 1
            root1 = RootHybridOffset(func1, func1dx, i, 0.001, a14);
            root2 = RootHybridOffset(func2, func2dx, i, 0.001, a2);
            root4 = RootHybridOffset(func4, func4dx, i, 0.001, a14);
        }
        for (int i = 1; i <= 200; i++){ // test over the range of 1/100 to 2 in increments of 1/100
            root3 = RootHybridOffset(func3, func3dx, i / 100, 0.001, a3);
        }
        std::cout << "Testing completed! Everything ok. " << std::endl;
    } else {
        // first find roots of all of the 4 functions
        root1 = RootHybridOffset(func1, func1dx, 2, 0.001, a14);
        root4 = RootHybridOffset(func4, func4dx, -1, 0.001, a14);
        root2 = RootHybridOffset(func2, func2dx, -10, 0.001, a2);
        root3 = RootHybridOffset(func3, func3dx, 0.1, 0.001, a3);
        // now output some useful text
        std::cout << "Function 1: for a = " << a14 << ", we arrive at a root of " << root1 << std::endl;
        std::cout << "Function 2: for a = " << a2 << ", we arrive at a root of " << root2 << std::endl;
        std::cout << "Function 3: for a = " << a3 << ", we arrive at a root of " << root3 << std::endl;
        std::cout << "Function 4: for a = " << a14 << ", we arrive at a root of " << root4 << std::endl;
    }
}