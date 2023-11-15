

class Config:
    # 流ID大小限制
    MAX_SIZE_SID = 64
    # 主题大小限制
    MAX_SIZE_TOPIC = 512
    # 元信息串大小限制
    MAX_SIZE_META_STRING = 4096
    # 分片大小限制
    MAX_SIZE_FRAGMENT = 1024 * 1024 * 16


    def clientMode(self):
        """
        返回一个布尔值，指示配置是否为客户端模式。
        """
        pass

    def getSchema(self):
        """
        返回协议架构。
        """
        pass

    def getCharset(self):
        """
        返回字符集。
        """
        pass

    def getCodec(self):
        """
        返回编解码器。
        """
        pass

    def getIdGenerator(self):
        """
        返回ID生成器。
        """
        pass

    def getFragmentHandler(self):
        """
        返回分片处理器。
        """
        pass

    def getSslContext(self):
        """
        返回SSL上下文。
        """
        pass

    def getExecutor(self):
        """
        返回执行器（第一优先级，某些底层可能不支持）。
        """
        pass

    def getCoreThreads(self):
        """
        返回核心线程数（第二优先级）。
        """
        pass

    def getMaxThreads(self):
        """
        返回最大线程数。
        """
        pass

    def getReplyTimeout(self):
        """
        返回答复超时时间（单位：毫秒）。
        """
        pass

    def getMaxRequests(self):
        """
        返回允许的最大请求数。
        """
        pass

    def getMaxUdpSize(self):
        """
        返回允许的最大UDP包大小。
        """
        pass
