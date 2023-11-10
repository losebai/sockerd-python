#客户端

from typing import Callable

class IClient:
    def heartbeatHandler(self, handler: Callable) -> 'IClient':...

    def config(self, consumer: Callable[['IClientConfig'], None]) -> 'IClient':...

    def process(self, processor: Callable) -> 'IClient':...

    def listen(self, listener: Callable) -> 'IClient':...

    def open(self):...

class IClientConfig:...

class IHeartbeatHandler:...

class IProcessor:...

class IListener:...
