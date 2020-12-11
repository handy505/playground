#include <iostream>
#include <fstream>

using namespace std;

int main(){

    cout << "Write file." << endl;

    fstream fd;
    fd.open("demo.txt", ios::out);
    fd << "This is a demo string." << endl;
    fd.close();

    return 0;
}

