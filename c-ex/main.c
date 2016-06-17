#include <stdio.h>
#include <time.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <unistd.h>
#include <math.h>
#include <pthread.h>
#include "myfunc.h"
#include "myobj.h"
#include "mythread.h"


int add(int arg1, int arg2){
    return arg1 + arg2;
}

void *printTimeThread(void *arg){
    unsigned char counter = 0;
    while(counter < 5){
        time_t now;
        time( &now );
        printf("printTimeThread: %d\n", now);
        counter++;
        sleep(1);
    }
}

int main(void){
    printf("hello C\n");

    // function call
    int var1 = add(2, 3);
    printf("current file function call: %d\n", var1);

    // cross file function call
    int var2 = addition(3, 4);
    printf("external file function call: %d\n", var2);

    // timestamp
    time_t now;
    time(&now);
    printf("now in seconds: %d\n", now);
    printf("ctime: %s", ctime(&now));

    struct tm *ptrUTCTm, *ptrLocalTm, *ptrtm;
    char buf[64];
    ptrUTCTm = gmtime(&now);
    if( strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", ptrUTCTm)){
        printf("utc time: %s\n", buf);
    }
        
    ptrLocalTm = localtime(&now);
    if( strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S, UTC %z", ptrLocalTm)){
        printf("local time: %s\n", buf);
    }

    // hardware access: mac address, via socket's ioctl()
    int fd;
    struct ifreq ifr;
    char *iface = "eth0";
    unsigned char *mac;

    fd = socket(AF_INET, SOCK_DGRAM, 0);
    ifr.ifr_addr.sa_family = AF_INET;
    strncpy(ifr.ifr_name, iface, IFNAMSIZ - 1);
    ioctl(fd, SIOCGIFHWADDR, &ifr);
    close(fd);
    mac = (unsigned char *)ifr.ifr_hwaddr.sa_data;
    printf("mac: %.2x:%.2x:%.2x:%.2x:%.2x:%.2x\n", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

    // file
    FILE *fp = fopen("abc.txt", "w");
    fprintf(fp, "%s\n", "abcdef");
    fclose(fp);

    // perfermence
    clock_t t1, t2;
    t1 = clock();
    int i = 0;
    float ans;
    for(i=0; i<100000; i++){
        ans = sqrt(2);
    }
    t2 = clock();
    printf("ans: %f, ticks: %d\n", ans, t2-t1);

    // object
    struct Circle c;
    newCircle(&c, 1.0);
    printf("circle area: %f with radius: %f\n", c.area(&c), c.getRadius(&c));    
    c.setRadius(&c, 2.0);
    printf("circle area: %f with radius: %f\n", c.area(&c), c.getRadius(&c));

    // thread - normal
    pthread_t tid;
    int ret = pthread_create(&tid, NULL, printTimeThread, NULL);
    printf("pthread_create() return: %d\n", ret);

    /*
    void *status;
    ret = pthread_join(tid, &status);
    printf("pthread_join() return: %d\n", ret);
    */

    // thread - external file
    pthread_t tid2;
    ret = pthread_create(&tid2, NULL, externalFileThread, NULL);
    printf("pthread_create() return: %d\n", ret);
    
    // thread - mutex lock
    pthread_exit(NULL);
    return 0;
}
