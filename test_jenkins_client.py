from unittest.mock import Mock, patch

from jenkins_client import get_build, normalize_build


def test_normalize_build():
    raw = {
        "fullDisplayName": "my-app #142",
        "number": 142,
        "result": "SUCCESS",
        "timestamp": 1762000000000,
        "url": "http://jenkins/job/my-app/142/",
        "changeSets": [{"items": [{"msg": "fix login bug PROJ-1234"}]}],
    }
    build = normalize_build(raw)
    assert build["build"] == 142
    assert build["result"] == "SUCCESS"
    assert build["commit_message"] == "fix login bug PROJ-1234"


def test_normalize_no_commit_message():
    raw = {"number": 143, "result": "FAILURE", "timestamp": 0, "url": "", "changeSets": []}
    build = normalize_build(raw)
    assert build["commit_message"] == ""
    assert build["result"] == "FAILURE"


def test_normalize_empty():
    assert normalize_build(None) is None
    assert normalize_build({}) is None


def test_get_build_success():
    fake = Mock()
    fake.status_code = 200
    fake.json.return_value = {"number": 142, "result": "SUCCESS"}
    with patch("jenkins_client.requests.get", return_value=fake) as get:
        result = get_build("http://jenkins", "my-app", 142, "user", "token")
    assert result == {"number": 142, "result": "SUCCESS"}
    assert "/job/my-app/142/api/json" in get.call_args[0][0]


def test_get_build_not_found():
    fake = Mock()
    fake.status_code = 404
    with patch("jenkins_client.requests.get", return_value=fake):
        assert get_build("http://jenkins", "my-app", 999, "user", "token") is None
