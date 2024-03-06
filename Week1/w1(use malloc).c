//chatgpt 幫我· malloc is used to make it easier for computing a bigger matrix.
#include <stdio.h>
#include <stdlib.h>

void inputMatrix(double* matrix, int rows, int cols) {
    for(int i = 0; i < rows; i++) {
        for(int j = 0; j < cols; j++) {
            printf("Element [%d][%d]: ", i+1, j+1);
            scanf("%lf", &matrix[i*cols + j]);
        }
    }
}
double* Transpose(double* matrix, int rows, int cols) {
    double* transposed = (double*) malloc(cols * rows * sizeof(double));
    if (transposed == NULL) {
        printf("Memory allocation failed for transposed matrix\n");
        exit(1); 
    }

    for(int i = 0; i < rows; i++) {
        for(int j = 0; j < cols; j++) {
            transposed[j*rows + i] = matrix[i*cols + j];
        }
    }
    
    return transposed;
}
double* Add(double* matrix1, double* matrix2, int rows, int cols) {
    double* sum = (double*) malloc(rows * cols * sizeof(double));
    if (sum == NULL) {
        printf("Memory allocation failed for sum matrix\n");
        exit(1);
    }

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            sum[i*cols + j] = matrix1[i*cols + j] + matrix2[i*cols + j];
        }
    }

    return sum;
}
double* Multiply(double* matrix1, int rows1, int cols1, double* matrix2, int rows2, int cols2) {
    if (cols1 != rows2) {
        printf("MULTIPLICATION ERROR : The number of columns of Matrix 1 must equal the number of rows of Matrix 2 for multiplication!\n");
        exit(1);
    }

    double* product = (double*)malloc(rows1 * cols2 * sizeof(double));
    if (product == NULL) {
        printf("Memory allocation failed for product matrix\n");
        exit(1);
    }

    for (int i = 0; i < rows1; i++) {
        for (int j = 0; j < cols2; j++) {
            product[i*cols2 + j] = 0; 
            for (int k = 0; k < cols1; k++) {
                product[i*cols2 + j] += matrix1[i*cols1 + k] * matrix2[k*cols2 + j];
            }
        }
    }

    return product;
}
double* reshape(double* matrix, int original_rows, int original_cols, int new_rows, int new_cols) {
    double* reshaped = (double*)malloc(new_rows * new_cols * sizeof(double));
    if (original_rows * original_cols != new_rows * new_cols) {
        printf("Reshape ERROR: total number not same.\n");
        exit(1);
    }

    for (int i = 0; i < original_rows * original_cols; i++) {
        int row = i / original_cols;
        int col = i % original_cols;
        int new_index = row * original_cols + col;
        reshaped[new_index] = matrix[i];
    }
    return reshaped;
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

int main() {
    int rows1=2, cols1=2, rows2=2, cols2=2;
    double *matrix1, *matrix2,*transposed1, *transposed2,*sum,*product,*Remake;

    matrix1 = (double*) malloc(rows1 * cols1 * sizeof(double));
    if (matrix1 == NULL) {
        printf("Memory allocation failed for Matrix 1\n");
        return 1;
    }
    matrix2 = (double*) malloc(rows2 * cols2 * sizeof(double));
    if (matrix2 == NULL) {
        printf("Memory allocation failed for Matrix 2\n");
        free(matrix1); 
        return 1;
    }
    matrix1[0] = 1; matrix1[1] = 2;
    matrix1[2] = 3; matrix1[3] = 4;

    matrix2[0] = 5; matrix2[1] = 6;
    matrix2[2] = 7; matrix2[3] = 8;
    
    printf("Matrix 1:\n");
    printMatrix(matrix1, rows1, cols1);
    printf("Matrix 2:\n");
    printMatrix(matrix2, rows2, cols2);

    transposed1 = Transpose(matrix1, rows1, cols1);
    transposed2 = Transpose(matrix2, rows2, cols2);
    printf("Transposed Matrix 1:\n");
    printMatrix(transposed1, cols1, rows1);
    printf("Transposed Matrix 2:\n");
    printMatrix(transposed2, cols2, rows2);

    if (rows1 != rows2 || cols1 != cols2) {
        printf("ADD ERROR: Addition not performed due to dimension mismatch.\n");
    } else {
        sum = Add(matrix1, matrix2, rows1, cols1);
        printf("Sum of Matrix 1 and Matrix 2:\n");
        printMatrix(sum, rows1, cols1);
    }
    
    if (cols1 != rows2) {
        printf("MULTIPLY ERROR: Multiplication not performed due to dimension mismatch.\n");
    } else {
        product = Multiply(matrix1, rows1, cols1, matrix2, rows2, cols2);
        printf("Product of Matrix 1 and Matrix 2:\n");
        printMatrix(product, rows1, cols2);
    }
    Remake=reshape(matrix1, rows1, cols1, 1, 4);
    printf("Reshaped Matrix 1 (1x4):\n");
    printMatrix(Remake, 1, 4);

    return 0;
}