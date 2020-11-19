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
