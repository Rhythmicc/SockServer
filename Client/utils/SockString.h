#pragma once
extern "C" {
#define BUFFER_SIZE 1024
struct SockString;
typedef struct SockString SockString, *SockString_t;

struct _node {
    char _src[BUFFER_SIZE];
    int _len;
    struct _node* _next;
};

struct SockString {
    struct _node*head, *end;
};

struct _node* new_node() {
    struct _node*res = (struct _node*)calloc(1, sizeof(struct _node));
    res->_len = 0;
    res->_next = NULL;
    return res;
}

SockString_t new_string() {
    SockString_t res = (SockString_t)malloc(sizeof(SockString));
    res->head = new_node();
    res->end = res->head;
    return res;
}

void stringAddNode(SockString_t s) {
    s->end = new_node();
    s->end = s->end->_next;
}

void stringCat(SockString_t s, char*dst) {
    while(*dst) {
        if (s->end->_len == BUFFER_SIZE - 1) stringAddNode(s);
        s->end->_src[s->end->_len++] = *dst++;
    }
}

void stringClean(SockString_t s) {
    memset(s->head->_src, 0, sizeof(char) * BUFFER_SIZE);
    s->head->_len = 0;
    s->end = s->head;
    struct _node*p = s->head->_next;
    while (p) {
        struct _node*tmp = p;
        p = p->_next;
        free(tmp);
    }
}

char* stringToCharArray(SockString_t s) {
    int _sz = 0;
    struct _node* p = s->head;
    while (p) {
        _sz += p->_len;
        p = p->_next;
    }
    char*res = (char*) malloc(sizeof(char) * (_sz + 1));
    p = s->head;
    while (p) {
        strcat(res, p->_src);
        p = p->_next;
    }
    return res;
}

void stringPuts(SockString_t s) {
    struct _node*p = s->head;
    while (p != s->end) {
        printf("%s", p->_src);
        p = p->_next;
    }
    printf("%s\n", p->_src);
}

void deleteString(SockString_t s){
    struct _node*p = s->head;
    while(p!=s->end){
        struct _node* tmp = p;
        p = p->_next;
        free(tmp);
    }
    free(s);
}
};