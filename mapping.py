import json
import os

from ticket_key import extract_ticket_key


def load_mapping(path):
    """Read the mapping table from a JSON file.

    Returns a dict like {"my-app": "PROJ-1234"}.
    Returns an empty dict if the file is missing or not valid JSON,
    so the tool can carry on with the regex way only.
    """
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (ValueError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def lookup_ticket_key(job, mapping):
    """Find the ticket key for a job name in the table, or None."""
    if not job or not mapping:
        return None
    return mapping.get(job)


def resolve_ticket_key(message, job, mapping):
    """Find the ticket key for a build, regex first, table second.

    Returns None when neither way gives a key, so the build is skipped.
    """
    key = extract_ticket_key(message)
    if key:
        return key
    return lookup_ticket_key(job, mapping)
