from websockets.server import WebSocketServer, WebSocketServerProtocol


class IWebSocketServer:

    async def register(self, protocol: WebSocketServerProtocol) -> None:

    async def on_open(self): ...

    async def on_error(self): ...

    async def on_message(self, conn:'WebSocketServer', message: bytes): ...

    async def on_close(self): ...