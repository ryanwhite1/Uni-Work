#include <array>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>

std::array<int, 2> randomwalk(int seed){
    // Random walk on a discrete grid. The walker will go 1 step up, down, left, or right. 
    std::mt19937 generator;
    generator.seed(seed);
    std::uniform_real_distribution<double> distribution(0.0, 1.0);
    double value = distribution(generator); // generate a uniform RV between 0 and 1
    std::array<int, 2> deltaCoords = {0}; // initialise array to store delta coordinates
    if (value <= 0.25){
        deltaCoords[0] += -1; // go left
    } if (0.25 < value && value <= 0.5){
        deltaCoords[0] += 1; // go right
    } if (0.5 < value && value <= 0.75){
        deltaCoords[1] += -1; // go down
    } if (0.75 < value && value <= 1){
        deltaCoords[1] += 1; // go up
    }
    return deltaCoords;
}

void question2a(){
    // initialise values and arrays
    const int steps = 50, runs = 400;
    const int initx = 0, inity = 0;
    std::array<int, 2> deltaCoords = {0};
    std::array<int, runs> squareDisplacement = {0};
    std::array<double, runs> aveVelocity = {0}, finalAngle = {0};
    double xy[2][steps * runs] = {0};
    double runTotDispl = 0;     // running total displacement
    double minx = 0, maxx = 0, miny = 0, maxy = 0;
    int index;

    std::ofstream outputFile;

    for (int i = 0; i < runs; i++){
        int x = initx, y = inity; // set the walker back to the origin
        for (int j=0; j < steps; j++){
            index = (i * steps) + j; // current index of *all* steps across *all* walks

            deltaCoords = randomwalk(index); // generate delta coordinates
            x += deltaCoords[0]; y += deltaCoords[1]; // move walker by delta coordinates
            xy[0][index] = x; xy[1][index] = y;

            // the below keeps a record of the max/min x and y values (to appropriately write the data to file later)
            if (x < minx) minx = x; if (x > maxx) maxx = x;
            if (y < miny) miny = y; if (y > maxy) maxy = y;
        }
        squareDisplacement[i] = pow(x, 2) + pow(y, 2);
        aveVelocity[i] = pow(squareDisplacement[i], 0.5) / steps;
        runTotDispl += squareDisplacement[i];
    }

    // now to write the grid data to file
    int z;
    outputFile.open("2a-XYZ.dat");
    for (int i = minx; i <= maxx; i++){ // loop over all x values
        for (int j = miny; j <= maxy; j++){ // loop over all y values
            z = 0;
            for (int k = 0; k < steps * runs; k++){     // this for loop finds how many times a walker has been in the (i, j) grid position
                if (xy[0][k] == i){
                    if (xy[1][k] == j) z += 1;  // increment frequency by 1
                }
            }
            outputFile << i << " " << j << " " << z << std::endl; // write x, y, and frequency to file
            z = 0;
        }
    }
    outputFile.close();

    // now to calculate statistical properties of random walks
    int runningX = 0, runningY = 0;
    for (int k = 0; k < steps * runs; k++){
        runningX += xy[0][k]; runningY += xy[1][k]; // gets cumulative total of all X and Y values
    }
    double meanX = runningX / (steps * runs), meanY = runningY / (steps * runs); // calculate X and Y mean vals
    double SDX = 0, SDY = 0;
    for (int k = 0; k < steps * runs; k++){
        SDX += pow((xy[0][k] - meanX), 2); SDY += pow((xy[1][k] - meanY), 2); 
    }
    SDX = pow(SDX / (steps * runs), 0.5);
    SDY = pow(SDY / (steps * runs), 0.5);
    double AverageVelocity = 0;
    for (int i = 0; i < runs; i++) AverageVelocity += aveVelocity[i];
    AverageVelocity = AverageVelocity / runs;

    // now to write the data to a file
    outputFile.open("2aResults.txt");
    outputFile << "MSD = " << runTotDispl / runs << std::endl;    // mean square displacement
    outputFile << "Mean X = " << meanX << std::endl;
    outputFile << "Mean Y = " << meanY << std::endl;
    outputFile << "Std Dev X = " << SDX << std::endl;
    outputFile << "Std Dev Y = " << SDY << std::endl;
    outputFile << "Average speed of walkers across all " << runs << " runs is " << AverageVelocity << " units / step" << std::endl;
    outputFile.close();
}