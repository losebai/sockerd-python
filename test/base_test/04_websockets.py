import sys
import unittest
import asyncio
import time

from loguru import logger
from websockets import serve, WebSocketServerProtocol, connect

from test.uitls import calc_async_time


class websockets_Test(unittest.TestCase):

    async def on_message(self, websocket: WebSocketServerProtocol, path: str):
        """ws_handler"""
        while True:
            message = await websocket.recv()
            logger.debug(message)
            if message == "close":
                await websocket.close()
                break
            if message is None:
                break

    async def _server(self):
        # set this future to exit the server
        __server = await serve(ws_handler=self.on_message, host="0.0.0.0", port=7780)

    async def client(self):
        uri = "ws://localhost:7780"
        async with connect(uri) as websocket:
            start_time = time.monotonic()
            for _ in range(100000):
                await websocket.send("test")
            end_time = time.monotonic()
            logger.info(f"Coroutine send took {(end_time - start_time) * 1000.0} monotonic to complete.")
            await websocket.send("close")
            await websocket.close()

    def test_application(self):
        logger.remove()
        logger.add(sys.stderr, level="INFO")
        @calc_async_time
        async def _main():
            # stop = asyncio.Future()
            await asyncio.gather(self._server(), self.client())
            # await stop
        asyncio.run(_main())


if __name__ == "__main__":
    websockets_Test().test_application()
