from abc import ABC

from Listener import Listener


class Processor(Listener, ABC):

    def set_listener(self, listener):
        pass

    def on_receive(self, channel, frame):
        pass
