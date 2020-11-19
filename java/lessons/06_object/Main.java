import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main{
    public static void main(String[] args){
        Circle c = new Circle(0,0,1);
        System.out.println(c.get_area());

    }
}


class Circle{
    private int x;
    private int y;
    private int r;

    Circle(int x, int y, int r){
        this.x = x;
        this.y = y;
        this.r = r;
    }

    public double get_area(){
        return r * r * 3.14;
    }

}
