"""Exact redirect, cancellation and PKCE contract without live Google credentials."""

from urllib.parse import parse_qs, urlparse

from routers import auth
from services import mobile_oauth
from test_release_hardening import setup


def test_reverse_proxy_callback_keeps_original_https_redirect(setup, monkeypatch):
    client, _ = setup
    original = "https://testserver/auth/google-callback-mobile"
    mobile_oauth.save_state("proxy-state", original, "a" * 43)
    monkeypatch.setattr(auth, "is_google_oauth_enabled", lambda: True)

    async def exchange(request, redirect_uri, mobile=False):
        assert str(request.base_url) == "http://testserver/"
        assert redirect_uri == original
        assert mobile_oauth.consume_state("proxy-state", redirect_uri) == "a" * 43
        return {"code": "single-use-grant"}

    monkeypatch.setattr(auth, "handle_google_callback", exchange)
    result = client.get("/auth/google-callback-mobile?code=code&state=proxy-state",
                        follow_redirects=False)
    query = parse_qs(urlparse(result.headers["location"]).query)
    assert query == {"code": ["single-use-grant"], "state": ["proxy-state"]}


def test_google_consent_cancel_is_distinct_and_consumes_state(setup, monkeypatch):
    client, _ = setup
    mobile_oauth.save_state("cancel-state", "https://testserver/auth/google-callback-mobile", "a" * 43)
    monkeypatch.setattr(auth, "is_google_oauth_enabled", lambda: True)
    response = client.get("/auth/google-callback-mobile?error=access_denied&state=cancel-state",
                          follow_redirects=False)
    assert "error=cancelled" in response.headers["location"]
    response = client.get("/auth/google-callback-mobile?error=access_denied&state=cancel-state",
                          follow_redirects=False)
    assert "error=oauth_failed" in response.headers["location"]


def test_mobile_redirect_configuration_is_public_but_credentials_are_not(setup, monkeypatch):
    client, _ = setup
    monkeypatch.setenv("MOBILE_OAUTH_REDIRECT_URI", "https://staging.example.test/auth/google-callback-mobile")
    response = client.get("/auth/mobile/config")
    assert response.status_code == 200
    assert response.json()["redirect_uri"].startswith("https://staging.example.test/")
    assert not {"client_secret", "access_token", "refresh_token"}.intersection(response.json())
