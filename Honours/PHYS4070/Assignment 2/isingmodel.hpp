# pragma once
#include <cmath>
#include <iostream>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <random>
#include "matrix.hpp"

class IsingLattice {
    private:
        std::mt19937 mt_generator;
        std::uniform_real_distribution<double> uniform_real;
        int Nrows, Ncols;
        Matrix lattice;
    public:
        IsingLattice(int rows, int cols, int seed)
            : mt_generator(seed), uniform_real(0., 1.), lattice(rows, cols), Nrows(rows), Ncols(cols){}
};