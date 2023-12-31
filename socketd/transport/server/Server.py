from typing import Callable, Coroutine
from asyncio import Future

from websockets.sync.server import WebSocketServer

from socketd.core.config.ServerConfig import ServerConfig
from socketd.core.Processor import Processor
from socketd.core.Listener import Listener


class Server:
    def config(self, consumer: Callable[[ServerConfig], ServerConfig]) -> 'Server': ...

    def process(self, processor: Processor) -> 'Server': ...

    def listen(self, listener: Listener) -> 'Server': ...

    def start(self) -> WebSocketServer | Coroutine: ...

    def stop(self) -> Coroutine: ...

    def get_assistant(self): ...

    def get_config(self): ...