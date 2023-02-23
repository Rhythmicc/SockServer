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
