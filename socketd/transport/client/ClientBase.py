
from Client import IClient
from socketd.core.ProcessorDefault import ProcessorDefault
from socketd.core.config.ClientConfig import ClientConfig


class ClientBase(IClient):

    def __init__(self, client_config: ClientConfig, assistant):
        self.processor = ProcessorDefault()
        self.heartbeat_handler = None
        self.config: ClientConfig = client_config
        self.assistant = assistant

    def assistant(self):
        return self.assistant

    def heartbeatInterval(self):
        return self.config.get_heartbeat_interval()

    def processor(self):
        return self.processor

    def heartbeatHandler(self, handler):
        if handler is not None:
            self.heartbeat_handler = handler

        return self

    def getConfig(self):
        return self.config

    def config(self, consumer):
        consumer(self.config)
        return self

    def process(self, processor):
        if processor is not None:
            self.processor = processor
        return self

    def listen(self, listener):
        self.processor.set_listener(listener)
        return self
