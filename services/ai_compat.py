"""Compatibility shims that let the codebase keep its old google-genai call
shape while the actual work is done by OpenAI (see services/gemini.py).

The whole app was written against `google.genai`: routers build multimodal
inputs with `types.Part.from_bytes(...)` and catch `ClientError` (reading its
`.code` for 429 rate limits). Rather than rewrite every call site, we keep those
exact names but back them with plain data holders. `services/gemini.py`
understands these Part objects and translates them into OpenAI vision/audio
requests, and raises `ClientError(code=...)` on failure so existing
`except ClientError` blocks keep working unchanged.
"""
from __future__ import annotations


class Part:
    """Stand-in for google.genai types.Part — just carries raw media bytes and
    their MIME type. The OpenAI adapter inspects these when building a request."""

    def __init__(self, data: bytes, mime_type: str | None = None):
        self.data = data
        self.mime_type = mime_type or "application/octet-stream"

    @classmethod
    def from_bytes(cls, data: bytes, mime_type: str | None = None) -> "Part":
        return cls(data=data, mime_type=mime_type)

    @property
    def is_image(self) -> bool:
        return (self.mime_type or "").startswith("image/")

    @property
    def is_audio(self) -> bool:
        return (self.mime_type or "").startswith("audio/")


class HttpOptions:
    """No-op stand-in — some legacy code passed http_options=types.HttpOptions(...)."""

    def __init__(self, *args, **kwargs):
        pass


class _Types:
    Part = Part
    HttpOptions = HttpOptions


# Importable as `from services.ai_compat import types` to mirror
# `from google.genai import types`.
types = _Types()


class ClientError(Exception):
    """Mirror of google.genai.errors.ClientError. Carries an HTTP-ish `.code`
    (e.g. 429 for rate limits) so existing handlers can branch on it."""

    def __init__(self, message: str = "", code: int | None = None):
        super().__init__(message)
        self.code = code
        self.message = message


class _GenaiShim:
    """Placeholder for the few modules that did `from google import genai` but
    only used it for type references — never to build a client at runtime."""

    Client = None


genai = _GenaiShim()
