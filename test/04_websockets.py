import unittest
import asyncio
from websockets import serve, WebSocketServerProtocol, connect


class Test(unittest.TestCase):

    async def on_message(self, websocket: WebSocketServerProtocol, path: str):
        """ws_handler"""
        while True:
            message = await websocket.recv()
            if message is None:
                break

    def test_appilction(self):
        loop = asyncio.get_event_loop()
        async def _server():
            stop = asyncio.Future()  # set this future to exit the server
            __server = await serve(ws_handler=self.on_message, host="0.0.0.0", port=7779)
            await asyncio.sleep(10)
            await stop

        async def client():
            uri = "ws://localhost:7779"
            async with connect(uri) as websocket:
                for _ in range(100000):
                    await websocket.send("test")

        loop.run_until_complete(_server())
        loop.run_until_complete(client())

if __name__ == "__main__":
    pass