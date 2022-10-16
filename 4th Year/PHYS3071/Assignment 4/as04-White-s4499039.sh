#!/bin/bash

touch Q1b.dat
touch Q1c.dat

g++ -g -std=c++11  as04-White-s4499039.cpp -o as04
./as04

gnuplot Q1b.gnu
gnuplot Q1c.gnu