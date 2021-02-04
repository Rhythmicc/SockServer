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
