#include <stdio.h>
#include "myobj.h"

// member method 
float circleArea(struct Circle *this){
    return 3.14 * this->radius * this->radius;
}

void setRadius(struct Circle *this, float arg){
    this->radius = arg;
}

float getRadius(struct Circle *this){
    return this->radius;
}

// constructure
void newCircle(struct Circle *this, float r){
    this->new = newCircle;
    this->area = circleArea;

    this->setRadius = setRadius;
    this->getRadius = getRadius;
    //this->radius = r;
    setRadius(this, r);

}




