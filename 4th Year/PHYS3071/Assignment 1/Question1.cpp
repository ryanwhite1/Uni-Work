#include <iostream>
#include <fstream>
#include <string>
#include <array>
#include <vector>
#include <cmath>

std::array<double, 3> roll(double x, double y, double angle, double dist, double angle_incr){
    double new_x, new_y;    // initialise variables
    if (angle >= 360) angle = angle - 360;  // Although not a problem, I'd rather not have angles greater than 360
    if (angle < 0) angle = angle + 360; // As above, but for below 0
    double angle_rad = angle * M_PI / 180;      // convert angle to radians
    // angle 0 is taken to be in the direction of the positive x-axis
    // the change in (x, y) depends on the quadrant of the cartesian plane. The following statements account for this
    if ((0 <= angle < 90) || (180 <= angle < 270)){
        new_x = x + (dist * cos(angle_rad));
        new_y = y + (dist * sin(angle_rad));
    } else if ((90 <= angle < 180) || (270 <= angle < 360)){
        new_x = x + (dist * sin(angle_rad));
        new_y = y + (dist * cos(angle_rad));
    }
    angle += angle_incr;    // increment the angle that the ball is facing
    std::array<double, 3> pos_array = {new_x, new_y, angle};    // put all of the values in an array to be output
    return pos_array;
}

double OriginDist(double x, double y){
    // this is a simple function to find the current distance to the origin (just pythagoras)
    return sqrt(pow(x, 2) + pow(y, 2));
}

void question1(std::string filename){
    std::cout << "This is a program that models the position of a ball (with respect to the origin) after it has been rolled to the left by some angle and some distance." << std::endl;
    std::cout << "On each step, the ball is rolled some angle, and some distance. The program will output the final position, and the closest point to the origin (and the step)." << std::endl;
    int steps;
    std::cout << "Enter the number of steps to iterate over: ";     // gets user input for the number of steps to use
    std::cin >> steps;
    double init_x = -1, init_y = 0, angle = 180;     // starting position (the ball is rolled 1cm left)
    double angle_incr, dist; // initialise variables
    // now get user defined input for the angle increment and distance to move the ball
    std::cout << "\nEnter the angle to increment each time: "; std::cin >> angle_incr;
    std::cout << "\nEnter the distance the ball will travel each increment: "; std::cin >> dist;

    // now create vectors for each quantity we care about, setting their initial values to what we need
    std::vector<double> step_array = {0}; step_array[0] = 0;
    std::vector<double> x_array = {0}; x_array[0] = init_x;
    std::vector<double> y_array = {0}; y_array[0] = init_y;
    std::vector<double> dist_array = {0}; dist_array[0] = 1;

    for (int i = 1; i <= steps; i++){
        std::array<double, 3> newpos = roll(x_array[i-1], y_array[i-1], angle, dist, angle_incr); // roll the ball
        x_array.push_back(newpos[0]); y_array.push_back(newpos[1]); angle = newpos[2]; // set new x, y and angle values
        dist_array.push_back(OriginDist(newpos[0], newpos[1])); // calculate distance from origin at new (x, y)
        step_array.push_back(i); // increment step by 1
    }
    x_array[0] = init_x; y_array[0] = init_y; dist_array[0] = 1; // for some reason the first values would get changed. this changes them back.
    double min_dist = 1; // initialise minimum distance from origin with the first (and only known) distance 
    int min_step = 0; // the min distance above occurred at step 0
    // now let's find at which step the ball was closest to the origin
    for (int i = 0; i < steps; i++){
        if (dist_array[i] < min_dist){ // if this distance is less than the current defined minimum
            min_dist = dist_array[i]; // set this as the new minimum
            min_step = i; // update the location of this minimum
        }
    }
    std::cout << "The ball was closest to the origin at step " << min_step << ", with a distance of " << min_dist << std::endl;
    std::cout << "The final position of the ball was (x, y) = (" << x_array[steps-1] << ", " << y_array[steps-1] << ")." << std::endl;
    std::cout << "Thank you for using the program! \n\n\n";
    // now to write the time-series position of the ball to a file
    std::ofstream outputFile;
    outputFile.open(filename);
    for (int i = 0; i < steps; i++){
        outputFile << step_array[i] << " " << x_array[i] << " " << y_array[i] << " " << dist_array[i] << std::endl;
    }
    outputFile.close();
}