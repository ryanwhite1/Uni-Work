#!/bin/bash

touch Q1data1.dat
touch Q1data2.dat
touch Q1data3.dat
touch Q2Interp.dat
touch Q2HighSampled.dat
touch Q2Residuals.dat

g++ as01-White-s4499039.cpp -o assignment1 -std=c++11
./assignment1

gnuplot Question1c.gnu
gnuplot Question2.gnu