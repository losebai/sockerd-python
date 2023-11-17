from loguru import logger

from socketd.transport.client.ClientBase import ClientBase
from socketd.core.config.ClientConfig import ClientConfig
from .WsAioChannelAssistant import WsAioChannelAssistant
from websockets.client import connect as Connect
from .WsAioClientConnector import WsAioClientConnector


class WsAioClient(ClientBase):

    def __init__(self, config: ClientConfig):
        super().__init__(config, WsAioChannelAssistant(config))
        self.client = None
        self.log = logger.opt()

    def open(self):
        client = WsAioClientConnector(self)
        client.connect()
        self.log.info(f"open {self._config.url}")
        self.client = Connect(self._config.url)
        return self.client
