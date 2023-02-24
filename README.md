# SockServer

## Screenshot

![](https://alapi.rhythmlian.cn/image/2021/06/12/d0aad9bd5711976580dbabb114d64a4b.jpg)

## Install

```shell
pip3 install sockserver -U
```

## Usage

```python
import json
from SockServer import SockServer

server = SockServer(8000, workers=8)


@server.register()
def hello(who: str):
    """
    :param who:
    :return:
    """
    if who == 'me':
        return {'status': False, 'result': 'you are not allowed to say hello to yourself'}
    return {'status': True, 'result': 'hello ' + who.strip()}


if __name__ == '__main__':
    server.start()
```

## Client Lib for `C`

- Install Client LIB

```shell
mkdir /usr/local/include/SockClient
mv Client/utils/* /usr/local/include/SockClient/
```

- Usage

```C
#include <SockClient/SockClient.h>
#include <SockClient/cJSON.h>

int main(int argc, char **argv) {
    struct sockaddr_in*server_addr = default_addr("127.0.0.1", 8000);
    SockString_t recv_buf = SockString_NewString();

    char post_buf[BUFFER_SIZE];

    cJSON* post_json = cJSON_CreateObject();
    cJSON_AddStringToObject(post_json, "func", argv[1]);
    cJSON* argvs_json = cJSON_CreateArray();
    for (int i = 2; i < argc; i++) {
        cJSON_AddItemToArray(argvs_json, cJSON_CreateString(argv[i]));
    }
    cJSON_AddItemToObject(post_json, "argv", argvs_json);
    cJSON_PrintPreallocated(post_json, post_buf, BUFFER_SIZE, 0);

    puts(post_buf);
    call_api(server_addr, post_buf, recv_buf);

    cJSON_Delete(post_json);
    
    char* recv_string = SockString_ToCharArray(recv_buf);
    cJSON* recv_json = cJSON_Parse(recv_string);
    free(recv_string);
    deleteString(recv_buf);

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

    free(server_addr);
    return 0;
}
```
