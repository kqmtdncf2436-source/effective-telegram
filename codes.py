import json
import os

CODES_FILE = "codes.json"


def load_codes():

    if not os.path.exists(CODES_FILE):
        return {}

    with open(CODES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_codes(codes):

    with open(CODES_FILE, "w", encoding="utf-8") as f:
        json.dump(
            codes,
            f,
            ensure_ascii=False,
            indent=4,
        )


def save_code(
    code,
    channel_id,
    message_id,
    title="بدون عنوان"
):

    codes = load_codes()

    codes[code] = {
        "channel_id": channel_id,
        "message_id": message_id,
        "title": title,
        "used": []
    }

    save_codes(codes)


def code_exists(code):

    return code in load_codes()


def get_code(code):

    return load_codes().get(code)


def user_used(code, user_id):

    codes = load_codes()

    if code not in codes:
        return False

    return str(user_id) in codes[code]["used"]


def mark_used(code, user_id):

    codes = load_codes()

    if code not in codes:
        return

    uid = str(user_id)

    if uid not in codes[code]["used"]:
        codes[code]["used"].append(uid)

    save_codes(codes)


def get_all_codes():

    return load_codes()
