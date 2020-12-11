#include <iostream>
#include <thread>
#include <mutex>
#include <unistd.h>

using namespace std;

mutex mtx;


int print(char c){
    mtx.lock();
    for (int i=0; i<10; i++){
        cout << c;
        sleep(0.1);

    }
    cout << endl;
    mtx.unlock();
    return 0;
}

int main(){

    cout << "Thread Demo." << endl;

    thread th1(print, 'A');
    thread th2(print, 'B');
    
    th1.join();
    th2.join();


    return 0;
}

/*
output without mutex:
----------------------
Thread Demo.
AABAABBAABBAABBABA
BB


output with mutex:
-------------------
Thread Demo.
AAAAAAAAAA
BBBBBBBBBB
*/
