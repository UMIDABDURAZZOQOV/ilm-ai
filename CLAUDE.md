# Ilm AI — Project Context (for Claude)

Multilingual (Uzbek / Russian / English) AI education platform for youth in Uzbekistan.
This repo (`ilm-ai`) is the **backend**. Companion repos: `ilm-ai-frontend` (web), `ilm-ai-mobile`.

> **NOTE (secrets):** never commit `.env`. Only `.env.example` is tracked. Real Gemini keys,
> DATABASE_URL, ElevenLabs, Telegram, Google/Gmail creds live in `.env` (copy it by hand onto
> each machine — it is NOT on GitHub).

## Architecture
- **Backend:** FastAPI + SQLAlchemy + uvicorn. Postgres in prod (Render); falls back to
  `sqlite:///data/ilm_ai.db` locally when the Postgres port is unreachable (`services/db.py`).
- **Frontend:** Next.js 14 (App Router, TS, Tailwind) → Vercel, auto-deploys from GitHub `main`.
  `NEXT_PUBLIC_API_URL` is baked into the bundle at build time.
- **Mobile:** React Native / Expo.
- **AI:** Google Gemini via `services/gemini.py` (multi-key rotation, `gemini-flash-latest`,
  drop-in `generate_content(**kwargs)` / `embed_content(**kwargs)`). ElevenLabs for TTS.

## Live URLs
- Backend (prod): **https://ilm-ai-backend-256x.onrender.com**  ← the `-256x` suffix is REAL.
  The un-suffixed `ilm-ai-backend.onrender.com` is someone else's app (returns a fake 404).
- Frontend (prod): https://ilm-ai-frontend.vercel.app
- Prod DB: Render Postgres `ilm-ai-db` (free plan). Config in `render.yaml`.

## Run locally (Windows)
```
cd ilm-ai
pip install -r requirements.txt        # put .env in this folder first
uvicorn main:app --reload              # API on http://127.0.0.1:8000
```
Frontend: `cd ilm-ai-frontend && npm install && npm run dev`.

## Gotchas (learned the hard way)
- **Restarting the backend on Windows:** `pkill` does NOT kill Windows `python.exe`. Verify a
  restart via PowerShell PID + check `/openapi.json` responds, don't assume.
- **Telegram bot is a SEPARATE process:** `run_telegram_bot.py` runs its own polling loop.
  Restarting the API does NOT start it. There are 2 schedulers by design (push vs telegram).
- **Bash tool cwd persists** across calls — a stray `cd` into the frontend folder made
  `data/ilm_ai.db` resolve to the wrong place and created an empty DB. Always `cd ilm-ai` first.

## What's been built so far (feature history)
Condensed record of work done to date (the code is the source of truth; read it for detail):
- **Auth & accounts:** email verification via SMTP code, forgot-password flow, unverified-login
  block, 8-char password rule + show/hide + live mismatch warning, Google Sign-In.
- **General AI assistant** (`routers/assistant.py`): unrestricted (not materials-grounded),
  voice input (audio→Gemini), free/premium daily limit, ElevenLabs TTS with device-TTS fallback.
- **Learning core:** materials-grounded Chat (RAG), Quiz, Knowledge-Gaps report, Learning-Plan
  generator, "Bugungi reja" today-plan card, spaced-repetition Review, score-trend chart.
- **SAT platform:** skill taxonomy (`services/sat_taxonomy.py`), filtered practice sessions +
  progress, Bluebook-style exam UI, results + AI, Mock Tests, Analytics, Official Full-Length
  Tests page, question-bank seeding/import + prod sync.
- **IELTS platform:** 8 tables + 18 routes (`routers/ielts.py`), Gemini rubric AI grading
  (Writing/Speaking), 4-skill frontend `/ielts` pages + mock test. (Content not on prod yet.)
- **Web frontend** (`ilm-ai-frontend`): dashboard panels for all of the above, light/dark theme
  toggle, full uz/ru/en i18n, ChatGPT-style Live Voice overlay.
- **Mobile** (`ilm-ai-mobile`, React Native/Expo): theming (light/dark), Settings screen,
  onboarding carousel + language picker + pre-auth flow, AI Assistant + Live Voice screens,
  push-notification infra, brand logo/icons, animations. (Launch paused — web is the priority.)
- **Deployed:** backend on Render (`ilm-ai-backend`, see URL above), frontend on Vercel
  (auto-deploy from `main`), Postgres on Render. Telegram bot runs as its own process.

## Status (as of 2026-07-15)
- **SAT:** live and working. Prod bank ≈ 2417 questions, topic-tagged. Source = OpenSAT API
  (text-only, no figures). ~9 prod questions reference a missing figure (optional cleanup).
  Local sqlite has more (~3687); prod syncs via `scripts/sync_sat_bank_to_prod.py` (needs the
  Render DB URL in `TARGET_DATABASE_URL`).
- **IELTS:** 8 tables + 18 routes (`routers/ielts.py`) + frontend `/ielts` pages.
  - AI grading (Writing/Speaking) is REAL — calls Gemini with an IELTS rubric, returns band
    score + 4 criteria + feedback (with a graceful fallback branch).
  - Content exists in LOCAL sqlite only (4 listening w/ real mp3s in frontend
    `public/audio/listening/`, ~7 unique reading, writing, 10 speaking, ~74 unique questions),
    but has DUPLICATES. Only Reading + Listening have child questions (`parent_id`).
  - **NOT on prod yet** — live `/ielts/*` endpoints return 0. Migrate with
    `scripts/sync_ielts_to_prod.py` (dedups, remaps parent_id, idempotent, additive) — not run yet.
- Almost no real users yet (not advertised). Fine.

## Open items
1. IELTS: dedup local content → run `sync_ielts_to_prod.py` → confirm listening audio serves on
   Vercel → generate more ORIGINAL content → verify AI grading against a running backend.
2. `services/gemini.py` is "sticky" (all load hits the last working key). Add round-robin
   load-balancing before advertising. ~10 keys configured; billing on 2-3 keys under consideration.

## ⚠️ Content policy (important)
Do NOT ingest or publish copyrighted exam material (Cambridge IELTS books, British Council
official tests, etc.) onto the platform — that is copyright infringement (true even while the
site is free; distribution is the issue, not payment). Use AI-generated ORIGINAL content in the
IELTS format, or genuinely open-licensed material. This matches the site's own "100% original
content" promise.
