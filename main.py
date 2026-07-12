import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from routers import auth, files, chat, quiz, plan, telegram_link, gaps, payments, feedback, evaluation, sat_ielts, assistant, notifications, review
from services.monitoring import init_monitoring
from services.db import engine, Base
from services.scheduler import start_scheduler
from services import telegram_webhook

load_dotenv()
init_monitoring()

# Auto-create tables in DB on startup
Base.metadata.create_all(bind=engine)

# Seed the SAT/IELTS question bank on a fresh (empty) database — production
# Postgres starts empty, so without this the Question Bank shows 0 questions.
from services.seed_bank import seed_question_bank_if_empty
seed_question_bank_if_empty()

# Spread placeholder-skill ("General"/null) questions across real taxonomy skills
# so every question is reachable by topic in the Question Bank.
from services.retag_bank import retag_general_questions, clean_question_text
clean_question_text()
retag_general_questions()

start_scheduler()

IS_PRODUCTION = os.environ.get("ENVIRONMENT") == "production"
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
if IS_PRODUCTION and SECRET_KEY == "your-secret-key-change-in-production":
    raise RuntimeError(
        "SECRET_KEY is not set. Refusing to start in production with the default "
        "value — this signs OAuth session cookies. Set SECRET_KEY in the environment."
    )

app = FastAPI(title="Ilm AI Backend", version="0.3.0")

# Add session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# ALLOWED_ORIGINS: comma-separated list of origins allowed to make credentialed
# requests (the web frontend). Mobile app requests don't send an Origin header
# so they aren't affected by this. Defaults to permissive for local dev only.
_allowed_origins_env = os.environ.get("ALLOWED_ORIGINS", "")
if _allowed_origins_env:
    ALLOWED_ORIGINS = [o.strip() for o in _allowed_origins_env.split(",") if o.strip()]
elif IS_PRODUCTION:
    raise RuntimeError(
        "ALLOWED_ORIGINS is not set. Refusing to start in production with a "
        "wildcard CORS origin combined with allow_credentials=True. Set "
        "ALLOWED_ORIGINS to a comma-separated list of your frontend origin(s)."
    )
else:
    ALLOWED_ORIGINS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(plan.router)
app.include_router(telegram_link.router)
app.include_router(gaps.router)
app.include_router(payments.router)
app.include_router(feedback.router)
app.include_router(evaluation.router)
app.include_router(sat_ielts.router)
app.include_router(assistant.router)
app.include_router(notifications.router)
app.include_router(review.router)

@app.get("/")
def root():
    return {"message": "Ilm AI Backend is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}


# ── Telegram bot in webhook mode (runs inside this web service) ────────────────

@app.on_event("startup")
async def _telegram_startup():
    try:
        await telegram_webhook.start_webhook()
    except Exception as e:  # noqa: BLE001 — never block API startup on the bot
        logging.getLogger(__name__).warning("Telegram webhook setup failed: %s", e)


@app.on_event("shutdown")
async def _telegram_shutdown():
    await telegram_webhook.stop_webhook()


@app.post("/telegram/webhook")
async def telegram_webhook_route(request: Request):
    data = await request.json()
    await telegram_webhook.process_update(data)
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)