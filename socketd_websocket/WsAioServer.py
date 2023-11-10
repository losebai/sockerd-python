from socketd.transport.Processor import Processor


class WsAioServer:

    def __init__(self):
        self.processor: Processor
