CC=gcc
CFLAGS = -g -Wall
#LDFLAGS = -lm

main: main.o myfunc.o myobj.o mythread.o
	gcc main.o myfunc.o myobj.o mythread.o -o main -lpthread

main.o: main.c
	gcc -c main.c

myfunc.o: myfunc.c
	gcc -c myfunc.c

myobj.o: myobj.c
	gcc -c myobj.c

mythread.o: mythread.c
	gcc -c mythread.c
run: main
	./main

clean:
	rm -rf *.o
