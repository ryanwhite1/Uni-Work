#include <cmath>

double simpsons(int steps, double start, double end, double (*function)(double)){
    auto inv_transform = [](int steps, double start, double end, double (*function)(double)){
        // this implements the inverse transform for absolutely large bounds 
        // this requires that neither 'start' nor 'end' are zero.
        double AUC = 0;
        double stepsize = ((1 / start) - (1 / end)) / steps; // get step size of new bounds
        if (stepsize < 0) stepsize *= -1; // we want a positive step size 
        double x1, x2, midpoint, y1, y2, y3; // initialise values
        for (int i = 0; i < steps; i++){
            x1 = (1 / end) + stepsize * i; x2 = x1 + stepsize; midpoint = (x1 + x2) / 2; // get value of each required point
            // now work out the function values at each required point
            y1 = (1 / pow(x1, 2)) * function(1 / x1); 
            y2 = (1 / pow(midpoint, 2)) * function(1 / midpoint);
            y3 = (1 / pow(x2, 2)) * function(1 / x2);
            AUC += (stepsize / 6) * (y1 + 4 * y2 + y3); // add the AUC from this step iteration to the running AUC
        }
        return AUC;
    };
    auto normalAUC = [](int steps, double start, double end, double (*function)(double)){
        // this is the normal AUC method by Simpson's rule 
        // first, initialise variables
        double AUC = 0;
        double x1, x2, midpoint, y1, y2, y3;
        double stepsize = (end - start) / steps;
        for (int i = 0; i < steps; i++){
            x1 = start + stepsize * i; x2 = x1 + stepsize; midpoint = (x1 + x2) / 2; // get value of each required point
            y1 = function(x1); y2 = function(midpoint); y3 = function(x2); // compute function at each point
            AUC += (stepsize / 6) * (y1 + 4 * y2 + y3); // compute Simpson's rule and add it to cumulative AUC
        }
        return AUC;
    };
    double rollingAUC = 0;
    if (end > 1e10){ // b -> infty
        double new_end = 1e5; // make the new upper bound reasonably smaller
        if (-1e10 < start && start <= 0){ // we need to split the integral up into two
            int steps1 = 2 * steps / 3;
            int steps2 = steps - steps1;
            double mid_bound = 50;
            rollingAUC += normalAUC(steps1, start, mid_bound, function);
            rollingAUC += inv_transform(steps2, mid_bound, new_end, function);
        } else if (start < -1e10){ // a -> -infty, b -> infty
            double new_start = -1e6;
            int steps1 = steps / 6, steps2 = 2 * steps / 3, steps3 = steps - (steps1 + steps2);
            double lower = -50, upper = 50;
            rollingAUC += inv_transform(steps1, new_start, lower, function);
            rollingAUC += normalAUC(steps2, lower, upper, function);
            rollingAUC += inv_transform(steps3, upper, new_end, function);
        } else { // just a inverse transform simpson's
            rollingAUC += inv_transform(steps, start, new_end, function);
        }
    } else if (start < -1e10){ // a -> -infty
        double new_start = -1e3;
        if (end >= 0){ // we need to split the integral up into two
            double midpoint = -50; 
            int steps1 = steps / 3, steps2 = steps - steps1;
            rollingAUC += inv_transform(steps1, new_start, midpoint, function);
            rollingAUC += normalAUC(steps2, midpoint, end, function);
        } else{ // otherwise just a normal inverse transform
            rollingAUC += inv_transform(steps, new_start, end, function);
        }
    } else { // just a normal simpson's rule!
        rollingAUC += normalAUC(steps, start, end, function);
    }
    return rollingAUC;
}