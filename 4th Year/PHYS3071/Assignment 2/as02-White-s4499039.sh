#!/bin/bash

touch Q1a-Results.txt
touch Q1b-Results.txt
touch 2aResults.txt
touch 2a-XYZ.dat
touch 2b-XYZ.dat
touch 2bResults.txt

g++ -g -std=c++11  as02-White-s4499039.cpp -o as02
./as02

gnuplot Q2a.gnu
gnuplot Q2b.gnu