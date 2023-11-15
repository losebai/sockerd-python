from abc import ABC, abstractmethod
from typing import Generator, Generic, Type, TypeVar, Union, Callable, Optional
from socketd.core.Costants import Function
from socketd.core.module.Frame import Frame

In = TypeVar("In", bound=Type)
Out = TypeVar("Out", bound=Type)


class Codec(ABC, Generic[In, Out]):
    """
    编解码器
    """

    @abstractmethod
    def read(self, buffer: In) -> Frame:
        """
        编码
        """
        pass

    @abstractmethod
    def write(self, frame, target: Function[Union[In, Type]]) -> Generator['Out']:
        """
        解码
        """
        pass
