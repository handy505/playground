#include <iostream>

int add(int a, int b){
    return a + b;
}


int main(){
    std::cout << "Hello C++\n";
    int ret = add(2, 3);
    std::cout << ret << "\n";
    return 0;
}

/*
$ g++ main.cpp 
$ ./a.out 
Hello C++
5

*/
