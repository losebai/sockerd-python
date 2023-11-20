from socketd.core.Buffer import Buffer
from socketd.core.Costants import Flag
from socketd.core.config.ServerConfig import ServerConfig
from socketd.core.module.EntityDefault import EntityDefault
from socketd.core.module.Frame import Frame
from socketd.core.module.MessageDefault import MessageDefault
from socketd.transport.CodecByteBuffer import CodecByteBuffer


def main():
    b = Buffer("\n你好11\n".encode("utf-8"))
    print(b.getvalue())
    b.flip()
    print(b.getvalue())

    code = CodecByteBuffer(ServerConfig("ws"))
    b1 = code.write(Frame(Flag.Message, MessageDefault().set_sid("sid").set_flag(Flag.Message).set_topic("top").set_entity(
        EntityDefault().set_meta_map({"meta":"meate"})
        .set_data("entityBytes"))),
                    lambda l: Buffer())
    print(b1.getvalue())
    b2 = code.read(b1)
    print(b2)


if __name__ == "__main__":
    main()
