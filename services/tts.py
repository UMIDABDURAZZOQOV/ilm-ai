import os

import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")


class TTSError(Exception):
    pass


def _openai_key() -> str:
    return os.environ.get("OPENAI_API_KEY") or (
        os.environ.get("OPENAI_API_KEYS", "").split(",")[0].strip()
    )


def _openai_tts(text: str) -> bytes:
    """OpenAI text-to-speech — natural multilingual voice (handles Uzbek far
    better than on-device TTS) and it reuses the OpenAI key we already use.

    Defaults to the newer `gpt-4o-mini-tts`, which is noticeably more natural
    and less accented (closer to ChatGPT's Advanced Voice) than the older
    `tts-1`, and supports an `instructions` steer for tone/accent. If that model
    (or the instructions arg) isn't accepted, we transparently fall back to
    tts-1 so voice never breaks over a quality upgrade."""
    key = _openai_key()
    if not key:
        raise TTSError("OPENAI_API_KEY not configured")
    from openai import OpenAI

    client = OpenAI(api_key=key, base_url=os.environ.get("OPENAI_BASE_URL") or None, timeout=60.0)
    model = os.environ.get("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
    voice = os.environ.get("OPENAI_TTS_VOICE", "nova")  # warm, clear, low-accent
    kwargs = dict(model=model, voice=voice, input=text, response_format="mp3")
    if model.startswith("gpt-4o"):
        kwargs["instructions"] = os.environ.get(
            "OPENAI_TTS_INSTRUCTIONS",
            "Speak naturally and clearly like a friendly tutor, with a neutral "
            "accent, calm warm tone, and a natural conversational pace.",
        )
    try:
        return client.audio.speech.create(**kwargs).content
    except Exception:
        # Newer model/instructions not available on this key — use the always-
        # available tts-1 with the same voice (nova is valid on both).
        return client.audio.speech.create(
            model="tts-1", voice=voice, input=text, response_format="mp3"
        ).content


def synthesize_speech(text: str, language: str) -> bytes:
    """Text -> speech. Prefer OpenAI TTS (good voice, same key we already use);
    fall back to ElevenLabs, then the caller falls back to on-device TTS."""
    try:
        return _openai_tts(text)
    except Exception as openai_err:
        if not ELEVENLABS_API_KEY:
            raise TTSError(f"OpenAI TTS failed, no ElevenLabs fallback: {openai_err}")
        # fall through to ElevenLabs below

    # Lower bitrate than the 128kbps default — halves payload size/transfer time
    # with no perceptible quality loss for spoken voice (vs. music).
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}?output_format=mp3_44100_64"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
    except requests.RequestException as e:
        raise TTSError(f"ElevenLabs request failed: {e}") from e

    if resp.status_code != 200:
        raise TTSError(f"ElevenLabs error {resp.status_code}: {resp.text[:200]}")

    return resp.content
