from ticket_key import extract_ticket_key


def test_finds_key():
    assert extract_ticket_key("fix login bug PROJ-1234") == "PROJ-1234"


def test_no_key():
    assert extract_ticket_key("fix login bug") is None


def test_lowercase_is_not_a_key():
    assert extract_ticket_key("fix login bug proj-1234") is None


def test_two_keys_is_unclear():
    assert extract_ticket_key("PROJ-1234 and JIRA-99") is None


def test_same_key_twice_is_clear():
    assert extract_ticket_key("PROJ-1234 PROJ-1234") == "PROJ-1234"


def test_empty_message():
    assert extract_ticket_key("") is None
