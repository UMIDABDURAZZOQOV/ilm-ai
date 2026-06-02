# Ilm AI

Ilm AI — personal learning companion (backend + frontend).

Quick start (development):

1. Copy `.env.example` to `.env` and set `GEMINI_API_KEY` and `TELEGRAM_BOT_TOKEN` (can be dummy for local tests).

2. Create a Python virtual environment and install dependencies:

```powershell
cd C:\Users\Larry\ilm-ai
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

3. Run backend:

```powershell
uvicorn main:app --reload
```

Database migration (optional):

Set `DATABASE_URL` in `.env` and run:

```powershell
python scripts/migrate_to_db.py
```

This will create tables and import existing `users.json`, `data/quiz_history` and `vectors/*.json` into Postgres.

Alembic migrations:

1. Install alembic (`pip install alembic`) or ensure it's in `requirements.txt`.
2. Configure `DATABASE_URL` in your environment.
3. Run migrations:

```powershell
alembic upgrade head
```

The repo includes a basic Alembic scaffold in the `alembic/` folder and an initial migration `alembic/versions/0001_initial.py`.

4. Serve frontend (from `ilm-ai-frontend`):

```powershell
cd C:\Users\Larry\ilm-ai-frontend
python -m http.server 5500
```

Open `http://127.0.0.1:5500` for the frontend and `http://127.0.0.1:8000/docs` for API docs.

Notes & missing items:

- Week 3 milestone features (quiz, gaps report, test-mode payments, Telegram bot, dashboard, feedback) are implemented.
- The project currently uses JSON files for storage (`users.json`, `data/` directories). PostgreSQL + `pgvector` is not yet integrated.
- OAuth (Google), JWT refresh tokens, CI/CD deployments, and production monitoring are NOT implemented yet. These are recommended next steps for a production-ready release.

What I changed locally to help testing:

- Added `python-docx` to `requirements.txt` and support for `.docx` uploads.
- Added developer Docker and GitHub Actions CI workflow files (see repo root).

If you want, I can continue and implement (in order of priority):
1. PostgreSQL + migrations + switch storage from JSON to DB
2. JWT + refresh tokens for auth
3. Google OAuth
4. Real payment provider integration (Stripe/Payme/Click)
5. Add evaluation harness and automated test samples

Tell me which of the above you want next and I will implement it.
