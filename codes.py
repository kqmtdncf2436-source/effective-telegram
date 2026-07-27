import json
import os


def load_codes():

    if os.path.exists("codes.json"):

        with open(
            "codes.json",
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return {}
