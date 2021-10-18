#include <time.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>

uint64_t fibonacci(uint64_t k) {
    if (k == 0 || k == 1){
        return 1;
    } else {
        return fibonacci(k - 1) + fibonacci(k - 2);
    }
}

int main() {
    clock_t begin = clock();
    printf("%" PRIu64 "\n", fibonacci(45));
    clock_t end1 = clock();
    printf("%" PRIu64 "\n", fibonacci(50));
    clock_t end2 = clock();
    printf("%" PRIu64 "\n", fibonacci(55));
    clock_t end3 = clock();

    double time_spent_1 = (double)(end1 - begin) / CLOCKS_PER_SEC;
    double time_spent_2 = (double)(end2 - end1) / CLOCKS_PER_SEC;
    double time_spent_3 = (double)(end3 - end2) / CLOCKS_PER_SEC;

    printf("Fibonacci 45: %f\n", time_spent_1);
    printf("Fibonacci 50: %f\n", time_spent_2);
    printf("Fibonacci 55: %f\n", time_spent_3);

    return 0;

/*
    1836311903
    20365011074
    225851433717
    Fibonacci 45: 10.952583
    Fibonacci 50: 82.760059
    Fibonacci 55: 877.220084
*/
}
