import os

import requests

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

_firebase_app = None
_firebase_init_attempted = False


def _get_firebase_app():
    """Lazily initializes the Firebase Admin SDK from a service account file,
    if configured. Returns None (never raises) if not configured or the
    credentials are invalid -- FCM sending is best-effort, same as the Expo
    path below."""
    global _firebase_app, _firebase_init_attempted
    if _firebase_init_attempted:
        return _firebase_app
    _firebase_init_attempted = True

    cred_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")
    if not cred_path or not os.path.exists(cred_path):
        return None
    try:
        import firebase_admin
        from firebase_admin import credentials

        _firebase_app = firebase_admin.initialize_app(credentials.Certificate(cred_path))
    except Exception:
        _firebase_app = None
    return _firebase_app


def _send_expo(token: str, title: str, body: str, data: dict | None) -> bool:
    payload = {"to": token, "title": title, "body": body}
    if data:
        payload["data"] = data
    try:
        resp = requests.post(EXPO_PUSH_URL, json=payload, timeout=10)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def _send_fcm(token: str, title: str, body: str, data: dict | None) -> bool:
    app = _get_firebase_app()
    if app is None:
        return False
    try:
        from firebase_admin import messaging

        message = messaging.Message(
            token=token,
            notification=messaging.Notification(title=title, body=body),
            data={k: str(v) for k, v in (data or {}).items()},
        )
        messaging.send(message, app=app)
        return True
    except Exception:
        return False


def send_push(token: str, title: str, body: str, data: dict | None = None) -> bool:
    """Send a push notification. Dispatches to Expo's relay for Expo-format
    tokens (existing RN app installs) or directly to FCM for everything else
    (the Flutter app's real device tokens) -- additive branch, the Expo path
    is untouched. A dead/invalid token or a network hiccup must never break
    the caller, so both paths swallow failures and just report success."""
    if not token:
        return False
    if token.startswith("ExponentPushToken[") or token.startswith("ExpoPushToken["):
        return _send_expo(token, title, body, data)
    return _send_fcm(token, title, body, data)
