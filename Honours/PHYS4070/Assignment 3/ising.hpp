#pragma once
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <complex>
#include "matrix.hpp"

// const std::complex<double> imag(0., 1.);

Matrix tensor_product(Matrix mat1, Matrix mat2){
    int num_rows = mat1.rows() * mat2.rows(), num_cols = mat1.cols() * mat2.cols();
    // std::cout << num_rows << " " << num_cols << std::endl;
    Matrix new_mat(num_rows, num_cols);
    for (int r1 = 0; r1 < mat1.rows(); r1++){
        for (int c1 = 0; c1 < mat1.cols(); c1++){
            for (int r2 = 0; r2 < mat2.rows(); r2++){
                for (int c2 = 0; c2 < mat2.cols(); c2++){
                    // std::cout << r1 * mat2.rows() + r2 - num_rows << " " << c1 * mat2.cols() + c2 - num_cols << std::endl;
                    new_mat(r1 * mat2.rows() + r2, c1 * mat2.cols() + c2) = mat1(r1, c1) * mat2(r2, c2);
                }
            }
        }
    }
    return new_mat;
}
Matrix tensor_power(Matrix mat, int power){
    if (power == 0){
        Matrix new_mat(1, 1);
        new_mat(0, 0) = 1.;
        return mat;
    } else {
        Matrix new_mat = mat;
        for (int i = 0; i < power; i++){
            new_mat = tensor_product(new_mat, mat);
        }
        return new_mat;
    }
}
Matrix identity_tensor_power(int power){
    int dim = (int)pow(2, power);
    Matrix new_mat(dim, dim);
    for (int i = 0; i < dim; i++){
        new_mat(i, i) = 1.;
    }
    return new_mat;
}
Matrix pauli_z(int N, int m){
    Matrix pauli_z_mat(2, 2);
    pauli_z_mat(0, 0) = 0.5; pauli_z_mat(1, 1) = -0.5;
    Matrix left_product = tensor_product(identity_tensor_power(m), pauli_z_mat);
    Matrix right_product = tensor_product(left_product, identity_tensor_power(N - 1 - m));
    return right_product;
}
Matrix pauli_x(int N, int m){
    Matrix pauli_x_mat(2, 2);
    pauli_x_mat(0, 1) = 0.5; pauli_x_mat(1, 0) = 0.5;
    Matrix left_product = tensor_product(identity_tensor_power(m), pauli_x_mat);
    Matrix right_product = tensor_product(left_product, identity_tensor_power(N - 1 - m));
    return right_product;
}
Matrix pauli_pauli_x(int N, int m){
    Matrix pauli_x_mat(2, 2);
    pauli_x_mat(0, 1) = 0.5; pauli_x_mat(1, 0) = 0.5;
    if (m == N - 1){
        Matrix left_product = tensor_product(pauli_x_mat, identity_tensor_power(m - 1));
        Matrix right_product = tensor_product(left_product, pauli_x_mat);
        return right_product;
    } else {
        Matrix left_product = tensor_product(identity_tensor_power(m), pauli_x_mat);
        Matrix middle_product = tensor_product(left_product, pauli_x_mat);
        Matrix right_product = tensor_product(middle_product, identity_tensor_power(N - 2 - m));
        return right_product;
    }
}

Matrix hamiltonian_matrix(int N, double g){
    int dim = (int)pow(2, N);
    Matrix hamiltonian(dim, dim);
    for (int m = 0; m < N; m++){
        Matrix pz = pauli_z(N, m);
        Matrix ppx = pauli_pauli_x(N, m);
        hamiltonian = hamiltonian - pz - g * ppx;
    }
    return hamiltonian;
}