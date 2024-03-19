# pragma once
# include <vector>
# include <cmath>
# include <iostream>
# include <cassert> // for assert(), used in matrix example
# include <string>
# include <fstream>

void output_1d_data(std::vector<double> x, std::vector<double> y, std::string filename){
    std::ofstream output_file;
    output_file.open(filename);
    for (int i = 0; i < (int)x.size(); i++){
        output_file << x[i] << "," << y[i] << "\n";
    }
    output_file.close();
}

void save_vector(std::vector<double> x, std::string filename){
    std::ofstream output_file;
    output_file.open(filename);
    for (int i = 0; i < (int)x.size(); i++){
        output_file << x[i] << "\n";
    }
    output_file.close();
}

std::vector<double> load_vector(std::string filename){
    std::vector<double> data;
    double tmp;

    std::ifstream input_file(filename, std::ios::in); 
    while (input_file >> tmp){
        data.push_back(tmp);
    }
    return data;
}