import asyncio
import logging

from websockets.client import connect as Connect, WebSocketClientProtocol

logger = logging.getLogger(__name__)


class WsAioClientConnector:
    def __init__(self, client: 'WsAioClient'):
        self.client: 'WsAioClient' = client
        self.real = None
        self.__loop = asyncio.get_event_loop()

    def connect(self) -> WebSocketClientProtocol:
        logger.debug('Start connecting to: {}'.format(self.client.getConfig().url))

        # 处理自定义架构的影响
        ws_url = self.client.getConfig().url.replace('-python://', '://')
        # parsed_url = urlparse(ws_url)

        # 支持 ssl
        if self.client.getConfig().get_ssl_context() is not None:
            # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            # ssl_context.load_cert_chain(certfile='path/to/certfile.pem', keyfile='path/to/keyfile.pem')
            # factory = ssl_context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=parsed_url.hostname)
            ws_url = ws_url.replace("ws", "wss")
        try:
            self.real = self.__loop.run_until_complete(Connect(ws_url, ssl=self.client.getConfig().get_ssl_context()))
            return self.real
        except RuntimeError as e:
            raise e
        except Exception as e:
            raise e

    def close(self):
        if self.real is None:
            return
        try:
            self.real.close()
            self.__loop.run_until_complete(self.real.__aexit__())
        except Exception as e:
            logger.debug('{}'.format(e))
