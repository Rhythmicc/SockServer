#include <SockClient.h>

int main(int argc, char **argv) {
    struct sockaddr_in*servaddr = default_addr("127.0.0.1", 8000);
    SockString_t recvbuf = new_string();

    char postbuf[BUFFER_SIZE];
    char argvs[BUFFER_SIZE];

    memset(argvs, 0, sizeof(argvs));

    for (int i = 2; i < argc; i++) {
        strcat(argvs, argv[i]);
        if (i != argc - 1) strcat(argvs, ", ");
    }
    sprintf(postbuf, "{\"func\": \"%s\", \"argv\": [%s]}", argv[1], argvs);

    puts(postbuf);
    call_api(servaddr, postbuf, recvbuf);
    stringPuts(recvbuf);

    deleteString(recvbuf);
    free(servaddr);
    return 0;
}
