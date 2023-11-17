import asyncio

from abc import ABC

from .SessionBase import SessionBase
from .Channel import Channel
from .Handshake import Handshake
from .module.Entity import Entity
from .module.Message import Message
from .module.Frame import Frame
from .Costants import Flag, Function
from .module.MessageDefault import MessageDefault


class SessionDefault(SessionBase, ABC):

    def __init__(self, channel: Channel):
        super().__init__(channel)
        self.__loop = asyncio.get_event_loop()

    def isValid(self) -> bool:
        return self.channel.is_valid()

    def getRemoteAddress(self) -> str:
        return self.channel.get_remote_address()

    def getLocalAddress(self) -> str:
        return self.channel.get_local_address()

    def getHandshake(self) -> Handshake:
        return self.channel.get_handshake()

    def sendPing(self):
        self.channel.send_ping()

    def send(self, topic: str, content: Entity):
        message = MessageDefault().sid(self.generateId()).topic(topic).entity(content)
        self.channel.send(Frame(Flag.Message, message), None)

    def sendAndRequest(self, topic: str, content: Entity) -> Entity:
        return self.sendAndRequest(topic, content, self.channel.getConfig().getReplyTimeout())

    def sendAndRequest(self, topic: str, content: Entity, timeout: int) -> Entity:
        if self.channel.getRequests().get() > self.channel.getConfig().getMaxRequests():
            raise Exception("Sending too many requests: " + str(self.channel.getRequests().get()))
        else:
            self.channel.getRequests().incrementAndGet()

        message = MessageDefault().sid(self.generateId()).topic(topic).entity(content)

        try:
            self.__loop.run_in_executor(None, lambda: self.channel.send(Frame(Flag.Request, message)))
        except Exception as e:
            raise Exception(e)
        finally:
            self.channel.remove_acceptor(message.getSid())
            self.channel.get_requests().denominator()

    def sendAndSubscribe(self, topic: str, content: Entity, consumer: Function[Entity]):
        message = MessageDefault().sid(self.generate_id()).topic(topic).entity(content)
        self.channel.send(Frame(Flag.Subscribe, message), AcceptorSubscribe(consumer))

    def reply(self, from_msg: Message, content: Entity):
        self.channel.send(Frame(Flag.Reply, MessageDefault().sid(from_msg.getSid()).entity(content)), None)

    def replyEnd(self, from_msg: Message, content: Entity):
        self.channel.send(Frame(Flag.ReplyEnd, MessageDefault().sid(from_msg.getSid()).entity(content)), None)

    def close(self):
        self.channel.close()


class AcceptorRequest:
    def __init__(self, future: CompletableFuture, timeout: int):
        self.future = future
        self.timeout = timeout

    def run(self):
        self.future.completeExceptionally(IOException("Request canceled or timed out"))


class AcceptorSubscribe(Runnable):
    def __init__(self, consumer: Consumer[Entity]):
        self.consumer = consumer

    def run(self):
        pass  # Perform your subscription logic here, e.g., invoking the consumer
