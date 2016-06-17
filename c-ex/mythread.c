#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include "mythread.h"


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

int num = 0;

//pthread_cond_t cond;

void *mutexDemoThread(void * arg){
    int i = 0;
    //pthread_mutex_init(&mutex, NULL);
    pthread_mutex_lock(&mutex);
    //pthread_cond_wait(&cond, &mutex);
    while(i < 5){
        i++;
        num++;
        sleep(1);
        printf("1) %d\n", num);
    }
    pthread_mutex_unlock(&mutex);
    //pthread_mutex_destroy(&mutex);
}

void *mutexDemoThread2(void * arg){
    int i = 0;
    //pthread_mutex_init(&mutex, NULL);
    pthread_mutex_lock(&mutex);
    //pthread_cond_wait(&cond, &mutex);
    while(i < 5){
        i++;
        num++;
        sleep(1);
        printf("2) %d\n", num);
    }
    pthread_mutex_unlock(&mutex);
    //pthread_mutex_destroy(&mutex);
}
