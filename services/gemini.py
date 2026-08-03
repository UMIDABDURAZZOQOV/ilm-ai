"""Centralized AI text/vision/embedding access — now backed by OpenAI.

Despite the filename (kept so the ~25 existing `from services.gemini import ...`
call sites don't have to change), this module now talks to OpenAI. It exposes the
same drop-in surface the codebase already uses:

    generate_content(model=..., contents=..., config=...)  -> obj with .text
    embed_content(model=..., contents=[...])               -> obj with .embeddings[i].values

`contents` keeps the google-genai shape: a string, or a list mixing strings with
`services.ai_compat.Part` objects (built via `types.Part.from_bytes`). This adapter
translates those into OpenAI calls:

  * text            -> a normal chat message
  * image Part      -> a vision image_url (base64 data URL)
  * audio Part      -> transcribed with Whisper first, then folded into the prompt
                       (so old `[prompt, audio_part]` call sites keep working)

The `model=` argument callers pass (e.g. "gemini-flash-latest") is ignored; the
real model comes from OPENAI_MODEL. Failures are raised as
`services.ai_compat.ClientError(code=...)` so existing `except ClientError` blocks
keep branching on 429 the same way.

Config (all via env):
    OPENAI_API_KEYS   comma-separated keys (falls back to OPENAI_API_KEY)
    OPENAI_MODEL      default "gpt-5-mini"
    OPENAI_EMBED_MODEL        default "text-embedding-3-small"
    OPENAI_TRANSCRIBE_MODEL   default "whisper-1"
    OPENAI_BASE_URL   optional, for OpenAI-compatible endpoints
"""
from __future__ import annotations

import base64
import io
import os

from services.ai_compat import ClientError, Part

_clients: list = []
_current = 0
_REQUEST_TIMEOUT_S = 60.0


def _model() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-5-mini")


def _embed_model() -> str:
    return os.environ.get("OPENAI_EMBED_MODEL", "text-embedding-3-small")


def _transcribe_model() -> str:
    return os.environ.get("OPENAI_TRANSCRIBE_MODEL", "whisper-1")


def _keys() -> list[str]:
    raw = os.environ.get("OPENAI_API_KEYS") or os.environ.get("OPENAI_API_KEY", "")
    return [k.strip() for k in raw.split(",") if k.strip()]


def _build_clients() -> list:
    global _clients
    if _clients:
        return _clients
    from openai import OpenAI

    keys = _keys()
    if not keys:
        raise ClientError("No OPENAI_API_KEYS / OPENAI_API_KEY configured", code=None)
    base_url = os.environ.get("OPENAI_BASE_URL") or None
    _clients = [OpenAI(api_key=k, base_url=base_url, timeout=_REQUEST_TIMEOUT_S) for k in keys]
    return _clients


def _status_code(exc: Exception) -> int | None:
    """Pull an HTTP status out of an OpenAI SDK error, if any."""
    for attr in ("status_code", "http_status", "code"):
        val = getattr(exc, attr, None)
        if isinstance(val, int):
            return val
    resp = getattr(exc, "response", None)
    if resp is not None:
        sc = getattr(resp, "status_code", None)
        if isinstance(sc, int):
            return sc
    return None


def _run_with_rotation(fn):
    """Call fn(client) across the key ring, rotating on any error except a 400
    (bad request — identical for every key). Mirrors the old Gemini rotation."""
    global _current
    clients = _build_clients()
    n = len(clients)
    last_err: Exception | None = None
    for offset in range(n):
        idx = (_current + offset) % n
        client = clients[idx]
        try:
            out = fn(client)
            _current = idx
            return out
        except Exception as e:  # noqa: BLE001 — normalize below
            code = _status_code(e)
            if code == 400:
                raise ClientError(str(e), code=400)
            last_err = e
            continue
    code = _status_code(last_err) if last_err else None
    raise ClientError(str(last_err) if last_err else "OpenAI request failed", code=code)


# --- response holders matching the old google-genai shape -------------------

