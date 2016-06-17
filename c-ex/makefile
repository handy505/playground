CC=gcc
CFLAGS = -g -Wall
#LDFLAGS = -lm

main: main.o myfunc.o myobj.o
	gcc main.o myfunc.o myobj.o -o main	

main.o: main.c
	gcc -c main.c

myfunc.o: myfunc.c
	gcc -c myfunc.c

myobj.o: myobj.c
	gcc -c myobj.c

run: main
	./main

clean:
	rm -rf *.o
