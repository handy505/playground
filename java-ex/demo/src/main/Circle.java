package main;

public class Circle{
	private int x = 0;
	private int y = 0;
	private float r = 1;

	public Circle(float r){ 
		this.r = r;
	}   

	public void setRadius(float r){ 
		if (r > 0)  this.r = r;
		else        this.r = 1;
	}   

	public float getRadius(){
		return this.r;
	}   

	public double getArea(){
		return this.r * this.r * java.lang.Math.PI;                                                                  
	}   
}