class _Resp:
    def __init__(self, text: str, total_tokens: int | None):
        self.text = text
        self.usage_metadata = _Usage(total_tokens) if total_tokens is not None else None


class _Usage:
    def __init__(self, total_tokens: int | None):
        self.total_token_count = total_tokens


class _Emb:
    def __init__(self, values: list[float]):
        self.values = values


class _EmbResp:
    def __init__(self, embeddings: list[_Emb]):
        self.embeddings = embeddings


# --- multimodal input translation -------------------------------------------

def _transcribe(client, part: Part) -> str:
    """Whisper transcription for an audio Part. Returns the text (or '')."""
    ext = "wav"
    mt = (part.mime_type or "").lower()
    if "mp3" in mt or "mpeg" in mt:
        ext = "mp3"
    elif "mp4" in mt or "m4a" in mt or "aac" in mt:
        ext = "m4a"
    elif "webm" in mt or "ogg" in mt:
        ext = "webm"
    buf = io.BytesIO(part.data)
    buf.name = f"audio.{ext}"
    tr = client.audio.transcriptions.create(model=_transcribe_model(), file=buf)
    return (getattr(tr, "text", "") or "").strip()


def _build_messages(client, contents) -> list[dict]:
    """Turn google-genai style `contents` into an OpenAI chat `messages` list."""
    items = contents if isinstance(contents, (list, tuple)) else [contents]

    text_bits: list[str] = []
    image_parts: list[Part] = []
    for item in items:
        if isinstance(item, Part):
            if item.is_image:
                image_parts.append(item)
            elif item.is_audio:
                spoken = _transcribe(client, item)
                if spoken:
                    text_bits.append(f"[The learner's spoken message, transcribed]: {spoken}")
            else:
                # Unknown binary — best effort: ignore rather than crash.
                continue
        elif item is not None:
            text_bits.append(str(item))

    text = "\n\n".join(b for b in text_bits if b).strip()

    if not image_parts:
        return [{"role": "user", "content": text or ""}]

    # Vision message: text + one or more images as data URLs.
    content: list[dict] = []
    if text:
        content.append({"type": "text", "text": text})
    for p in image_parts:
        b64 = base64.b64encode(p.data).decode("ascii")
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{p.mime_type};base64,{b64}"},
        })
    return [{"role": "user", "content": content}]


def _wants_json(config) -> bool:
    if not config:
        return False
    if isinstance(config, dict):
        mime = config.get("response_mime_type")
    else:
        mime = getattr(config, "response_mime_type", None)
    return mime == "application/json"


# --- public drop-in API ------------------------------------------------------

def generate_content(*, model: str | None = None, contents=None, config=None, **_ignored):
    """Drop-in for the old Gemini generate_content, backed by OpenAI chat."""

    def call(client):
        messages = _build_messages(client, contents)
        kwargs: dict = {"model": _model(), "messages": messages}
        if _wants_json(config):
            kwargs["response_format"] = {"type": "json_object"}
        out = client.chat.completions.create(**kwargs)
        text = (out.choices[0].message.content or "") if out.choices else ""
        total = None
        usage = getattr(out, "usage", None)
        if usage is not None:
            total = getattr(usage, "total_tokens", None)
        return _Resp(text=text, total_tokens=total)

    return _run_with_rotation(call)


def embed_content(*, model: str | None = None, contents=None, **_ignored):
    """Drop-in for the old Gemini embed_content, backed by OpenAI embeddings.

    Accepts a string or a list of strings (the codebase always passes a list)
    and returns an object whose `.embeddings[i].values` holds each vector."""
    inputs = contents if isinstance(contents, (list, tuple)) else [contents]
    inputs = [str(t) for t in inputs]

    def call(client):
        resp = client.embeddings.create(model=_embed_model(), input=inputs)
        # OpenAI preserves input order in resp.data.
        ordered = sorted(resp.data, key=lambda d: d.index)
        return _EmbResp(embeddings=[_Emb(values=list(d.embedding)) for d in ordered])

    return _run_with_rotation(call)
