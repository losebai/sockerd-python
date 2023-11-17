from abc import ABC
from typing import Dict, Union, Generator, TypeVar

from websockets.protocol import State

from socketd.core.ChannelBase import ChannelBase
from socketd.core.Costants import Function, Flag
from socketd.core.Session import Session
from socketd.core.SessionDefault import SessionDefault
from socketd.core.ThreadSafeDict import ThreadSafeDict
from socketd.core.config.Config import Config
from socketd.core.module.Frame import Frame
from socketd.core.module.MessageDefault import MessageDefault
from socketd.transport.ChannelAssistant import ChannelAssistant

from websockets.server import WebSocketServerProtocol

S = TypeVar("S")

thread_safe_dict = ThreadSafeDict()


class ChannelDefault(ChannelBase, Generator[S], ABC):

    def __init__(self, source: S, config: Config, assistant: ChannelAssistant[S], serve: WebSocketServerProtocol):
        super().__init__(config)
        self.source = source
        self.assistant = assistant
        self.acceptorMap = {}
        self.session: Session = None
        self.serve = serve

    def removeAcceptor(self, sid: str):
        self.acceptorMap.pop(sid)

    def isValid(self) -> bool:
        return self.assistant.is_valid(self.source)

    def getRemoteAddress(self) -> str:
        return self.assistant.get_remote_address(self.source)

    def getLocalAddress(self) -> str:
        return self.assistant.get_local_address(self.source)

    def assertClosed(self):
        assert self.serve.state == State.CLOSED

    def send(self, frame: Frame, acceptor: Function) -> None:

        if frame.get_message() is not None:
            message = frame.get_message()

            if acceptor is not None:
                self.acceptorMap[message.get_sid()] = acceptor

            if message.get_entity() is not None:
                with message.get_entity().get_data() as ins:
                    if message.get_entity().get_data_size() > Config.MAX_SIZE_FRAGMENT:
                        fragmentIndex = thread_safe_dict.set("AtomicReference", 0)
                        while True:
                            fragmentEntity = self.get_config().getFragmentHandler().nextFragment(self.get_config(),
                                                                                                 fragmentIndex,
                                                                                                 message.get_entity())
                            if fragmentEntity is not None:
                                fragmentFrame = Frame(frame.get_flag(), MessageDefault()
                                                      .flag(frame.get_flag())
                                                      .sid(message.get_sid())
                                                      .entity(fragmentEntity))
                                self.assistant.write(self.source, fragmentFrame)
                            else:
                                return
                    else:
                        self.assistant.write(self.source, frame)
                        return

        self.assistant.write(self.source, frame)

    def retrieve(self, frame: Frame) -> None:
        acceptor = self.acceptorMap.get(frame.get_message().get_sid())

        if acceptor is not None:
            if acceptor.isSingle() or frame.get_flag() == Flag.ReplyEnd:
                self.acceptorMap.pop(frame.get_message().get_sid())

            acceptor.accept(frame.get_message())

    def getSession(self) -> Session:
        if self.session is None:
            self.session = SessionDefault(self)

        return self.session

    def close(self) -> None:
        super().close()
        self.acceptorMap.clear()
        self.assistant.close(self.source)
