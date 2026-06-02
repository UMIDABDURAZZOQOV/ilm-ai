from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers import auth, files, chat, quiz, plan, telegram_link, gaps, payments, feedback

load_dotenv()

app = FastAPI(title="Ilm AI Backend", version="0.3.0")

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

@app.get("/")
def root():
    return {"message": "Ilm AI Backend is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}