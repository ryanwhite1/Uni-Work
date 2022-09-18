
#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

// std::vector <double> InnerCoords(double len, double theta){
//     // Returns a vector of {x, y} coordinates of an inner pendulum, given a length and an angle w.r.t. the origin
//     std::vector <double> coords = {len * sin(theta), -len * cos(theta)};
//     return coords;
// }
// std::vector <double> OuterCoords(double len1, double len2, double theta1, double theta2){
//     // Returns a vector of {x, y} coordinates of the outer mass of a double pendulum, given lengths l1 and l2, and angles w.r.t. the origin theta1 and theta2
//     std::vector <double> coords = {len1 * sin(theta1) + len2 * sin(theta2), -len1 * cos(theta1) - len2 * cos(theta2)};
//     return coords;
// }
std::vector <double> SystemCoords(double len1, double len2, double theta1, double theta2){
    // Returns a vector of {x1, y1, x2, y2} coordinates of both masses of a double pendulum.
    std::vector <double> coords = {len1 * sin(theta1), -len1 * cos(theta1), len1 * sin(theta1) + len2 * sin(theta2), -len1 * cos(theta1) - len2 * cos(theta2)};
    return coords;
}
double speed(double initX, double finalX, double initY, double finalY, double deltaTime){
    // returns the instantaneous speed of a particle, having moved from init{x, y} to final{x, y} over a time step of deltaTime
    double speed = sqrt(pow(finalX - initX, 2) + pow(finalY - initY, 2)) / deltaTime;
    return speed;
}

double A(double m1, double m2, double l2, double theta1, double theta2, double theta2dash){
    // this function is a part of the system of equations that allows for a numerical solution of the double pendulum
    double At = m2 * l2 * pow(theta2dash, 2) * sin(theta1 - theta2) + (m1 + m2) * 9.81 * sin(theta1);
    return At;
}
double B(double m2, double l1, double theta1, double theta2, double theta1dash){
    // this function is a part of the system of equations that allows for a numerical solution of the double pendulum
    double Bt = -m2 * l1 * pow(theta1dash, 2) * sin(theta1 - theta2) + m2 * 9.81 * sin(theta2);
    return Bt;
}
double theta1ddash(double m1, double m2, double l1, double l2, double t1, double t2, double t1d, double t2d){
    // this is a function to calculate the double derivative of theta 1 given the system parameters
    double t1dd = (-A(m1, m2, l2, t1, t2, t2d) + cos(t1 - t2) * B(m2, l1, t1, t2, t1d)) / (l1*(m1 + m2) - m2*l1*pow(cos(t1-t2), 2));
    return t1dd;
}
double theta2ddash(double m1, double m2, double l1, double l2, double t1, double t2, double t1d, double t2d){
    // this is a function to calculate the double derivative of theta 2 given the system parameters
    double t2dd = (m2*cos(t1-t2)*A(m1,m2,l2,t1,t2, t2d) - (m1 + m2)*B(m2, l1, t1, t2, t1d)) / (m2*l2*(m1 + m2) - m2*m2*l2*pow(cos(t1-t2), 2));
    return t2dd;
}

double energy(double m1, double m2, double initX1, double finalX1, double initX2, double finalX2, double initY1, double finalY1, double initY2, double finalY2, double deltaTime){
    // calculates the *approximate* energy of the system at some time by the formula E = T + V, where 
    // T = 1/2 (m1*v1^2 + m2*v2^2)      and         V = -g (m1*y1 + m2*y2)
    // the velocities in the above are approximated as the instantaneous speeds (since the square removes any directional component anyway)
    double speed1 = speed(initX1, finalX1, initY1, finalY1, deltaTime), speed2 = speed(initX2, finalX2, initY2, finalY2, deltaTime);
    double E = 0.5 * (m1 * pow(speed1, 2) + m2 * pow(speed2, 2)) - 9.81 * (m1 * finalY1 + m2 * finalY2);
    return E;
}

