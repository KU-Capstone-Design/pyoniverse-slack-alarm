import json
import os

from chalice import Chalice
from chalice.app import SQSEvent

from chalicelib.model.record import Record


if os.getenv("LOG_LEVEL", "DEBUG") == "DEBUG":
    debug = True
else:
    debug = False

app = Chalice(app_name='pyoniverse-slack-alarm', debug=debug)


@app.on_sqs_message(queue=os.getenv("QUEUE_NAME"),
                    batch_size=1,
                    )
def send_slack(event: SQSEvent):
    for _record in event:
        record: Record = Record.load(json.loads(_record.body))
        return record
