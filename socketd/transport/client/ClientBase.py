from abc import ABC

from .Client import Client
from socketd.core.ProcessorDefault import ProcessorDefault
from socketd.core.config.ClientConfig import ClientConfig


class ClientBase(Client, ABC):

    def __init__(self, client_config: ClientConfig, assistant):
        self._processor = ProcessorDefault()
        self._heartbeat_handler = None
        self._config: ClientConfig = client_config
        self._assistant = assistant

    def assistant(self):
        return self._assistant

    def heartbeatInterval(self):
        return self._config.get_heartbeat_interval()

    def processor(self):
        return self._processor

    def heartbeatHandler(self, handler):
        if handler is not None:
            self._heartbeat_handler = handler
        return self

    def getConfig(self):
        return self._config

    def config(self, consumer):
        consumer(self._config)
        return self

    def process(self, processor):
        if processor is not None:
            self._processor = processor
        return self

    def listen(self, listener):
        self._processor.set_listener(listener)
        return self
