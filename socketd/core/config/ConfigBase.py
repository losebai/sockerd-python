import os
import ssl

from typing import Callable
from .Config import Config
from socketd.core.handler.FragmentHandlerDefault import FragmentHandlerDefault
from socketd.transport.Codec import Codec
from socketd.transport.CodecByteBuffer import CodecByteBuffer


class ConfigBase(Config):

    def __init__(self, clientMode: bool):
        self._clientMode = clientMode
        self._charset = "UTF-8"
        self._codec: Codec = CodecByteBuffer(self)
        self._idGenerator: Callable = None
        self._fragmentHandler: FragmentHandlerDefault = FragmentHandlerDefault()
        self._sslContext = None
        self._executor = None
        self._coreThreads = os.cpu_count() * 2
        self._maxThreads = self._coreThreads * 8
        self._replyTimeout = 3000
        self._maxRequests = 10
        self._maxUdpSize = 2048

    def clientMode(self):
        return self._clientMode

    def getCharset(self):
        return self._charset

    def charset(self, charset):
        self._charset = charset
        return self

    def getCodec(self):
        return self._codec

    def codec(self, codec):
        assert codec is None
        self._codec = codec
        return self

    def getFragmentHandler(self):
        return self.fragmentHandler

    def fragmentHandler(self, fragmentHandler):
        assert fragmentHandler is None
        self._fragmentHandler = fragmentHandler
        return self

    def getIdGenerator(self):
        return self._idGenerator

    def idGenerator(self, _idGenerator):
        # assert _idGenerator is None
        self._idGenerator = _idGenerator
        return self

    def getSslContext(self):
        return self._sslContext

    def sslContext(self, localhost_pem: str):
        self._sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self._sslContext.load_cert_chain(localhost_pem)
        return self

    def getExecutor(self):
        return self._executor

    def executor(self, executor):
        self._executor = executor
        return self

    def getCoreThreads(self):
        return self._coreThreads

    def coreThreads(self, coreThreads):
        self._coreThreads = coreThreads
        return self

    def getMaxThreads(self):
        return self._maxThreads

    def maxThreads(self, maxThreads):
        self._maxThreads = maxThreads
        return self

    def getReplyTimeout(self):
        return self._replyTimeout

    def replyTimeout(self, replyTimeout):
        self._replyTimeout = replyTimeout
        return self

    def getMaxRequests(self):
        return self._maxRequests

    def maxRequests(self, maxRequests):
        self._maxRequests = maxRequests
        return self

    def getMaxUdpSize(self):
        return self._maxUdpSize

    def maxUdpSize(self, maxUdpSize):
        self._maxUdpSize = maxUdpSize
        return self
