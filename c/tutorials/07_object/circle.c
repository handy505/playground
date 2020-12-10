#include <stdio.h>
#include "circle.h"

// member method 
float getArea(struct Circle *this){
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
    this->area = getArea;
    this->setRadius = setRadius;
    this->getRadius = getRadius;
    //this->radius = r;
    setRadius(this, r);
}




