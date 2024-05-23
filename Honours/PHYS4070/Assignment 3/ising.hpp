#pragma once
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <complex>
#include "matrix.hpp"

// const std::complex<double> imag(0., 1.);

Matrix tensor_product(Matrix mat1, Matrix mat2){
    // generic function for a tensor product given two matrices
    int num_rows = mat1.rows() * mat2.rows(), num_cols = mat1.cols() * mat2.cols(); // calculate the dimensions of our final matrix
    Matrix new_mat(num_rows, num_cols); // initialise a matrix with these dimensions
    for (int r1 = 0; r1 < mat1.rows(); r1++){ // for each row in the first matrix
        for (int c1 = 0; c1 < mat1.cols(); c1++){ // for each column in the first matrix
            for (int r2 = 0; r2 < mat2.rows(); r2++){ // for each row in the second matrix
                for (int c2 = 0; c2 < mat2.cols(); c2++){ // for each column in the second matrix
                    new_mat(r1 * mat2.rows() + r2, c1 * mat2.cols() + c2) = mat1(r1, c1) * mat2(r2, c2); // fill the final matrix with the element wise product
                }
            }
        }
    }
    return new_mat;
}
Matrix tensor_power(Matrix mat, int power){
    // function to calculate the tensor power given the integer power and tensor
    if (power == 0){ // then our output will just be a 1x1 matrix with element 1
        Matrix new_mat(1, 1);
        new_mat(0, 0) = 1.;
        return mat;
    } else { // perform the tensor product for the specified number of iterations
        Matrix new_mat = mat;
        for (int i = 0; i < power; i++){
            new_mat = tensor_product(new_mat, mat);
        }
        return new_mat;
    }
}
Matrix identity_tensor_power(int power){
    // more efficient tensor product-like operation, specifically for taking the power of the identity matrix
    int dim = (int)pow(2, power);
    Matrix new_mat(dim, dim);
    for (int i = 0; i < dim; i++){
        new_mat(i, i) = 1.; // only need to populate the diagonal!
    }
    return new_mat;
}
Matrix pauli_z(int N, int m){
    // calculates the pauli z spin matrix from the formula given in the task sheet
    Matrix pauli_z_mat(2, 2); // initialise the 2x2 matrix
    pauli_z_mat(0, 0) = 0.5; pauli_z_mat(1, 1) = -0.5; // populate diagonal terms
    Matrix left_product = tensor_product(identity_tensor_power(m), pauli_z_mat); // perform first tensor product
    Matrix right_product = tensor_product(left_product, identity_tensor_power(N - 1 - m)); // perform second tensor product
    return right_product;
}
Matrix pauli_x(int N, int m){
    // as above, but for the x spin matrix
    Matrix pauli_x_mat(2, 2);
    pauli_x_mat(0, 1) = 0.5; pauli_x_mat(1, 0) = 0.5;
    Matrix left_product = tensor_product(identity_tensor_power(m), pauli_x_mat);
    Matrix right_product = tensor_product(left_product, identity_tensor_power(N - 1 - m));
    return right_product;
}
Matrix pauli_pauli_x(int N, int m){
    // a more efficient way to calculate the product of ^(m) * ^(m + 1) pauli x spin matrices, using the formula from the task sheet
    Matrix pauli_x_mat(2, 2);
    pauli_x_mat(0, 1) = 0.5; pauli_x_mat(1, 0) = 0.5;
    if (m == N - 1){ // special case that accounts for the periodic boundary conditions
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
    // constructs the hamiltonian matrix for the transverse ising spin model
    int dim = (int)pow(2, N); // calculate dimension of final matrix
    Matrix hamiltonian(dim, dim); // initialise matrix 
    for (int m = 0; m < N; m++){ // for each particle in our system perform the z and x direction sums
        Matrix pz = pauli_z(N, m);
        Matrix ppx = pauli_pauli_x(N, m);
        hamiltonian = hamiltonian - pz - g * ppx;
    }
    return hamiltonian;
}
// dsyev_ is a symbol in the LAPACK library files
// Documentation: http://www.netlib.org/lapack/explore-html/index.html
extern "C" {
extern int dsyev_(char *jobz, char *uplo, int *dimension, double *in_out_matrix,
                  int *dimension2, double *out_e_values,
                  double *workspace_array, int *workspace_size, int *info);
// The variable names in the declaration here are not required, but I find them
// helpful
//   extern int dsyev_(char *, char *, int *, double *, int *, double *,
//                     double *, int *, int *);
// LAPACK uses fortran, and in order to get c++ to talk to fortran we need to
// pass raw pointers to the data - LAPACK takes all values as pointers.
// extern "C"  essentially means we are calling an external (non c++) function
}

MatrixAndVector solveEigenSystem(Matrix matrix, int dimension){
    // function to solve the eigenvalue/vector problem for A*u = lambda*u system
    Matrix matcopy = matrix;
    char jobz{'V'};
    char uplo{'U'};
    // create a blank vector to store calculated eigenvalues:
    std::vector<double> evals(dimension);
    int lwork = 6 * dimension;
    int info = 0; // will hold potential error message
    std::vector<double> work(lwork);
    dsyev_(&jobz, &uplo, &dimension, matcopy.data(), &dimension, evals.data(), work.data(), &lwork, &info);   
    MatrixAndVector mat_and_vec(dimension, dimension); // store the eigenvectors and values in a Matrix and Vector class

    mat_and_vec.mat = matcopy;
    mat_and_vec.vec = evals;

    if (info != 0){
        std::cout << info << std::endl;
    }
    
    return mat_and_vec;
}