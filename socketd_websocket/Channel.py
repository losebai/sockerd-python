from typing import Any


class Channel:

    def __init__(self):
        self.is_closed: bool
        self.live_time: float

    def getAttachment(self, name): ...

    """
        获取附件
    """

    def setAttachment(self, name, val: Any): ...

    """
        设置附件
    """

    def removeAcceptor(self, sid): ...

    """
        移除接收器
    """

    def isValid(self): ...

    """
        是否有效
    """

    def isClosed(self): ...

    """
        是否已关闭
    """

    def getConfig(self) -> Any: ...

    """
        获取配置
    """

    def getRequests(self): ...

    """
        获取请求计数（用于背压控制）
    """

    def setHandshake(self, handshake): ...

    """
        设置握手信息
    """
