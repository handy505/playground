#include <iostream>
#include <ctime>
#include <unistd.h>
using namespace std;

void task1(){
    cout << "task1" << endl;


    for(int i=0; i<5; i++){

        time_t now = time(0);
        tm *dt = localtime(&now);
        int hour   = dt->tm_hour;
        int minute = dt->tm_min;
        int second = dt->tm_sec;

        cout << hour << ":" << minute << ":" << second << endl;
        sleep(1);

    }


}

