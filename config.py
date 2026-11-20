import os

REQUIRED = [
    "JENKINS_URL",
    "JENKINS_USER",
    "JENKINS_TOKEN",
    "JIRA_URL",
    "JIRA_EMAIL",
    "JIRA_TOKEN",
]


def load_config(env=None):
    if env is None:
        env = os.environ
    missing = [name for name in REQUIRED if not env.get(name)]
    if missing:
        return None, missing
    config = {name: env[name] for name in REQUIRED}
    return config, []
