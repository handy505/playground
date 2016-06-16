CC=gcc
CFLAGS = -g -Wall
#LDFLAGS = -lm

main: main.o myfunc.o
	gcc main.o myfunc.o -o main	

main.o: main.c
	gcc -c main.c

myfunc.o : myfunc.c
	gcc -c myfunc.c

clean:
	rm -rf *.o
