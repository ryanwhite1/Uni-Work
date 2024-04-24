#!/bin/bash
mkdir -p "Ising_Datasets"

g++	-o	ass_two	-Wall	-Wextra	-Wpedantic Assignment2.cpp -llapack -lblas -O3 -fopenmp
./ass_two

# python3 plot_part_one.py
# python3 plot_part_two_one.py
# python3 plot_part_two_two.py