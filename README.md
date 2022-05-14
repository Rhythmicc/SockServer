# SockServer

## Screenshot

![](https://alapi.rhythmlian.cn/image/2021/06/12/d0aad9bd5711976580dbabb114d64a4b.jpg)

## Install

1. 将`SockServer`文件夹添加到你的`Python::3`第三方库文件夹(`**/site-packages/`)中，即可完成安装
2. `python3 setup.py install`


## Usage

```python3
from SockServer import SockServer

server = SockServer(8000, workers=8)


@server.register()
def hello(who: str):
    """
    :param who:
    :return: 
    """
    if who == 'me':
        return "who should not be 'me'"
    return {'status': True, 'msg': 'hello ' + who.strip()}


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