std::vector<std::vector<double>> DPendEuler(int steps, double stepsize, double m1, double m2, double l1, double l2, double initT1, double initT2, double initT1d, double initT2d){
    // this function numerically solves the double pendulum (using the euler method) for a given number of steps and some initial conditions
    // it outputs the values of theta1 (for the inner pendulum) and theta2 (for the outer pendulum) for each step into a 2d vector
    std::vector <std::vector <double>> ThetaVals(steps, std::vector<double> (2, 0)); // initialise a 2d array of {steps} number of rows, and 2 columns.
    double currT1 = initT1, currT2 = initT2, currT1d = initT1d, currT2d = initT2d; // set the current state of the system to the initial conditions
    for (int i = 0; i < steps; i++){
        ThetaVals[i][0] = currT1; ThetaVals[i][1] = currT2;     // put the current values in the timeseries array
        currT1 += stepsize * currT1d; currT2 += stepsize * currT2d;     // euler step on the theta values
        // now the euler step on the derivatives of the theta vals:
        currT1d += stepsize * theta1ddash(m1, m2, l1, l2, currT1, currT2, currT1d, currT2d);
        currT2d += stepsize * theta2ddash(m1, m2, l1, l2, currT1, currT2, currT1d, currT2d);
    }
    return ThetaVals;
}

std::vector<std::vector<double>> DPendRK4(int steps, double stepsize, double m1, double m2, double l1, double l2, double initT1, double initT2, double initT1d, double initT2d){
    // this function numerically solves the double pendulum (using the Runge-Kutta 4 method) for a given number of steps and some initial conditions
    // it outputs the values of theta1 (for the inner pendulum) and theta2 (for the outer pendulum) for each step into a 2d vector
    std::vector <std::vector <double>> ThetaVals(steps, std::vector<double> (2, 0)); // initialise a 2d array of {steps} number of rows, and 2 columns.
    double currT1 = initT1, currT2 = initT2, currT1d = initT1d, currT2d = initT2d; // set the current state of the system to the initial conditions
    double k1, k2, k3, k4, k11, k12, k13, k14, k21, k22, k23, k24; // initialise the runge-kutta variables needed
    auto theta1dashRK4 = [&](double t1){
        // double k1, k2, k3, k4;
        // this lambda function performs the RK4 method on the first derivative of theta1 using the double derivative of theta1 as the derivative function
        k1 = stepsize * theta1ddash(m1, m2, l1, l2, t1, currT2, currT1d, currT2d);
        k2 = stepsize * theta1ddash(m1, m2, l1, l2, t1, currT2, currT1d + k1 / 2, currT2d);
        k3 = stepsize * theta1ddash(m1, m2, l1, l2, t1, currT2, currT1d + k2 / 2, currT2d);
        k4 = stepsize * theta1ddash(m1, m2, l1, l2, t1, currT2, currT1d + k3, currT2d);
        double newT1d = currT1d + (k1 + 2 * (k2 + k3) + k4) / 6;
        return newT1d;
    };
    auto theta2dashRK4 = [&](double t2){
        // double k1, k2, k3, k4;
        // this lambda function performs the RK4 method on the first derivative of theta2 using the double derivative of theta2 as the derivative function
        k1 = stepsize * theta2ddash(m1, m2, l1, l2, currT1, t2, currT1d, currT2d);
        k2 = stepsize * theta2ddash(m1, m2, l1, l2, currT1, t2, currT1d, currT2d + k1 / 2);
        k3 = stepsize * theta2ddash(m1, m2, l1, l2, currT1, t2, currT1d, currT2d + k2 / 2);
        k4 = stepsize * theta2ddash(m1, m2, l1, l2, currT1, t2, currT1d, currT2d + k3);
        double newT2d = currT2d + (k1 + 2 * (k2 + k3) + k4) / 6;
        return newT2d;
    };
    for (int i = 0; i < steps; i++){    // now to perform the RK4 method on the theta values and their derivatives
        ThetaVals[i][0] = currT1; ThetaVals[i][1] = currT2;     // put the current values in the timeseries array
        k11 = stepsize * currT1d;   // first RK4 step on theta1
        k12 = stepsize * theta1dashRK4(currT1 + k11 / 2); // second
        k13 = stepsize * theta1dashRK4(currT1 + k12 / 2); // third 
        k14 = stepsize * theta1dashRK4(currT1 + k13); // fourth
        currT1 = currT1 + (k11 + 2 * (k12 + k13) + k14) / 6; // set the new value of theta1

        k21 = stepsize * currT2d;   // as above, but for theta2
        k22 = stepsize * theta2dashRK4(currT2 + k21 / 2);
        k23 = stepsize * theta2dashRK4(currT2 + k22 / 2);
        k24 = stepsize * theta2dashRK4(currT2 + k23);
        currT2 = currT2 + (k21 + 2 * (k22 + k23) + k24) / 6;

        currT1d = theta1dashRK4(currT1); currT2d = theta2dashRK4(currT2); // now set the new values for the derivatives using the RK4 lambda functions
    }
    return ThetaVals;
}

