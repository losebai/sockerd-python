from socketd.core.Buffer import Buffer
from socketd.core.Costants import Flag
from socketd.core.config.ServerConfig import ServerConfig
from socketd.core.module.Frame import Frame
from socketd.core.module.MessageDefault import MessageDefault
from socketd.core.module.StringEntity import StringEntity
from socketd.transport.CodecByteBuffer import CodecByteBuffer


def main():
    b = Buffer()
    b.put_int(Flag.Message.value)
    print(b.getvalue())
    b.flip()
    print(b.getvalue())
    print(b.size())

    code = CodecByteBuffer(ServerConfig("ws"))
    b1 = code.write(Frame(Flag.Message,
                          MessageDefault().set_sid("1700534070000000001")
                          .set_flag(Flag.Subscribe)
                          .set_topic("tcp-java://127.0.0.1:9386/path?u=a&p=2")
                          .set_entity(StringEntity("test"))
                          ),
                    lambda l: Buffer())
    print(b1.getvalue())
    b1.seek(0)
    b2 = code.read(b1)
    print(b2)
    b1.close()


if __name__ == "__main__":
    main()
