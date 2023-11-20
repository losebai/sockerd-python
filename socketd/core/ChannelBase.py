import time
import asyncio
from abc import ABC

from socketd.core.Channel import Channel
from socketd.core.Frames import Frames


class ChannelBase(Channel, ABC):
    def __init__(self, config):
        self.config = config
        self.requests = 0
        self.handshake = None
        self.liveTime = 0
        self.attachments = {}
        self.isClosed = False

    def get_attachment(self, name):
        return self.attachments.get(name, None)

    def set_attachment(self, name, val):
        self.attachments[name] = val

    def is_closed(self):
        return self.is_closed()

    def get_requests(self):
        return self.requests

    def set_handshake(self, handshake):
        self.handshake = handshake

    def get_handshake(self):
        return self.handshake

    def set_live_time(self):
        self.liveTime = int(time.time() * 1000)

    def get_live_time(self):
        return self.liveTime

    def send_connect(self, uri):
        self.send(Frames.connectFrame(self.config.get_id_generator().generate(), uri), None)

    def send_connack(self, connect_message):
        self.send(Frames.connackFrame(connect_message), None)

    def send_ping(self):
        self.send(Frames.pingFrame(), None)

    def send_pong(self):
        self.send(Frames.pongFrame(), None)

    def send_close(self):
        self.send(Frames.closeFrame(), None)

    async def close(self, code: int = 1000,
                    reason: str = "", ):
        await self.close(code, reason)
        self.isClosed = True
        self.attachments.clear()

    def get_config(self) -> 'Config':
        return self.config
