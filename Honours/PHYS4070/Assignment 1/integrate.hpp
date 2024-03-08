# pragma once
# include <vector>
# include <cmath>
# include <iostream>
# include <cassert> // for assert(), used in matrix example
# include "bspline.hpp"
# include "matrix.hpp"
# include "linalgSolvers.hpp"

double trapezoid_area(double x1, double x2, double y1, double y2){
    // calculates the area of a single trapezoid
    return 0.5 * (y1 + y2) * fabs(x2 - x1);
}
double trapezoid_integration(std::vector<double> x, std::vector<double> y){
    // calculates the area under the curve (with the trapezoid rule) by points specified by (x,y)
    int N = x.size();
    double run_total = 0.;
    for (int i = 0; i < N-1; i++){
        run_total += trapezoid_area(x[i], x[i+1], y[i], y[i+1]);
    }
    return run_total;
}