import os
import traceback

import dotenv


dotenv.load_dotenv()
import json
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Chalice deploy script",
    )
    parser.add_argument("--stage", type=str)
    args = parser.parse_args()

    # load config file
    with open(r".chalice/config.json", "r") as f:
        config = json.load(f)

    # backup config file
    with open(r".chalice/config.json.bak", "w") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    try:
        # update config file
        config["manage_iam_role"] = False
        config["iam_role_arn"] = os.getenv("IAM_ROLE_ARN")
        env_variables = {}
        env_variables["QUEUE_NAME"] = os.getenv("QUEUE_NAME")
        env_variables["SLACK_WEBHOOK_URL"] = os.getenv("SLACK_WEBHOOK_URL")
        env_variables["MONITOR_DB_CHANNEL"] = os.getenv("MONITOR_DB_CHANNEL")
        env_variables["MONITOR_CHANNEL"] = os.getenv("MONITOR_CHANNEL")

        config[args.stage]["environment_variables"]: dict = (
            config[args.stage]["environment_variables"] or {}
        )
        config[args.stage]["environment_variables"].update(env_variables)

        # save config file
        with open(r".chalice/config.json", "w") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        # deploy
        os.system(f"chalice deploy --stage {args.stage}")
    except Exception as e:
        tb = traceback.format_exc()
        print(f"Error: {tb}")
    finally:
        # rollback config file
        with open(r".chalice/config.json.bak", "r") as f:
            config = json.load(f)
        with open(r".chalice/config.json", "w") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        # remove backup file
        os.remove(r".chalice/config.json.bak")
