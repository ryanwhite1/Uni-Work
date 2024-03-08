# include <vector>
# include <cmath>
# include <iostream>
# include <cassert> // for assert(), used in matrix example
# include "bspline.hpp"



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

Matrix operator+(Matrix &a, Matrix &b) {
    // overload matrix addition so we can easily add two matrices together
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
            mat_and_vec.mat.at(i, j) = matcopy.at(i, j);
        }
        mat_and_vec.vec.at(dimension-i-1) = evals.at(dimension-i-1);
    }

    for (int i = 0; i < dimension; i++){
        for (int j = 0; j < dimension; j++){
            mat_and_vec.mat.at(i, j) = matcopy.at(i, j);
        }
        mat_and_vec.vec.at(dimension-i-1) = evals.at(dimension-i-1);
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

double trapezoid_area(double x1, double x2, double y1, double y2){
    // calculates the area of a single trapezoid
    return 0.5 * (y1 + y2) * fabs(x2 - x1);
}
double trapezoid_integration(std::vector<double> x, std::vector<double> y){
    // calculates the area under the curve (with the trapezoid rule) by points specified by (x,y)
    int N = x.size();
    double run_total = 0.;
    for (int i = 0; i < N-1; i++){
        run_total += trapezoid_area(x[i], x[i+1], y[i], y[i+1]);
    }
    return run_total;
}
double Bspl_deriv(BSpline bspline, int i, double r){
    // Approximates the bspline derivative value over a very small interval
    double dr = 5.e-7;
    return (bspline.b(i, r + dr/2.) - bspline.b(i, r - dr/2.)) / dr;
}

double hydrogen_like_potential(double r, int l, double Z){
    // potential for our Hydrogen-like atoms
    return -Z/r + l * (l + 1.) / (2. * r*r);
}
double hydrogen_potential(double r, int l){return hydrogen_like_potential(r, l, 1.);}
double lithium_potential(double r, int l){return hydrogen_like_potential(r, l, 3.);}

void populate_Hamiltonian(Matrix &mat, std::vector<double> r, BSpline bspline, int l, double (*potential)(double, int)){
    int N = mat.cols();
    int r_N = r.size();
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            std::vector<double> int1(r_N), int2(r_N);
            for (int k = 0; k < r_N; k++){
                int1[k] = Bspl_deriv(bspline, i+2, r[k]) * Bspl_deriv(bspline, j+2, r[k]);  // b'_i * b'_j
                int2[k] = bspline.b(i+2, r[k]) * potential(r[k], l) * bspline.b(j+2, r[k]); // b_i * V(r) * b_j
            }
            mat.at(i, j) = 0.5 * trapezoid_integration(r, int1) + trapezoid_integration(r, int2); 
        }
    }
}

void populate_B_Matrix(Matrix &mat, std::vector<double> r, BSpline bspline){
    int N = mat.cols();
    int r_N = r.size();
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            std::vector<double> int1(r_N), int2(r_N);
            for (int k = 0; k < r_N; k++){
                int1[k] = bspline.b(i+2, r[k]) * bspline.b(j+2, r[k]);
            }
            mat.at(i, j) = trapezoid_integration(r, int1);
        }
    }
}





int main(){

    // // PART A:
    // int dimension = 2; // N if we have NxN matrix

    // Matrix mat(2, 2);
    // for (int i = 0; i < dimension; i++){
    //     for (int j = 0; j < dimension; j++){
    //         mat.at(i, j) = 1. / (i + j + 1.);
    //     }
    // }
    // MatrixAndVector matvec = solveEigenSystem(mat, dimension);

    // std::cout << "Eigenvecs = {";
    // for (int i = 0; i < dimension; i++){
    //     std::cout << "{";
    //     for (int j = 0; j < dimension; j++){
    //         std::cout << matvec.mat.at(i, j);
    //         if (j < dimension-1){
    //             std::cout << ", ";
    //         }
    //     }
    //     if (i < dimension-1){
    //         std::cout << "}, " << std::endl;
    //     }
    // }
    // std::cout << "}}" << std::endl;

    // std::cout << "Eigenvals = {";
    // for (int i = 0; i < dimension; i++){
    //     std::cout << matvec.vec.at(i);
    //     if (i < dimension - 1){
    //         std::cout << ", ";
    //     }
    // }
    // std::cout << "}" << std::endl;

    

    // PART B:
    int N = 50;
    double r0 = 1.e-5;
    double rmax = 50.;
    int k_spline = 7;
    int l = 0;

    int r_N = 3000;
    std::vector<double> r(r_N);
    double step_size = (rmax - r0) / r_N;
    for (int i = 0; i < r_N; i++){
        r[i] = r0 + i * step_size;
    }

    BSpline bspl(k_spline, N, r0, rmax);

    int N_red = N - 3;
    Matrix matrix_H(N_red, N_red);
    Matrix matrix_B(N_red, N_red);
    populate_Hamiltonian(matrix_H, r, bspl, l, &lithium_potential);
    // matrix_H.print_matrix();
    populate_B_Matrix(matrix_B, r, bspl);
    
    MatrixAndVector matandvec = solveEigenSystem_AveBv(matrix_H, matrix_B, N_red);

    // matandvec.print_matrix();
    matandvec.print_vector(10); // print first 10 elements in vector
    

    return 0;
}