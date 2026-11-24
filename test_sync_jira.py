from sync_jira import run_sync

ENV = {
    "JENKINS_URL": "https://jenkins.example.com",
    "JENKINS_USER": "vajrang",
    "JENKINS_TOKEN": "jenkins-token",
    "JIRA_URL": "https://jira.example.com",
    "JIRA_EMAIL": "vajrang@example.com",
    "JIRA_TOKEN": "jira-token",
}

RAW_SUCCESS = {
    "fullDisplayName": "my-app #142",
    "number": 142,
    "result": "SUCCESS",
    "timestamp": 1763200000000,
    "url": "https://jenkins.example.com/job/my-app/142/",
    "changeSets": [{"items": [{"msg": "fix login bug PROJ-1234"}]}],
}

RAW_NO_KEY = {
    "fullDisplayName": "my-app #142",
    "number": 142,
    "result": "SUCCESS",
    "timestamp": 1763200000000,
    "url": "https://jenkins.example.com/job/my-app/142/",
    "changeSets": [{"items": [{"msg": "fix login bug"}]}],
}


class FakeResponse:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data

    def json(self):
        return self._data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("http error " + str(self.status_code))


class FakeHttp:
    def __init__(self, raw=None, get_status=200, post_status=201):
        self.raw = raw if raw is not None else RAW_SUCCESS
        self.get_status = get_status
        self.post_status = post_status
        self.posted = 0
        self.last_post_url = None

    def get(self, url, auth=None, timeout=None):
        return FakeResponse(self.get_status, self.raw)

    def post(self, url, auth=None, json=None, timeout=None):
        self.posted += 1
        self.last_post_url = url
        return FakeResponse(self.post_status, {"id": "10001"})


def test_sync_posts_comment_for_success_build():
    http = FakeHttp()
    report, seen = run_sync("my-app", 142, mapping={}, seen=[], env=ENV, http=http)
    assert report["action"] == "posted"
    assert report["comment_id"] == "10001"
    assert report["issue"] == "PROJ-1234"
    assert seen == ["PROJ-1234:142:SUCCESS"]
    assert http.posted == 1


def test_sync_skips_when_no_ticket_key():
    http = FakeHttp(raw=RAW_NO_KEY)
    report, seen = run_sync("my-app", 142, mapping={}, seen=[], env=ENV, http=http)
    assert report["action"] == "skipped_no_key"
    assert http.posted == 0


def test_sync_uses_mapping_table_when_no_key_in_message():
    http = FakeHttp(raw=RAW_NO_KEY)
    report, seen = run_sync(
        "my-app", 142, mapping={"my-app": "PROJ-1234"}, seen=[], env=ENV, http=http
    )
    assert report["action"] == "posted"
    assert report["issue"] == "PROJ-1234"


def test_sync_skips_second_run_for_same_build():
    http = FakeHttp()
    report, seen = run_sync(
        "my-app", 142, mapping={}, seen=["PROJ-1234:142:SUCCESS"], env=ENV, http=http
    )
    assert report["action"] == "skipped_already_posted"
    assert http.posted == 0


def test_sync_fails_when_post_fails():
    http = FakeHttp(post_status=500)
    report, seen = run_sync("my-app", 142, mapping={}, seen=[], env=ENV, http=http)
    assert report["action"] == "failed"
    assert seen == []


def test_sync_fails_when_build_not_found():
    http = FakeHttp(get_status=404, raw={})
    report, seen = run_sync("my-app", 999, mapping={}, seen=[], env=ENV, http=http)
    assert report["action"] == "failed"
    assert http.posted == 0


def test_sync_fails_when_settings_missing():
    http = FakeHttp()
    report, seen = run_sync("my-app", 142, mapping={}, seen=[], env={}, http=http)
    assert report["action"] == "failed"
    assert http.posted == 0
