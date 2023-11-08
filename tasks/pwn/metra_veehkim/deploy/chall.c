#include <unistd.h>
#include <stdio.h>
#include <string.h>
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
    char *addr;
    printf("Address: ");
    scanf("%lu%*c", &addr);
    char *mem = mmap(addr, 0x2000, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    if (mem == MAP_FAILED) {
        puts("Invalid address");
        return 0;
    }
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