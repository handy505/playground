#ifndef MYTHREAD_H_INCLUDED
#define MYTHREAD_H_INCLUDED

#include <pthread.h>

void *externalFileThread(void *arg);

void *mutexDemoThread(void * arg);

void *mutexDemoThread2(void * arg);

void *mutexDemoThreadWithArgs(void * arg);

pthread_mutex_t mutex;
pthread_mutex_t mutex2;

typedef struct param{
    int number;
    char threadName[32];
}param_t;

#endif
