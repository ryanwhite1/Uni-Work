# pragma once
#include <cmath>
#include <iostream>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <random>
#include <omp.h>
#include <cassert> // for assert(), used in matrix example
#include "matrix.hpp"

class IsingLattice {
    private:
        std::mt19937 mt_generator;
        std::uniform_real_distribution<double> uniform_real; // uniform real random generator for our monte carlo sampling
        std::uniform_int_distribution<int> rand_row, rand_col; // random int number generators to yield a random row and column
        int Nrows, Ncols;
        Matrix lattice;
        double temperature, energy, magnetisation_per_s;
        std::ofstream output_file;
        std::string filename;
    public:
        IsingLattice(int rows, int cols, double temp, int seed, std::string output_filename)
            : mt_generator(seed), 
            uniform_real(0., 1.), 
            rand_row(0, rows - 1),
            rand_col(0, cols - 1),
            lattice(rows, cols), 
            Nrows(rows), 
            Ncols(cols), 
            temperature(temp),
            energy(0.),
            magnetisation_per_s(0.),
            filename(output_filename)
            {}

        void print_params(){
            std::cout << "Energy = " << energy << "\nMagnetisation per dipole = " << magnetisation_per_s << std::endl;
        }
        void output_params(){
            output_file << temperature << "\t" << energy << "\t" << magnetisation_per_s << std::endl;
        }
        void close_file(){
            output_file.close();
        }
        void change_temperature(double temp){
            // changes the temperature of our lattice thermal bath
            temperature = temp;
        }
        
        std::vector<int> neighbouring_indices(int row, int col){
            /*Calculates the neighbouring indices of the monopole at position {row, col}, returning them in the format [left, right, top, down]*/
            std::vector<int> indices(4, 0.);
            indices[0] = (col + Ncols - 1) % Ncols; // left index
            indices[1] = (col + 1) % Ncols; // right index
            indices[2] = (row + Nrows - 1) % Nrows; // top index
            indices[3] = (row + 1) % Nrows; // down index
            return indices;
        }

        void total_lattice_energy(){
            // calculates the total lattice energy (should only be run when initialising the lattice)
            for (int i = 0; i < Nrows; i++){
                for (int j = 0; j < Ncols; j++){
                    // we only want to sum the current monopole with that to the left of it and that above, so that we don't double count monopole pairs
                    std::vector<int> neighbours = neighbouring_indices(i, j);
                    double left_val = lattice(i, neighbours[0]), top_val = lattice(neighbours[2], j);
                    energy += - lattice(i, j) * (left_val + top_val);
                }
            }
            energy /= Nrows * Ncols; // our energy variable stores energy per spin
        }
        
        void initialise_lattice(){
            /*Initialise the lattice with a random arrangement of spin ups (1) and spin downs (-1)*/
            double rand_num = 0., val = 0.;
            for (int i = 0; i < Nrows; i++){
                for (int j = 0; j < Ncols; j++){
                    rand_num = uniform_real(mt_generator);
                    if (rand_num > 0.5){val = 1.;} else {val = -1.;}
                    lattice(i, j) = val;
                    magnetisation_per_s += val;
                }
            }
            magnetisation_per_s /= (Nrows * Ncols);
            total_lattice_energy();

            output_file.open(filename);
        }

        void print_lattice(){
            /* Prints the lattice spins {"O" for spin up, "-" for spin down} to the terminal*/
            std::string val = "";
            for (int i = 0; i < Nrows; i++){
                for (int j = 0; j < Ncols; j++){
                    if (lattice(i, j) == 1.){val = "O";} else {val = "-";}
                    std::cout << val << " ";
                }
                std::cout << std::endl;
            }
        }

        double delta_energy(int row, int col){
            /*Calculates the change in energy if we flip the monopole at position {row, col}*/
            std::vector<int> neighbours = neighbouring_indices(row, col);
            double init_energy = 0., flip_energy = 0., neighbour_val = 0.;
            for (int i = 0; i < 4; i++){
                // loop over each of our neighbouring dipoles and add their energy contribution to a running total
                if (i < 2){neighbour_val = lattice(row, neighbours[i]);} else {neighbour_val = lattice(neighbours[i], col);}
                init_energy += - lattice(row, col) * neighbour_val;
                flip_energy += lattice(row, col) * neighbour_val;
            }
            return flip_energy - init_energy;
        }

