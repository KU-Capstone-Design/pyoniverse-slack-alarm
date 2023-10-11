from copy import deepcopy


class MessageBlockBuilder:
    """
    넣어진 순서대로 메시지 빌딩
    """

    def __init__(self):
        self.__block = []

    def add_header(self, text: str) -> "MessageBlockBuilder":
        self.__block.append(
            {
                "type": "header",
                "text": {"type": "plain_text", "text": text, "emoji": True},
            }
        )
        return self

    def add_markdown_section(self, text: str) -> "MessageBlockBuilder":
        self.__block.append(
            {"type": "section", "text": {"type": "mrkdwn", "text": text}}
        )
        return self

    def add_divider(self) -> "MessageBlockBuilder":
        self.__block.append({"type": "divider"})
        return self

    def add_plain_text_section(self, text: str) -> "MessageBlockBuilder":
        self.__block.append(
            {
                "type": "section",
                "text": {"type": "plain_text", "text": text, "emoji": True},
            }
        )
        return self

    def build(self) -> list:
        return deepcopy(self.__block)
