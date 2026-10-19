# jenkins-jira-sync

A small Python tool that connects Jenkins builds to Jira tickets.

When a Jenkins build finishes, this tool finds the matching Jira ticket and posts a short comment with the build result. So the ticket always shows the latest build status, and nobody has to update it by hand.

This is my Sem 1 OJT open source project (G391, Jenkins Jira Integration).

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

## Status

Week 1. Setting things up: learning the Jenkins and Jira APIs, writing the plan, making test data.
