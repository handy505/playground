#include <iostream>
#include <ctime>

using namespace std;

int main(){

    cout << "Datetime Demo." << endl;

    time_t now = time(0);
    cout << now << endl;

    tm *dt = localtime(&now);

    int year   = 1900 + dt->tm_year;
    int month  = 1 + dt->tm_mon;
    int day    = dt->tm_mday;
    int hour   = dt->tm_hour;
    int minute = dt->tm_min;
    int second = dt->tm_sec;

    cout << year << "-" << month << "-" << day  << " "
         << hour << ":" << minute << ":" << second << endl;


    return 0;
}

