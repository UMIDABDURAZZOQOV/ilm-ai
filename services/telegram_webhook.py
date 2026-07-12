"""Run the Telegram bot in webhook mode inside the FastAPI web service.

This lets the bot run on hosts that don't offer background workers (e.g. Render's
free plan): Telegram pushes updates to POST /telegram/webhook, which are fed to
the python-telegram-bot Application here — no separate polling process needed.

Gated behind a public base URL (RENDER_EXTERNAL_URL, set automatically on Render,
or TELEGRAM_WEBHOOK_BASE to override). When it's absent (local dev), this does
nothing and the bot keeps using run_telegram_bot.py (polling).
"""
import logging
import os

from telegram import Update

logger = logging.getLogger(__name__)

_application = None


def _public_base_url() -> str | None:
    return os.environ.get("TELEGRAM_WEBHOOK_BASE") or os.environ.get("RENDER_EXTERNAL_URL")


def webhook_enabled() -> bool:
    return bool(_public_base_url()) and bool(os.environ.get("TELEGRAM_BOT_TOKEN"))


async def start_webhook() -> None:
    """Initialise the bot and register the webhook. Safe no-op if not enabled."""
    global _application
    if not webhook_enabled():
        logger.info("Telegram webhook disabled (no public URL) — skipping.")
        return
    from telegram_bot.bot import build_application

    _application = build_application()
    await _application.initialize()
    await _application.start()  # starts the job queue (daily reminders, etc.)

    base = _public_base_url().rstrip("/")
    url = f"{base}/telegram/webhook"
    await _application.bot.set_webhook(
        url=url,
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )
    logger.info("Telegram webhook registered at %s", url)


async def stop_webhook() -> None:
    global _application
    if _application is not None:
        try:
            await _application.stop()
            await _application.shutdown()
        finally:
            _application = None


async def process_update(data: dict) -> None:
    if _application is None:
        return
    update = Update.de_json(data, _application.bot)
    await _application.process_update(update)
