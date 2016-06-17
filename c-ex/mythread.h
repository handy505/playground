#ifndef MYTHREAD_H_INCLUDED
#define MYTHREAD_H_INCLUDED

#include <pthread.h>

void *externalFileThread(void *arg);

void *mutexDemoThread(void * arg);

void *mutexDemoThread2(void * arg);

pthread_mutex_t mutex;
#endif
