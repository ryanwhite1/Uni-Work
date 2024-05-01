#include <cmath>
#include <iostream>
#include <vector>
#include <omp.h>

double second_deriv(double (*func)(double), double x, double delta_x){
    // second derivative with the central difference method
    return (func(x + delta_x) - 2. * func(x) + func(x - delta_x)) / (delta_x * delta_x);
}
