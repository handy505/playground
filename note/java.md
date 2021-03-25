## JDK installation, on ubuntu


### download
http://www.oracle.com/technetwork/java/javase/downloads


### unzip
`tar -zxvf jdk-xxx.tar.gz`  


### copy to `/usr/lib/jdk`
`sudo cp -r ~/Downloads/jdk-xxx/. /usr/lib/jdk/`  
if need, create the jdk folder


### env variable, `~/.bashrc`, or  `/etc/profile`(not test)
```
export JAVA_HOME=/usr/lib/jdk/jdk1.8.0_65
export JRE_HOME=/usr/lib/jdk/jdk1.8.0_65/jre
export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
export CLASSPATH=$CLASSPATH:.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
```

### default jdk setting
```
sudo update-alternatives --install /usr/bin/java java /usr/lib/jdk/jdk1.8.0_65/bin/java 300
sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jdk/jdk1.8.0_65/bin/javac 300
sudo update-alternatives --config java
sudo update-alternatives --config javac
```

### check version
`java -version`  
show below:
```
java version "1.8.0_65"
Java(TM) SE Runtime Environment (build 1.8.0_65-b17)
Java HotSpot(TM) 64-Bit Server VM (build 25.65-b01, mixed mode)
```

### NetBean installation


### NetBeans font type  
Tools/Options/Fonts & Colors
select Font as **Droid Sans Mono**


### NetBeans font AntiAliasing
http://blog.lyhdev.com/2013/11/netbeans-ide-on-ubuntu-linux.html  
enable the **AntiAliasing** effect via modify the conf   file `~/netbeans-8.1/etc/netbeans.conf`  
search the string: **netbeans_default_options**  
add configuration: **-J-Dswing.aatext=true** and **-J-Dawt.useSystemAAFontSettings=lcd** at tail  
look like below:
```
netbeans_default_options="-J-client -J-Xss2m -J-Xms32m -J-Dapple.laf.useScreenMenuBar=true -J-Dappl    e.awt.graphics.UseQuartz=true -J-Dsun.java2d.noddraw=true -J-Dsun.java2d.dpiaware=true -J-Dsun.zip.    disableMemoryMapping=true -J-Dswing.aatext=true -J-Dawt.useSystemAAFontSettings=lcd"
```

## About java Error: Could not find or load main class xxx

	handy@handy-dell ~/democode/java-ex/main $ ls
	Main.java
	handy@handy-dell ~/democode/java-ex/main $ cat Main.java
	package main;

	public class Main {
	    public static void main(String[] args) {
		System.out.println("hello java");
	    }
	}
	handy@handy-dell ~/democode/java-ex/main $ javac Main.java
	handy@handy-dell ~/democode/java-ex/main $ ls
	Main.class  Main.java
	handy@handy-dell ~/democode/java-ex/main $ java Main
	錯誤: 找不到或無法載入主要類別 Main
	handy@handy-dell ~/democode/java-ex/main $

it is due to namespace setting(package), excute java should notice the **location relation** between the directorys.  
for example:


	handy@handy-dell ~/democode/java-ex/main $ ls
	Main.class  Main.java
	handy@handy-dell ~/democode/java-ex/main $ cd ..
	handy@handy-dell ~/democode/java-ex $ ls
	main
	handy@handy-dell ~/democode/java-ex $ java main.Main
	hello java
	handy@handy-dell ~/democode/java-ex $
