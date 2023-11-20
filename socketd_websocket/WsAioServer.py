import asyncio
from loguru import logger

from websockets.server import WebSocketServer, serve as Serve, WebSocketServerProtocol
from websockets import broadcast

from socketd.transport.server.ServerBase import ServerBase
from .WsAioChannelAssistant import WsAioChannelAssistant
from socketd.core.config.ServerConfig import ServerConfig
from .impl.AIOWebSocketServerImpl import AIOWebSocketServerImpl

log = logger.opt()


class WsAioServer(ServerBase):

    def __init__(self, config: ServerConfig):
        super().__init__(config, WsAioChannelAssistant(config))
        self.__loop = asyncio.get_event_loop()
        self.server: Serve = None
        self.stop = asyncio.Future()  # set this future to exit the server

    def start(self) -> 'WsAioServer':
        if self.isStarted:
            raise Exception("Server started")
        else:
            self.isStarted = True
        if self._config.getHost() is not None:
            self.server = AIOWebSocketServerImpl(host="0.0.0.0", port=self._config.getPort(),
                                                 ws_server=self,
                                                 ssl=self._config.get_ssl_context())
        else:
            self.server = AIOWebSocketServerImpl(host=self._config.getHost(), port=self._config.getPort(),
                                                 ws_server=self,
                                                 ssl=self._config.get_ssl_context())
        self.__loop.run_until_complete(self.server)
        log.info("Server started: {server=" + self._config.getLocalUrl() + "}")
        return self

    def message_all(self, message: str):
        """广播"""
        broadcast(self.server.ws_server.websockets, message)

    def stop(self):
        self.__loop.run_until_complete(asyncio.wait(self.stop))
