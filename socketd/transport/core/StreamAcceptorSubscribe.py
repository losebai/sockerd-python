from typing import Callable

from socketd.core.module.Entity import Entity
from socketd.core.module.Message import Message
from socketd.transport.core.StreamAcceptorBase import StreamAcceptorBase


class StreamAcceptorSubscribe(StreamAcceptorBase):

    def __init__(self, future, timeout):
        self.future: Callable[[Entity], None] = future
        self.timeout = timeout

    def is_single(self):
        return False

    def is_done(self):
        return False

    def accept(self, message: Message, onError) -> None:
        try:
            self.future(message)
        except Exception as e:
            onError(e)
