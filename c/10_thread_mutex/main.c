#include <stdio.h>
#include <time.h>
#include "mythread.h"


int main(void){

    // thread - mutex lock
    pthread_t tid3, tid4;
    pthread_mutex_init(&mutex, NULL);
    pthread_create(&tid3, NULL, mutexDemoThread, NULL);
    pthread_create(&tid4, NULL, mutexDemoThread2, NULL);
    pthread_join(tid3, NULL);
    pthread_join(tid4, NULL);

    pthread_t tidA, tidB;
    pthread_mutex_init(&mutex2, NULL);
    param_t paramA = {3, "threadA"};
    pthread_create(&tidA, NULL, mutexDemoThreadWithArgs, (void*)&paramA);
    param_t paramB = {4, "threadB"};
    pthread_create(&tidB, NULL, mutexDemoThreadWithArgs, (void*)&paramB);

    pthread_exit(NULL);


}
