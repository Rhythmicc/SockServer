import inspect
import time
import json
import signal
import socket
from inspect import isfunction
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor, wait


class SockServer:
    console = Console()
    status = console.status('SockServer 工作中')
    errorString = '[bold red][错误]'
    warnString = '[bold yellow][警告]'
    infoString = '[bold cyan][提示]'

    def __init__(self, port, host: str = '127.0.0.1', workers: int = 4):
        """
        简单的 Socket 多线程服务框架，基于JSON的传输协议，并带有基础的类型检查能力。

        :param port: 端口
        :param host: 地址
        :param workers: 线程数量
        """
        self.port = port
        self.host = host
        self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketServer.bind((host, port))
        self.socketServer.listen(10)
        self.functionTable = {}
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
        try:
            infoBody = json.loads(msg)
        except Exception as e:
            return False, repr(e)

        _errorFlag = False
        function, argv = infoBody.get('func'), infoBody.get('argv')
        if not function:
            _errorFlag = True
            result = 'SockServer Error: Invalid Request Format'
        elif function not in self.functionTable:
            _errorFlag = True
            result = f'SockServer Error: No registered function named {function}'
        else:
            typeTable = list(self.functionTable[function]['analyser'].parameters.values())
            for index, value in enumerate(argv):
                if typeTable[index].annotation is inspect._empty:
                    continue
                if not isinstance(value, typeTable[index].annotation):
                    return 'SockServer Error: Invalid Request with wrong parameters'
            try:
                result = self.functionTable[function]['func'](*argv) \
                    if argv else self.functionTable[function]['func']()
            except Exception as e:
                SockServer.console.print(SockServer.errorString, repr(e))
                result = repr(e)
        return result

    def __readAndDoAction(self, client_sc):
        """
        接手请求，读取 ==> 处理 ==> 返回

        :param client_sc: socket 对象
        :return:
        """
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
        tm_string = time.strftime("%m-%d %H:%M:%S", time.localtime(time.time()))
        SockServer.console.print(SockServer.infoString, f'GET: {msg}', tm_string)
        result = self.__dealMsg(msg)
        if hasattr(result, '__str__'):
            client_sc.send(str(result).encode('utf-8'))
        else:
            SockServer.console.print(SockServer.warnString, 'Result can\'t be transformed to string.')
            client_sc.send('SockServer Warning: Result can\'t be transformed to string.')
        client_sc.close()
        SockServer.console.print('-' * SockServer.console.width)

    def __getAccess(self):
        """
        等待请求

        :return: socket对象，地址
        """
        try:
            client_sc, addr = self.socketServer.accept()
        except Exception as e:
            SockServer.console.print(SockServer.errorString, repr(e))
        else:
            return client_sc, addr

    def register(self):
        """
        注册函数

        * 注册的函数返回的对象必须可被转换为字符串

        * 被添加类型注解的参数，会触发对请求的类型检查

        * 客户端只能通过固定格式的JSON调用: {"func": "<function name>", "argv": [...]}

        :return:
        """
        def wrapper(func):
            if not isfunction(func):
                SockServer.console.print(SockServer.errorString, f'{func} is not a function!')
                return
            analyser = inspect.signature(func)
            if func.__name__ in self.functionTable:
                SockServer.console.print(SockServer.warnString, f'{func.__name__} already registered.')
            self.functionTable[func.__name__] = {'func': func, 'analyser': analyser}
            SockServer.console.print(SockServer.infoString, f'Registered: {func}')
        return wrapper

    def stop(self, a, b):
        """
        停止socketServer

        :param a: ignore value
        :param b: ignore value
        :return:
        """
        SockServer.status.update(status='SockServer 关闭中')
        self.socketServer.close()  # * 关闭服务
        wait(self.PoolDoing)
        SockServer.status.stop()
        SockServer.console.print()
        SockServer.console.print(SockServer.infoString, 'Stop SockServer')
        exit(0)

    def start(self):
        SockServer.status.start()
        SockServer.status.update(status='注册终止函数')

        signal.signal(signal.SIGINT, self.stop)  # 注册终止函数
        SockServer.console.print(SockServer.infoString, f'Start SockServer at: {self.host + ":" + str(self.port)}')
        SockServer.console.print('-'*SockServer.console.width)

        SockServer.status.update(status='SockServer 服务中')
        while True:
            client_sc, addr = self.__getAccess()
            SockServer.console.print(SockServer.infoString, f'Request from: {addr[0]}:{addr[1]}')
            self.PoolDoing.append(self.threadPool.submit(self.__readAndDoAction, client_sc))
