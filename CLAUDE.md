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

## Detailed work log (chronological, with outcomes)
Full history of what was done and the result, from the start to 2026-07-15. The code is the
source of truth; this is the narrative so context isn't lost across machines/sessions.

### Phase 1 — Mobile MVP audit & foundational fixes
- Audited the Expo/React Native app against the MVP feature list. Result: found and fixed a
  missing `@react-native-community/datetimepicker` dependency; got the app running end-to-end
  against the local backend.
- Fixed **Google Sign-In** (was broken end-to-end on mobile — callback not completing).
- Fixed the **premium upgrade flow** (non-functional in test mode) and added the deep-link
  scheme to `app.json`.
- Fixed i18n gaps in `QuestionCard.tsx` and improved short-answer grading.
- Replaced placeholder logo/icon with the real brand logo on web + mobile.
- Fixed a markdown-rendering bug in the Knowledge-Gaps report.

### Phase 2 — Auth hardening & email verification
- Built an **SMTP email-code service** + `EmailVerificationCode` DB model/migration.
- Reworked signup to **require email verification**; blocked login for unverified accounts.
- Added **forgot-password via email code**. Built mobile `VerifyEmailScreen` +
  `ForgotPasswordScreen`, and the web equivalents.
- Raised min password length to 8 with an upfront hint, live mismatch warning, show/hide toggle,
  and a "check your spam folder" hint on verify screens.

### Phase 3 — General AI Assistant, voice & TTS
- Backend: **unrestricted general-purpose assistant** endpoint (distinct from materials-grounded
  Chat) with a free/premium **daily limit**. Added **voice input** (audio → Gemini).
- Backend: **ElevenLabs TTS** endpoint with a device-TTS fallback. Verified end-to-end after
  getting `ELEVENLABS_API_KEY`.
- Mobile: built the **AI Assistant screen** (text + voice) as a new nav item.
- Fixes: strip markdown asterisks before TTS; fixed a stale-backend-process bug; fixed long
  voice answers hanging silently (no audio in Live Voice).

### Phase 4 — Dashboard/learning features
- **Score-trend sparkline** on the dashboard (`quizStats.score_trend`).
- **"Bugungi reja"** today-plan card.
- **Push-notification** infrastructure.
- **Knowledge Gaps → spaced-repetition** Review loop.

### Phase 5 — Mobile entry-flow redesign
- Built shared components: `BrandLogo`, `PillButton`, `FlagIcon`, `OnboardingIllustration`.
- Built full-screen `LanguageSelectScreen` (flag picker); rewrote onboarding as a swipeable
  carousel; built `PreAuthStack` and rewired `RootNavigator` order; restyled Splash/Login/SignUp.
- Built a light/dark **theming system** and a proper **Settings screen**; added animations
  across screens.

### Phase 6 — Pivot to web-first, and web build-out
- Decision (2026-07-09): **web (IELTS/SAT mock test + AI) is now the priority; mobile paused.**
- Audited the web frontend for the IELTS/SAT-first launch.
- Ported mobile-only features to web: `assistantApi.ts` + `AssistantDashboard.tsx`,
  `reviewApi.ts` + `ReviewDashboard.tsx`, wired new panels + Today's-Plan card into `page.tsx`.
- Added a real light/dark **theme toggle** (was hardcoded dark); matched web password validation
  to mobile; removed hardcoded strings for full **uz/ru/en i18n**; built a ChatGPT-style
  **Live Voice overlay**.

### Phase 7 — SAT platform (full build)
- Backend: skill **taxonomy** (`services/sat_taxonomy.py`: sections → domains → skills),
  filtered practice sessions + progress tracking.
- Frontend: `/sat` app shell + Home + Question Bank; **Bluebook-style** exam UI + results + AI
  integration; Mock Tests + Analytics; **Official Full-Length Tests** page; a premium cohesive
  redesign of `/sat` pages.
- Question bank: seeded via fixtures + a Gemini scale script; imported from the **OpenSAT API**
  (`pinesat.duckdns.org`, text-only, no figures). Fixed a mass mis-tagging problem where imports
  landed as "General"/domain-name placeholders — rewrote `services/retag_bank.py` with
  content-aware Math classification + round-robin, giving **0 unassigned / 0 null** locally
  (~3687 questions).
- **Prod sync:** `scripts/sync_sat_bank_to_prod.py` (dedupe by question_text, additive, no
  restart). Result: prod grew **899 → 2417** unique questions (1518 inserted, rest dupes).
- Established the real prod backend URL is `ilm-ai-backend-256x.onrender.com` (the un-suffixed
  one is someone else's app). Confirmed prod healthy: 72 routes / 16 router groups, protected
  routes 401/422 (no 500s), all frontend pages 200.
- Figures: OpenSAT has none (all `svg_content="null"`); real SAT is ~15-20% figures. User decided
  building figure generation is "shart emas" (not needed) for now.

### Phase 8 — IELTS platform
- Windsurf scaffolded 8 tables + 18 routes (`routers/ielts.py`) + frontend `/ielts` pages.
  Initially the grading endpoints were `# TODO` stubs (no Gemini call).
- Verified (2026-07-15) the grading is now **REAL**: `/writing/submit` + `/speaking/submit` call
  `services.gemini.generate_content(...)` with an IELTS rubric and parse JSON (with a fallback).
- Content audit found problems and Windsurf iterated: **duplicates** (10 writing = 5 unique ×2,
  etc.), passages too short (~250 words vs real 700-900), listening `audio_url`s pointing to
  non-existent files, and content mislabeled "Cambridge 16/17/18". After cleanup local has
  ~7 unique reading (proper length), real mp3s now in frontend `public/audio/listening/`, but
  still some dupes. **Prod IELTS is still empty (0 rows).**
- Created `scripts/sync_ielts_to_prod.py` to migrate local→prod (dedupe by natural key, remap
  question `parent_id`, idempotent) — NOT run yet.
- **Copyright:** user tried to upload a real Cambridge IELTS 16 Reading Test file; declined to
  publish copyrighted exam content (see policy below). Held the line; offered AI-generated
  originals instead.

### Phase 9 — New computer migration & continuity (2026-07-15)
- Pushed all 3 repos to **github.com/UMIDABDURAZZOQOV** (verified `.env` never committed — only
  `.env.example`). New machine username is **Page**; repos cloned to
  `C:\Users\Page\Desktop\Projects\`. Taught: use `git pull` not re-`clone`.
- Created this **CLAUDE.md** so any Claude on any machine auto-loads project context (feeding the
  full chat PDF into Claude Code overflowed the context window — CLAUDE.md is the right tool).
- Exported the full conversation to a personal **PDF** (`ilm-ai-suhbatlar.pdf`, 562 pages) for the
  user's own archive — not for feeding to Claude.

### Immediate next steps
1. IELTS → prod: dedupe local content, run `scripts/sync_ielts_to_prod.py`, confirm listening
   audio serves on Vercel, then generate more ORIGINAL content and verify AI grading live.
2. `services/gemini.py` round-robin load-balancing before advertising.

## ⚠️ Content policy (important)
Do NOT ingest or publish copyrighted exam material (Cambridge IELTS books, British Council
official tests, etc.) onto the platform — that is copyright infringement (true even while the
site is free; distribution is the issue, not payment). Use AI-generated ORIGINAL content in the
IELTS format, or genuinely open-licensed material. This matches the site's own "100% original
content" promise.
