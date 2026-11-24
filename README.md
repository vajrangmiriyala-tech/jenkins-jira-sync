# Jenkins Jira Integration

A small Python tool that connects Jenkins builds to Jira tickets.

When a Jenkins build finishes, this tool finds the matching Jira ticket and posts the build result as a short comment on it. The ticket always shows the latest build status, and nobody has to update it by hand.

![Tests](https://github.com/vajrangmiriyala-tech/jenkins-jira-sync/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

My Sem 1 OJT open source project. Group G391, Polaris School of Technology, Bangalore. Mentor: Shivam Nandu Ubhale.

> **Figma design of this README:** [jenkins-jira-sync README](https://www.figma.com/design/9kLw3IhKfV0pQK8SgH1uNS/jenkins-jira-sync-README?node-id=2-2)

## How it works

1. Reads one build from Jenkins through the Jenkins REST API.
2. Finds the ticket key, like PROJ-1234, in the commit message. If the commit has no key, it uses the mapping table instead.
3. Checks the comment was not already posted. If it was, it posts nothing new.
4. Posts a short comment on the right Jira ticket.
5. Writes one audit report for the run, with tokens hidden.

## Quick start

```bash
git clone https://github.com/vajrangmiriyala-tech/jenkins-jira-sync.git
cd jenkins-jira-sync
pip install requests
```

Set the settings, then run one build:

```bash
python3 sync_jira.py --job my-app --build 142
```

## Settings

All six come from environment variables. Nothing is written in the code.

| Setting | What it is |
| --- | --- |
| JENKINS_URL | Address of the Jenkins server |
| JENKINS_USER | Jenkins login name |
| JENKINS_TOKEN | Jenkins API token |
| JIRA_URL | Address of the Jira site |
| JIRA_EMAIL | Jira login email |
| JIRA_TOKEN | Jira API token |

If any of them is missing, the tool stops with a clear error before it talks to either server.

## The comment

A comment posted on a ticket looks like this:

```
Build my-app #142: SUCCESS
Commit: fix login bug PROJ-1234
Link: https://jenkins.example.com/job/my-app/142/
```

Short, so the ticket stays easy to read.

## Files

| File | What it does |
| --- | --- |
| ticket_key.py | Finds the ticket key in a commit message |
| jenkins_client.py | Reads one build from Jenkins and cleans it |
| config.py | Checks all six settings are there |
| mapping.py | Backup way to find a ticket, from mapping.json |
| jira_client.py | Makes the comment and posts it on Jira |
| idempotency.py | Stops the same comment twice |
| audit.py | One report per build |
| redact.py | Hides tokens in logs |
| sync_jira.py | The full command that runs all the parts |
| mock_demo.py | One pass, one fail, one repeat that posts nothing |
| testfile.py | Runs the whole flow step by step, 10 steps |

## Rules

- Never posts the same comment twice.
- Never prints passwords or tokens in logs.
- Never changes a ticket status, never deletes a comment, never changes Jira admin settings.
- Never guesses a ticket. If the commit has no key or two different keys, the build is skipped.

## Testing

55 tests, all passing. They use fake data, so no live Jenkins or Jira server is needed.

```bash
python3 -m pytest
python3 testfile.py
python3 mock_demo.py
```

GitHub Actions runs the tests on every push and fails the run if coverage is under 85 percent.

## Limits

The tool only posts comments. A live test with a real Jenkins and Jira still needs sample data or access from the mentor.
