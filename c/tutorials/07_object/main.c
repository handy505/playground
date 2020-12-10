#include <stdio.h>
#include "circle.h"

int main(void){

    struct Circle c;
    newCircle(&c, 1.0);
    printf("circle area: %f with radius: %f\n", c.area(&c), c.getRadius(&c));    
    c.setRadius(&c, 2.0);
    printf("circle area: %f with radius: %f\n", c.area(&c), c.getRadius(&c));

}
