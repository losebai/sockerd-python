from abc import ABC

from .Entity import Entity


class EntityDefault(Entity, ABC):
    def __init__(self):
        self.metaMap = None
        self.metaString = "DEF_META_STRING"
        self.metaStringChanged = False
        self.data = None
        self.dataSize = 0

    def set_metaString(self, metaString):
        self.metaMap = None
        self.metaString = metaString
        self.metaStringChanged = False
        return self

    def getMetaString(self):
        if self.metaStringChanged:
            buf = ""
            for name, val in self.getMetaMap().items():
                buf += f"{name}={val}&"
            if len(buf) > 0:
                buf = buf[:-1]
            self.metaString = buf
            self.metaStringChanged = False
        return self.metaString

    def set_metaMap(self, metaMap):
        self.metaMap = metaMap
        self.metaString = None
        self.metaStringChanged = True
        return self

    def getMetaMap(self):
        if self.metaMap is None:
            self.metaMap = {}
            self.metaStringChanged = False
            if self.metaString:
                for kvStr in self.metaString.split("&"):
                    kv = kvStr.split("=")
                    if len(kv) > 1:
                        self.metaMap[kv[0]] = kv[1]
                    else:
                        self.metaMap[kv[0]] = ""
        return self.metaMap

    def set_meta(self, name, val):
        self.putMeta(name, val)
        return self

    def putMeta(self, name, val):
        self.getMetaMap()[name] = val
        self.metaStringChanged = True

    def getMeta(self, name):
        return self.getMetaMap().get(name)

    def getMetaOrDefault(self, name, default_val):
        return self.getMetaMap().get(name, default_val)

    def set_data(self, data):
        self.data = data
        self.dataSize = len(data)
        return self

    def getData(self):
        return self.data

    def getDataAsString(self):
        return str(self.data, 'utf-8')  # Assuming data is of type bytes

    def getDataSize(self):
        return self.dataSize

    def __str__(self):
        return f"Entity(meta='{self.getMetaString()}', data=byte[{self.dataSize}])"


