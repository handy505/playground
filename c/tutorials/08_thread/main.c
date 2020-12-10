#include <stdio.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>


void *printTimeThread(void *arg){
    unsigned char counter = 0;
    while(counter < 5){
        time_t now;
        time( &now );
        printf("printTimeThread: %ld\n", now);
        counter++;
        sleep(1);
    }
}

int main(void){

    // thread - normal
    pthread_t tid;
    int ret = pthread_create(&tid, NULL, printTimeThread, NULL);
    printf("pthread_create() return: %d\n", ret);

    void *status;
    ret = pthread_join(tid, &status);
    printf("pthread_join() return: %d\n", ret);

}
