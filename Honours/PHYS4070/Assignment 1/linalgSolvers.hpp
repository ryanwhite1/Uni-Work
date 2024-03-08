# pragma once
# include <vector>
# include <cmath>
# include <iostream>
# include "matrix.hpp"

// dsyev_ is a symbol in the LAPACK library files
// Documentation: http://www.netlib.org/lapack/explore-html/index.html
extern "C" {

extern int dsyev_(char *jobz, char *uplo, int *dimension, double *in_out_matrix,
                  int *dimension2, double *out_e_values,
                  double *workspace_array, int *workspace_size, int *info);
extern "C" int dsygv_(
int *ITYPE, // =1 for problems of type Av=eBv
char *JOBZ, // ='V' means calculate eigenvectors
char *UPLO, // 'U': upper triangle of matrix is stored, 'L': lower
int *N, // dimension of matrix A
double *A, // c-style array for matrix A (ptr to array, pointer to a[0])
// On output, A contains matrix of eigenvectors
int *LDA, // For us, LDA=N
double *B, // c-style array for matrix B [Av=eBv]
int *LDB, // For us, LDB =N
double *W, // Array of dimension N - will hold eigenvalues
double *WORK, // 'workspace': array of dimension LWORK
int *LWORK, // dimension of workspace: ~ 6*N works well
int *INFO // error code: 0=worked.
);

// The variable names in the declaration here are not required, but I find them
// helpful
//   extern int dsyev_(char *, char *, int *, double *, int *, double *,
//                     double *, int *, int *);
// LAPACK uses fortran, and in order to get c++ to talk to fortran we need to
// pass raw pointers to the data - LAPACK takes all values as pointers.
// extern "C"  essentially means we are calling an external (non c++) function
}


MatrixAndVector solveEigenSystem(Matrix matrix, int dimension){
    Matrix matcopy = matrix;
    char jobz{'V'};
    char uplo{'U'};
    // create a blank vector to store calculated eigenvalues:
    std::vector<double> evals(dimension);
    int lwork = 6 * dimension;
    int info = 0; // will hold potential error message
    std::vector<double> work(lwork);
    dsyev_(&jobz, &uplo, &dimension, matcopy.data(), &dimension, evals.data(), work.data(), &lwork, &info);   
    MatrixAndVector mat_and_vec(dimension, dimension);

    mat_and_vec.mat = matcopy;
    mat_and_vec.vec = evals;

    if (info != 0){
        std::cout << info << std::endl;
    }
    
    return mat_and_vec;
}

MatrixAndVector solveEigenSystem_AveBv(Matrix matrix_A, Matrix matrix_B, int dimension){
    // copy the arrays to avoid overwriting them
    Matrix matcopy_A = matrix_A;
    Matrix matcopy_B = matrix_B;
    int itype = 1;
    char jobz{'V'};
    char uplo{'U'};
    std::vector<double> evals(dimension);
    int lwork = 6 * dimension;
    int info = 0; // will hold potential error message
    // create a blank vector to store calculated eigenvalues:
    std::vector<double> work(lwork);

    MatrixAndVector mat_and_vec(dimension, dimension);

    dsygv_(&itype, &jobz, &uplo, &dimension, matcopy_A.data(), &dimension, matcopy_B.data(), &dimension, evals.data(), work.data(), &lwork, &info);
    
    mat_and_vec.mat = matcopy_A;
    mat_and_vec.vec = evals;
    
    if (info != 0){
        std::cout << info << std::endl;
    }
    return mat_and_vec;
}