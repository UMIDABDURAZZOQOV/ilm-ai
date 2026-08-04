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
    """OpenAI text-to-speech — natural multilingual voice (also handles Uzbek far
    better than on-device TTS) and it reuses the OpenAI key we already pay for."""
    key = _openai_key()
    if not key:
        raise TTSError("OPENAI_API_KEY not configured")
    from openai import OpenAI

    client = OpenAI(api_key=key, base_url=os.environ.get("OPENAI_BASE_URL") or None, timeout=60.0)
    model = os.environ.get("OPENAI_TTS_MODEL", "tts-1")
    voice = os.environ.get("OPENAI_TTS_VOICE", "alloy")
    resp = client.audio.speech.create(model=model, voice=voice, input=text, response_format="mp3")
    return resp.content


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
