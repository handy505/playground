#include <stdio.h>
#include "myfunc.h"

int add(int arg1, int arg2){
    return arg1 + arg2;
}

int main(void){
    printf("hello C\n");

    // function call
    int var1 = add(2, 3);
    printf("current file function call: %d\n", var1);

    // cross file function call
    int var2 = addition(3, 4);
    printf("external file function call: %d\n", var2);
    // timestamp
    // hardware access: mac address
    return 0;
}
