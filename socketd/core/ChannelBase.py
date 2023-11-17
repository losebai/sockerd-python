import time
from abc import ABC

from socketd.core.Channel import Channel


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
        return self.isClosed

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
        # Implement the send method based on your requirements
        pass

    def send_connack(self, connect_message):
        # Implement the send method based on your requirements
        pass

    def send_ping(self):
        # Implement the send method based on your requirements
        pass

    def send_pong(self):
        # Implement the send method based on your requirements
        pass

    def send_close(self):
        # Implement the send method based on your requirements
        pass

    def close(self):
        self.isClosed = True
        self.attachments.clear()