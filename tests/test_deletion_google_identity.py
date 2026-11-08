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


def test_unverified_password_signup_cannot_claim_google_identity(monkeypatch):
    import asyncio
    from starlette.requests import Request
    from services import mobile_oauth

    monkeypatch.setenv("EMAIL_FREE_AUTHENTICATION", "true")
    monkeypatch.setattr(google_oauth, "GOOGLE_CLIENT_ID", "synthetic-client")
    monkeypatch.setattr(google_oauth, "GOOGLE_CLIENT_SECRET", "synthetic-secret")
    monkeypatch.setattr(mobile_oauth, "consume_state", lambda *args: None)
    monkeypatch.setattr(google_oauth, "find_user_by_oauth", lambda *args: None)
    monkeypatch.setattr(
        google_oauth,
        "find_user_by_email",
        lambda *args: {"id": 1, "oauth_provider": None, "email_verified": False},
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


@pytest.mark.parametrize(
    "mutation",
    [
        "valid",
        "wrong_nonce",
        "stale_auth",
        "missing_auth_time",
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
    if mutation == "stale_auth":
        claims["auth_time"] = now - 3600
    if mutation == "missing_auth_time":
        claims.pop("auth_time")
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
    if mutation == "valid":
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
