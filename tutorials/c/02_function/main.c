#include <stdio.h>

int add(int a, int b){
    return a + b;
}

int main(void){
    int ret = add(2,3);
    printf("%d\n", ret);
    return 0;
}
