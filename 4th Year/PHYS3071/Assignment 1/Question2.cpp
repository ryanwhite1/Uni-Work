#include "cubic_interpolation.cpp"
#include <iostream>
#include <fstream>
#include <string>
#include <array>
#include <vector>
#include <cmath>

double normalDist(double x, double mean, double sd){
    // this is just the normal distribution for some mean and standard deviation
    double y = exp(- pow((x - mean), 2) / (2 * pow(sd, 2))) / sqrt(2 * M_PI * pow(sd, 2));
    return y;
}

void question2(){
    // initialise constants
    const int datalen = 10, interpPoints = 100;  // the number of data points (datalen) is 10. interpPoints is the number of points to interpolate
    const double start = -2, end = 2;
    std::array<double, datalen> xdata = {0}, ydata = {0};

    std::ifstream dataFile;
    dataFile.open("exp-model-distribution.dat");
    int i = 0;
    double col1, col2;
    // now, write the data from file into two arrays so we can use it in the program
    while(dataFile) {
        dataFile >> col1 >> col2;
        if (i < 10){
            xdata[i] = col1;
            ydata[i] = col2;
        }
        i += 1;
    }
    dataFile.close();

    std::array<double, datalen> d2y = {0}; // initialise double derivative array
    cspline_init(xdata, ydata, d2y); // estimate double derivatives from the interpolation file
    std::array<double, interpPoints> x_interp = {0}, y_interp = {0}; // initialise arrays
    for (int i = 0; i < interpPoints; i++){
        x_interp[i] = start + ((end - start) / interpPoints) * i; // calculate the x value position
        y_interp[i] = cspline_interp(xdata, ydata, d2y, x_interp[i]); // infer interpolated y value at this x value
    }

    std::ofstream outputFile;
    outputFile.open("Q2Interp.dat");
    // write the interpolated data to a file
    for (int i = 0; i < interpPoints; i++){
        outputFile << x_interp[i] << " " << y_interp[i] << std::endl;
    }
    outputFile.close();
    // now we need to estimate the mean and standard deviation
    // the mean will be at the peak of the distribution, so we need to find the max
    double max = y_interp[0]; int mean_loc = 0; // initialise variables
    for (int i = 0; i < interpPoints; i++){
        if (y_interp[i] > max){ // if the current y value is bigger than the previously defined maximum
            max = y_interp[i]; // set this as the new maximum
            mean_loc = i; // and update the location of the maximum
        }
    }
    double mean_est = x_interp[mean_loc];
    double sd_est = 1 / (max * sqrt(2 * M_PI)); // the mean occurs when the exp term is 0, so can rearrange the normal dist formula to find the s.d. given the maximum
    // now generate data with better sampling, and calculate the residuals of the interpolated data
    std::array<double, interpPoints> accurate_y = {0}, residuals = {0}; // initialise arrays
    for (int i = 0; i < interpPoints; i++){
        accurate_y[i] = normalDist(x_interp[i], mean_est, sd_est); // calculate y value of higher sampled data
        residuals[i] = y_interp[i] - accurate_y[i]; // calculate residuals of the interpolated vs model
    }
    // now write both the higher sampled data to file...
    outputFile.open("Q2HighSampled.dat");
    for (int i = 0; i < interpPoints; i++){
        outputFile << x_interp[i] << " " << accurate_y[i] << std::endl;
    }
    outputFile.close();
    // and the residuals to file.
    outputFile.open("Q2Residuals.dat");
    for (int i = 0; i < interpPoints; i++){
        outputFile << x_interp[i] << " " << residuals[i] << std::endl;
    }
    outputFile.close();
    
}