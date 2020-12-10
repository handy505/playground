#ifndef _CIRCLE_H_
#define _CIRCLE_H_

class Circle{
    private:
        int radius;

    public:
        Circle();
        Circle(int r);
        void setRadius(int r);
        int getRadius();
        double getArea();
};

#endif
