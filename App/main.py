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
