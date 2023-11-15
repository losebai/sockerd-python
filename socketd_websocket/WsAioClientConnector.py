import logging
import socket
import ssl
from websockets.client import connect as Connect
from urllib.parse import urlparse
from WsAioClient import WsAioClient

logger = logging.getLogger(__name__)


class WsBioClientConnector:
    def __init__(self, client: WsAioClient):
        self.client: WsAioClient = client
        self.real = None

    def connect(self):
        logger.debug('Start connecting to: {}'.format(self.client.getConfig().getUrl()))

        # 处理自定义架构的影响
        ws_url = self.client.getConfig().getUrl().replace('-java://', '://')
        # parsed_url = urlparse(ws_url)

        # 支持 ssl
        if self.client.getConfig().getSslContext() is not None:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.load_cert_chain(certfile='path/to/certfile.pem', keyfile='path/to/keyfile.pem')
            # factory = ssl_context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=parsed_url.hostname)
            self.client.getConfig().getSslContext()
            ws_url = ws_url.replace("ws", "wss")
        try:
            self.real = Connect(ws_url, ssl=self.client.getConfig().getSslContext())
        except RuntimeError as e:
            raise e
        except Exception as e:
            raise e

    def close(self):
        if self.real is None:
            return

        try:
            self.real.close()
        except Exception as e:
            logger.debug('{}'.format(e))
