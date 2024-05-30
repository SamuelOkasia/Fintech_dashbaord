#include <stdio.h>
#include <stdlib.h>

int main() {
    int months = 12;
    double profits[12] = {1000, -500, 1500, -1000, 2000, -750, 2500, -1200, 3000, -1500, 3500, -2000};
    double losses[12] = {0};

    for (int i = 0; i < months; i++) {
        if (profits[i] < 0) {
            losses[i] = -profits[i];
            profits[i] = 0;
        }
    }

    printf("[");
    for (int i = 0; i < months; i++) {
        printf("{\"month\":%d,\"profit\":%.2f,\"loss\":%.2f}", i + 1, profits[i], losses[i]);
        if (i < months - 1) {
            printf(",");
        }
    }
    printf("]");

    return 0;
}
