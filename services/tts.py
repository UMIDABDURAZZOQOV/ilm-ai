import os

import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")


class TTSError(Exception):
    pass


def synthesize_speech(text: str, language: str) -> bytes:
    """Turn text into natural-sounding speech via ElevenLabs. Raises TTSError
    on any failure (missing key, quota exhausted, network error) so callers
    can fall back to on-device TTS instead of breaking the conversation."""
    if not ELEVENLABS_API_KEY:
        raise TTSError("ELEVENLABS_API_KEY not configured")

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
