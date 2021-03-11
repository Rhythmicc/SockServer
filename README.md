# SockServer

## Screenshot

![](https://api-img.alapi.cn/image/2021/02/05/f613e100ef5d07b07d20e23a41aa88bf.png)

## Install

1. 将`SockServer`文件夹添加到你的`Python::3`第三方库文件夹(`**/site-packages/`)中，即可完成安装
2. `python3 setup.py install`


## Usage

```python3
from SockServer import SockServer

server = SockServer(8000, workers=8)


def HelloCallback(status: bool, result: str):
    print(status, result)


@server.register("hello", callback=HelloCallback)
def hello(who: str) -> (bool, str):
    """
    :param who:
    :return: bool -> 是否调用成功, str -> 返回结果
    """
    if who == 'me':
        return False, "who should not be 'me'"
    return True, f'hello {who}!'


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
#include "SockClient/SockClient.h"

int main(int argc, char **argv) {
    struct sockaddr_in*servaddr = default_addr();
    string_t recvbuf = new_string();

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
```

