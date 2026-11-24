from audit import report_text
from sync_jira import run_sync

ENV = {
    "JENKINS_URL": "https://jenkins.example.com",
    "JENKINS_USER": "vajrang",
    "JENKINS_TOKEN": "jenkins-token",
    "JIRA_URL": "https://jira.example.com",
    "JIRA_EMAIL": "vajrang@example.com",
    "JIRA_TOKEN": "jira-token",
}

MAPPING = {"my-app": "PROJ-1234"}


def make_raw(number, result, message):
    return {
        "fullDisplayName": "my-app #" + str(number),
        "number": number,
        "result": result,
        "timestamp": 1763200000000,
        "url": "https://jenkins.example.com/job/my-app/" + str(number) + "/",
        "changeSets": [{"items": [{"msg": message}]}],
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
    def __init__(self, raws):
        self.raws = raws
        self.calls = 0

    def get(self, url, auth=None, timeout=None):
        raw = self.raws[self.calls]
        self.calls += 1
        return FakeResponse(200, raw)

    def post(self, url, auth=None, json=None, timeout=None):
        return FakeResponse(201, {"id": "10001"})


def main():
    print("Jenkins Jira Integration - mock demo")
    print("Fake Jenkins and fake Jira only. Nothing live.")
    print()
    raws = [
        make_raw(142, "SUCCESS", "fix login bug PROJ-1234"),
        make_raw(143, "FAILURE", "break login page PROJ-1234"),
        make_raw(142, "SUCCESS", "fix login bug PROJ-1234"),
    ]
    http = FakeHttp(raws)
    seen = []

    print("Run 1: build 142, SUCCESS")
    report, seen = run_sync("my-app", 142, mapping=MAPPING, seen=seen, env=ENV, http=http)
    print(report_text(report))
    print()

    print("Run 2: build 143, FAILURE")
    report, seen = run_sync("my-app", 143, mapping=MAPPING, seen=seen, env=ENV, http=http)
    print(report_text(report))
    print()

    print("Run 3: build 142 again, SUCCESS")
    report, seen = run_sync("my-app", 142, mapping=MAPPING, seen=seen, env=ENV, http=http)
    print(report_text(report))
    print()
    print("Mock demo done. Two comments posted, the repeat posted nothing new.")


if __name__ == "__main__":
    main()
