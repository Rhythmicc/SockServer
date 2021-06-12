"""
简单的 Socket 多线程服务框架，基于JSON的传输协议，并带有基础的类型检查能力。

它诞生的初衷是通过socket与不便实现http的程序沟通，并借助Python强大生态，完成一系列事务：

* 不便用其他语言完成的事，直接让Python代理

* 持久化的服务减少你的业务额外开销

* 通过JSON，像调用函数一样使用Socket API

* 自动验证请求是否符合函数参数的类型注解

Author: RhythmLian
"""
from .SockServer import *
