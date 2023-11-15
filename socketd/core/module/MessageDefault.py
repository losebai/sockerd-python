from Message import Message
from ..Costants import Constants, Flag


class MessageDefault(Message):
    def __init__(self):
        self.sid = Constants.DEF_SID
        self.topic = Constants.DEF_TOPIC
        self.entity = None
        self.flag = Flag.Unknown

    def get_flag(self):
        return self.flag

    def set_flag(self, flag):
        self.flag = flag

    def sid(self, sid):
        self.sid = sid
        return self

    def topic(self, topic):
        self.topic = topic
        return self

    def entity(self, entity):
        self.entity = entity
        return self

    def is_request(self):
        return self.flag == Flag.Request

    def is_subscribe(self):
        return self.flag == Flag.Subscribe

    def get_sid(self):
        return self.sid

    def get_topic(self):
        return self.topic

    def get_entity(self):
        return self.entity

    def __str__(self):
        return f"Message{{sid='{self.sid}', topic='{self.topic}', entity={self.entity}}}"