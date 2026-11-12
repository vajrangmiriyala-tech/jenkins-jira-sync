import requests


def get_build(base_url, job, build_number, user, token):
    url = base_url.rstrip("/") + "/job/" + job + "/" + str(build_number) + "/api/json"
    response = requests.get(url, auth=(user, token), timeout=10)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def normalize_build(raw):
    if not raw:
        return None
    message = ""
    for change_set in raw.get("changeSets", []):
        for item in change_set.get("items", []):
            message = item.get("msg", "")
            if message:
                break
        if message:
            break
    return {
        "job": raw.get("fullDisplayName", ""),
        "build": raw.get("number"),
        "result": raw.get("result"),
        "timestamp": raw.get("timestamp"),
        "url": raw.get("url", ""),
        "commit_message": message,
    }
