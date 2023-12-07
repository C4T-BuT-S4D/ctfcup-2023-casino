#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <sys/fcntl.h>

typedef struct {
    unsigned long id;
    unsigned long val;
} item;

#define MAX_SIZE 0x4000
#define MAX_VAL  0x1000
item storage[MAX_SIZE];

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

    srand(time(0));
    unsigned int cnt = 0;
    char c[2] = {};

    while (1) {
        printf("Count: ");
        scanf("%d%*c", &cnt);
        if (cnt == 0 || cnt > MAX_SIZE) {
            puts("Count is too big");
            continue;
        }
        for (int i = 0; i < cnt; ++i) {
            storage[i].id = i+1;
            storage[i].val = 0;
        }
        while (1) {
            long idx = 0, n = 0;
            printf("Index (1-%d): ", cnt);
            scanf("%ld%*c", &idx);
            idx -= 1;
            if (storage[idx].id > cnt) {
                puts("Invalid index");
                continue;
            }
            printf("Value: ");
            scanf("%ld%*c", &n);
            if (n < 0) {
                puts("Invalid value");
                continue;
            }
            storage[idx].val += n;
            printf("You've added %d to %d storage. Now it's value is %ld\n", n, storage[idx].id, storage[idx].val);
            if (storage[idx].val > MAX_VAL) {
                puts("Bot win");
                break;
            }

            idx = rand() % (cnt);
            n = rand() % (MAX_VAL-1) +1;
            storage[idx].val += n;
            printf("Bot added %d to %d storage. Now it's value is %ld\n", n, storage[idx].id, storage[idx].val);
            if (storage[idx].val > MAX_VAL) {
                puts("You win");
                break;
            }
        }
        printf("Play again [y/n]: ");
        read(0, &c, sizeof(c));
        if (c[0] != 'y') {
            break;
        }
    }

    return 0;
}