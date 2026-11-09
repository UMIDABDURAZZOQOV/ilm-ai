"""Actual RSA signature/issuer/audience/nonce/freshness checks, no provider calls."""

from datetime import timedelta
import json
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import HTTPException

from services import deletion_reauth as service, google_oauth
from services.study import utcnow


@pytest.mark.parametrize('verified', [False, True])
@pytest.mark.parametrize('email_free', ['true', 'false'])
@pytest.mark.parametrize('legacy_provider', [None, 'google'])
def test_password_signup_cannot_claim_google_identity_by_email(monkeypatch, verified, email_free, legacy_provider):
    import asyncio
    from starlette.requests import Request
    from services import mobile_oauth

    monkeypatch.setenv("EMAIL_FREE_AUTHENTICATION", email_free)
    monkeypatch.setattr(google_oauth, "GOOGLE_CLIENT_ID", "synthetic-client")
    monkeypatch.setattr(google_oauth, "GOOGLE_CLIENT_SECRET", "synthetic-secret")
    monkeypatch.setattr(mobile_oauth, "consume_state", lambda *args: None)
    monkeypatch.setattr(google_oauth, "find_user_by_oauth", lambda *args: None)
    monkeypatch.setattr(
        google_oauth,
        "find_user_by_email",
        lambda *args: {"id": 1, "oauth_provider": legacy_provider, "email_verified": verified},
    )
    monkeypatch.setattr(
        google_oauth.requests,
        "post",
        lambda *args, **kwargs: SimpleNamespace(
            status_code=200,
            json=lambda: {"access_token": "synthetic-provider-response"},
        ),
    )
    monkeypatch.setattr(
        google_oauth.requests,
        "get",
        lambda *args, **kwargs: SimpleNamespace(
            status_code=200,
            json=lambda: {
                "email": "owned@example.org",
                "email_verified": True,
                "sub": "verified-sub",
            },
        ),
    )
    request = Request({"type": "http", "query_string": b"code=fixture&state=fixture"})
    with pytest.raises(HTTPException) as error:
        asyncio.run(
            google_oauth.handle_google_callback(
                request, "https://staging.example.test/auth/google-callback"
            )
        )
    assert error.value.status_code == 409
    assert error.value.detail == "account_link_requires_verified_identity"


@pytest.fixture(scope="module")
def signing_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.mark.parametrize('legacy_email_verified', [False, True])
def test_existing_google_subject_preserves_account_despite_email_change(monkeypatch, legacy_email_verified):
    import asyncio
    from starlette.requests import Request
    from services import mobile_oauth
    monkeypatch.setattr(google_oauth, 'GOOGLE_CLIENT_ID', 'synthetic-client')
    monkeypatch.setattr(google_oauth, 'GOOGLE_CLIENT_SECRET', 'synthetic-secret')
    monkeypatch.setattr(mobile_oauth, 'consume_state', lambda *args: None)
    monkeypatch.setattr(google_oauth, 'find_user_by_oauth', lambda provider, subject: {
        'id': 42, 'oauth_provider': 'google', 'oauth_provider_id': 'verified-sub',
        'email_verified': legacy_email_verified, 'email': 'old@example.test', 'age': 18,
    })
    def forbidden(*args, **kwargs):
        raise AssertionError('Existing provider identity must not merge or create an account')
    monkeypatch.setattr(google_oauth, 'find_user_by_email', forbidden)
    monkeypatch.setattr(google_oauth, 'create_user_with_oauth', forbidden)
    monkeypatch.setattr(google_oauth, 'create_access_token', lambda uid: 'synthetic-access-'+str(uid))
    monkeypatch.setattr(google_oauth, 'create_refresh_token', lambda uid: 'synthetic-refresh-'+str(uid))
    monkeypatch.setattr(google_oauth.requests, 'post', lambda *args, **kwargs:
                        SimpleNamespace(status_code=200, json=lambda: {'access_token': 'synthetic-provider'}))
    monkeypatch.setattr(google_oauth.requests, 'get', lambda *args, **kwargs:
                        SimpleNamespace(status_code=200, json=lambda: {
                            'email': 'changed@example.test', 'email_verified': True, 'sub': 'verified-sub',
                        }))
    request = Request({'type': 'http', 'query_string': b'code=fixture&state=fixture'})
    result = asyncio.run(google_oauth.handle_google_callback(request, 'https://staging.example.test/auth/google-callback'))
    assert result['user_id'] == 42
    assert result['access_token'] == 'synthetic-access-42'


