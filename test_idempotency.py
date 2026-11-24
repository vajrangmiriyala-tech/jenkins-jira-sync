import os
import tempfile

from idempotency import already_posted, load_seen, make_key, mark_posted, save_seen


def test_make_key():
    assert make_key("PROJ-1234", 142, "SUCCESS") == "PROJ-1234:142:SUCCESS"


def test_already_posted_false_for_new_build():
    assert already_posted("PROJ-1234", 142, "SUCCESS", []) is False


def test_mark_then_already_posted_true():
    seen = mark_posted("PROJ-1234", 142, "SUCCESS", [])
    assert already_posted("PROJ-1234", 142, "SUCCESS", seen) is True


def test_different_result_is_a_new_key():
    seen = mark_posted("PROJ-1234", 142, "SUCCESS", [])
    assert already_posted("PROJ-1234", 142, "FAILURE", seen) is False


def test_different_build_is_a_new_key():
    seen = mark_posted("PROJ-1234", 142, "SUCCESS", [])
    assert already_posted("PROJ-1234", 143, "SUCCESS", seen) is False


def test_mark_twice_keeps_one_key():
    seen = mark_posted("PROJ-1234", 142, "SUCCESS", [])
    seen = mark_posted("PROJ-1234", 142, "SUCCESS", seen)
    assert seen == ["PROJ-1234:142:SUCCESS"]


def test_load_and_save_seen_round_trip():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "seen.json")
        save_seen(path, ["PROJ-1234:142:SUCCESS"])
        assert load_seen(path) == ["PROJ-1234:142:SUCCESS"]


def test_load_seen_missing_file_returns_empty():
    assert load_seen("no-such-file.json") == []
