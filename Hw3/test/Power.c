#include <stdio.h>
int power(int x, int n) {
    if (n == 0) {
        return 1;
    }
    else if (n < 0) {
        return 1 / power(x, -n);
    }
    return x * power(x, n - 1);
}
int main(){
    printf("power(3, 4) = %d \n", power(3, 4));
}