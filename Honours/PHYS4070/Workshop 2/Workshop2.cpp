# include <vector>
# include <cmath>
# include <iostream>
# include <cassert> // for assert(), used in matrix example
# include "bspline.hpp"



class Matrix {
    private:
        // use a std::vector to store the data
        std::vector<double> m_data;
        // store the # of rows/cols
        int m_rows, m_cols;
        // I use 'm_' to signify these are member variables (just convention)

    public:
        // contructor: contructs a matrix of dimension: rows X cols
        Matrix(int rows, int cols)
            : m_data(rows * cols), m_rows(rows), m_cols(cols) {}

        // note: this returns a reference to double, so we can modify the data
        double &at(int i, int j) {
            assert(i < m_rows && j < m_cols);
            return m_data[i * m_cols + j];
        }

        int rows() { return m_rows; }
        int cols() { return m_cols; }

        // to be fancy, we can also supply a '()' operator
        double &operator()(int i, int j) { 
            return at(i, j); 
        }

        // provide function that returns pointer to first element
        // (allows us to use this class as though it were a plain c-style array)
        double *data() {
            return m_data.data();
            // We used std::vector function data() here. It is equivilant to:
            // return &m_data[0];
        }
};

Matrix operator+(Matrix &a, Matrix &b) {
  Matrix sum = a;
  for (int i = 0; i < b.rows(); i++) {
    for (int j = 0; j < b.cols(); j++) {
      sum(i, j) += b(i, j);
    }
  }
  return sum;
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


class MatrixAndVector{
    private:
        Matrix mat;
        std::vector<double> vec;
        int rows, cols;
    public:
        MatrixAndVector(int rows, int cols) 
            : mat(rows, cols), vec(cols) {}
        
        double &mat_at(int i, int j){
            // assert(i < rows && j < cols);
            return mat(i, j);
        }
        double &vec_at(int i){
            // assert(i < rows);
            return vec.at(i);
        }
        double *mat_data(){
            return mat.data();
        }
        
};

MatrixAndVector solveEigenSystem(Matrix matrix, int dimension){
    Matrix matcopy = matrix;
    char jobz{'V'};
    char uplo{'U'};
    std::vector<double> evals(dimension);
    int lwork = 6 * dimension;
    int info = 0; // will hold potential error message
    // create a blank vector to store calculated eigenvalues:
    std::vector<double> work(lwork);
    dsyev_(&jobz, &uplo, &dimension, matcopy.data(), &dimension, evals.data(), work.data(), &lwork, &info);   

    MatrixAndVector mat_and_vec(dimension, dimension);
    for (int i = 0; i < dimension; i++){
        for (int j = 0; j < dimension; j++){
            mat_and_vec.mat_at(i, j) = matcopy.at(i, j);
        }
        mat_and_vec.vec_at(dimension-i-1) = evals.at(dimension-i-1);
    }

    return mat_and_vec;
}



int main(){
    int dimension = 2; // N if we have NxN matrix

    Matrix mat(2, 2);
    for (int i = 0; i < dimension; i++){
        for (int j = 0; j < dimension; j++){
            mat.at(i, j) = 1. / (i + j + 1.);
        }
    }
    MatrixAndVector matvec = solveEigenSystem(mat, dimension);

    std::cout << "Eigenvecs = {";
    for (int i = 0; i < dimension; i++){
        std::cout << "{";
        for (int j = 0; j < dimension; j++){
            std::cout << matvec.mat_at(i, j);
            if (j < dimension-1){
                std::cout << ", ";
            }
        }
        if (i < dimension-1){
            std::cout << "}, " << std::endl;
        }
    }
    std::cout << "}}" << std::endl;


    std::cout << "Eigenvals = {";
    for (int i = 0; i < dimension; i++){
        std::cout << matvec.vec_at(i);
        if (i < dimension - 1){
            std::cout << ", ";
        }
    }
    std::cout << "}" << std::endl;

    return 0;
}