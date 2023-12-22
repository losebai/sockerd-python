import asyncio

from test.modelu.BaseTestCase import BaseTestCase

from websockets.legacy.server import WebSocketServer
from loguru import logger

from socketd.core.Session import Session
from socketd.core.SocketD import SocketD
from socketd.core.config.ServerConfig import ServerConfig
from socketd.core.module.StringEntity import StringEntity
from socketd.transport.server.Server import Server
from test.modelu.SimpleListenerTest import SimpleListenerTest, config_handler, send_and_subscribe_test


class TestCase03_client_session_close(BaseTestCase):

    def __init__(self, schema, port):
        super().__init__(schema, port)
        self.server: Server
        self.server_session: WebSocketServer
        self.client_session: Session
        self.loop = asyncio.get_event_loop()

    async def _start(self):
        self.server: Server = SocketD.create_server(ServerConfig(self.schema).set_port(self.port))
        _simple = SimpleListenerTest()
        _server = self.server.config(config_handler).listen(_simple)
        self.server_session: WebSocketServer = await _server.start()

        serverUrl = self.schema + "://127.0.0.1:" + str(self.port) + "/path?u=a&p=2"
        self.client_session: Session = await SocketD.create_client(serverUrl) \
            .config(config_handler).open()
        await self.client_session.send_and_request("demo", StringEntity("test"), 100)


        try:
            await self.client_session.close()
            await self.client_session.send("demo", StringEntity("test"))
            await self.client_session.send_and_subscribe("demo", StringEntity("test"), send_and_subscribe_test, 100)
        except Exception as e:
            pass
        await asyncio.sleep(5)
        logger.info(f"counter {_simple.server_counter.get()} close_counter {_simple.close_counter.get()}")

    def start(self):
        super().start()
        self.loop.run_until_complete(self._start())

    async def _stop(self):
        if self.client_session:
            await self.client_session.close()

        if self.server_session:
            self.server_session.close()
        if self.server:
            await self.server.stop()

    def stop(self):
        super().stop()
        self.loop.run_until_complete(self._stop())

    def on_error(self):
        try:
            super().on_error()
        except Exception as e:
            logger.error(e)
