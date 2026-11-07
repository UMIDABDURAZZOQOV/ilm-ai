"""Synthetic pre-update token formats; never a real production account/token."""
import time
import jwt
from services import tokens
from services.models import RefreshToken, User, UserLessonProgress

pytest_plugins = ["test_release_hardening"]


def test_legacy_access_and_refresh_restore_same_profile_and_progress(setup):
    client, factory = setup
    now = int(time.time())
    # Same HS256/sub/iat/exp shape as the inspected old backend. Construct
    # independently, rather than asking the replacement issuer for a new token.
    access = jwt.encode({"sub": "1", "iat": now - 30, "exp": now + 300},
                        tokens.JWT_SECRET, algorithm="HS256")
    refresh = "ref_" + "a" * 64
    with factory.begin() as db:
        db.get(User, 1).xp_total = 137
        db.get(User, 1).age = 19
        db.add(RefreshToken(token=refresh, user_id=1, exp=now + 86400))
        db.add(UserLessonProgress(user_id=1, lesson_id=1, stars=2, attempts=1, xp_earned=137))
    profile = client.get("/auth/profile/1", headers={"Authorization": "Bearer " + access})
    assert profile.status_code == 200
    assert profile.json()["id"] == profile.json()["user_id"] == 1
    assert profile.json()["needs_onboarding"] is False
    assert client.get("/auth/profile/2", headers={"Authorization": "Bearer " + access}).status_code == 403
    rotated = client.post("/auth/refresh", json={"refresh_token": refresh})
    assert rotated.status_code == 200
    replacement = rotated.json()
    assert tokens.verify_access_token(replacement["access_token"]) == 1
    assert client.post("/auth/refresh", json={"refresh_token": refresh}).status_code == 401
    assert client.get("/auth/profile/1", headers={
        "Authorization": "Bearer " + replacement["access_token"],
    }).json()["id"] == 1
    assert client.post("/auth/logout", json={"refresh_token": replacement["refresh_token"]}).status_code == 200
    assert client.post("/auth/refresh", json={"refresh_token": replacement["refresh_token"]}).status_code == 401
    with factory() as db:
        assert db.query(User).count() == 2
        assert db.get(User, 1).xp_total == 137
        assert db.query(UserLessonProgress).filter_by(user_id=1, lesson_id=1).one().xp_earned == 137
