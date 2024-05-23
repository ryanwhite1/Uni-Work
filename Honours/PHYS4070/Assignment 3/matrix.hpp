// # pragma once
# include <vector>
# include <cmath>
# include <iostream>
# include <cassert> // for assert(), used in matrix example

class Matrix {
    // Matrix class kindly supplied by Ben Roberts
    // https://github.com/benroberts999/cpp-cheatsheet/blob/main/lapack_matrix.cpp
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

        void print_matrix(){
            for (int i = 0; i < m_rows; i++){
                for (int j = 0; j < m_cols; j++){
                    std::cout << m_data[i * m_cols + j] << "\t";
                }
                std::cout << std::endl;
            }
        }
};

// now overload operators so that we can do cursed Matrix/vector operations
Matrix operator+(Matrix a, Matrix b) {
    // overload matrix addition so we can easily add two matrices together
    Matrix sum = a;
    for (int i = 0; i < b.rows(); i++) {
        for (int j = 0; j < b.cols(); j++) {
            sum(i, j) += b(i, j);
        }
    }
    return sum;
}
Matrix operator+(Matrix a, double b){
    Matrix new_mat(a.rows(), a.cols());
    for (int i = 0; i < new_mat.rows(); i++){
        for (int j = 0; j < new_mat.cols(); j++){
            new_mat(i, j) = b;
        }
    }
    return a + new_mat;
}
Matrix operator*(Matrix a, double b) {
    Matrix new_mat = a;
    // overload matrix addition so we can easily add two matrices together
    for (int i = 0; i < a.rows(); i++) {
        for (int j = 0; j < a.cols(); j++) {
            new_mat(i, j) = new_mat(i, j) * b;
        }
    }
    return new_mat;
}
Matrix operator*(double b, Matrix a){return a * b;}
Matrix operator/(Matrix a, double b){return a * (1. / b);}
Matrix operator/(double b, Matrix a){return a * (1. / b);}
Matrix operator+(double b, Matrix a){return a + b;}
Matrix operator-(Matrix a, Matrix b){return a + (-1.*b);}
Matrix operator-(Matrix a, double b){return a + (-1. * b);}
Matrix operator-(double b, Matrix a){return a - b;}
Matrix operator*(Matrix a, Matrix b){
    assert(a.rows() == b.rows() && a.cols() == b.cols());
    Matrix new_mat(a.rows(), a.cols());
    for (int i = 0; i < a.rows(); i++){
        for (int j = 0; j < a.cols(); j++){
            for (int k = 0; k < a.rows(); k++){
                new_mat(i, j) += a(i, k) * b(k, j);
            }
        }
    }
    return new_mat;
}
Matrix transpose(Matrix a){
    int Nrows = a.rows(), Ncols = a.cols();
    Matrix new_mat(Ncols, Nrows);
    for (int i = 0; i < Nrows; i++){
        for (int j = 0; j < Ncols; j++){
            new_mat(j, i) = a(i, j);
        }
    }
    return new_mat;
}


class MatrixAndVector{
    private:
        int rows, cols;
    public:
        Matrix mat;
        std::vector<double> vec;

        MatrixAndVector(int rows, int cols) 
            : rows(rows), cols(cols), mat(rows, cols), vec(cols) {}

        int m_rows() { return rows; }
        int m_cols() { return cols; }
        
        void print_vector(int num = 0){
            int N = num;
            if (num == 0){N = rows;}
            for (int i = 0; i < N; i++){
                std::cout << vec.at(i) << "\t";
            }
            std::cout << std::endl;
        }

        void print_matrix(){
            mat.print_matrix();
        }
};

