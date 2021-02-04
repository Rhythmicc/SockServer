import json
import signal
import socket
from threading import Lock
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor, wait


class SockServer:
    console = Console()
    errorString = '[bold red][错误]'
    warnString = '[bold yellow][警告]'
    infoString = '[bold cyan][提示]'

    def __init__(self, port, workers: int = 4):
        self.port = port
        self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketServer.bind(('127.0.0.1', port))
        self.socketServer.listen(10)
        self.functionTable, self.functionTableLock = {}, Lock()
        self.threadPool = ThreadPoolExecutor(workers)
        self.PoolDoing = []

    def __dealMsg(self, msg):
        """
        :param msg: {
            "func": "Registered Function Name",
            "argv": ["prams", "for", "function"]
        }
        :return: Status, return msg
        """
        infoBody = json.loads(msg)
        _errorFlag = False
        function, argv = infoBody.get('func'), infoBody.get('argv')
        if not function:
            _errorFlag = True
            status, result = False, 'Invalid Request Format'
        elif function not in self.functionTable:
            _errorFlag = True
            status, result = False, f'No registered function named {function}'
        else:
            try:
                status, result = self.functionTable[function]['func'](*argv) \
                    if argv else self.functionTable[function]['func']()
            except Exception as e:
                status, result = False, repr(e)
        if (not _errorFlag) and self.functionTable[function]['callback']:
            self.functionTable[function]['callback'](status, result)
        return status, result

    def __readAndDoAction(self, client_sc):
        client_sc.setblocking(0)
        msg = ''
        while True:
            try:
                concat = client_sc.recv(1024)
                msg += concat.decode('utf-8')
                if len(concat) < 1024:
                    break
            except ConnectionResetError:
                pass
            except Exception as e:
                SockServer.console.print(SockServer.errorString, repr(e))
                return
        msg = msg.strip()
        SockServer.console.print(SockServer.infoString, f'GET: {msg}')
        status, result = self.__dealMsg(msg)
        client_sc.send(result.encode('utf-8'))
        client_sc.close()
        SockServer.console.print('-' * SockServer.console.width)

    def __getAccess(self):
        try:
            client_sc, addr = self.socketServer.accept()
        except Exception as e:
            SockServer.console.print(SockServer.errorString, repr(e))
        else:
            return client_sc, addr

    def register(self, name, callback=None):
        """
        注册函数

        :param name: 函数名
        :param callback: 回调函数
        :return:
        """
        def wrapper(func):
            if name in self.functionTable:
                SockServer.console.print(SockServer.warnString, f'{name} already registered.')
            self.functionTableLock.acquire()
            self.functionTable[name] = {'func': func, 'callback': callback}
            self.functionTableLock.release()
            SockServer.console.print(SockServer.infoString, f'Registered: {{"func": {func}, "callback": {callback}}}')
        return wrapper

    def stop(self, a, b):
        self.socketServer.close()  # * 关闭服务
        wait(self.PoolDoing)
        SockServer.console.print()
        SockServer.console.print(SockServer.infoString, 'Stop SockServer')
        exit(0)

    def start(self):
        signal.signal(signal.SIGINT, self.stop)
        SockServer.console.print(SockServer.infoString, f'Start SockServer with port: {self.port}')
        SockServer.console.print('-'*SockServer.console.width)
        while True:
            client_sc, addr = self.__getAccess()
            SockServer.console.print(SockServer.infoString, f'Request from: {addr[0]}:{addr[1]}')
            self.PoolDoing.append(self.threadPool.submit(self.__readAndDoAction, client_sc))
