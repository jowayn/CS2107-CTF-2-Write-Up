#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

typedef unsigned short u16;
typedef unsigned int u32;

#define HEXDUMP_COLS 16

typedef struct
{
    u16 src_port;
    u16 dst_port;
    u16 len;
    u16 checksum;
} UDPHeader;

typedef struct
{
    UDPHeader header;
    char data[0x1000]; // put a cap on amount of data
} UDPPacket;

void setup();
u16 checksum(UDPPacket *packet);
void read_packet(UDPPacket* packet, u16 data_len);
void hexdump(void *mem, unsigned int len);

// *cough* this is just here for uh.. fun :)
void win() {
    system("/bin/sh");
}

int main()
{
    setup();

    UDPPacket packet;
    packet.header.checksum = 0;

    puts("######### CS2105 UDP Packet Viewer #########");

    printf("Source Port > ");
    scanf("%hu", &packet.header.src_port);

    printf("Destination Port > ");
    scanf("%hu", &packet.header.dst_port);

    u16 data_len;
    printf("Data Length > ");
    scanf("%hu", &data_len);
    getchar(); //ignore this line

    // len is length in bytes of UDP Header and UDP data
    packet.header.len = data_len + sizeof(UDPHeader);
    if (packet.header.len > sizeof(UDPPacket))
    {
        puts("Too much data!");
        return 1;
    }

    printf("Data > ");
    read_packet(&packet, data_len);

    // Calculate checksum
    packet.header.checksum = checksum(&packet);

    puts("\nPacket bytes: \n");
    // View packet bytes
    hexdump(&packet, packet.header.len);
}


// IGNORE
void setup()
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

u16 checksum(UDPPacket *packet)
{
    u16 *bytes = (u16 *)packet;
    u32 sum = 0;
    for (int i = 0; i < packet->header.len; i += 2)
    {
        sum += bytes[i];
        u16 carry = (sum >> 16) & 1;
        sum = (sum & 0xffff) + carry;
    }
    return ~sum;
}

void read_packet(UDPPacket* packet, u16 data_len) {
    fgets(packet->data, data_len, stdin);
}

void hexdump(void *mem, unsigned int len)
{
    unsigned int i, j;

    for (i = 0; i < len + ((len % HEXDUMP_COLS) ? (HEXDUMP_COLS - len % HEXDUMP_COLS) : 0); i++)
    {
        /* print offset */
        if (i % HEXDUMP_COLS == 0)
        {
            printf("0x%06x: ", i);
        }

        /* print hex data */
        if (i < len)
        {
            printf("%02x ", 0xFF & ((char *)mem)[i]);
        }
        else /* end of block, just aligning for ASCII dump */
        {
            printf("   ");
        }

        /* print ASCII dump */
        if (i % HEXDUMP_COLS == (HEXDUMP_COLS - 1))
        {
            for (j = i - (HEXDUMP_COLS - 1); j <= i; j++)
            {
                if (j >= len) /* end of block, not really printing */
                {
                    putchar(' ');
                }
                else if (isprint(((char *)mem)[j])) /* printable char */
                {
                    putchar(0xFF & ((char *)mem)[j]);
                }
                else /* other char */
                {
                    putchar('.');
                }
            }
            putchar('\n');
        }
    }
}

// END IGNORE