#include <stdio.h>

int main(void){

    FILE *fp = fopen("demo.txt", "w");
    fprintf(fp, "%s\n", "this is a demo string");
    fclose(fp);

}
