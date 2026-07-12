import requests

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"


def send_push(token: str, title: str, body: str, data: dict | None = None) -> bool:
    """Send an Expo push notification. A dead/invalid token or a network hiccup
    must never break the caller — swallow failures and just report success."""
    if not token:
        return False
    payload = {"to": token, "title": title, "body": body}
    if data:
        payload["data"] = data
    try:
        resp = requests.post(EXPO_PUSH_URL, json=payload, timeout=10)
        return resp.status_code == 200
    except requests.RequestException:
        return False
