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


// constructor
Circle::Circle(){
    radius = 1;
}

Circle::Circle(int r){
    radius = r;
}


// method
void Circle::setRadius(int r){
    radius = r;
}

int Circle::getRadius(){
    return radius;
}

double Circle::getArea(){
    double result = radius * radius * 3.14;
    return result;
}

