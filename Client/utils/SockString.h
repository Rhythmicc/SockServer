#pragma once
#define BUFFER_SIZE 1024
struct string;
typedef struct string string, *string_t;

struct _node {
    char _src[BUFFER_SIZE];
    int _len;
    struct _node* _next;
};

struct string {
    struct _node*head, *end;
};

struct _node* new_node() {
    struct _node*res = (struct _node*)calloc(1, sizeof(struct _node));
    res->_len = 0;
    res->_next = NULL;
    return res;
}

string_t new_string() {
    string*res = (string*)malloc(sizeof(string));
    res->head = new_node();
    res->end = res->head;
    return res;
}

void stringAddNode(string_t s) {
    s->end = new_node();
    s->end = s->end->_next;
}

void stringCat(string_t s, char*dst) {
    while(*dst) {
        if (s->end->_len == BUFFER_SIZE - 1) stringAddNode(s);
        s->end->_src[s->end->_len++] = *dst++;
    }
}

void stringClean(string_t s) {
    memset(s->head->_src, 0, sizeof(char) * BUFFER_SIZE);
    s->_len = 0;
    s->end = s->head;
    struct _node*p = head->_next;
    while (p) {
        struct _node*tmp = p;
        p = p->_next;
        free(tmp);
    }
}

void stringPuts(string_t s) {
    struct _node*p = s->head;
    while (p != s->end) {
        printf("%s", p->_src);
        p = p->_next;
    }
    printf("%s\n", p->_src);
}

void deleteString(string_t s){
    struct _node*p = s->head;
    while(p!=s->end){
        struct _node* tmp = p;
        p = p->_next;
        free(tmp);
    }
    free(s);
}
