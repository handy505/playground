package main;

import main.Main;

public class MutexDemoThread implements Runnable{
	private Object lock = null;
	private Integer num = null;
	private Main main;
	private int threadId;
	public MutexDemoThread(int threadId, Main main, Integer num){
	//public MutexDemoThread(int threadId, Integer num){
		this.main = main;
		this.num = num;
		this.threadId = threadId;
	}

	public void run(){
		System.out.println("threadId: " + threadId + ", num: " + main.num);

		for(int i=0; i<5; i++){
			main.num += 1;
			System.out.println("threadId: " + threadId + ", num: " + main.num);
		
			try{ Thread.sleep(1000);}
			catch(Exception e){ System.out.println(e.toString()); }
		}

	}
}
