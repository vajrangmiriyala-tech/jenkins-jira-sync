import json
import os


def make_key(issue_key, build_number, result):
    """Make one key for one posted comment."""
    return issue_key + ":" + str(build_number) + ":" + result


def already_posted(issue_key, build_number, result, seen):
    """Check if this build result was already posted on this ticket."""
    return make_key(issue_key, build_number, result) in seen


def mark_posted(issue_key, build_number, result, seen):
    """Remember that this build result was posted. Returns the new list."""
    key = make_key(issue_key, build_number, result)
    if key not in seen:
        seen = list(seen) + [key]
    return seen


def load_seen(path):
    """Read the list of posted comments from a JSON file.

    Returns an empty list if the file is missing or not valid JSON.
    """
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (ValueError, OSError):
        return []
    if not isinstance(data, list):
        return []
    return data


def save_seen(path, seen):
    """Save the list of posted comments to a JSON file."""
    with open(path, "w") as f:
        json.dump(seen, f)
