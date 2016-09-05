package main;

public class MyThreadNormal implements Runnable{
	public void run(){
		long start = System.currentTimeMillis();
		System.out.println("start: " + start);

		while( System.currentTimeMillis() - start < 5000){
			System.out.println(System.currentTimeMillis());
			try{ Thread.sleep(1000);}
			catch(Exception e){ System.out.println(e.toString()); }
		}
		System.out.println("exit MyThreadNormal");
	}
}
