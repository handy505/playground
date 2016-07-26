package main;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.io.FileWriter;
import java.io.IOException;

import main.MyObj;
import main.Circle;
import main.MyThreadNormal;
import main.MutexDemoThread;


public class Main implements Runnable {
	
	public Integer num = 0;
	private Object lock = new Object();
	public Object getLock(){ return lock; }

	private int add(int arg1, int arg2){
		return arg1 + arg2;
	}

	public void run(){

		// hello
       	System.out.println("hello java");

		// function call (method)
		int var1 = add(2, 3);
		System.out.println("local function call: " + var1);

		// external function call
		MyObj obj = new MyObj();
		int var2 = obj.add(3, 4);
		System.out.println("external function call: " + var2);

		// timestamp
		String strdate = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(new Date());
		System.out.println(strdate);
		
		// hardware access
		

		// file
		try( FileWriter fw = new FileWriter("abc.txt", true) ){
			fw.write("abcdefg\n");
			fw.flush();
		}catch(IOException e){ System.out.println( e.toString() ); }

		// perfermence
		long start = System.currentTimeMillis();
		/*try{ Thread.sleep(1000);}
		catch(Exception e){System.out.println(e.toString());}*/
		for(int i=0; i<1000000; i++){
			double ans = java.lang.Math.sqrt(2);
		}
		long end = System.currentTimeMillis();
		System.out.println("elapsed time: " + (end - start) );
		
		// object
		Circle c = new Circle(2);
		System.out.println(c.getArea());

		// thread - normal
		MyThreadNormal mtn = new MyThreadNormal();
		Thread normalThread = new Thread(mtn);
		normalThread.start();

		try{
			normalThread.join();
		}catch(Exception e){ System.out.println(e.toString()); }


		// thread - external file
		// thread - mutex lock

		MutexDemoThread mdt1 = new MutexDemoThread(1, this, num);
		Thread mutexThread1 = new Thread(mdt1);
		MutexDemoThread mdt2 = new MutexDemoThread(2, this, num);
		Thread mutexThread2 = new Thread(mdt2);

		mutexThread1.start();
		mutexThread2.start();

		try{
			mutexThread1.join();
			mutexThread2.join();
		}catch(Exception e){ System.out.println(e.toString()); }

	}

    public static void main(String[] args) {

		Main m = new Main();
		Thread mainthread = new Thread(m);
		mainthread.start();

		try{
			mainthread.join();
		}catch(Exception e){
			System.out.println(e.toString());
		}

    }
}
