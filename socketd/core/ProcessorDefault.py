from loguru import logger
from Processor import Processor
from Costants import Flag


class ProcessorDefault(Processor):

    def __init__(self):
        self.listener = SimpleListener()

    def setListener(self, listener):
        if listener is not None:
            self.listener = listener

    def onReceive(self, channel, frame):
        if self.log.isTraceEnabled():
            self.log.trace("{}", frame)

        if frame.getFlag() == Flag.Connect:
            connectMessage = frame.getMessage()
            channel.setHandshake(Handshake(connectMessage))
            channel.sendConnack(connectMessage)
            self.onOpen(channel.getSession())
        elif frame.getFlag() == Flag.Connack:
            message = frame.getMessage()
            channel.setHandshake(Handshake(message))
            self.onOpen(channel.getSession())
        else:
            if channel.getHandshake() is None:
                channel.close()
                if self.log.isWarnEnabled():
                    self.log.warn("Channel handshake is None, sessionId={}", channel.getSession().getSessionId())
                return

            channel.setLiveTime()

            try:
                if frame.getFlag() == Flag.Ping:
                    channel.sendPong()
                elif frame.getFlag() == Flag.Pong:
                    pass
                elif frame.getFlag() == Flag.Close:
                    channel.close()
                    self.onClose(channel.getSession())
                elif frame.getFlag() in [Flag.Message, Flag.Request, Flag.Subscribe]:
                    self.onReceiveDo(channel, frame, False)
                elif frame.getFlag() in [Flag.Reply, Flag.ReplyEnd]:
                    self.onReceiveDo(channel, frame, True)
                else:
                    channel.close()
                    self.onClose(channel.getSession())
            except Exception as e:
                self.onError(channel.getSession(), e)

    def onReceiveDo(self, channel, frame, isReply):
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
            self.onMessage(channel.getSession(), frame.getMessage())

    def onOpen(self, session):
        self.listener.onOpen(session)

    def onMessage(self, session, message):
        self.listener.onMessage(session, message)

    def onClose(self, session):
        self.listener.onClose(session)

    def onError(self, session, error):
        self.listener.onError(session, error)
