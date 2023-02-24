from QuickProject.Commander import Commander
from SockServer import SockServer
from . import *

app = Commander(executable_name)
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


@app.command()
def start():
    """
    启动服务
    Start service
    """
    server.start()


def main():
    """
    注册为全局命令时, 默认采用main函数作为命令入口, 请勿将此函数用作它途.
    When registering as a global command, default to main function as the command entry, do not use it as another way.
    """
    app()


if __name__ == "__main__":
    main()
