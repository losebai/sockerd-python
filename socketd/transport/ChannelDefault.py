import io
import socket
from typing import Any, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
from abc import ABC, abstractmethod
from  module.Message import Message
from module.Frame import Frame
from Costants import Flag
from config.Config import Config
from Session import Session


class ChannelDefault('ChannelBase', 'Channel'):
    def __init__(self, source: S, config: 'Config', assistant: 'ChannelAssistant'):
        super().__init__(config)
        self.source = source
        self.assistant = assistant
        self.acceptor_map = {}
        self.session = None

    def remove_acceptor(self, sid: str) -> None:
        del self.acceptor_map[sid]

    def is_valid(self) -> bool:
        return self.assistant.is_valid(self.source)

    def get_remote_address(self) -> socket.Address:
        return self.assistant.get_remote_address(self.source)

    def get_local_address(self) -> socket.Address:
        return self.assistant.get_local_address(self.source)

    def send(self, frame: 'Frame', acceptor: 'Acceptor') -> None:
        self.assert_closed()

        if frame.message is not None:
            message = frame.message

            if acceptor is not None:
                self.acceptor_map[message.sid] = acceptor

            if message.entity is not None:
                with message.entity.data as ins:
                    if message.entity.data_size > Config.MAX_SIZE_FRAGMENT:
                        fragment_index = 0
                        while True:
                            fragment_entity = self.config.fragment_handler.nextFragment(
                                self.config, fragment_index, message.entity
                            )

                            if fragment_entity is not None:
                                fragment_frame = Frame(
                                    frame.flag,
                                    MessageDefault()
                                    .flag(frame.flag)
                                    .sid(message.sid)
                                    .entity(fragment_entity),
                                )
                                self.assistant.write(self.source, fragment_frame)
                            else:
                                return
                    else:
                        self.assistant.write(self.source, frame)
                        return

        self.assistant.write(self.source, frame)

    def retrieve(self, frame: 'Frame') -> None:
        acceptor = self.acceptor_map.get(frame.message.sid)
        if acceptor is not None:
            if acceptor.is_single() or frame.flag == Flag.ReplyEnd:
                del self.acceptor_map[frame.message.sid]

            acceptor.accept(frame.message)

    def get_session(self) -> Session:
        if self.session is None:
            self.session = SessionDefault(self)
        return self.session

    def close(self) -> None:
        super().close()
        self.acceptor_map.clear()
        self.assistant.close(self.source)


class ChannelAssistant(ABC):
    @abstractmethod
    def is_valid(self, source: Any) -> bool:
        pass

    @abstractmethod
    def get_remote_address(self, source: Any) -> socket.Address:
        pass

    @abstractmethod
    def get_local_address(self, source: Any) -> socket.Address:
        pass

    @abstractmethod
    def write(self, source: Any, frame: Frame) -> None:
        pass

    @abstractmethod
    def close(self, source: Any) -> None:
        pass
