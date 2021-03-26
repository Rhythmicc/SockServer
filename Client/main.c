#include "SockClient/SockClient.h"

int main(int argc, char **argv) {
    struct sockaddr_in*servaddr = default_addr();
    SockString_t recvbuf = new_string();

    char postbuf[BUFFER_SIZE];
    memset(postbuf, 0, BUFFER_SIZE);
    strcpy(postbuf, argv[1]);
    for (int i=2; i < argc; ++i) {
        strcat(postbuf, " ");
        strcat(postbuf, argv[i]);
    }

    puts(postbuf);
    call_api(servaddr, postbuf, recvbuf);
    stringPuts(recvbuf);

    deleteString(recvbuf);
    free(servaddr);
    return 0;
}
