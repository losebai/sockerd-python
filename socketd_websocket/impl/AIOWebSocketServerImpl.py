import asyncio

from websockets.server import WebSocketServer, serve as Serve, WebSocketServerProtocol

from socketd.core.ChannelDefault import ChannelDefault
from socketd.core.module.Frame import Frame
from loguru import logger


log = logger.opt()


class AIOWebSocketServerImpl(WebSocketServerProtocol):
    """暂时忽略"""

    def __init__(self, ws_handler, ws_server: WebSocketServer, ws_aio_server, *args, **kwargs):
        self.__loop = asyncio.get_event_loop()
        # self.server: Serve = Serve(self.on_message, host=self.__host, port=self.__port, *args, **kwargs,
        #                            )
        self.ws_aio_server = ws_aio_server
        self.__ws_server: WebSocketServer = ws_server
        self.channel = None
        WebSocketServerProtocol.__init__(self, self.on_message, self.__ws_server, *args, **kwargs)

    # async def __aenter__(self) -> WebSocketServer:
    #     return await self.server.__aenter__()
    #
    # async def __aexit__(self,
    #                     exc_type: Optional[Type[BaseException]],
    #                     exc_value: Optional[BaseException],
    #                     traceback: Optional[Exception],
    #                     ):
    #     await self.server.__aexit__(exc_type, exc_value, traceback)

    def connection_open(self) -> None:
        """握手完成回调"""
        super().connection_open()
        log.debug("AIOWebSocketServerImpl 打开握手完成回调")
        self.on_open(self.ws_server)

    # def __await__(self) -> Generator[Any, None, WebSocketServer]:
    #     return self.server.__await__()

    def on_open(self, server) -> None:
        """create_protocol"""
        pass

    async def on_error(self, conn: 'WebSocketServerProtocol', e: Exception):
        pass

    async def on_message(self, conn: 'WebSocketServerProtocol', path: str):
        """ws_handler"""
        try:
            if self.channel is None:
                channel = ChannelDefault(conn, self.ws_aio_server.get_config(),
                                         self.ws_aio_server.get_assistant())
                self.channel = channel
            message = await conn.recv()
            log.debug(message)
            frame: Frame = self.ws_aio_server.get_assistant().read(message)
            if frame is not None:
                await self.ws_aio_server._processor.on_receive(self.channel, frame)
        except Exception as e:
            log.error(e)
            raise e

    async def on_close(self, conn: 'WebSocketServerProtocol'):
        await conn.close()  # 完成握手


