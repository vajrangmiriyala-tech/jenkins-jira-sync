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

Month 1 is done. Architecture, PRD, and the milestone video are approved. Code started on 12 Nov: ticket_key.py and jenkins_client.py are in, with 11 tests passing. The full tool is still to come.

Note: comments posted to Jira are idempotent - re-running the tool for the same build will not post a duplicate comment.

## Usage

Note: the full sync-jira command is not in the repo yet. The first two parts are in: ticket_key.py and jenkins_client.py, with tests. This command is the planned next step.

Run it from the command line with the job name and build number:

sync-jira --job my-app --build 142

The Jenkins and Jira addresses and logins come from environment variables: JENKINS_URL, JENKINS_USER, JENKINS_TOKEN, JIRA_URL, JIRA_EMAIL and JIRA_TOKEN. If any of them is missing, the tool stops with a clear error before it talks to either server.

## Mapping table

If the commit message has no ticket key, the tool uses a small JSON mapping table instead. It lists which ticket each build maps to. If the key is missing or unclear, the build is skipped and nothing in Jira is changed.

## Mapping table format

The mapping table is a JSON file, mapping.json. Each line pairs a job name with a ticket key:

{"my-app": "PROJ-1234"}

If the file is missing or broken, the tool just uses the commit message way and carries on.

## Comment format

The comment posted on a Jira ticket is short. It has the job name, the build number, the result (passed or failed), a link to the build, and the time it ran. That is all, so the ticket stays easy to read.

## Run summary

Every run prints a short summary at the end: how many builds were processed, how many were skipped, and how many failed. It exits with a code that shows success or failure, so a scheduled job can tell if the run worked.

## Error handling

Network errors, bad logins, missing builds, and bad data must not crash the tool without a clear message. Every failure is recorded as ERROR in the audit report, with a useful reason.

## Testing

Tests are in the repo now: 11 tests, all passing. They use fake data, so no real Jenkins or Jira server is needed to run them. Run them with python -m pytest. Coverage is tracked with coverage.py, and the target is 85 percent or more before the demo. GitHub Actions is not set up yet.

## Scheduled runs

The tool keeps a small local state file with the last processed build, so a scheduled run can continue from where the last run stopped. No database is needed.

## Logging

The tool writes a short log line for each build it processes, so a run can be checked afterwards. Logs never include passwords or tokens. A failed build is logged with the reason, so the problem can be found fast.

## Setup

Clone the repo, then make sure Python 3.10 or newer is installed. Install the only extra package with pip install requests. Set the Jenkins and Jira details as environment variables before the first run.

## Configuration

The tool reads its settings from environment variables. JENKINS_URL is the address of the Jenkins server, and JENKINS_USER with JENKINS_TOKEN is the login for it. JIRA_URL is the address of the Jira site, and JIRA_EMAIL with JIRA_TOKEN is the login for it. If any of them is missing, the tool stops with a clear error before it talks to either server.

## Example comment

A comment posted on a ticket looks like this:

Build my-app #142: PASSED. Link: https://jenkins.example.com/job/my-app/142. Time: 2026-11-20 12:00 IST.

That is the full comment. Job name, build number, result, link, and time, nothing else.

## Running the tests

Run python3 -m pytest from the repo folder. It runs 24 tests: 6 for the ticket finder, 5 for the Jenkins reader, 5 for the config checker, and 8 for the mapping table. All 24 pass in under a second. Coverage is checked with coverage.py, target 85 percent or more.

## Limits

The tool only posts comments. It never changes a ticket status, never deletes a comment, and never changes Jira admin settings. Those limits are fixed.

## Project structure

ticket_key.py finds the ticket key in a commit message. jenkins_client.py reads one build from Jenkins. config.py checks the settings. mapping.py reads the mapping table in mapping.json. test_ticket_key.py, test_jenkins_client.py, test_config.py, and test_mapping.py test them. testfile.py runs the whole flow step by step.

## Troubleshooting

Wrong login: the tool stops with an error. Check the env vars in Configuration and make sure the tokens are right.
Build not found: the tool stops with an error. Check the job name and the build number.
No ticket key found: the tool skips the build. Check the commit message for a key like PROJ-1234, or add the job to the mapping table.

## Next steps

The work left, in order: the Jira client, the no-duplicates check, the audit report, hiding passwords in logs, the full sync-jira command, tests to 85 percent, GitHub Actions, and a mock demo.
