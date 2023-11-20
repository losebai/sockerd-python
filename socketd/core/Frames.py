from socketd.core.Costants import Flag
import socketd.core.SocketD as SocketD
from socketd.core.module.EntityDefault import EntityDefault
from socketd.core.module.Frame import Frame
from socketd.core.module.MessageDefault import MessageDefault


class Frames:

    @staticmethod
    def connectFrame(sid, url):
        entity = EntityDefault()
        entity.putMeta("META_SOCKETD_VERSION", SocketD.SocketD.version())
        return Frame(Flag.Connect, MessageDefault().sid(sid).topic(url).entity(entity))

    @staticmethod
    def connackFrame(connectMessage):
        entity = EntityDefault()
        entity.putMeta("META_SOCKETD_VERSION", SocketD.SocketD.version())
        return Frame(Flag.Connack, MessageDefault().sid(connectMessage.sid).topic(connectMessage.topic).entity(entity))

    @staticmethod
    def pingFrame():
        return Frame(Flag.Ping, None)

    @staticmethod
    def pongFrame():
        return Frame(Flag.Pong, None)

    @staticmethod
    def closeFrame():
        return Frame(Flag.Close, None)