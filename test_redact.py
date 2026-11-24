from redact import is_secret_key, log_safe, redact_config, redact_text

CONFIG = {
    "JENKINS_URL": "https://jenkins.example.com",
    "JENKINS_USER": "vajrang",
    "JENKINS_TOKEN": "jenkins-token",
    "JIRA_URL": "https://jira.example.com",
    "JIRA_EMAIL": "vajrang@example.com",
    "JIRA_TOKEN": "jira-token",
}


def test_redact_text_hides_one_secret():
    assert redact_text("token is jenkins-token", ["jenkins-token"]) == "token is ***"


def test_redact_text_hides_all_secrets():
    text = redact_text("a jenkins-token and b jira-token", ["jenkins-token", "jira-token"])
    assert text == "a *** and b ***"


def test_redact_text_leaves_normal_text_alone():
    assert redact_text("all good, nothing secret", ["jenkins-token"]) == "all good, nothing secret"


def test_redact_text_empty_secret_does_nothing():
    assert redact_text("all good", [""]) == "all good"


def test_is_secret_key():
    assert is_secret_key("JENKINS_TOKEN") is True
    assert is_secret_key("JIRA_TOKEN") is True
    assert is_secret_key("JENKINS_URL") is False
    assert is_secret_key("JIRA_EMAIL") is False


def test_redact_config_hides_tokens_keeps_rest():
    safe = redact_config(CONFIG)
    assert safe["JENKINS_TOKEN"] == "***"
    assert safe["JIRA_TOKEN"] == "***"
    assert safe["JENKINS_URL"] == "https://jenkins.example.com"
    assert safe["JIRA_EMAIL"] == "vajrang@example.com"


def test_log_safe_hides_tokens_from_a_line():
    line = "calling https://jira.example.com with jira-token"
    assert log_safe(line, CONFIG) == "calling https://jira.example.com with ***"
