import json


def build_report(build, issue_key, action, comment_id=None):
    """Make one audit report for one build."""
    return {
        "job": build["job"],
        "build": build["build"],
        "result": build["result"],
        "issue": issue_key,
        "commit_message": build["commit_message"],
        "url": build["url"],
        "action": action,
        "comment_id": comment_id,
    }


def report_text(report):
    """Make the report as plain lines a person can read."""
    lines = [
        "Job: " + report["job"],
        "Build: " + str(report["build"]),
        "Result: " + report["result"],
        "Ticket: " + str(report["issue"]),
        "Commit: " + report["commit_message"],
        "Link: " + report["url"],
        "Action: " + report["action"],
    ]
    if report["comment_id"]:
        lines.append("Comment id: " + report["comment_id"])
    return "\n".join(lines)


def save_report(path, report):
    """Save one report to a JSON file."""
    with open(path, "w") as f:
        json.dump(report, f, indent=2)


def load_report(path):
    """Read one report back from a JSON file."""
    with open(path, "r") as f:
        return json.load(f)
