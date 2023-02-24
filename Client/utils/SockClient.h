#pragma once
#ifdef __cplusplus
extern "C" {
#endif
#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/shm.h>
#include "SockString.h"

void call_api(struct sockaddr_in* servaddr, char*cmd, SockString_t result) {
    int sc = socket(AF_INET, SOCK_STREAM, 0);
    int status = connect(sc, (struct sockaddr *)servaddr, sizeof(*servaddr));
    if (status == -1) {
        puts("连接错误 | Connect Error");
        return;
    }
    send(sc, cmd, strlen(cmd), 0); ///发送

    char buffer[BUFFER_SIZE];
    while(1){
        memset(buffer, 0, BUFFER_SIZE);
        ssize_t ret = recv(sc, buffer, BUFFER_SIZE, 0); ///接收
        if(ret<=0)break;
        SockString_Cat(result, buffer);
    }
    close(sc);
}

struct sockaddr_in* default_addr(const char* addr, const int port) {
    struct sockaddr_in*res = (struct sockaddr_in*)malloc(sizeof(struct sockaddr_in));
    memset(res, 0, sizeof(struct sockaddr_in));
    res->sin_family = AF_INET;
    res->sin_port = htons(port);
    res->sin_addr.s_addr = inet_addr(addr);
    return res;
}
#ifdef __cplusplus
};
#endif
