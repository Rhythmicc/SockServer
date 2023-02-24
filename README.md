# SockServer

A very tiny RPC framework, with ability to perform basic type checks.

## Screenshot

![demo](https://cos.rhythmlian.cn/ImgBed/0ba3cba4b129c1cfaea588a5821415ad.png)

## Install

```shell
pip3 install sockserver -U
```

## Usage

```python
from SockServer import SockServer

server = SockServer(8000, workers=8)


@server.register()
def hello(who: str):
    """
    :param who:
    :return:
    """
    if who == "me":
        return {
            "status": False,
            "result": "you are not allowed to say hello to yourself",
        }
    return {"status": True, "result": "hello " + who.strip()}


if __name__ == '__main__':
    server.start()
```

### Support [Qpro](https://github.com/Rhythmicc/QuickProject) Template

```shell
Qpro create <server_name>

# Choose "内置模板 / Inner Template" -> "SockServer"
```

## Client Lib for `C`

- Install Client LIB

```shell
mkdir -p /usr/local/include/SockClient
cp Client/utils/* /usr/local/include/SockClient/
```

- Usage

```C
#include <SockClient/SockClient.h>
#include <SockClient/cJSON.h>

int main(int argc, char **argv)
{
    /*
    * 服务端地址与端口，请自行修改
    ! 由于SockClient不具备域名解析功能，因此需要使用IP地址
    ! 如果服务端在本机，请使用 127.0.0.1
    */
    struct sockaddr_in *server_addr = default_addr("10.64.128.99", 8080);

    /*
     * 构建JSON对象，用于存储API调用的函数名与参数
     * 数据形如: {"func": argv[1], "argv": [argv[2], argv[3], ...]}
     */
    cJSON *post_json = cJSON_CreateObject();
    cJSON_AddStringToObject(post_json, "func", argv[1]);
    cJSON *argvs_json = cJSON_CreateArray();
    for (int i = 2; i < argc; i++)
    {
        cJSON_AddItemToArray(argvs_json, cJSON_CreateString(argv[i]));
    }
    cJSON_AddItemToObject(post_json, "argv", argvs_json);

    /*
     * 用于存储服务器返回的数据，SockString 是一个字符串链表，用于动态存储大量数据
     */
    SockString_t recv_buf = SockString_NewString();
    char post_buf[BUFFER_SIZE];

    cJSON_PrintPreallocated(post_json, post_buf, BUFFER_SIZE, 0); // * 将JSON对象转换为字符串

    /*
     * 调用API，将post_buf中的数据发送到服务器，服务器返回的数据存储在recv_buf中
     */
    call_api(server_addr, post_buf, recv_buf);

    cJSON_Delete(post_json); // * 释放JSON对象

    char *recv_string = SockString_ToCharArray(recv_buf); // * 将SockString转换为字符串
    cJSON *recv_json = cJSON_Parse(recv_string);          // * 将字符串转换为JSON对象
    free(recv_string);                                    // * 释放字符串
    SockString_Delete(recv_buf);                          // * 释放SockString

    cJSON_Print(recv_json); // * 打印收到的JSON对象

    if (cJSON_IsFalse(cJSON_GetObjectItem(recv_json, "status")))
    {
        /*
         * 如果服务器返回的status为false，则说明调用API失败
         */
        printf("Error: %s\n", cJSON_GetObjectItem(recv_json, "result")->valuestring);
        return 1;
    }

    /*
     * 如果服务器返回的status为true，则说明调用API成功
     * 读取result字段，根据其类型进行处理
     */
    cJSON *result = cJSON_GetObjectItem(recv_json, "result");
    if (result->type == cJSON_String)
    {
        printf("%s\n", result->valuestring);
    }
    else if (result->type == cJSON_Number)
    {
        printf("%d\n", result->valueint);
    }
    else if (result->type == cJSON_Array)
    {
        for (int i = 0; i < cJSON_GetArraySize(result); i++)
        {
            cJSON *item = cJSON_GetArrayItem(result, i);
            if (item->type == cJSON_String)
            {
                printf("%s\n", item->valuestring);
            }
            else if (item->type == cJSON_Number)
            {
                printf("%d\n", item->valueint);
            }
        }
    }

    free(server_addr); // * 释放服务器地址
    return 0;
}
```
