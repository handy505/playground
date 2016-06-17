#include <stdio.h>
#include <time.h>
#include <unistd.h>

void *externalFileThread(void *arg){
    unsigned char counter = 0;
    while(counter < 5){
        time_t now;
        time( &now );
        printf("externalFileThread: %d\n", now);
        counter++;
        sleep(1);
    }
}

