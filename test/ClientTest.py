import asyncio
import uuid
import time
from abc import ABC

from websockets.legacy.client import Connect, WebSocketClientProtocol

from socketd.core.Listener import Listener
from socketd.core.SocketD import SocketD
from socketd.core.config.ServerConfig import ServerConfig
from socketd.core.module.Message import Message
from socketd.core.module.StringEntity import StringEntity


class SimpleListener(Listener, ABC):

    def on_open(self, session):
        pass

    def on_message(self, session, message: Message):
        if message.is_request():
            session.replyEnd(message, StringEntity("test"))
        elif message.is_subscribe():
            session.replyEnd(message, StringEntity("test"))

    def on_close(self, session):
        pass

    def on_error(self, session, error):
        pass


def idGenerator(config):
    return config.id_generator(uuid.uuid4)


def main():
    server = SocketD.create_server(ServerConfig("ws").setPort(7779))
    server_session = server.config(idGenerator).listen(
        SimpleListener()).start()

    time.sleep(3)
    #
    client_session: WebSocketClientProtocol = SocketD.create_client("ws://127.0.0.1:7779") \
        .config(idGenerator).open()

    asyncio.get_event_loop().run_until_complete(client_session.send("org.noear.socketd.\nloser.bai".encode()))

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
