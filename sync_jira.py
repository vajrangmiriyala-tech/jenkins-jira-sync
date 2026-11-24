import argparse

from audit import build_report, report_text, save_report
from config import load_config
from idempotency import already_posted, load_seen, mark_posted, save_seen
from jenkins_client import get_build, normalize_build
from jira_client import build_comment_body, post_comment
from mapping import load_mapping, resolve_ticket_key
from redact import log_safe


def run_sync(job, build_number, mapping=None, seen=None, env=None, http=None):
    """Run one sync for one build. Returns (report, seen).

    mapping is a dict like {"my-app": "PROJ-1234"}.
    seen is a list of keys already posted.
    http is the requests module, or a fake one in tests and demos.
    """
    import requests

    if http is None:
        http = requests
    config, missing = load_config(env)
    if missing:
        report = {
            "job": job,
            "build": build_number,
            "result": None,
            "issue": None,
            "commit_message": "",
            "url": "",
            "action": "failed",
            "comment_id": None,
        }
        return report, list(seen) if seen else []
    if mapping is None:
        mapping = load_mapping("mapping.json")
    if seen is None:
        seen = load_seen("seen.json")
    seen = list(seen)

    raw = get_build(
        config["JENKINS_URL"],
        job,
        build_number,
        config["JENKINS_USER"],
        config["JENKINS_TOKEN"],
        http=http,
    )
    if raw is None:
        report = build_report(
            {"job": job, "build": build_number, "result": None,
             "commit_message": "", "url": ""},
            None,
            "failed",
        )
        return report, seen
    build = normalize_build(raw)
    if build is None:
        report = build_report(
            {"job": job, "build": build_number, "result": None,
             "commit_message": "", "url": ""},
            None,
            "failed",
        )
        return report, seen

    key = resolve_ticket_key(build["commit_message"], job, mapping)
    if not key:
        return build_report(build, None, "skipped_no_key"), seen
    if already_posted(key, build_number, build["result"], seen):
        return build_report(build, key, "skipped_already_posted"), seen

    body = build_comment_body(build)
    comment_id = post_comment(
        config["JIRA_URL"],
        config["JIRA_EMAIL"],
        config["JIRA_TOKEN"],
        key,
        body,
        http=http,
    )
    if comment_id is None:
        return build_report(build, key, "failed"), seen
    seen = mark_posted(key, build_number, build["result"], seen)
    return build_report(build, key, "posted", comment_id), seen


def main():
    parser = argparse.ArgumentParser(description="Sync one Jenkins build to Jira.")
    parser.add_argument("--job", required=True, help="Jenkins job name")
    parser.add_argument("--build", required=True, type=int, help="Build number")
    parser.add_argument("--mapping", default="mapping.json", help="Mapping table file")
    parser.add_argument("--seen", default="seen.json", help="Posted comments file")
    parser.add_argument("--report", default=None, help="Where to save the report")
    args = parser.parse_args()

    config, missing = load_config()
    if missing:
        print("Missing settings:", ", ".join(missing))
        return 1
    mapping = load_mapping(args.mapping)
    seen = load_seen(args.seen)
    report, seen = run_sync(args.job, args.build, mapping=mapping, seen=seen)
    save_seen(args.seen, seen)
    if args.report:
        save_report(args.report, report)
    print(log_safe(report_text(report), config))
    if report["action"] == "posted":
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
