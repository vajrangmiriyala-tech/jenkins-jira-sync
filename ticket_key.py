import re

KEY_PATTERN = re.compile(r"\b[A-Z][A-Z0-9]*-\d+\b")


def extract_ticket_key(message):
    if not message:
        return None
    keys = KEY_PATTERN.findall(message)
    if len(set(keys)) != 1:
        return None
    return keys[0]
