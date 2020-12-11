#include <iostream>
#include "myfunc.h"


int main(){
    std::cout << "Hello C++\n";
    int ret = add(2, 3);
    std::cout << ret << "\n";
    return 0;
}

/*
$ g++ -o main main.cpp myfunc.cpp 
$ ./main
Hello C++
5
*/
