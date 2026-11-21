import json
import os
import tempfile

from mapping import load_mapping, lookup_ticket_key, resolve_ticket_key

MAPPING = {"my-app": "PROJ-1234", "login-fix": "PROJ-5678"}


def test_load_mapping_reads_file():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "mapping.json")
        with open(path, "w") as f:
            json.dump(MAPPING, f)
        assert load_mapping(path) == MAPPING


def test_load_mapping_missing_file_returns_empty():
    assert load_mapping("no-such-file.json") == {}


def test_load_mapping_bad_json_returns_empty():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "mapping.json")
        with open(path, "w") as f:
            f.write("{not json")
        assert load_mapping(path) == {}


def test_lookup_finds_key():
    assert lookup_ticket_key("my-app", MAPPING) == "PROJ-1234"


def test_lookup_missing_job_returns_none():
    assert lookup_ticket_key("other-app", MAPPING) is None


def test_resolve_regex_wins_over_table():
    assert resolve_ticket_key("fix bug PROJ-9999", "my-app", MAPPING) == "PROJ-9999"


def test_resolve_falls_back_to_table():
    assert resolve_ticket_key("fix login bug", "my-app", MAPPING) == "PROJ-1234"


def test_resolve_no_key_anywhere_returns_none():
    assert resolve_ticket_key("fix login bug", "other-app", MAPPING) is None
