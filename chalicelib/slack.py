import json
import logging
import os

from requests import post

from chalicelib.converter.member_id_converter import MemberIdConverter
from chalicelib.converter.message_type_color_converter import MessageTypeColorConverter
from chalicelib.model.message import Message


class Slack:
    def __init__(self, log_name: str = None, **kwargs):
        self.logger = logging.getLogger(log_name or "pyoniverse-slack")
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send(self, message: Message, **kwargs) -> bool:
        """
        webhook 으로 POST 요청
        """
        # TODO : 이쁘게 만들기
        member_id_converter = MemberIdConverter()
        color_converter = MessageTypeColorConverter()
        channel_id = kwargs.get("channel_id", os.getenv("SLACK_CHANNEL_ID"))
        mention = " ".join(map(lambda x: f"<@{member_id_converter[x]}>", message.cc))
        color = color_converter[message.type]
        body = {
            "text": f"*{message.source} - {message.type}*",
            "channel": f"{channel_id}",
            "attachments": [
                {
                    "fallback": f"{message.source} - {message.type}",
                    "color": color,
                    "fields": [
                        {
                            "title": "CC",
                            "value": mention,
                            "short": True,
                        },
                        {
                            "title": "message",
                            "value": message.text,
                            "short": True,
                        },
                    ],
                },
                {
                    "fallback": "PS",
                    "color": color,
                    "fields": [
                        {"title": "PS", "value": v, "short": True} for v in message.ps
                    ],
                },
            ],
        }
        res = post(self.webhook_url, data=json.dumps(body))
        if res.status_code != 200:
            self.logger.error(f"Fail to send {body}")
            return False
        else:
            self.logger.info(f"Success to send {message}(Channel: {channel_id})")
            return True
