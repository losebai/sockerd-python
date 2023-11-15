import uuid
import os
import ssl

from typing import Callable
from Config import Config
from socketd.core.handler.FragmentHandlerDefault import FragmentHandlerDefault
from socketd.transport.Codec import Codec


class ConfigBase(Config):

    def __init__(self, clientMode: bool):
        self.clientMode = clientMode
        self.charset = "UTF-8"
        self.codec: Codec = Codec()
        self.idGenerator: Callable = uuid.uuid4
        self.fragmentHandler: FragmentHandlerDefault = FragmentHandlerDefault()
        self.sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.executor = None
        self.coreThreads = os.cpu_count() * 2
        self.maxThreads = self.coreThreads * 8
        self.replyTimeout = 3000
        self.maxRequests = 10
        self.maxUdpSize = 2048

    def clientMode(self):
        return self.clientMode

    def getCharset(self):
        return self.charset

    def charset(self, charset):
        self.charset = charset
        return self

    def getCodec(self):
        return self.codec

    def codec(self, codec):
        assert codec is None
        self.codec = codec
        return self

    def getFragmentHandler(self):
        return self.fragmentHandler

    def fragmentHandler(self, fragmentHandler):
        assert fragmentHandler is None
        self.fragmentHandler = fragmentHandler
        return self

    def getIdGenerator(self):
        return self.idGenerator

    def idGenerator(self, idGenerator):
        assert idGenerator is None
        self.idGenerator = idGenerator
        return self

    def getSslContext(self):
        return self.sslContext

    def sslContext(self, localhost_pem: str):
        self.sslContext.load_cert_chain(localhost_pem)
        return self

    def getExecutor(self):
        return self.executor

    def executor(self, executor):
        self.executor = executor
        return self

    def getCoreThreads(self):
        return self.coreThreads

    def coreThreads(self, coreThreads):
        self.coreThreads = coreThreads
        return self

    def getMaxThreads(self):
        return self.maxThreads

    def maxThreads(self, maxThreads):
        self.maxThreads = maxThreads
        return self

    def getReplyTimeout(self):
        return self.replyTimeout

    def replyTimeout(self, replyTimeout):
        self.replyTimeout = replyTimeout
        return self

    def getMaxRequests(self):
        return self.maxRequests

    def maxRequests(self, maxRequests):
        self.maxRequests = maxRequests
        return self

    def getMaxUdpSize(self):
        return self.maxUdpSize

    def maxUdpSize(self, maxUdpSize):
        self.maxUdpSize = maxUdpSize
        return self
