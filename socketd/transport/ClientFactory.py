from Client import IClient, IClientConfig


class ClientConfig(IClientConfig):
    """协议号"""
    schema: str
    url: str
    uri: str
    port: int
    heartbeatInterval: float
    """连接超时"""
    connectTimeout: float
    """读缓冲大小"""
    readBufferSize: int
    """写缓冲大小"""
    writeBufferSize: int
    """是否自动重链"""
    autoReconnect: bool


class ClientFactory:
    """
        协议架构
    """

    def schema(self) -> str: ...

    """
        创建客户端
    """

    def createClient(self, clientConfig: ClientConfig) -> IClient: ...
