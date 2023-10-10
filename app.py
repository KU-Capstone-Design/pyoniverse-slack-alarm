import json
import os
from dataclasses import asdict
from functools import reduce

import dotenv
from chalice import Chalice
from chalice.app import SQSEvent
from marshmallow import ValidationError

from chalicelib.model.enum.message_enum import MessageTypeEnum
from chalicelib.model.message import Message
from chalicelib.slack import Slack


# Local debug
if ".env" in os.listdir():
    dotenv.load_dotenv()

if os.getenv("LOG_LEVEL", "DEBUG") == "DEBUG":
    debug = True
else:
    debug = False

app = Chalice(app_name="pyoniverse-slack", debug=debug)
slack = Slack(log_name=app.app_name)


@app.on_sqs_message(
    queue=os.getenv("QUEUE_NAME"),
    batch_size=1,
)
def send_message(event: SQSEvent):
    success = 0
    total = 0
    invalid_messages = []
    for _record in event:
        total += 1
        try:
            message: Message = Message.load(json.loads(_record.body))
        except ValidationError as e:
            invalid_messages.append((json.loads(_record.body), e.messages))
        else:
            if slack.send(message=message):
                success += 1
    app.log.info(f"result: {success}/{total}")
    if invalid_messages:
        message = Message(
            type=MessageTypeEnum.DEBUG,
            source=app.app_name,
            text="Invalid Message Format",
            ps=[str({"reason": m[1], "message": m[0]}) for m in invalid_messages],
            cc=reduce(lambda acc, cur: acc + cur[0]["cc"], invalid_messages, []),
        )
        slack.send(message)
    return {"result": f"{success}/{total}"}
