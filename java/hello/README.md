## Java compile / excute operation
source file: MyObj.java  

	package main;
	public class MyObj{...}

source file: Main.java  

	import main.MyObj;
	public class Main implements Runnable{...}


compile: `javac -sourcepath src/ -d classes/ src/Main.java`  
excute: `java -cp classes/ Main`  


	handy@handy-dell ~/democode/java-ex/demo $ ls -R
	.:
	classes  src

	./classes:
	main  Main.class

	./classes/main:
	MyObj.class

	./src:
	main  Main.java

	./src/main:
	MyObj.java
	handy@handy-dell ~/democode/java-ex/demo $ javac -sourcepath src/ -d classes/ src/Main.java
	handy@handy-dell ~/democode/java-ex/demo $ java -cp classes/ Main
	hello java
	local function call: 5
	external function call: 7

## another example

	handy@handy-dell ~/democode/java-ex/demo $ ls -R
	.:
	abc.txt  classes  README.md  src

	./classes:
	abc.txt  main

	./classes/main:
	Circle.class  Main.class  MutexDemoThread.class  MyObj.class  MyThreadNormal.class

	./src:
	main

	./src/main:
	Circle.java  Main.java  MutexDemoThread.java  MyObj.java  MyThreadNormal.java
	[2]+  Done                    atom README.md

in Main.java file

	package main;

	import main.MyObj;
	import main.Circle;
	import main.MyThreadNormal;
	import main.MutexDemoThread;

compile with: `javac -sourcepath src/ -d classes/ src/main/Main.java`  
excute with: `java -cp classes/ main.Main`  
