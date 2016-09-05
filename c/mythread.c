#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <string.h>
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

void *mutexDemoThreadWithArgs(void * arg){
    // get parameter
    //int number = (int)((param_t)arg)->number;
    //int number = (int)arg->number;
    int number = ((struct param*)arg)->number;
    char threadName[32];
    strncpy(threadName,((struct param*)arg)->threadName, sizeof(((struct param*)arg)->threadName));

    int i = 0;
    pthread_mutex_lock(&mutex2);
    while(i < 5){
        i++;
        num++;
        sleep(1);
        printf("%s) %d\n",threadName, num);
    }
    pthread_mutex_unlock(&mutex2);
}
