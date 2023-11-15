from typing import Callable
from Server import Server
from socketd.core.config.ServerConfig import ServerConfig
from socketd.core.ProcessorDefault import ProcessorDefault


class ServerBase(Server):
    """
    服务端基类
    """

    def __init__(self, config, assistant):
        self.processor = ProcessorDefault()
        self.config: ServerConfig = config
        self.assistant = assistant
        self.isStarted = False

    def assistant(self):
        """
        获取通道助理
        """
        return self.assistant

    def config(self, consumer: 'function'):
        """
        获取配置
        """
        consumer(self.config)
        return self

    def process(self, processor):
        """
        设置处理器
        """
        if processor is not None:
            self.processor = processor
        return self

    def listen(self, listener):
        """
        设置监听器
        """
        self.processor.setListener(listener)
        return self
