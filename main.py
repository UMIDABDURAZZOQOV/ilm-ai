import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from routers import auth, files, chat, quiz, plan, telegram_link, gaps, payments, feedback, evaluation, sat_ielts
from services.monitoring import init_monitoring
from services.db import engine, Base
from services.google_oauth import oauth

load_dotenv()
init_monitoring()

# Auto-create tables in DB on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ilm AI Backend", version="0.3.0")

# Add session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SECRET_KEY", "your-secret-key-change-in-production"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.get("/")
def root():
    return {"message": "Ilm AI Backend is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)