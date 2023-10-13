import json
import logging
import os

from requests import post

from chalicelib.builder.message_block_builder import MessageBlockBuilder
from chalicelib.converter.member_id_converter import MemberIdConverter
from chalicelib.converter.message_type_color_converter import MessageTypeColorConverter
from chalicelib.converter.message_type_emoji_converter import MessageTypeEmojiConverter
from chalicelib.model.message import Message


class Slack:
    def __init__(self, log_name: str = None, **kwargs):
        self.logger = logging.getLogger(log_name or "pyoniverse-slack")
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send(self, message: Message, **kwargs) -> bool:
        """
        webhook 으로 POST 요청
        """
        member_id_converter = MemberIdConverter()
        color_converter = MessageTypeColorConverter()
        emoji_converter = MessageTypeEmojiConverter()
        channel_id = kwargs.get("channel_id", os.getenv("SLACK_CHANNEL_ID"))
        mention = " ".join(map(lambda x: f"<@{member_id_converter[x]}>", message.cc))
        color = color_converter[message.type]
        emoji = emoji_converter[message.type]

        block_builder = MessageBlockBuilder()
        block_builder.add_header(f"{message.type}: {message.source} :{emoji}:")
        block_builder.add_markdown_section(mention)
        block_builder.add_divider()
        block_builder.add_plain_text_section(message.text)
        block_builder.add_divider()
        block_builder.add_header("Additional Information")
        for k, v in message.ps.items():
            block_builder.add_markdown_section(f"*{k}*")
            block_builder.add_plain_text_section(v)
            block_builder.add_divider()
        body = {"blocks": block_builder.build()}
        res = post(self.webhook_url, data=json.dumps(body))
        if res.status_code != 200:
            self.logger.error(f"Fail to send {body}. Because {res.text}")
            return False
        else:
            self.logger.info(f"Success to send {message}(Channel: {channel_id})")
            return True
