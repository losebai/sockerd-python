from abc import ABC, abstractmethod
from ClientConnector import ClientConnector
from ClientBase import ClientBase


class ClientConnectorBase(ABC, ClientConnector):
    def __init__(self, client: ClientBase):
        self.client = client

    @abstractmethod
    def heartbeatHandler(self):
        return self.client.heartbeat_handler

    @abstractmethod
    def heartbeatInterval(self):
        return self.client.heartbeatInterval()

    @abstractmethod
    def autoReconnect(self):
        return self.client.config.is_auto_reconnect()