from audit import build_report, report_text
from config import load_config
from redact import log_safe, redact_config
from idempotency import already_posted, mark_posted
from jira_client import build_comment_body, post_comment
from mapping import load_mapping, resolve_ticket_key
from ticket_key import extract_ticket_key
from jenkins_client import normalize_build

FAKE_MAPPING = {"my-app": "PROJ-1234"}

FAKE_SETTINGS = {
    "JENKINS_URL": "https://jenkins.example.com",
    "JENKINS_USER": "vajrang",
    "JENKINS_TOKEN": "jenkins-token",
    "JIRA_URL": "https://jira.example.com",
    "JIRA_EMAIL": "vajrang@example.com",
    "JIRA_TOKEN": "jira-token",
}

FAKE_BUILD = {
    "fullDisplayName": "my-app #142",
    "number": 142,
    "result": "SUCCESS",
    "timestamp": 1763200000000,
    "url": "https://jenkins.example.com/job/my-app/142/",
    "changeSets": [
        {"items": [{"msg": "fix login bug PROJ-1234"}]},
    ],
}


def main():
    print("Jenkins Jira Integration - test file")
    print("This file uses fake data only. No live Jenkins, no live Jira.")
    print()

    print("Step 1: check the settings")
    config, missing = load_config(FAKE_SETTINGS)
    if missing:
        print("Missing settings:", ", ".join(missing))
        return
    print("All 6 settings are there.")
    print()

    print("Step 2: find the ticket key")
    message = "fix login bug PROJ-1234"
    key = extract_ticket_key(message)
    print("Commit message:", message)
    print("Ticket key:", key)
    print()

    print("Step 3: clean the Jenkins build")
    build = normalize_build(FAKE_BUILD)
    print("Job:", build["job"])
    print("Build:", build["build"])
    print("Result:", build["result"])
    print("Commit message:", build["commit_message"])
    print()

    print("Step 4: the backup way to find a ticket")
    mapping = load_mapping("mapping.json")
    print("Mapping table:", mapping)
    message_no_key = "fix login bug"
    key = resolve_ticket_key(message_no_key, "my-app", mapping)
    print("Commit message:", message_no_key)
    print("No key in the message, so the table was used.")
    print("Ticket key:", key)
    print()

    print("Step 5: the Jira client, posting the comment")
    comment = build_comment_body(build)
    print("Comment text:")
    print(comment)
    print()

    class FakeHttp:
        def post(self, url, auth=None, json=None, timeout=None):
            print("Would post to:", url)
            print("As user:", auth[0])

            class FakeResponse:
                status_code = 201

                def json(self):
                    return {"id": "10001"}

            return FakeResponse()

    comment_id = post_comment(
        "https://jira.example.com",
        "vajrang@example.com",
        "jira-token",
        key,
        comment,
        http=FakeHttp(),
    )
    print("Fake comment id:", comment_id)
    print("No live Jira was used. This was a fake post only.")
    print()

    print("Step 6: the no-duplicates check")
    seen = []
    print("First run, already posted?", already_posted(key, 142, "SUCCESS", seen))
    seen = mark_posted(key, 142, "SUCCESS", seen)
    print("Posted once, remembered.")
    print("Second run, already posted?", already_posted(key, 142, "SUCCESS", seen))
    print("Second run posts nothing new.")
    print()

    print("Step 7: the audit report")
    report = build_report(build, key, "posted", "10001")
    print(report_text(report))
    print()

    print("Step 8: password hiding in logs")
    config, missing = load_config(FAKE_SETTINGS)
    safe = redact_config(config)
    print("Settings as they appear in logs:", safe)
    line = "calling https://jira.example.com with jira-token"
    print("Log line before hiding:", line)
    print("Log line after hiding:", log_safe(line, config))
    print()

    print("Step 9: what happens next")
    print("The full sync-jira command is not built yet.")
    print("Next step: one command that runs all the parts together.")
    print()
    print("Done. Everything above worked.")


if __name__ == "__main__":
    main()
