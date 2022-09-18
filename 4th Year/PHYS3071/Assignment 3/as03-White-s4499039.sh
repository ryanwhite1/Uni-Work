#!/bin/bash

touch EulerMethod1.dat
touch EulerMethod2.dat
touch RK4Method1.dat
touch RK4Method2.dat
touch EulerCool.dat
touch RK4Cool.dat

g++ -g -std=c++11  as03-White-s4499039.cpp -o as03
./as03

gnuplot Ass3.gnu