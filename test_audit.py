import os
import tempfile

from audit import build_report, load_report, report_text, save_report

BUILD = {
    "job": "my-app #142",
    "build": 142,
    "result": "SUCCESS",
    "timestamp": 1763200000000,
    "url": "https://jenkins.example.com/job/my-app/142/",
    "commit_message": "fix login bug PROJ-1234",
}


def test_build_report_posted():
    report = build_report(BUILD, "PROJ-1234", "posted", "10001")
    assert report["job"] == "my-app #142"
    assert report["build"] == 142
    assert report["result"] == "SUCCESS"
    assert report["issue"] == "PROJ-1234"
    assert report["action"] == "posted"
    assert report["comment_id"] == "10001"


def test_build_report_skipped_no_key():
    report = build_report(BUILD, None, "skipped_no_key")
    assert report["action"] == "skipped_no_key"
    assert report["issue"] is None
    assert report["comment_id"] is None


def test_build_report_skipped_already_posted():
    report = build_report(BUILD, "PROJ-1234", "skipped_already_posted")
    assert report["action"] == "skipped_already_posted"


def test_report_text_shows_key_lines():
    report = build_report(BUILD, "PROJ-1234", "posted", "10001")
    text = report_text(report)
    assert "Job: my-app #142" in text
    assert "Result: SUCCESS" in text
    assert "Action: posted" in text
    assert "Comment id: 10001" in text


def test_save_and_load_report_round_trip():
    report = build_report(BUILD, "PROJ-1234", "posted", "10001")
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "report.json")
        save_report(path, report)
        assert load_report(path) == report
