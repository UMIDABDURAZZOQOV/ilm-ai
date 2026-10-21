import logging

from services.access_log_redaction import AuthQueryRedaction


def test_oauth_code_and_state_do_not_enter_access_log():
    record = logging.LogRecord("uvicorn.access", logging.INFO, "", 0,
        '%s - "%s %s HTTP/%s" %s',
        ("127.0.0.1", "GET", "/auth/google-callback-mobile?code=private-code&state=private-state", "1.1", 307), None)
    assert AuthQueryRedaction().filter(record)
    assert "private-code" not in record.getMessage()
    assert "private-state" not in record.getMessage()
    assert "/auth/google-callback-mobile" in record.getMessage()


def test_non_auth_access_log_is_unchanged():
    args = ("127.0.0.1", "GET", "/mobile/skills/subjects", "1.1", 200)
    record = logging.LogRecord("uvicorn.access", logging.INFO, "", 0, "%s %s %s %s %s", args, None)
    assert AuthQueryRedaction().filter(record)
    assert record.args == args
