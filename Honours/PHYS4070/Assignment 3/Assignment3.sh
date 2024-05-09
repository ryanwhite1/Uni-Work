#!/bin/bash

g++	-o	ass_three	-Wall	-Wextra	-Wpedantic Assignment3.cpp -llapack -lblas -O3
./ass_three

python3 Plot_Ass3.py