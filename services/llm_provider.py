"""
One text-generation call, whichever provider is configured.

⚠️ OFFLINE CONTENT SEEDING ONLY — DO NOT WIRE THIS INTO A REQUEST PATH.

The seeding key may be on a data-sharing plan (OpenAI grants free daily tokens in
exchange for training on everything sent through it), and that is only acceptable
because these prompts carry no user data at all: a prompt here is "Fan: Matematika,
Bo'lim: Trigonometriya, Mavzu: Sinus teoremasi — write teaching cards", built from the
hand-authored syllabus in skilltree_taxonomy.py.

Runtime features handle real student work — the AI assistant, chat, IELTS Writing
grading — and those go through `services/gemini.py` on a separate key. Routing any of
them here would send a learner's own essay to be trained on. If that ever becomes
desirable, the data-sharing plan has to be turned off first.

The content seeders were written against Gemini's client directly, which was fine
until the free tier's daily cap started pacing the work. This lets an OpenAI key (or
any OpenAI-compatible endpoint — DeepSeek, Groq, a local server) carry the batch
instead, without touching a seeder.

Provider is chosen by `SEED_PROVIDER`, or inferred from whichever key is present:

    SEED_PROVIDER=gemini   GEMINI_API_KEYS=a,b,c        (default)
    SEED_PROVIDER=openai   OPENAI_API_KEYS=sk-...       OPENAI_MODEL=gpt-4o-mini
                           OPENAI_BASE_URL=...          (optional, for compatibles)

Keys are used round-robin and a call sweeps the whole ring several times before
giving up: a batch this size regularly exhausts several keys at once, and bailing on
the first full sweep threw away a whole lesson over what was usually a per-minute
limit.

A response is returned as a small object with `.text`, matching what the seeders
already expect from Gemini.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass


@dataclass
class LlmResponse:
    text: str


def _keys(*names: str) -> list[str]:
    for name in names:
        raw = os.environ.get(name)
        if raw:
            keys = [k.strip() for k in raw.split(",") if k.strip()]
            if keys:
                return keys
    return []


class GeminiProvider:
    name = "gemini"

    def __init__(self) -> None:
        from google import genai
        from google.genai import types as genai_types

        self.model = os.environ.get("SEED_GEMINI_MODEL", "gemini-flash-lite-latest")
        # 60s timeout: without it a stalled connection hangs the batch instead of
        # failing over to the next key.
        self.clients = [
            genai.Client(api_key=k, http_options=genai_types.HttpOptions(timeout=60_000))
            for k in _keys("GEMINI_API_KEYS", "GEMINI_API_KEY")
        ]

    def call(self, client, prompt: str) -> LlmResponse:
        return LlmResponse(client.models.generate_content(model=self.model, contents=prompt).text)


class OpenAiProvider:
    name = "openai"

    def __init__(self) -> None:
        from openai import OpenAI

        self.model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        base_url = os.environ.get("OPENAI_BASE_URL") or None
        self.clients = [
            OpenAI(api_key=k, base_url=base_url, timeout=60.0)
            for k in _keys("OPENAI_API_KEYS", "OPENAI_API_KEY")
        ]

    def call(self, client, prompt: str) -> LlmResponse:
        out = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return LlmResponse(out.choices[0].message.content or "")


def _build():
    choice = (os.environ.get("SEED_PROVIDER") or "").strip().lower()
    if not choice:
        # Infer: an OpenAI key with no Gemini key means OpenAI was the intent.
        choice = "openai" if (_keys("OPENAI_API_KEYS", "OPENAI_API_KEY")
                              and not _keys("GEMINI_API_KEYS", "GEMINI_API_KEY")) else "gemini"
    provider = OpenAiProvider() if choice == "openai" else GeminiProvider()
    if not provider.clients:
        raise RuntimeError(
            f"No API keys for provider '{provider.name}'. Set "
            f"{'OPENAI_API_KEYS' if provider.name == 'openai' else 'GEMINI_API_KEYS'}."
        )
    return provider


_provider = None
_index = 0


def generate(prompt: str, rounds: int = 3) -> LlmResponse:
    """Round-robin across every key, sweeping the ring `rounds` times."""
    global _provider, _index
    if _provider is None:
        _provider = _build()

    clients = _provider.clients
    last_err: Exception | None = None
    for attempt in range(rounds):
        for _ in range(len(clients)):
            client = clients[_index]
            idx = _index
            _index = (_index + 1) % len(clients)
            try:
                return _provider.call(client, prompt)
            except Exception as exc:
                print(f"  {_provider.name} key #{idx} failed: {str(exc)[:120]}")
                last_err = exc
        if attempt < rounds - 1:
            time.sleep(20)
    raise last_err if last_err else RuntimeError("generation failed")


def provider_name() -> str:
    global _provider
    if _provider is None:
        _provider = _build()
    return f"{_provider.name}:{_provider.model} ({len(_provider.clients)} keys)"
