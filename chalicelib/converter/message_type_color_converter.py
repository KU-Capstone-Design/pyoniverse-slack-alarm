from collections import UserDict

from chalicelib.model.enum.message_enum import MessageTypeEnum


class MessageTypeColorConverter(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(
            {
                MessageTypeEnum.SUCCESS: "#00FF00",  # GREEN
                MessageTypeEnum.ERROR: "#FF0000",  # RED
                MessageTypeEnum.TEST: "#0000FF",  # BLUE
                MessageTypeEnum.DEBUG: "#FF00FF",  # PINK
            }
        )
