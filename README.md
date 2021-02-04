# SockServer

## Install

1. 将`SockServer`文件夹添加到你的`Python::3`第三方库文件夹(`**/site-packages/`)中，即可完成安装
2. `python3 setup.py install`


## Usage

```python3
from SockServer.SockServer import SockServer

server = SockServer(8000)


def HelloCallback(status: bool, result: str):
    print(status, result)


@server.register("fuck", callback=HelloCallback)
def hello(who: str) -> (bool, str):
    """
    :param who:
    :return: bool -> 是否调用成功, str -> 返回结果
    """
    return True, f'hello {who}!'


if __name__ == '__main__':
    server.start()
```
## Screenshot

![](https://api-img.alapi.cn/image/2021/02/05/f613e100ef5d07b07d20e23a41aa88bf.png)
