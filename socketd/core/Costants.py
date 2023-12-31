from io import BytesIO
from enum import Enum
from typing import Callable


Function = Callable


class Flag:
    Unknown = 0
    Connect = 10
    Connack = 11
    Ping = 20
    Pong = 21
    Close = 30
    Message = 40
    Request = 41
    Subscribe = 42
    Reply = 48
    ReplyEnd = 49

    @staticmethod
    def of(code):
        if code == 10:
            return Flag.Connect
        elif code == 11:
            return Flag.Connack
        elif code == 20:
            return Flag.Ping
        elif code == 21:
            return Flag.Pong
        elif code == 30:
            return Flag.Close
        elif code == 40:
            return Flag.Message
        elif code == 41:
            return Flag.Request
        elif code == 42:
            return Flag.Subscribe
        elif code == 48:
            return Flag.Reply
        elif code == 49:
            return Flag.ReplyEnd
        else:
            return Flag.Unknown

    @staticmethod
    def name(code):
        if code == 10:
            return "Connect"
        elif code == 11:
            return"Connack"
        elif code == 20:
            return "Ping"
        elif code == 21:
            return "Pong"
        elif code == 30:
            return "Close"
        elif code == 40:
            return "Message"
        elif code == 41:
            return "Request"
        elif code == 42:
            return "Subscribe"
        elif code == 48:
            return "Reply"
        elif code == 49:
            return "ReplyEnd"
        else:
            return "Unknown"


class Constants:
    DEF_SID = ""
    DEF_EVENT = ""
    DEF_META_STRING = ""
    DEF_DATA = BytesIO()
