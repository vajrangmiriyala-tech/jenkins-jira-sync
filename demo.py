from config import load_config
from ticket_key import extract_ticket_key
from jenkins_client import normalize_build

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
    print("Jenkins Jira Integration - demo")
    print("This demo uses fake data only. No live Jenkins, no live Jira.")
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

    print("Step 4: what happens next")
    print("The Jira client is not built yet.")
    print("Next step: post the result as a comment on ticket", key)
    print()
    print("Demo done. Everything above worked.")


if __name__ == "__main__":
    main()