        void flip_monopole(int row, int col, double delta_E){
            // flips a dipole and updates the lattice parameters accordingly
            lattice(row, col) *= -1;
            // factor of two in the below lines comes out from the expression being: quantity += new_spin - old_spin = new_spin - (- new_spin) = 2 * new_spin
            energy += delta_E / (Nrows * Ncols);
            magnetisation_per_s += 2 * lattice(row, col) / (Nrows * Ncols); 
        }

        void monte_carlo_step(){
            // performs one monte carlo step (checks if a random dipole should flip, and if so, flips it)
            int row = rand_row(mt_generator), col = rand_col(mt_generator);
            double delta_E = delta_energy(row, col);
            if (delta_E <= 0){
                flip_monopole(row, col, delta_E);
            } else {
                double rand_num = uniform_real(mt_generator);
                double alpha = exp(-delta_E / temperature);
                if (rand_num <= alpha){
                    flip_monopole(row, col, delta_E);
                }
            }
        }

        void run_monte_carlo(int sweeps, int output){
            // runs several (sweeps * 10 * N*N) monte carlo steps, and outputs the data to file if output == 1
            for (int s = 0; s < sweeps; s++){
                for (int n = 0; n < 10*Ncols*Nrows; n++){
                    monte_carlo_step();
                }
                if (output == 1){
                    output_params();
                }
            }
        }

        void run_monte_carlo_parallel(int sweeps, int num_threads){
            // code for a parallelised monte carlo simulation
            assert(Nrows%num_threads == 0);

            omp_set_num_threads(num_threads); // update the number of threads we're using
            int N = Ncols*Nrows;
            #pragma omp parallel default(none) shared(lattice, sweeps, N) // initialise parallel region, sharing the lattice configuration, number of sweeps, and number of dipoles
            {
                std::mt19937 rand_generator((int)omp_get_wtime()); // random generator with wall time seed (so that each thread will have different random numbers)
                for (int s = 0; s < sweeps; s++){
                    for (int n = 0; n < N; n++){
                        double delta_E = 0.;
                        #pragma omp for
                        for (int row = 0; row < Nrows - 1; row += 2){ // iterate over even rows in the lattice so that each thread doesn't try to update the same dipole at the same time
                            // now iterate over our columns sequentially. do a monte carlo step for each dipole in the row
                            for (int col = 0; col < Ncols; col++){
                                delta_E = delta_energy(row, col);
                                if (delta_E <= 0){
                                    flip_monopole(row, col, delta_E);
                                } else {
                                    double rand_num = uniform_real(rand_generator);
                                    double alpha = exp(-delta_E / temperature);
                                    if (rand_num <= alpha){
                                        flip_monopole(row, col, delta_E);
                                    }
                                }
                            }
                        }
                        // there is an implicit barrier at the end of the above for loop, so we don't need to manually make the code wait before starting the next loop
                        #pragma omp for
                        for (int row = 1; row < Nrows; row += 2){ // iterate over odd rows in the lattice so that each thread doesn't try to update the same dipole at the same time
                            // now iterate over columns sequentially. do a monte carlo step for each dipole in the row
                            for (int col = 0; col < Ncols; col++){
                                delta_E = delta_energy(row, col);
                                if (delta_E <= 0){
                                    flip_monopole(row, col, delta_E);
                                } else {
                                    double rand_num = uniform_real(rand_generator);
                                    double alpha = exp(-delta_E / temperature);
                                    if (rand_num <= alpha){
                                        flip_monopole(row, col, delta_E);
                                    }
                                }
                            }
                        }
                        // there is an implicit barrier at the end of the above for loop, so we don't need to manually make the code wait before starting the next sweep
                    }
                }
            }
        }
};