@pytest.mark.parametrize(
    "mutation",
    [
        "valid",
        "wrong_nonce",
        "old_google_session_fresh_app_response",
        "missing_auth_time",
        "stale_issued_at",
        "token_issued_before_flow",
        "missing_issued_at",
        "invalid_issued_at_type",
        "future_issued_at",
        "wrong_audience",
        "wrong_issuer",
        "wrong_azp",
        "expired",
        "future_auth",
        "wrong_signature",
    ],
)
def test_google_requires_verified_fresh_identity(monkeypatch, signing_key, mutation):
    client = "synthetic.apps.googleusercontent.com"
    monkeypatch.setattr(google_oauth, "GOOGLE_CLIENT_ID", client)
    now = int(utcnow().timestamp())
    claims = dict(
        sub="verified-provider-sub",
        aud=client,
        iss="https://accounts.google.com",
        exp=now + 120,
        iat=now,
        nonce="owned-nonce",
        auth_time=now,
    )
    if mutation == "wrong_nonce":
        claims["nonce"] = "another-flow"
    if mutation == "old_google_session_fresh_app_response":
        claims["auth_time"] = now - 3600
    if mutation == "missing_auth_time":
        claims.pop("auth_time")
    if mutation == "stale_issued_at":
        claims["iat"] = now - 600
        claims.pop("auth_time")
    if mutation == "token_issued_before_flow":
        claims["iat"] = now - 120
        claims.pop("auth_time")
    if mutation == "missing_issued_at":
        claims.pop("iat")
    if mutation == "invalid_issued_at_type":
        claims["iat"] = True
    if mutation == "future_issued_at":
        claims["iat"] = now + 3600
    if mutation == "wrong_audience":
        claims["aud"] = "other.apps.googleusercontent.com"
    if mutation == "wrong_issuer":
        claims["iss"] = "https://attacker.invalid"
    if mutation == "wrong_azp":
        claims["azp"] = "other-client"
    if mutation == "expired":
        claims["exp"] = now - 120
    if mutation == "future_auth":
        claims["auth_time"] = now + 3600
    signer = (
        rsa.generate_private_key(public_exponent=65537, key_size=2048)
        if mutation == "wrong_signature"
        else signing_key
    )
    encoded = jwt.encode(
        claims, signer, algorithm="RS256", headers={"kid": "fixture-key"}
    )
    public = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(signing_key.public_key()))
    public["kid"] = "fixture-key"

    def post(url, **kwargs):
        assert url == "https://oauth2.googleapis.com/token"
        assert kwargs["allow_redirects"] is False
        return SimpleNamespace(status_code=200, json=lambda: {"id_token": encoded})

    def get(url, **kwargs):
        assert url == "https://www.googleapis.com/oauth2/v3/certs"
        assert kwargs["allow_redirects"] is False
        return SimpleNamespace(status_code=200, json=lambda: {"keys": [public]})

    monkeypatch.setattr(service.requests, "post", post)
    monkeypatch.setattr(service.requests, "get", get)
    if mutation in {
        "valid",
        "old_google_session_fresh_app_response",
        "missing_auth_time",
    }:
        assert (
            service.verify_google_identity(
                "fixture-code",
                service.sha("owned-nonce"),
                utcnow() - timedelta(seconds=5),
            )
            == "verified-provider-sub"
        )
    else:
        with pytest.raises((HTTPException, jwt.PyJWTError)):
            service.verify_google_identity(
                "fixture-code",
                service.sha("owned-nonce"),
                utcnow() - timedelta(seconds=5),
            )


def test_reauth_failure_logs_only_fixed_categories(caplog):
    marker = "never-log-this-provider-token-or-identity"
    with caplog.at_level("WARNING", logger=service.__name__):
        service.log_google_failure(HTTPException(400, marker))
        service.log_google_failure(jwt.DecodeError(marker))
        service.log_google_failure(service.requests.RequestException(marker))
    assert marker not in caplog.text
    assert "provider_rejected" in caplog.text
    assert "invalid_signed_identity" in caplog.text
    assert "provider_connection_failed" in caplog.text
