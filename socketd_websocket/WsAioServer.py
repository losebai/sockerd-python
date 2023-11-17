import asyncio
from loguru import logger

from websockets.server import WebSocketServer, serve as Serve, WebSocketServerProtocol
from websockets import broadcast
from typing import Optional, Type, Union, Callable, Awaitable, Any

from socketd.transport.server.ServerBase import ServerBase
from .WsAioChannelAssistant import WsAioChannelAssistant
from socketd.core.config.ServerConfig import ServerConfig

log = logger.opt()


class WsAioServer(ServerBase):

    def __init__(self, config: ServerConfig, ws_handler: Union[
        Callable[[WebSocketServerProtocol], Awaitable[Any]],
        Callable[[WebSocketServerProtocol, str], Awaitable[Any]],  # deprecated
    ] = None):
        super().__init__(config, WsAioChannelAssistant(config))
        if ws_handler is None:
            self.ws_handler: Union = ws_handler
        else:
            self.ws_handler: Union = ws_handler
        self.__loop = asyncio.get_event_loop()
        self.server: Serve = None
        self.stop = asyncio.Future()  # set this future to exit the server

    def start(self) -> 'WsAioServer':
        if self.isStarted:
            raise Exception("Server started")
        else:
            self.isStarted = True
        if self._config.getHost() is not None:
            self.server = Serve(self.ws_handler, host="0.0.0.0", port=self._config.getPort(),
                                ssl=self._config.getSslContext())
        else:
            self.server = Serve(self.ws_handler, host=self._config.getHost(), port=self._config.getPort(),
                                ssl=self._config.getSslContext())

        self.server = self.__loop.run_until_complete(self.server)
        log.info("Server started: {server=" + self._config.getLocalUrl() + "}")
        return self

    def message_all(self, message: str):
        """广播"""
        broadcast(self.server.ws_server.websockets, message)

    def stop(self):
        self.__loop.run_until_complete(asyncio.wait(self.stop))
