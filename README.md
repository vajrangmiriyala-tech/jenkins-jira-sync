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

Week 1. Setting things up: learning the Jenkins and Jira APIs, writing the plan, making test data.

Note: comments posted to Jira are idempotent - re-running the tool for the same build will not post a duplicate comment.

## Usage

Run it from the command line with the job name and build number:

sync-jira --job my-app --build 142

The Jenkins and Jira addresses and logins come from environment variables: JENKINS_URL, JENKINS_USER, JENKINS_TOKEN, JIRA_URL, JIRA_EMAIL and JIRA_TOKEN. If any of them is missing, the tool stops with a clear error before it talks to either server.
