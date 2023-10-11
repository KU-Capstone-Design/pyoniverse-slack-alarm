from collections import UserDict

from chalicelib.model.enum.message_enum import MessageTypeEnum


class MessageTypeEmojiConverter(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(
            {
                MessageTypeEnum.SUCCESS: "party_blob",
                MessageTypeEnum.ERROR: "sadblob",
                MessageTypeEnum.DEBUG: "eyes-moving",
                MessageTypeEnum.TEST: "shipit",
            }
        )
