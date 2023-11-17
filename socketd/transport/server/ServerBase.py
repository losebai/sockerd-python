from .Server import Server
from socketd.core.config.ServerConfig import ServerConfig
from socketd.core.ProcessorDefault import ProcessorDefault


class ServerBase(Server):
    """
    服务端基类
    """

    def __init__(self, config, assistant):
        self._processor = ProcessorDefault()
        self._config: ServerConfig = config
        self._assistant = assistant
        self.isStarted = False

    def assistant(self):
        """
        获取通道助理
        """
        return self._assistant

    def config(self, consumer: 'Function'):
        """
        获取配置
        """
        consumer(self._config)
        return self

    def process(self, processor):
        """
        设置处理器
        """
        if processor is not None:
            self._processor = processor
        return self

    def listen(self, listener):
        """
        设置监听器
        """
        self._processor.set_listener(listener)
        return self
