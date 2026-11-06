"""Verified provider identity regression; fake provider, disposable SQLite only."""
import asyncio
import secrets
from urllib.parse import urlencode, urlparse, parse_qs

import pytest
from fastapi import HTTPException, Request
from services import google_oauth, mobile_oauth
from services.models import User
from test_release_hardening import setup


def callback(monkeypatch, info):
    class Response:
        status_code = 200

        def __init__(self, value):
            self.value = value

        def json(self):
            return self.value

    monkeypatch.setattr(google_oauth, 'is_google_oauth_enabled', lambda: True)
    monkeypatch.setattr(google_oauth.requests, 'post', lambda *a, **kw: Response({'access_token': 'provider-test-token'}))
    monkeypatch.setattr(google_oauth.requests, 'get', lambda *a, **kw: Response(info))
    redirect = 'http://testserver/auth/google-callback-mobile'
    state = secrets.token_urlsafe(24)
    mobile_oauth.save_state(state, redirect, 'a' * 43)
    request = Request({'type': 'http', 'method': 'GET', 'path': '/',
                       'query_string': urlencode({'state': state, 'code': 'test-code'}).encode(),
                       'headers': []})
    return asyncio.run(google_oauth.handle_google_callback(request, redirect, mobile=True))


def test_same_verified_subject_restores_existing_profile_after_email_change(setup, monkeypatch):
    _, factory = setup
    info = dict(email='new@example.test', email_verified=True, sub='verified-sub-1', name='Same name')
    first = callback(monkeypatch, info)
    with factory() as db:
        learner = db.get(User, first['user_id'])
        learner.age = 14
        learner.xp_total = 75
        db.commit()
        count = db.query(User).count()
    again = callback(monkeypatch, dict(info, email='renamed@example.test', name='New display name'))
    assert again['user_id'] == first['user_id']
    with factory() as db:
        assert db.query(User).count() == count
        learner = db.get(User, first['user_id'])
        assert learner.xp_total == 75 and learner.age == 14
        assert learner.name == 'Same name'  # Provider names do not overwrite saved profiles.


def test_distinct_verified_subjects_never_share_identity_by_display_name(setup, monkeypatch):
    info = dict(email='first@example.test', email_verified=True, sub='first-sub', name='Same name')
    first = callback(monkeypatch, info)
    second = callback(monkeypatch, dict(info, email='second@example.test', sub='second-sub'))
    assert second['user_id'] != first['user_id']
    with pytest.raises(HTTPException):
        callback(monkeypatch, dict(info, sub='someone-else'))
    with pytest.raises(HTTPException):
        callback(monkeypatch, dict(info, email_verified=False))


def test_ambiguous_legacy_provider_identity_fails_closed(setup, monkeypatch):
    _, factory = setup
    with factory() as db:
        for uid in (1, 2):
            learner = db.get(User, uid)
            learner.oauth_provider = 'google'
            learner.oauth_provider_id = 'duplicate-legacy-id'
        db.commit()
    with pytest.raises(HTTPException):
        callback(monkeypatch, dict(email='learner1@example.test', email_verified=True,
                                   sub='duplicate-legacy-id', name='Same name'))


def test_registration_opens_account_choice_with_existing_state_and_pkce_contract(setup, monkeypatch):
    class Client:
        async def load_server_metadata(self):
            return {'authorization_endpoint': 'https://accounts.google.com/o/oauth2/v2/auth'}

    monkeypatch.setattr(google_oauth, 'is_google_oauth_enabled', lambda: True)
    monkeypatch.setattr(google_oauth.oauth, 'create_client', lambda _: Client())
    request = Request({'type': 'http', 'method': 'GET', 'path': '/', 'headers': [], 'query_string': b''})
    redirect = 'http://testserver/auth/google-callback-mobile'
    url, state = asyncio.run(google_oauth.get_google_auth_url(request, redirect, 'a' * 43))
    query = parse_qs(urlparse(url).query)
    assert query['prompt'] == ['select_account']
    assert query['state'] == [state]
    assert mobile_oauth.consume_state(state, redirect) == 'a' * 43
