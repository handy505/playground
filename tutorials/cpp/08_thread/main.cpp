#include <iostream>
#include <thread>

using namespace std;

void task1(){
    cout << "task1" << endl;
}

void task2(string x){
    cout << "task2 with " << x << endl;
}

int main(){

    cout << "Thread Demo." << endl;
    thread th1(task1);
    thread th2(task2, "hello");

    th1.join();
    th2.join();


    return 0;
}

