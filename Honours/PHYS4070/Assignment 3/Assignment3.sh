#!/bin/bash

g++	-o	ass_three	-Wall	-Wextra	-Wpedantic Assignment3.cpp -llapack -lblas -O3
./ass_three

# python3 Plot_Part1.py
# python3 Plot_Part2.py