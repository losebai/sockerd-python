from io import BytesIO

from socketd.core.Buffer import Buffer
from socketd.core.config.Config import Config
from socketd.core.module.Frame import Frame
from websockets.server import WebSocketServer, WebSocketServerProtocol
from websockets.protocol import State
from socketd.transport.ChannelAssistant import ChannelAssistant


class WsAioChannelAssistant(ChannelAssistant):
    def __init__(self, config: Config):
        self.config = config

    async def write(self, source: WebSocketServerProtocol, frame: Frame) -> None:
        writer = self.config.get_codec().write(frame, lambda l: BytesIO())
        await source.send(writer)

    def is_valid(self, target: WebSocketServerProtocol) -> bool:
        return target.state() == State.OPEN

    async def close(self, target: WebSocketServerProtocol) -> None:
        await target.close()

    def get_remote_address(self, target: WebSocketServerProtocol) -> str:
        return target.remote_address

    def get_local_address(self, target: WebSocketServerProtocol) -> str:
        return target.local_address

    def read(self, buffer: bytearray) -> Frame:
        return self.config.get_codec().read(Buffer(buffer))
