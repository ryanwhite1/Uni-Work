#!/bin/bash

touch PartA.dat
touch PartB.dat
touch PartC.dat

g++ -g -std=c++11  as05-White-s4499039.cpp -o ass5
./ass5

gnuplot Ass5Plots.gnu