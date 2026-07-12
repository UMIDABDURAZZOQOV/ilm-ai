"""Centralized Gemini access with automatic multi-key fallback.

Set GEMINI_API_KEYS to a comma-separated list of keys (falls back to the single
GEMINI_API_KEY). generate_content() tries the current key and, if it hits a
quota / rate-limit / key error, automatically rotates to the next key — so a
single free-tier key running out does not surface an error to users while other
keys still have quota. Once a working key is found, it sticks with it.
"""
import os

from google import genai
from google.genai.errors import ClientError

_clients: dict[str, genai.Client] = {}
_current = 0

# A 400 (bad request) is caused by the prompt itself, so it is identical for
# every key — no point retrying it across keys. EVERY other error (429 quota,
# 403 permission, 404 model access, 5xx, network, etc.) may be specific to one
# key, so we rotate to the next key and try again. This keeps the site working
# for users as long as a single healthy key remains.
_NO_ROTATE_CODES = {400}


def _keys() -> list[str]:
    raw = os.environ.get("GEMINI_API_KEYS") or os.environ.get("GEMINI_API_KEY", "")
    return [k.strip() for k in raw.split(",") if k.strip()]


def _client_for(key: str) -> genai.Client:
    c = _clients.get(key)
    if c is None:
        c = genai.Client(api_key=key)
        _clients[key] = c
    return c


def _call(method_name: str, **kwargs):
    """Invoke client.models.<method_name>(**kwargs) with key rotation."""
    global _current
    keys = _keys()
    if not keys:
        raise RuntimeError("No GEMINI_API_KEYS / GEMINI_API_KEY configured")

    n = len(keys)
    last_err: Exception | None = None
    for offset in range(n):
        idx = (_current + offset) % n
        key = keys[idx]
        try:
            method = getattr(_client_for(key).models, method_name)
            resp = method(**kwargs)
            _current = idx  # remember the key that worked
            return resp
        except ClientError as e:
            code = getattr(e, "code", None)
            if code in _NO_ROTATE_CODES:
                raise  # bad request — same for every key, don't waste the others
            last_err = e
            continue  # quota / permission / model / etc. — try the next key
        except Exception as e:  # network/other transient — try next key
            last_err = e
            continue

    if last_err is not None:
        raise last_err
    raise RuntimeError(f"Gemini {method_name} failed with no keys available")


def generate_content(**kwargs):
    """Drop-in for client.models.generate_content(...) with key rotation."""
    return _call("generate_content", **kwargs)


def embed_content(**kwargs):
    """Drop-in for client.models.embed_content(...) with key rotation."""
    return _call("embed_content", **kwargs)
