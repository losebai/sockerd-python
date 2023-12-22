from typing import Callable

from socketd.core.module.Entity import Entity
from socketd.core.module.Message import Message
from socketd.transport.core.StreamAcceptorBase import StreamAcceptorBase


class StreamAcceptorSubscribe(StreamAcceptorBase):

    def __init__(self, future, timeout):
        self.future: Callable[[Entity], None] = future
        self.timeout = timeout

    def is_single(self):
        """
        判断是否单身
        :param self: 实例对象
        :return: 单身返回False，非单身返回True
        """
        return False

    def is_done(self):
        """
        判断是否完成任务

        :return: 返回布尔值，表示任务是否完成
        """
        return False


    def accept(self, message: Message, onError) -> None:
        """
        接受消息并处理
        :param message: 要处理的消息
        :param onError: 处理异常的回调函数
        :return: None
        """
        try:
            self.future(message)
        except Exception as e:
            onError(e)

