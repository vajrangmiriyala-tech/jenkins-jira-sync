import requests


def build_comment_body(build):
    """Make the comment text for one build."""
    return "Build {job}: {result}\nCommit: {message}\nLink: {url}".format(
        job=build["job"],
        result=build["result"],
        message=build["commit_message"],
        url=build["url"],
    )


def post_comment(jira_url, email, token, issue_key, body, http=requests):
    """Post a comment on a Jira issue.

    Returns the new comment id on success, or None when it fails.
    """
    url = jira_url.rstrip("/") + "/rest/api/3/issue/" + issue_key + "/comment"
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": body}],
                }
            ],
        }
    }
    response = http.post(url, auth=(email, token), json=payload, timeout=10)
    if response.status_code not in (200, 201):
        return None
    return response.json().get("id")
