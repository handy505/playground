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
