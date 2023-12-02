import asyncio
from typing import Optional, Sequence

from loguru import logger
from websockets.extensions import ClientExtensionFactory
from websockets.protocol import State
from websockets.uri import WebSocketURI

from socketd.core.ChannelDefault import ChannelDefault
from websockets import WebSocketClientProtocol, Origin, Subprotocol, HeadersLike

log = logger.opt()


class AIOWebSocketClientImpl(WebSocketClientProtocol):
    def __init__(self, client, *args, **kwargs):
        WebSocketClientProtocol.__init__(self, *args, **kwargs)
        self.client = client
        self.channel = ChannelDefault(self, client.get_config(), client.assistant())
        self.status_state = State.CONNECTING

    def get_channel(self):
        return self.channel

    async def handshake(self, wsuri: WebSocketURI, origin: Optional[Origin] = None,
                        available_extensions: Optional[Sequence[ClientExtensionFactory]] = None,
                        available_subprotocols: Optional[Sequence[Subprotocol]] = None,
                        extra_headers: Optional[HeadersLike] = None) -> None:
        """开始握手"""
        return_data = await super().handshake(wsuri, origin, available_extensions, available_subprotocols, extra_headers)
        await self.on_open()
        return return_data

    def connection_open(self) -> None:
        """打开握手完成回调"""
        super().connection_open()
        log.debug("AIOWebSocketClientImpl connection_open")

    async def on_open(self):
        log.info("Client:Websocket onOpen...")
        try:
            await self.channel.send_connect(self.client.get_config().get_url())
        except Exception as e:
            log.warning(str(e), exc_info=True)
            raise e

    def on_message(self, data: bytes):
        """处理消息"""
        try:
            frame = self.client.get_assistant().read(data)
            if frame is not None:
                self.client.processor().onReceive(self.channel, frame)
        except Exception as e:
            log.warning(str(e), exc_info=True)

    def on_close(self):
        self.client.processor().on_close(self.channel.get_session())

    def on_error(self, e):
        self.client.processor().on_error(self.channel.get_session(), e)