int main(){
    double m1 = 0.5, m2 = 0.5, l1 = 1, l2 = 1; // values for the masses and strings in the double pendulum
    int steps = 10000; 
    double stepsize = 10.0 / steps; // we want to go up to 10 seconds, so divide 10 by number of steps to get stepsize
    double initT1 = M_PI / 6, initT2 = M_PI / 6, initT1d = 0, initT2d = 0;  // initial angles of the pendulum masses
    // now, perform Euler's method and RK4 for the double pendulum given the above conditions, and save to a named variable
    std::vector <std::vector <double>> Euler1 = DPendEuler(steps, stepsize, m1, m2, l1, l2, initT1, initT2, initT1d, initT2d); // Q1ci
    std::vector <std::vector <double>> RK41 = DPendRK4(steps, stepsize, m1, m2, l1, l2, initT1, initT2, initT1d, initT2d); // Q1ci

    initT1 = 9 * M_PI / 10; initT2 = -9 * M_PI / 10; initT1d = - M_PI; initT2d = 0; // now change the initial conditions, and do it again
    std::vector <std::vector <double>> Euler2 = DPendEuler(steps, stepsize, m1, m2, l1, l2, initT1, initT2, initT1d, initT2d); // Q1cii
    std::vector <std::vector <double>> RK42 = DPendRK4(steps, stepsize, m1, m2, l1, l2, initT1, initT2, initT1d, initT2d); //Q1cii

    initT1 = M_PI / 2; initT2 = 3/2 * M_PI; initT1d = -M_PI; initT2d = M_PI; // change the initial conditions once more and do it again
    std::vector <std::vector <double>> CoolEuler = DPendEuler(steps, stepsize, m1, m2, l1, l2, initT1, initT2, initT1d, initT2d); // Q1e
    std::vector <std::vector <double>> CoolRK4 = DPendRK4(steps, stepsize, m1, m2, l1, l2, initT1, initT2, initT1d, initT2d); // Q1e

    std::ofstream outputFile, outputFile2, outputFile3, outputFile4, outputFileCoolEuler, outputFileCoolRK4; // initialise output files

    outputFile.open("EulerMethod1.dat"); outputFile2.open("EulerMethod2.dat"); // open all of the files so that we can write in them
    outputFile3.open("RK4Method1.dat"); outputFile4.open("RK4Method2.dat");
    outputFileCoolEuler.open("EulerCool.dat"); outputFileCoolRK4.open("RK4Cool.dat");

    // now initialise all vectors and variables to write data into (and subsequently write to file)
    std::vector <double> Euler1New (4, 0), Euler2New (4, 0), EulerCoolNew (4, 0), RK41New (4, 0), RK42New (4, 0), RK4CoolNew (4, 0);
    std::vector <double> Euler1Old (4, 0), Euler2Old (4, 0), EulerCoolOld (4, 0), RK41Old (4, 0), RK42Old (4, 0), RK4CoolOld (4, 0);
    double Euler1Energy, Euler2Energy, EulerCoolEnergy, RK41Energy, RK42Energy, RK4CoolEnergy;

    for (int i = 0; i < steps; i++){
        Euler1New = SystemCoords(l1, l2, Euler1[i][0], Euler1[i][1]); // this stores the {x1, y1, x2, y2} data for this run of the code
        Euler2New = SystemCoords(l1, l2, Euler2[i][0], Euler2[i][1]); // as above for a different run
        EulerCoolNew = SystemCoords(l1, l2, CoolEuler[i][0], CoolEuler[i][1]); // etc
        RK41New = SystemCoords(l1, l2, RK41[i][0], RK41[i][1]);
        RK42New = SystemCoords(l1, l2, RK42[i][0], RK42[i][1]);
        RK4CoolNew = SystemCoords(l1, l2, CoolRK4[i][0], CoolRK4[i][1]);


        if (i != 0) {
            // now, calculate the energy for each step for each run. Since this relies on the values from the previous step, we can't do this if i==0 (the initial state)
            Euler1Energy = energy(m1, m2, Euler1Old[0], Euler1New[0], Euler1Old[2], Euler1Old[2], Euler1Old[1], Euler1New[1], Euler1Old[3], Euler1New[3], stepsize);
            Euler2Energy = energy(m1, m2, Euler2Old[0], Euler2New[0], Euler2Old[2], Euler2Old[2], Euler2Old[1], Euler2New[1], Euler2Old[3], Euler2New[3], stepsize);
            EulerCoolEnergy = energy(m1, m2, EulerCoolOld[0], EulerCoolNew[0], EulerCoolOld[2], EulerCoolOld[2], EulerCoolOld[1], EulerCoolNew[1], 
            EulerCoolOld[3], EulerCoolNew[3], stepsize);

            RK41Energy = energy(m1, m2, RK41Old[0], RK41New[0], RK41Old[2], RK41Old[2], RK41Old[1], RK41New[1], RK41Old[3], RK41New[3], stepsize);
            RK42Energy = energy(m1, m2, RK42Old[0], RK42New[0], RK42Old[2], RK42Old[2], RK42Old[1], RK42New[1], RK42Old[3], RK42New[3], stepsize);
            RK4CoolEnergy = energy(m1, m2, RK4CoolOld[0], RK4CoolNew[0], RK4CoolOld[2], RK4CoolOld[2], RK4CoolOld[1], RK4CoolNew[1], 
            RK4CoolOld[3], RK4CoolNew[3], stepsize);
        }
        
        // now write all of the data to the respective file in the format "x1 y1 x2 y2 energy"
        outputFile << Euler1New[0] << " " << Euler1New[1] << " " << Euler1New[2] << " " << Euler1New[3] << " " << i * stepsize << " " << Euler1Energy << std::endl;
        outputFile2 << Euler2New[0] << " " << Euler2New[1] << " " << Euler2New[2] << " " << Euler2New[3] << " " << i * stepsize << " " << Euler2Energy << std::endl;
        outputFileCoolEuler << EulerCoolNew[0] << " " << EulerCoolNew[1] << " " << EulerCoolNew[2] << " " << EulerCoolNew[3] << " " << i * stepsize << " " << EulerCoolEnergy << std::endl;

        outputFile3 << RK41New[0] << " " << RK41New[1] << " " << RK41New[2] << " " << RK41New[3] << " " << i * stepsize << " " << RK41Energy << std::endl;
        outputFile4 << RK42New[0] << " " << RK42New[1] << " " << RK42New[2] << " " << RK42New[3] << " " << i * stepsize << " " << RK42Energy << std::endl;
        outputFileCoolRK4 << RK4CoolNew[0] << " " << RK4CoolNew[1] << " " << RK4CoolNew[2] << " " << RK4CoolNew[3] << " " << i * stepsize << " " << RK4CoolEnergy << std::endl;

        // now set the "old" state to be equal to the current state so that we can calculate energy on the next step
        Euler1Old = Euler1New; Euler2Old = Euler2New; EulerCoolOld = EulerCoolNew; 
        RK41Old = RK41New; RK42Old = RK42New; RK4CoolOld = RK4CoolNew;
    }
    outputFile.close(); outputFile2.close(); outputFile3.close(); outputFile4.close(); outputFileCoolEuler.close(); outputFileCoolRK4.close(); // close all files
    return 0;
}