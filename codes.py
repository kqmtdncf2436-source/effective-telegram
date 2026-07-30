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


def delete_code(code):

    codes = load_codes()

    if code not in codes:
        return False

    del codes[code]

    save_codes(codes)

    return True


def update_code(old_code, new_code=None, new_title=None):

    codes = load_codes()

    if old_code not in codes:
        return False

    data = codes[old_code]

    if new_title is not None:
        data["title"] = new_title

    if new_code is not None:

        codes[new_code] = data

        del codes[old_code]

    save_codes(codes)

    return True

def update_title(code, new_title):

    codes = load_codes()

    if code not in codes:
        return False

    codes[code]["title"] = new_title

    save_codes(codes)

    return True
    
def get_all_users():

    codes = load_codes()

    users = set()

    for data in codes.values():

        for user in data.get("used", []):
            users.add(user)

    return list(users)
    
