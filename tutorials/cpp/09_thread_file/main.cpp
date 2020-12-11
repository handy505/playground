#include <iostream>
#include <thread>
#include <unistd.h>

#include "mythread.h"

using namespace std;


int main(){

    cout << "Thread Demo." << endl;

    thread th1(task1);
    th1.join();


    return 0;
}

