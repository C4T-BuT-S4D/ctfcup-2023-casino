#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/fcntl.h>

#define ITEMS_LIST_SIZE 3
#define ITEMS_SIZE 0x10

char items[ITEMS_LIST_SIZE][ITEMS_SIZE] = {
    "Option1\0\0\0\0\0\0\0\0\0",
    "Option2\0\0\0\0\0\0\0\0\0",
    "Option3\0\0\0\0\0\0\0\0\0",
};

void print_menu() {
    puts("===== Menu =====");
    for (int i = 0; i < ITEMS_LIST_SIZE; ++i) {
        printf("%d. %s\n", i, items[i]);
    }
}

void create() {
    printf("Number of orders: ");
    unsigned long n;
    scanf("%lu%*c", &n);
    if (n < 1 || n > 10) {
        puts("Invalid number");
        return;
    }

    char raw[0x10] = {};
    int fd = open("/dev/urandom", O_RDONLY);
    read(fd, raw, sizeof(raw));
    close(fd);
    char hex[0x21] = {};
    for (int i = 0; i < sizeof(raw); ++i) {
        sprintf(&hex[2*i], "%02hhx", raw[i]);
    }
    char filename[0x40] = {};
    strcpy(filename, "./orders/");
    strcat(filename, hex);

    print_menu();

    fd = open(filename, O_WRONLY|O_CREAT, 0600);
    for (int i = 0; i < n; ++i) {
        unsigned long item_idx;
        printf("Item: ");
        scanf("%lu%*c", &item_idx);
        write(fd, &items[item_idx], ITEMS_SIZE);
    }
    close(fd);
    printf("Your order id is: %s\n", hex);
}

void get() {
    char order_id[0x21] = {};
    printf("Order id: ");
    read(0, order_id, sizeof(order_id));
    order_id[0x20] = '\0';
    if (strlen(order_id) != 0x20) {
        puts("Invalid id");
        return;
    }
    for (int i = 0; i < 0x20; ++i) {
        if (!('0' <= order_id[i] && order_id[i] <= '9' || 'a' <= order_id[i] && order_id[i] <= 'f')) {
            puts("Invalid id");
            return;
        }
    }
    char filename[0x40] = {};
    strcpy(filename, "./orders/");
    strcat(filename, order_id);
    int fd = open(filename, O_RDONLY);
    if (fd < 0) {
        puts("Invalid id");
        return;
    }
    char buf[ITEMS_SIZE + 1] = {};
    int n = 0, i = 0;
    printf("===== Order %s =====\n", order_id);
    while ((n = read(fd, &buf, ITEMS_SIZE)) == ITEMS_SIZE) {
        printf("%d. %s\n", i++, buf);
    }
    close(fd);
}

void edit() {
    char order_id[0x21] = {};
    printf("Order id: ");
    read(0, order_id, sizeof(order_id));
    order_id[0x20] = '\0';

    char filename[0x40] = {};
    strcpy(filename, "./orders/");
    strcat(filename, order_id);

    int fd = open(filename, O_WRONLY);
    if (fd < 0) {
        puts("Invalid id");
        return;
    }

    unsigned long n = 0;
    printf("Item number: ");
    scanf("%lu%*c", &n);

    unsigned end = lseek(fd, 0, SEEK_END);
    if (n >= (end / ITEMS_SIZE)) {
        puts("Invalid number");
        return;
    }

    if (lseek(fd, n*ITEMS_SIZE, SEEK_SET) != n*ITEMS_SIZE) {
        puts("Invalid item");
        return;
    }

    print_menu();

    unsigned long item_idx;
    printf("New item: ");
    scanf("%lu%*c", &item_idx);
    write(fd, items[item_idx], ITEMS_SIZE);
    close(fd);
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(60);

    char token[0x40] = {};
    printf("Task token: ");
    int _n = read(0, &token, 0x40-1);
    if (_n > 0 && token[_n-1] == '\n') token[_n-1] = 0;
    
    if (strcmp(token, getenv("TOKEN")) != 0) {
        puts("Invalid task token");
        return 0;
    }

    while (1) {
        puts("===== Orders =====");
        puts("1. Create new order");
        puts("2. Get order");
        puts("3. Change order");
        printf("> ");
        int c;
        scanf("%d%*c", &c);
        switch (c) {
            case 1:
                create();
                break;
            case 2:
                get();
                break;
            case 3:
                edit();
                break;
            default:
                return 0;
        }
    }
    return 0;
}