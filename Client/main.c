#include <SockClient.h>
#include <cJSON.h>

int main(int argc, char **argv) {
    struct sockaddr_in*servaddr = default_addr("127.0.0.1", 8000);
    SockString_t recvbuf = SockString_NewString();

    char postbuf[BUFFER_SIZE];

    cJSON* json = cJSON_CreateObject();
    cJSON_AddStringToObject(json, "func", argv[1]);
    cJSON* argvs_json = cJSON_CreateArray();
    for (int i = 2; i < argc; i++) {
        cJSON_AddItemToArray(argvs_json, cJSON_CreateString(argv[i]));
    }
    cJSON_AddItemToObject(json, "argv", argvs_json);
    cJSON_PrintPreallocated(json, postbuf, BUFFER_SIZE, 0);

    puts(postbuf);
    call_api(servaddr, postbuf, recvbuf);

    cJSON_Delete(json);
    
    char* recv_string = SockString_ToCharArray(recvbuf);
    cJSON* recv_json = cJSON_Parse(recv_string);
    free(recv_string);
    deleteString(recvbuf);

    cJSON_Print(recv_json);

    if (cJSON_IsFalse(cJSON_GetObjectItem(recv_json, "status"))) {
        printf("Error: %s\n", cJSON_GetObjectItem(recv_json, "result")->valuestring);
        return 1;
    }
    
    cJSON* result = cJSON_GetObjectItem(recv_json, "result");
    if (result->type == cJSON_String) {
        printf("%s\n", result->valuestring);
    } else if (result->type == cJSON_Number) {
        printf("%d\n", result->valueint);
    } else if (result->type == cJSON_Array) {
        for (int i = 0; i < cJSON_GetArraySize(result); i++) {
            cJSON* item = cJSON_GetArrayItem(result, i);
            if (item->type == cJSON_String) {
                printf("%s\n", item->valuestring);
            } else if (item->type == cJSON_Number) {
                printf("%d\n", item->valueint);
            }
        }
    }

    free(servaddr);
    return 0;
}
