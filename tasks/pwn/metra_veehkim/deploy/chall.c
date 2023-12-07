#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <linux/mman.h>

const char allowed[] = " Metra_Veehkim";

int check(char c) {
    for (int i = 0; i < strlen(allowed); ++i) {
        if (allowed[i] == c) return 1;
    }
    return 0;
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    char token[0x40] = {};
    printf("Task token: ");
    int _n = read(0, &token, 0x40-1);
    if (_n > 0 && token[_n-1] == '\n') token[_n-1] = 0;
    
    if (strcmp(token, getenv("TOKEN")) != 0) {
        puts("Invalid task token");
        return 0;
    }

    char *addr = 0;
    printf("Address: ");
    scanf("%lu%*c", &addr);
    char *mem = mmap(addr, 0x2000, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    if (mem == MAP_FAILED) {
        puts("Invalid address");
        return 0;
    }
    memset(mem, 0, 0x2000);
    printf("Code: ");
    int n = read(0, addr, 0x1000);
    if (n < 1) {
        puts("Invalid code");
        return 0;
    }
    if (addr[n-1] == '\n') addr[n-1] = 'a';
    for (int i = 0; i < n; ++i) {
        if (!check(addr[i])) {
            puts("Invalid code");
            return 0;
        }
    }
    ((void (*)())addr)();
}