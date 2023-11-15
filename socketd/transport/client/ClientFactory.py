from Client import IClient
from socketd.core.config.ClientConfig import ClientConfig


class ClientFactory:

    """
        协议架构
    """
    def schema(self) -> str: ...

    """
        创建客户端
    """
    def createClient(self, clientConfig: ClientConfig) -> IClient: ...
