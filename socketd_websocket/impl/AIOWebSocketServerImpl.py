import asyncio
from websockets.server import WebSocketServer, serve as Serve, WebSocketServerProtocol
from typing import Optional, Type, Union, Callable, Awaitable, Any, Generator

from socketd.core.ChannelDefault import ChannelDefault
from socketd.core.module.Frame import Frame
from loguru import logger

from socketd_websocket.IWebSocketServer import IWebSocketServer
import socketd_websocket.WsAioServer as WsAioServer

log = logger.opt()


class AIOWebSocketServerImpl(IWebSocketServer):
    """暂时忽略"""

    def __init__(self, host: str, port: int, ws_server: 'WsAioServer', *args, **kwargs):
        self.__host = host
        self.__port = port
        self.__loop = asyncio.get_event_loop()
        self.server: Serve = Serve(self.on_message, host=self.__host, port=self.__port, *args, **kwargs,
                                   create_protocol=self.on_open
                                   )
        self.ws_server = ws_server

    async def __aenter__(self) -> WebSocketServer:
        return await self.server.__aenter__()

    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[Exception],
                        ):
        await self.server.__aexit__(exc_type, exc_value, traceback)

    def __await__(self) -> Generator[Any, None, WebSocketServer]:
        # Create a suitable iterator by calling __await__ on a coroutine.
        return self.server.__await__()

    def on_open(self, *args, **kwargs) -> WebSocketServerProtocol:
        conn = WebSocketServerProtocol(*args, **kwargs)
        channel = ChannelDefault( self.ws_server._config,
                                 self.ws_server._assistant,*args, **kwargs)
        conn.__setattr__("channel", channel)
        return conn

    async def on_error(self, conn: 'WebSocketServerProtocol', e: Exception):
        pass

    async def on_message(self, conn: 'WebSocketServerProtocol', path: str):
        try:
            message = await conn.recv()
            frame: Frame = self.ws_server.assistant().read(message)
            if frame is not None:
                self.ws_server._processor.on_receive(conn, frame)
            log.debug(message)
        except Exception as e:
            log.error(e)

    async def on_close(self, conn: 'WebSocketServerProtocol'):
        await conn.close()  # 完成握手
        self.server.ws_server.unregister(conn)

    def register(self, protocol: WebSocketServerProtocol) -> None:
        self.server.ws_server.register(protocol)
