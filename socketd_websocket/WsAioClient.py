from socketd.transport.client.ClientBase import ClientBase
from socketd.core.config.ClientConfig import ClientConfig
from WsAioChannelAssistant import WsAioChannelAssistant
from websockets.client import connect as Connect


class WsAioClient(ClientBase):

    def __init__(self, config: ClientConfig):
        super().__init__(config, WsAioChannelAssistant(config))
        self.client = None

    def open(self):
        self.client = Connect(self.config.uri)
        return self.client
