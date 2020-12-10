#include <iostream>
#include "circle.h"

using namespace std;


int main(){

    cout << "Object Demo." << endl;

    Circle *c = new Circle(1);
    cout << c->getRadius() << endl;
    cout << c->getArea() << endl;

    c->setRadius(2);
    cout << c->getArea() << endl;

    Circle c2(5);
    cout << c2.getArea() << endl;

    return 0;
}

