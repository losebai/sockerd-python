import pickle

from typing import Callable, Generator
from io import BytesIO
from .Codec import Codec
from socketd.core.module.Frame import Frame
from socketd.core.module.MessageDefault import MessageDefault
from socketd.core.module.EntityDefault import EntityDefault
from socketd.core.Costants import Flag
from socketd.core.config.Config import Config


class CodecByteBuffer(Codec):
    def __init__(self, config):
        self.config = config

    def write(self, frame: Frame, factory: Callable[[int], BytesIO]) -> BytesIO:
        if frame.message is None:
            # length (flag + int.bytes)
            len = 2 * 4
            target = factory(len)

            # length
            target.write(len)
            # flag
            target.write(frame.flag.value)
            target.flush()

            return target
        else:
            # sid
            sidB = frame.message.get_sid().encode(self.config.charset)
            # topic
            topicB = frame.message.get_topic().encode(self.config.charset)
            # metaString
            metaStringB = frame.message.get_entity().get_meta_string().encode(self.config.charset)

            # length (flag + sid + topic + metaString + data + int.bytes + \n*3)
            len = len(sidB) + len(topicB) + len(metaStringB) + frame.message.get_entity().get_data_size() + 2 * 3 + 2 * 4

            self.assertSize("sid", len(sidB), Config.MAX_SIZE_SID)
            self.assertSize("topic", len(topicB), Config.MAX_SIZE_TOPIC)
            self.assertSize("metaString", len(metaStringB), Config.MAX_SIZE_META_STRING)
            self.assertSize("data", frame.message.get_entity().get_data_size(), Config.MAX_SIZE_FRAGMENT)

            target = factory(len)

            # length
            target.write(len)

            # flag
            target.write(frame.flag.value)

            # sid
            target.write(sidB)
            target.write('\n')

            # topic
            target.write(topicB)
            target.write('\n')

            # metaString
            target.write(metaStringB)
            target.write('\n')

            # data
            pickle.dump(frame.message.get_entity().get_data(), target)
            target.flush()

            return target

    def read(self, buffer: BytesIO) -> Frame:
        len0 = ord(buffer.read(4))

        remaining_data = buffer.getbuffer()[buffer.tell():]  # 获取剩余的字节数据
        remaining_length = len(remaining_data)  # 获取剩余字节数据的长度
        if len0 > (remaining_length + 4):
            return None

        flag = buffer.read()

        if len0 == 8:
            # len + flag
            return Frame(Flag.of(flag), None)
        else:
            remaining_data = buffer.getbuffer()[buffer.tell():]  # 获取剩余的字节数据
            remaining_length = len(remaining_data)  # 获取剩余字节数据的长度
            metaBufSize = min(Config.MAX_SIZE_META_STRING, remaining_length)

            # 1. decode sid and topic
            sb = BytesIO()
            sid = self.decodeString(buffer, sb, Config.MAX_SIZE_SID)
            topic = self.decodeString(buffer, sb, Config.MAX_SIZE_TOPIC)
            metaString = self.decodeString(buffer, sb, Config.MAX_SIZE_META_STRING)

            # 2. decode body
            dataRealSize = len0 - buffer.position()
            if dataRealSize > Config.MAX_SIZE_FRAGMENT:
                # exceeded the limit, read and discard the bytes
                data = bytearray(Config.MAX_SIZE_FRAGMENT)
                buffer.readinto(data)
                for i in range(dataRealSize - Config.MAX_SIZE_FRAGMENT):
                    buffer.read()
            else:
                data = buffer.read(dataRealSize)

            message = MessageDefault().sid(sid).topic(topic).entity(
                EntityDefault().metaString(metaString).set_data(data)
            )
            message.flag = Flag.of(flag)
            return Frame(message.flag, message)

    def decodeString(self, reader: BytesIO, buf: BytesIO, maxLen: int) -> str:
        buf.seek(0)

        while True:
            c = reader.read(1)

            if c == b'\n':
                break

            if 0 < maxLen <= buf.tell():
                # exceeded the limit, read and discard the bytes
                pass
            else:
                if c != b' ':
                    buf.write(c)

        buf.seek(0)
        value = buf.getvalue().decode(self.config.charset)
        buf.truncate(0)
        buf.seek(0)

        return value

    def assertSize(self, name: str, size: int, limitSize: int) -> None:
        if size > limitSize:
            buf = f"This message {name} size is out of limit {limitSize} ({size})"
            raise RuntimeError(buf)