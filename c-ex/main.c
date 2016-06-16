#include <stdio.h>
#include <time.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <unistd.h>
#include "myfunc.h"

int add(int arg1, int arg2){
    return arg1 + arg2;
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
    // perfermence
    // object
    // thread - normal
    // thread - external file
    // thread - mutex lock
    return 0;
}
