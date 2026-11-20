from config import load_config

FULL = {
    "JENKINS_URL": "https://jenkins.example.com",
    "JENKINS_USER": "vajrang",
    "JENKINS_TOKEN": "jenkins-token",
    "JIRA_URL": "https://jira.example.com",
    "JIRA_EMAIL": "vajrang@example.com",
    "JIRA_TOKEN": "jira-token",
}


def test_all_present():
    config, missing = load_config(FULL)
    assert missing == []
    assert config["JENKINS_URL"] == "https://jenkins.example.com"
    assert config["JIRA_TOKEN"] == "jira-token"


def test_one_missing():
    env = dict(FULL)
    del env["JIRA_TOKEN"]
    config, missing = load_config(env)
    assert config is None
    assert missing == ["JIRA_TOKEN"]


def test_two_missing():
    env = dict(FULL)
    del env["JENKINS_URL"]
    del env["JENKINS_USER"]
    config, missing = load_config(env)
    assert config is None
    assert missing == ["JENKINS_URL", "JENKINS_USER"]


def test_empty_value_is_missing():
    env = dict(FULL)
    env["JENKINS_TOKEN"] = ""
    config, missing = load_config(env)
    assert config is None
    assert missing == ["JENKINS_TOKEN"]


def test_nothing_given():
    config, missing = load_config({})
    assert config is None
    assert missing == [
        "JENKINS_URL",
        "JENKINS_USER",
        "JENKINS_TOKEN",
        "JIRA_URL",
        "JIRA_EMAIL",
        "JIRA_TOKEN",
    ]
