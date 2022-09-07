#include <array>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>


std::array<int, 2> randomwalk2b(int seed){
    // Random walk on a discrete grid. The walker will go 1 step up, down, left, or right. 
    std::mt19937 generator;
    generator.seed(seed);
    std::uniform_real_distribution<double> distribution(0.0, 1.0);
    double value = distribution(generator); // generate a uniform RV between 0 and 1
    std::array<int, 2> movement = {0}; // initialise array to store delta coordinates
    if (value <= 0.25){ 
        movement[0] += -1; // go left
    } if (0.25 < value && value <= 0.5){
        movement[0] += 1; // go right
    } if (0.5 < value && value <= 0.75){
        movement[1] += -1; // go down
    } if (0.75 < value && value <= 1){
        movement[1] += 1; // go up
    }
    return movement;
}


void question2b(){
    const int height = 1001, width = 1001;  // this is the fixed length/width of the barrier data grid
    std::vector <std::vector <int>> barriers(width, std::vector<int> (height, 0));  // a 2d vector for all of the barrier data (grid)

    std::ifstream dataFile;
    dataFile.open("barrier_data.txt");
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            if (!(dataFile >> barriers[i][j])) {    // this writes the barrier data to the 2d vector and also checks if its a valid write
                std::cerr << "Unexpected end of file\n" << std::endl;
                exit(1);   // call system to stop
            }
        }
    }
    dataFile.close();

    // now to populate arrays with grid coordinates
    std::vector<int> X(width * height, 0), Y(width * height, 0), Z(width * height, 0);
    for (int i = 0; i < width; i++){
        for (int j = 0; j < height; j++){
            X[i * width + j] = i;
            Y[i * width + j] = j;
        }
    }

    // initialise variables and arrays
    const int steps = 150000, runs = 40, initx = 500, inity = 500;
    int x = 0, y = 0, index = 0, extra = 0, escapes = 0;
    std::array <int, 2> deltaCoords = {0};
    bool permit;
    std::ofstream outputFile;

    outputFile.open("2bResults.txt");   // we'll write walker escape data to this file
    outputFile << "Escape | x | y | step | ave velocity " << std::endl;

    for (int i = 0; i < runs; i++){
        x = initx, y = inity;   // start the walker at the 'origin'
        for (int j = 0; j < steps; j++){
            index = (i * steps) + j;    // this is the index of the current step out of *all* steps across *all* walks
            permit = false;     // set it so that the walker hasnt moved yet
            extra = 0;
            while (!permit){    // while the walker hasn't moved
                deltaCoords = randomwalk2b(index + extra);  // get movement coordinates
                if (barriers.at(x + deltaCoords[0]).at(y) != 0){ // if there is no barrier in the x direction of movement
                    x += deltaCoords[0]; // move the walker
                    permit = true;  // the walker has moved!
                } if (barriers.at(x).at(y + deltaCoords[1]) != 0){ // if there is no barrier in the y direction of movement
                    y += deltaCoords[1]; // as above
                    permit = true;
                }
                extra += 1;     // increment the walk seed by 1 to potentially move in a different direction
            }
            Z[x * width + y] += 1;  // add one to the frequency of walkers being in this position

            if (x <= 0 || x >= width-1 || y <= 0 || y >= height-1){ // check to see if walker is at the grid edge
                escapes += 1; // we have an escape!
                outputFile << escapes << " | " << x << " | " << y << " | " << j << " | " << sqrt(pow(x, 2) + pow(y, 2)) / j << std::endl; // write data to results file
                break;  // finish this for loop, move to the next walker
            }
        }
    }
    outputFile.close();

    // now to write the frequencies (of each walker being at a XY position) to a file
    outputFile.open("2b-XYZ.dat");
    for (int i = 0; i < width * height; i++){
        outputFile << X[i] << " " << Y[i] << " " << Z[i] << std::endl;
    }
    outputFile.close();
}