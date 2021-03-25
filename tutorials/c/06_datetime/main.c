#include <stdio.h>
#include <time.h>

int main(void){

    time_t now;
    time(&now);
    printf("now in seconds: %ld\n", now);
    printf("ctime: %s", ctime(&now));



    time_t t = time(NULL);
    struct tm *tm = localtime(&t);
    printf("%p\n", &t);
    printf("%p\n", tm);

    char s[64];
    strftime(s, sizeof(s), "%Y-%m-%d %H:%M:%S", tm);
    printf("%s\n", s);

}

/*
$ ./a.out 
now in seconds: 1607505281
ctime: Wed Dec  9 17:14:41 2020
0x7fff7e852020
0x7fc5d2d871c0
2020-12-09 17:14:41
*/
