import asyncio
from websockets.server import WebSocketServer, serve, WebSocketServerProtocol
from typing import Optional, Type, Union, Callable, Awaitable, Any
from websockets.legacy.client import WebSocketClientProtocol
from AIOWebSocketServerImpl import IWebSocketServer


class AIOWebSocketServerImpl(IWebSocketServer):

    def __init__(self, ws_handler: Union[
        Callable[[WebSocketServerProtocol], Awaitable[Any]],
        Callable[[WebSocketServerProtocol, str], Awaitable[Any]],  # deprecated
    ], host: str, port: int):
        self.__loop = asyncio.get_event_loop()
        self.server: serve = serve(ws_handler, host=host, port=port)
        self.ws_server: WebSocketServer = self.server.ws_server

    async def __aenter__(self) -> WebSocketServer:
        return await self.server.__aenter__()

    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[Exception],
                        ):
        await self.server.__aexit__(exc_type, exc_value, traceback)

    async def on_open(self):
        return await self.server.__aenter__()

    async def on_error(self):
        pass

    async def on_message(self, conn: WebSocketServer, message: bytes):
        for i in self.ws_server.websockets:
            data = await i.recv()

    async def on_close(self):
        await self.server.ws_server.close()

    async def register(self, protocol: WebSocketServerProtocol) -> None:
        self.server.ws_server.register(protocol)

