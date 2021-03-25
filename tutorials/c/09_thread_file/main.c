#include <stdio.h>
#include <time.h>
#include "mythread.h"



int main(void){
    // thread - external file
    pthread_t tid2;
    int ret = pthread_create(&tid2, NULL, externalFileThread, NULL);
    printf("pthread_create() return: %d\n", ret);
    
    void *status;
    ret = pthread_join(tid2, &status);
    printf("pthread_join() return: %d\n", ret);

}
