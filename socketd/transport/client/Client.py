# 客户端
from abc import ABC, abstractmethod
from typing import Callable


class Client(ABC):

    @abstractmethod
    def heartbeatHandler(self, handler: Callable) -> 'Client': ...

    @abstractmethod
    def config(self, consumer: Callable[['ClientConfig'], None]) -> 'Client': ...

    @abstractmethod
    def process(self, processor: Callable) -> 'Client': ...

    @abstractmethod
    def listen(self, listener: Callable) -> 'Client': ...

    @abstractmethod
    def open(self): ...
