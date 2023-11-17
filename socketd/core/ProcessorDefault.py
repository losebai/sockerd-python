from abc import ABC
from loguru import logger

from .Handshake import Handshake
from .Processor import Processor
from .Costants import Flag
from .SimpleListener import SimpleListener
from .module.Entity import EntityMetas


class ProcessorDefault(Processor, ABC):

    def __init__(self):
        self.listener = SimpleListener()
        self.log = logger.opt()

    def set_listener(self, listener):
        if listener is not None:
            self.listener = listener

    def on_receive(self, channel, frame):
        self.log.trace("{}", frame)

        if frame.getFlag() == Flag.Connect:
            connectMessage = frame.getMessage()
            channel.setHandshake(Handshake(connectMessage))
            channel.sendConnack(connectMessage)
            self.on_open(channel.getSession())
        elif frame.getFlag() == Flag.Connack:
            message = frame.getMessage()
            channel.setHandshake(Handshake(message))
            self.on_open(channel.getSession())
        else:
            if channel.getHandshake() is None:
                channel.close()
                self.log.warning("Channel handshake is None, sessionId={}", channel.getSession().getSessionId())
                return

            channel.setLiveTime()

            try:
                if frame.getFlag() == Flag.Ping:
                    channel.sendPong()
                elif frame.getFlag() == Flag.Pong:
                    pass
                elif frame.getFlag() == Flag.Close:
                    channel.close()
                    self.on_close(channel.getSession())
                elif frame.getFlag() in [Flag.Message, Flag.Request, Flag.Subscribe]:
                    self.on_receive_do(channel, frame, False)
                elif frame.getFlag() in [Flag.Reply, Flag.ReplyEnd]:
                    self.on_receive_do(channel, frame, True)
                else:
                    channel.close()
                    self.on_close(channel.getSession())
            except Exception as e:
                self.on_error(channel.getSession(), e)

    def on_receive_do(self, channel, frame, isReply):
        fragmentIdxStr = frame.getMessage().getEntity().getMeta(EntityMetas.META_DATA_FRAGMENT_IDX)
        if fragmentIdxStr is not None:
            index = int(fragmentIdxStr)
            frameNew = channel.getConfig().getFragmentHandler().aggrFragment(channel, index, frame)

            if frameNew is None:
                return
            else:
                frame = frameNew

        if isReply:
            channel.retrieve(frame)
        else:
            self.on_message(channel.getSession(), frame.getMessage())

    def on_open(self, session):
        self.listener.on_open(session)

    def on_message(self, session, message):
        self.listener.on_message(session, message)

    def on_close(self, session):
        self.listener.on_close(session)

    def on_error(self, session, error):
        self.listener.on_error(session, error)
