#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>

// IGNORE
void setup() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

long read_long() {
    char buf[8];
    fgets(buf, sizeof(buf), stdin);
    return strtol(buf, NULL, 10);
}

// END IGNORE

long moon = 384400;


void main() {
    setup();

    char name[40];
    long altitude;

    puts("Provide current altitude:");
    altitude = read_long();
    if (altitude > moon) altitude = 0;

    puts("What's your name?");
    gets(name);

    if (altitude > moon) {
        printf("You are over the moon, %s!", name);
        system("/bin/sh"); // get your free remote shell!
    } else {
        printf("You are in altitude %lld km, %s. Too bad!", altitude, name);
    }
}