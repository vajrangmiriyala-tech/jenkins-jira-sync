# jenkins-jira-sync

A small Python tool that connects Jenkins builds to Jira tickets.

When a Jenkins build finishes, this tool finds the matching Jira ticket and posts a short comment with the build result. So the ticket always shows the latest build status, and nobody has to update it by hand.

This is my Sem 1 OJT open source project (G391, Jenkins Jira Integration).

## Requirements

- Python 3.10 or newer
- A Jenkins server you can reach (for build info)
- A Jira site with an API token (for posting comments)

## How it works

- Reads build info from Jenkins using the Jenkins REST API
- Finds the Jira ticket key (like PROJ-1234) in the commit message
- Posts a short build result comment on the right Jira ticket
- Skips the build if no ticket is found, or if the comment is already there
- Writes a report of everything it did

## Rules

- Never posts the same comment twice
- Never prints passwords or tokens in logs
- Only updates tickets it is allowed to, never changes ticket status

## Audit report

Each run writes one report entry per build. It lists the build number, the ticket key it mapped to, what happened (Updated, Skipped, or Error), and the time it ran.

## Status

Month 1. Architecture and plan are done. README and docs are done. Signed PRD submitted on 2 Nov. Code implementation is the next step.

Note: comments posted to Jira are idempotent - re-running the tool for the same build will not post a duplicate comment.

## Usage

Note: the code for this command is not in the repo yet. This is the planned command for the next step.

Run it from the command line with the job name and build number:

sync-jira --job my-app --build 142

The Jenkins and Jira addresses and logins come from environment variables: JENKINS_URL, JENKINS_USER, JENKINS_TOKEN, JIRA_URL, JIRA_EMAIL and JIRA_TOKEN. If any of them is missing, the tool stops with a clear error before it talks to either server.

## Mapping table

If the commit message has no ticket key, the tool uses a small JSON mapping table instead. It lists which ticket each build maps to. If the key is missing or unclear, the build is skipped and nothing in Jira is changed.

## Comment format

The comment posted on a Jira ticket is short. It has the job name, the build number, the result (passed or failed), a link to the build, and the time it ran. That is all, so the ticket stays easy to read.

## Run summary

Every run prints a short summary at the end: how many builds were processed, how many were skipped, and how many failed. It exits with a code that shows success or failure, so a scheduled job can tell if the run worked.

## Error handling

Network errors, bad logins, missing builds, and bad data must not crash the tool without a clear message. Every failure is recorded as ERROR in the audit report, with a useful reason.

## Testing

Tests use pytest with requests-mock, so no real Jenkins or Jira server is needed to run them. Coverage is tracked with coverage.py, and the target is 85 percent or more before the demo. Every pull request runs the tests in GitHub Actions.

## Scheduled runs

The tool keeps a small local state file with the last processed build, so a scheduled run can continue from where the last run stopped. No database is needed.
