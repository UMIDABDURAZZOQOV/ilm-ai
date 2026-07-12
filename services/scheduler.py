"""Background jobs running inside the main FastAPI process (push notifications).

Distinct from telegram_bot/bot.py's job_queue, which runs in a separate process
and only knows about Telegram chat ids — this scheduler is for push-token-based
reminders, which need to fire independent of the Telegram bot.
"""
import os
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler

from services.push import send_push
from services.users import users_with_push_reminder_at, find_user_by_id

TZ = ZoneInfo("Asia/Tashkent")

_scheduler: BackgroundScheduler | None = None


def _keep_alive():
    """Ping our own public URL so a free host (e.g. Render) never spins the
    service down — this keeps the Telegram webhook always reachable."""
    base = os.environ.get("RENDER_EXTERNAL_URL")
    if not base:
        return
    try:
        urllib.request.urlopen(f"{base.rstrip('/')}/health", timeout=20)
    except Exception:  # noqa: BLE001 — best-effort keep-alive
        pass


def _check_daily_reminders():
    now = datetime.now(TZ)
    for user in users_with_push_reminder_at(now.hour, now.minute):
        send_push(
            user["push_token"],
            "Ilm AI",
            "Bugungi o'quv rejangizni ko'rish vaqti keldi 📚",
        )


def _check_due_reviews():
    from services.review import count_due_by_user

    for user_id, due_count in count_due_by_user().items():
        user = find_user_by_id(user_id)
        if not user or not user.get("push_token"):
            continue
        send_push(
            user["push_token"],
            "Ilm AI",
            f"Bugun {due_count} ta mavzuni takrorlash vaqti keldi 🎯",
        )


def start_scheduler():
    global _scheduler
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler(timezone=TZ)
    _scheduler.add_job(_check_daily_reminders, "interval", seconds=60, id="push_daily_reminder")
    _scheduler.add_job(_check_due_reviews, "cron", hour=8, minute=0, id="push_due_reviews")
    # Keep the free instance awake so the Telegram webhook never sleeps.
    if os.environ.get("RENDER_EXTERNAL_URL"):
        _scheduler.add_job(_keep_alive, "interval", minutes=10, id="keep_alive")
    _scheduler.start()
