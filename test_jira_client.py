from jira_client import build_comment_body, post_comment

BUILD = {
    "job": "my-app #142",
    "build": 142,
    "result": "SUCCESS",
    "timestamp": 1763200000000,
    "url": "https://jenkins.example.com/job/my-app/142/",
    "commit_message": "fix login bug PROJ-1234",
}


class FakeResponse:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data

    def json(self):
        return self._data


class FakeHttp:
    def __init__(self, status_code=201, data=None):
        self.status_code = status_code
        self.data = data or {"id": "10001"}
        self.last_url = None
        self.last_auth = None
        self.last_payload = None

    def post(self, url, auth=None, json=None, timeout=None):
        self.last_url = url
        self.last_auth = auth
        self.last_payload = json
        return FakeResponse(self.status_code, self.data)


def test_build_comment_body_success():
    body = build_comment_body(BUILD)
    assert body == (
        "Build my-app #142: SUCCESS\n"
        "Commit: fix login bug PROJ-1234\n"
        "Link: https://jenkins.example.com/job/my-app/142/"
    )


def test_build_comment_body_failure():
    build = dict(BUILD, result="FAILURE")
    body = build_comment_body(build)
    assert "Build my-app #142: FAILURE" in body


def test_post_comment_posts_to_right_url_and_returns_id():
    http = FakeHttp()
    comment_id = post_comment(
        "https://jira.example.com",
        "vajrang@example.com",
        "jira-token",
        "PROJ-1234",
        "Build my-app #142: SUCCESS",
        http=http,
    )
    assert comment_id == "10001"
    assert http.last_url == (
        "https://jira.example.com/rest/api/3/issue/PROJ-1234/comment"
    )
    assert http.last_auth == ("vajrang@example.com", "jira-token")


def test_post_comment_returns_none_on_failure():
    http = FakeHttp(status_code=404, data={})
    comment_id = post_comment(
        "https://jira.example.com",
        "vajrang@example.com",
        "jira-token",
        "PROJ-1234",
        "Build my-app #142: SUCCESS",
        http=http,
    )
    assert comment_id is None
