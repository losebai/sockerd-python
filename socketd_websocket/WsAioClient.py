import asyncio

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
        self.__loop = asyncio.get_event_loop()

    def open(self):
        client = WsAioClientConnector(self)
        self.log.info(f"open {self._config.url}")
        self.client = client.connect()
        return self.client