std::vector<double> operator+(std::vector<double> &a, std::vector<double> &b) {
    // overload matrix addition so we can easily add two matrices together
    std::vector<double> sum = a;
    for (int i = 0; i < (int)a.size(); i++) {
        sum[i] += b[i];
    }
    return sum;
}
std::vector<double> operator*(std::vector<double> &a, std::vector<double> &b) {
    // overload matrix addition so we can easily add two matrices together
    std::vector<double> mult = a;
    for (int i = 0; i < (int)a.size(); i++) {
        mult[i] *= b[i];
    }
    return mult;
}
std::vector<std::complex<double>> operator*(std::vector<std::complex<double>> a, std::vector<std::complex<double>> &b) {
    // overload matrix addition so we can easily add two matrices together
    std::vector<std::complex<double>> mult = a;
    for (int i = 0; i < (int)a.size(); i++) {
        mult[i] *= b[i];
    }
    return mult;
}
std::vector<double> operator*(Matrix a, std::vector<double> b){
    // square matrix * column vector multiplication
    int vec_size = (int)b.size();
    assert(a.cols() == vec_size);
    std::vector<double> new_vec(vec_size, 0.);
    for (int i = 0; i < vec_size; i++){
        for (int k = 0; k < vec_size; k++){
            new_vec[i] += a(i, k) * b[k];
        }
    }
    return new_vec;
}
std::vector<std::complex<double>> operator*(Matrix a, std::vector<std::complex<double>> b){
    // square matrix * column vector multiplication
    int vec_size = (int)b.size();
    assert(a.cols() == vec_size);
    std::vector<std::complex<double>> new_vec(vec_size, 0.);
    for (int i = 0; i < vec_size; i++){
        for (int k = 0; k < vec_size; k++){
            new_vec[i] += a(i, k) * b[k];
        }
    }
    return new_vec;
}
std::vector<double> operator*(std::vector<double> a, Matrix b){
    // row vector * square matrix multiplication
    int vec_size = (int)a.size();
    assert(b.rows() == vec_size);
    std::vector<double> new_vec(vec_size, 0.);
    for (int i = 0; i < vec_size; i++){
        for (int k = 0; k < vec_size; k++){
            new_vec[i] += a[k] * b(k, i);
        }
    }
    return new_vec;
}
std::vector<std::complex<double>> operator*(std::vector<std::complex<double>> a, Matrix b){
    // row vector * square matrix multiplication
    int vec_size = (int)a.size();
    assert(b.rows() == vec_size);
    std::vector<std::complex<double>> new_vec(vec_size, 0.);
    for (int i = 0; i < vec_size; i++){
        for (int k = 0; k < vec_size; k++){
            new_vec[i] += a[k] * b(k, i);
        }
    }
    return new_vec;
}
double dot_product(std::vector<double> a, std::vector<double> b){
    assert((int)a.size() == (int)b.size());
    double sum = 0.;
    for (int i = 0; i < (int)a.size(); i++){
        sum += a[i] * b[i];
    }
    return sum;
}
double dot_product(std::vector<std::complex<double>> a, std::vector<std::complex<double>> b){
    int a_size = (int)a.size();
    assert(a_size == (int)b.size());
    std::complex<double> sum = 0.;
    for (int i = 0; i < a_size; i++){
        sum += conj(a[i]) * b[i];
    }
    // double sum_double = norm(sum);
    double sum_double = sum.real();
    return sum_double;
}


std::vector<std::vector<std::complex<double>>> operator*(Matrix a, std::vector<std::vector<std::complex<double>>> b){
    assert(a.rows() == (int)b.size() && a.cols() == (int)b[0].size());
    std::vector<std::vector<std::complex<double>>> new_mat((int)b.size(), std::vector<std::complex<double>> ((int)b[0].size(), 0.));
    for (int i = 0; i < a.rows(); i++){
        for (int j = 0; j < a.cols(); j++){
            for (int k = 0; k < a.rows(); k++){
                new_mat[i][j] += a(i, k) * b[k][j];
            }
        }
    }
    return new_mat;
}
std::vector<std::vector<std::complex<double>>> operator*(std::vector<std::vector<std::complex<double>>> a, Matrix b){
    assert(b.rows() == (int)a.size() && b.cols() == (int)a[0].size());
    std::vector<std::vector<std::complex<double>>> new_mat((int)a.size(), std::vector<std::complex<double>> ((int)a[0].size(), 0.));
    for (int i = 0; i < b.rows(); i++){
        for (int j = 0; j < b.cols(); j++){
            for (int k = 0; k < b.rows(); k++){
                new_mat[i][j] += a[i][k] * b(k, j);
            }
        }
    }
    return new_mat;
}
std::vector<std::complex<double>> operator*(std::vector<std::vector<std::complex<double>>> a, std::vector<std::complex<double>> b){
    // square matrix * column vector multiplication
    int vec_size = (int)b.size();
    assert((int)a.size() == vec_size);
    std::vector<std::complex<double>> new_vec(vec_size, 0.);
    for (int i = 0; i < vec_size; i++){
        for (int k = 0; k < vec_size; k++){
            new_vec[i] += a[i][k] * b[k];
        }
    }
    return new_vec;
}