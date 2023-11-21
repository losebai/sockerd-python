import threading
from abc import ABC

from socketd.core.ChannelBase import ChannelBase
from socketd.transport.client.ClientConnector import ClientConnector


class ClientChannel(ChannelBase, ABC):
    def __init__(self, real: 'AIOConnect', connector: ClientConnector):
        super().__init__(real.get_config())
        self.real = real
        self.connector: ClientConnector = connector
        self.heartbeatHandler = connector.heartbeatHandler()

        # if self.heartbeatHandler is None:
        #     self.heartbeatHandler = HeartbeatHandlerDefault()
        connector.autoReconnect()
        # if connector.autoReconnect() and self.heartbeatScheduledFuture is None:
        #     self.heartbeatScheduledFuture = threading.Timer(connector.heartbeatInterval(), self.heartbeatHandle)
        #     self.heartbeatScheduledFuture.start()

    def removeAcceptor(self, sid):
        if self.real is not None:
            self.real.removeAcceptor(sid)

    def isValid(self):
        if self.real is None:
            return False
        else:
            return self.real.isValid()

    def isClosed(self):
        if self.real is None:
            return False
        else:
            return self.real.isClosed()

    def getRemoteAddress(self):
        if self.real is None:
            return None
        else:
            return self.real.getRemoteAddress()

    def getLocalAddress(self):
        if self.real is None:
            return None
        else:
            return self.real.get_local_address()

    def heartbeatHandle(self):
        self.assert_closed()

        with self:
            try:
                self.prepareSend()
                self.heartbeatHandler.heartbeatHandle(self.getSession())
            except Exception as e:
                if self.connector.autoReconnect():
                    self.real.close()
                    self.real = None
                raise e

    async def send(self, frame, acceptor):
        # self.assert_closed()
        try:
            self.prepareSend()
            await self.real.send(frame, acceptor)
        except Exception as e:
            if self.connector.autoReconnect():
                self.real.close()
                self.real = None

            raise e

    def retrieve(self, frame):
        self.real.retrieve(frame)

    def getSession(self):
        return self.real.getSession()

    async def close(self, code: int = 1000,
                    reason: str = "", ):
        try:
            await super().close(code, reason)
            if self.real is not None:
                self.real.close()
        except:
            pass

    def prepareSend(self):
        if self.real is None or not self.real.is_valid():
            self.real = self.connector.connect()
            return True
        else:
            return False
