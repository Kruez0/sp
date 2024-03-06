//after understanding
#include <stdio.h>
#include <stdlib.h>
#define rows1 2
#define cols1 2
#define rows2 2
#define cols2 2
void inputMatrix(double* matrix, int rows, int cols) {
    for(int i = 0; i < rows; i++) {
        for(int j = 0; j < cols; j++) {
            printf("Element [%d][%d]: ", i+1, j+1);
            scanf("%lf", &matrix[i*cols + j]);
        }
    }
}
void Transpose(double* matrix, double*transposed, int rows, int cols) {
    for(int i = 0; i < rows; i++) {
        for(int j = 0; j < cols; j++) {
            transposed[j*rows + i] = matrix[i*cols + j];
        }
    }
}
void Add(double* matrix1, double* matrix2, double *sum, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            sum[i*cols + j] = matrix1[i*cols + j] + matrix2[i*cols + j];
        }
    }
}
void Multiply(double* matrix1, int rowz1, int colz1, double* matrix2, int rowz2, int colz2, double* product) {
    for (int i = 0; i < rowz1; i++) {
        for (int j = 0; j < colz2; j++) {
            product[i*colz2 + j] = 0; 
            for (int k = 0; k < colz1; k++) {
                product[i*colz2 + j] += matrix1[i*colz1 + k] * matrix2[k*colz2 + j];
            }
        }
    }
}
void printMatrix(double* matrix, int rows, int cols) {
    for(int i = 0; i < rows; i++) {
        printf("| ");
        for(int j = 0; j < cols; j++) {
            printf("%2.0lf|", matrix[i*cols + j]);
        }
        printf("\n");
    }
}
void reshape(double* matrix, double* reshaped, int original_rows, int original_cols, int new_rows, int new_cols) {
    if (original_rows * original_cols != new_rows * new_cols) {
        printf("Reshape ERROR: total number not same.\n");
        return;
    }

    for (int i = 0; i < original_rows * original_cols; i++) {
        int row = i / original_cols;
        int col = i % original_cols;
        int new_index = row * original_cols + col;
        reshaped[new_index] = matrix[i];
    }
}

int main() {
    double matrix1[] = {1, 2, 3, 4};
    double matrix2[] = {5, 6, 7, 8};
    double transposed1[rows1*cols1]; 
    double transposed2[rows2*cols2];
    double sum[rows1*cols1];
    double product[rows1*cols2];
    double reshaped[4*1];

    printf("Matrix 1:\n");
    printMatrix(matrix1, rows1, cols1);
    printf("Matrix 2:\n");
    printMatrix(matrix2, rows2, cols2);

    Transpose(matrix1,transposed1, rows1, cols1);
    Transpose(matrix2,transposed2, rows2, cols2);
    printf("Transposed Matrix 1:\n");
    printMatrix(transposed1, cols1, rows1);
    printf("Transposed Matrix 2:\n");
    printMatrix(transposed2, cols2, rows2);

    if (rows1 != rows2 || cols1 != cols2) {
        printf("ADD ERROR: dimension difference.\n");
    } else {
        Add(matrix1, matrix2, sum,rows1, cols1);
        printf("Sum of Matrix 1 and Matrix 2:\n");
        printMatrix(sum, rows1, cols1);
    }
    
    if (cols1 != rows2) {
        printf("MULTIPLY ERROR: dimension mismatch.\n");
    } else {
        Multiply(matrix1, rows1, cols1, matrix2, rows2, cols2, product);
        printf("Product of Matrix 1 and Matrix 2:\n");
        printMatrix(product, rows1, cols2);
    }
    reshape(matrix1, reshaped, rows1, cols1, 1, 4);
    printf("Reshaped Matrix 1 (1x4):\n");
    printMatrix(reshaped, 1, 4);
    return 0;
}