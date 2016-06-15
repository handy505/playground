CC=gcc
CFLAGS = -g -Wall -O0
LDFLAGS = -lm

main : main.o myfunc.o
	$(CC) $(LDFLAGS) -o $@ $^
	
main.o : main.c
	$(CC) $(LDFLAGS) -o $@ $<

myfunc.o : myfunc.c
	$(CC) $(LDFLAGS) -o $@ $<
