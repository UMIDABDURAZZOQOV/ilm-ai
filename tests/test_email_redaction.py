"""No real email/network: verification codes and provider failures stay private."""

import pytest
from services import email


@pytest.fixture(autouse=True)
def no_delivery(monkeypatch):
    for key in [
        "BREVO_API_KEY",
        "RESEND_API_KEY",
        "GMAIL_ADDRESS",
        "GMAIL_APP_PASSWORD",
    ]:
        monkeypatch.setattr(email, key, None)
    monkeypatch.setattr(email, "BREVO_FROM_EMAIL", "")


def test_no_provider_never_prints_code_or_recipient(caplog, capsys):
    assert email.send_verification_code("private@example.test", "739154") is False
    output = caplog.text + str(capsys.readouterr())
    assert "739154" not in output and "private@example.test" not in output


def test_raw_provider_exception_never_reaches_logs(monkeypatch, caplog, capsys):
    monkeypatch.setattr(email, "BREVO_API_KEY", "synthetic-key")
    monkeypatch.setattr(email, "BREVO_FROM_EMAIL", "sender@example.test")

    def fail(*args):
        raise RuntimeError("Bearer synthetic-key private@example.test 739154")

    monkeypatch.setattr(email, "_send_via_brevo", fail)
    assert not email.send_verification_code("private@example.test", "739154")
    output = caplog.text + str(capsys.readouterr())
    for secret in ["synthetic-key", "private@example.test", "739154", "Bearer"]:
        assert secret not in output


def test_only_successful_delivery_returns_true(monkeypatch):
    monkeypatch.setattr(email, "RESEND_API_KEY", "synthetic-key")
    monkeypatch.setattr(email, "_send_via_resend", lambda *args: False)
    assert not email.send_verification_code("private@example.test", "739154")
    monkeypatch.setattr(email, "_send_via_resend", lambda *args: True)
    assert email.send_verification_code("private@example.test", "739154")
