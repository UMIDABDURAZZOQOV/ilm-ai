# Ilm AI — Project Context (for Claude)

Multilingual (Uzbek / Russian / English) AI education platform for youth in Uzbekistan.
This repo (`ilm-ai`) is the **backend**. Companion repos: `ilm-ai-frontend` (web), `ilm-ai-flutter`
(mobile, active).

> **NOTE (2026-07-17):** the old `ilm-ai-mobile` (React Native) GitHub repo was permanently
> deleted — it is fully replaced by `ilm-ai-flutter` (public: github.com/UMIDABDURAZZOQOV/ilm-ai-flutter).
> Don't reference `ilm-ai-mobile` as an existing repo anymore; all mobile work happens in Flutter now.

> **NOTE (secrets):** never commit `.env`. Only `.env.example` is tracked. Real Gemini keys,
> DATABASE_URL, ElevenLabs, Telegram, Google/Gmail creds live in `.env` (copy it by hand onto
> each machine — it is NOT on GitHub).

## Architecture
- **Backend:** FastAPI + SQLAlchemy + uvicorn. Postgres in prod (Render); falls back to
  `sqlite:///data/ilm_ai.db` locally when the Postgres port is unreachable (`services/db.py`).
- **Frontend:** Next.js 14 (App Router, TS, Tailwind) → Vercel, auto-deploys from GitHub `main`.
  `NEXT_PUBLIC_API_URL` is baked into the bundle at build time.
- **Mobile:** Flutter (`ilm-ai-flutter`) — full rewrite, replaces the React Native app. Riverpod +
  go_router + dio. The old `ilm-ai-mobile` (React Native/Expo) GitHub repo no longer exists (deleted
  2026-07-17); Flutter is the only mobile codebase now.
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
- **Mobile** — **fully rebuilt in Flutter** (`ilm-ai-flutter`), replacing the old React Native
  app (its GitHub repo, `ilm-ai-mobile`, was deleted 2026-07-17). Full 27-screen parity: auth, dashboard, chat, AI
  assistant + Live Voice, quiz, knowledge base, math solver (camera + CustomPainter graph plot),
  college explorer (bell-curve chart), learning plan, knowledge gaps, subscription, Telegram
  linking, settings (theme/language), profile w/ avatar pipeline. Riverpod + go_router + dio
  (queued token-refresh interceptor) + flutter_secure_storage. Push notifications wired via
  `firebase_messaging` on an additive FCM branch in `services/push.py` (Expo path untouched).
  (Launch paused — web is the priority; the migration itself is done.)
  **Scope note: SAT and IELTS are web-only, intentionally NOT in mobile** (neither the old RN app
  nor the new Flutter app) — those platforms live exclusively in `ilm-ai-frontend`. Mobile's
  "college explorer" shows SAT *score stats* (bell curve, accepted-range) as reference data for
  college research, which is not the same as the SAT practice/exam platform.
- **Milliy Sertifikat Skill Tree (Duolingo-style)** — the newest and biggest addition (2026-07-18).
  A gamified, learn-then-test course for Uzbekistan's Milliy Sertifikat exam. **12 subjects, ~253
  lessons, ~2500+ questions**, all Gemini-generated then committed as static seed fixtures (never
  live-generated at request time). Subjects (slug → display): `ona_tili` (Ona tili), `matematika`,
  `ingliz_tili`, `biologiya`, `kimyo`, `fizika`, `jahon_tarixi` (Jahon tarixi / World History),
  `tarix` (O'zbekiston tarixi — note: slug is `tarix` but it's Uzbekistan history specifically;
  world history is the separate `jahon_tarixi`), and (added 2026-07-18, +65 lessons / ~648 Q)
  `ozbek_adabiyoti` (O'zbek adabiyoti), `jahon_adabiyoti` (Jahon adabiyoti / World Literature),
  `koreys_tili` (Koreys tili / Korean), `fransuz_tili` (Fransuz tili / French). **Seeder note:** on
  Windows run the seeder with `PYTHONIOENCODING=utf-8` (+`SEED_GEMINI_MODEL=gemini-flash-lite-latest`
  for speed) or its progress `print()`s crash on non-cp1251 chars (Korean/French) — generation is
  resumable, so re-running fills gaps and re-dumps the fixture. Each lesson = **theory cards first** (Duolingo
  "teach-then-test": the `SkillLesson.theory` JSON column holds hand-shaped teaching cards) **then
  10 MCQs GROUNDED in those cards** (the seed prompt embeds the theory so questions never test
  un-taught material). Backend: `routers/skills.py` (all `/skills/*` endpoints), `services/
  skill_tree.py` (lock/unlock via `SkillLessonPrerequisite`, computed at read time, no stored
  state), `services/skilltree_taxonomy.py` (hand-authored unit/lesson structure — add a subject
  here then run the seeder), `scripts/seed_skilltree.py` (Gemini gen w/ round-robin across all keys
  + `--regen-questions` + `SEED_GEMINI_MODEL` override — used `gemini-flash-lite-latest` when
  `gemini-2.5-flash` hit 503/quota), `services/seed_skilltree_bank.py` (loads committed fixtures on
  startup, wired in `main.py`). New tables: `SkillSubject/Unit/Lesson/LessonPrerequisite/Question/
  UserLessonProgress/SkillLessonAttempt/SkillMistake/SkillDailyChallenge`. **Hearts were built then
  removed** per product decision (no lives gate; XP/stars/streak only). Engagement features (all
  reuse the committed question bank → **zero API cost at runtime**): daily challenge (once/day,
  deterministic per user+day), mistakes notebook (`SkillMistake`, auto-recorded on wrong answers,
  resolved when finally correct), lightning round (60s timer), weekly leaderboard, derived
  achievements (16 tiers, computed on the fly), share card (canvas PNG → Telegram), **referral**
  (`User.referral_code`/`referred_by`, +50 XP both sides), **league tiers** (Bronza→Kumush→Oltin→
  Olmos, derived from weekly XP — NOT cohort-batched), **profile/stats** (per-subject progress,
  strongest/weakest, 84-day activity heatmap), **marathon** (30 Qs from one subject, exam-pressure).
  Daily-goal ring (20 XP). Telegram evening streak-saver nudge added to `services/scheduler.py`
  (19:00 Tashkent, direct Bot API call). Web UI: `src/app/dashboard/skills/SkillsDashboard.tsx`
  (the hub) + `src/components/skills/*` + immersive lesson route `src/app/skills/session/
  [lessonId]/page.tsx` + standalone `/skills` page; own owl **mascot** (canvas-drawn). Also on the
  Flutter app (`lib/features/skills/`). Landing page has a "Milliy Sertifikat" feature card + the
  top platform switcher lists it. **As of 2026-07-18 the full suite (engagement + mock/class/parent
  + AI tutor) is on Flutter too** — see the "Flutter port" section below.
- **Deployed:** backend on Render (`ilm-ai-backend`, see URL above), frontend on Vercel
  (auto-deploy from `main`), Postgres on Render. Telegram bot runs as its own process.
  Frontend prod domain is now **https://ilm-ai-edu.vercel.app** (Vercel project renamed
  `ilm-ai-frontend` → `ilm-ai`; old `ilm-ai-frontend.vercel.app` domain removed). **ALLOWED_ORIGINS
  on Render must include `https://ilm-ai-edu.vercel.app`** or new-domain API/login calls hit CORS.

## Milliy Sertifikat — mock exam, class mode, parent dashboard (BUILT 2026-07-18)
All three of the priority features below are now built (web + backend). Zero extra Gemini cost —
they reuse the committed question bank and existing progress tables. New tables are brand-new so
`Base.metadata.create_all()` picks them up with no migration.
1. **Mock exam + score prediction** (`routers/mock_exam.py`, prefix `/skills`, tables
   `skilltree_mock_exams`). Per-subject, 30 Qs, 30-min timer, **server-graded** (client never sends
   a score — start returns questions WITHOUT answers; complete compares to `correct_answer`).
   Percentage → DTM-style certificate grade (A+ ≥93, A ≥85, B+ ≥78, B ≥70, C+ ≥65, C ≥60, else
   "Sertifikatsiz"; 60% = certificate floor — clearly labelled as a mock scale, not the official DTM
   table). **Prediction** blends latest mock % (0.5) + avg past mocks (0.3) + lesson mastery (0.2),
   with a low/medium/high confidence from evidence count. Endpoints: `GET /skills/{uid}/mock-exam?
   subject=`, `POST /skills/mock-exam/start`, `POST /skills/mock-exam/{id}/complete` (returns grade,
   certificate bool, prediction, per-question review). Web: `components/skills/MockExam.tsx`
   (overview → timed runner → grade + prediction + review), dashboard card "Sinov imtihoni" →
   subject pick → exam.
2. **Teacher / class mode** (`routers/classes.py`, prefix `/classes`, tables `skilltree_classes`,
   `skilltree_class_members`, `skilltree_class_assignments`). Any user can open a class (becomes its
   teacher) and share a 6-char join code; students join; teacher sees a live roster (each student's
   lessons done / weekly XP / streak / active-today, from `services/skill_stats.py::student_row`) and
   assigns homework (subject or lesson). No global "teacher" role — identity is the JWT. Endpoints:
   `POST /classes`, `GET /classes/mine`, `POST /classes/join`, `POST /classes/leave`,
   `GET /classes/{id}` (teacher-only roster+assignments, 403 otherwise), `POST /classes/{id}/assign`,
   `DELETE …/assignments/{aid}`, `DELETE …/members/{sid}`, `DELETE /classes/{id}` (archive). Web:
   `components/skills/ClassMode.tsx`, dashboard card "Sinf rejimi".
3. **Parent dashboard** (`routers/parent.py`, prefix `/parent`, tables `skilltree_family_codes`,
   `skilltree_parent_links`). A student generates a stable 6-char family code (`GET /parent/my-code`);
   a parent redeems it (`POST /parent/link`) to get READ-ONLY view of the child's XP/streak/lessons/
   strongest+weakest subject/activity heatmap (`services/skill_stats.py::student_detail`). Endpoints
   also: `GET /parent/children`, `GET /parent/child/{id}` (403 if not linked), `POST /parent/unlink`.
   Guards self-link. Web: `components/skills/ParentDashboard.tsx` (parent's children + the child's own
   shareable code in one screen), dashboard card "Ota-onalar uchun".
- Shared: `services/skill_stats.py` — `student_row` (compact) / `student_detail` (full, with 84-day
  activity + strongest/weakest), reused by both class roster and parent view so numbers match the
  learner's own Profile screen. All three registered in `main.py`. Verified end-to-end via curl with
  minted JWTs (mock start→grade→predict; class create→cross-user join→roster→assign→403; parent
  code→link→children→self-link 400). **Now also ported to Flutter** (see the "Flutter port" section).

## In-lesson AI tutor (AI repetitor) — BUILT 2026-07-18
On-demand only. `routers/tutor.py` (`POST /skills/tutor/explain`, prefix `/skills`). When a learner
gets a question WRONG, a "🤔 Tushuntirib ber" button appears in the feedback; tapping it calls
Gemini (`gemini-flash-latest`, plain text) for a short, warm, `lang`-aware explanation that says why
the correct answer is right and gently corrects the wrong pick. NOT called per question, so API cost
stays low; the fetched explanation is cached in component state. Body: `{question_text, options,
correct_answer, user_answer, lang}` → `{explanation}`; graceful 502 `tutor_unavailable` on failure.
Web: `components/skills/AiTutor.tsx`, wired into the lesson session page, `PracticeSession` (daily/
mistakes/marathon — not lightning, which has no feedback pause), and the mock-exam review list.
Verified live (returned a correct Uzbek explanation).

**Extended platform-wide 2026-07-18:** the same `/skills/tutor/explain` endpoint + `AiTutor.tsx`
component are now reused OUTSIDE Milliy Sertifikat — on wrong answers in **IELTS Reading**
(`src/app/ielts/reading/page.tsx`), **IELTS Listening** (`src/app/ielts/listening/page.tsx`), and the
**SAT session results review** (`src/app/sat/session/page.tsx`). (SAT Bluebook practice already had
its own richer *conversational* tutor via `askAssistant`, so it was left as-is.) The endpoint is
generic — it just needs question/options/correct/user-answer/lang — so no backend change was needed;
verified live on a SAT-style algebra question (it correctly diagnosed picking 3x instead of x).
SAT/IELTS are web-only (no Flutter features), so this is a web-only extension.

## Premium UI redesign + interactive libraries (web, 2026-07-18)
Owner wanted the whole web app to feel premium/animated like top ed-tech sites (OnePrep-inspired for
SAT/IELTS/College, Duolingo-inspired for Milliy Sertifikat). **Boundary agreed with owner:** no
copying of any logos/mascots/illustrations/marketing copy — all illustrations & animations are drawn
from scratch (SVG/CSS/framer-motion), Ilm AI keeps its own brand/logo; only the *layout & interaction
patterns* are the inspiration. What was built:
- **Reusable UI kit** `src/components/ui/premium.tsx` — `PremiumCard` (entrance + hover-lift),
  `StatCard` (count-up stat tile), `ProgressRing` (animated SVG ring), `CountUp` (in-view count-up),
  `SectionTitle`. This is the shared design language — use it when upgrading any remaining screen.
- **Screens rebuilt with the kit:** `src/app/sat/page.tsx` (countdown + predicted-score ring +
  animated analytics + hover practice cards), `src/app/ielts/page.tsx` (band ring + gradient skill
  cards + count-up stats), `src/app/sat/college/page.tsx` (selectivity tier chips + acceptance bars +
  hover-lift + auto-animate filtering). `src/app/dashboard/page.tsx` got a light, safe pass (stat
  cards animate in — the file is 2600+ lines so it was NOT fully rebuilt).
- **Animated landing** `src/app/page.tsx`: `src/components/landing/ProductDemos.tsx` (4 tabbed,
  self-playing interactive demos — SAT question+score, IELTS band dial, College cards, Milliy
  skill-tree) and `src/components/landing/ParticleBackground.tsx` (interactive hero particles).
- **Confetti** `src/components/skills/Confetti.tsx` — dependency-free celebration on lesson
  completion (1+ star) and mock-exam certificate results.
- **New npm deps (all MIT, config is ours):** `react-parallax-tilt` (3D card tilt on landing
  features), `@tsparticles/react`+`@tsparticles/slim` (hero particle field — **v4 API**: wrap in
  `ParticlesProvider init={...}`, gate render on `useParticlesProvider().loaded`, NOT the old
  `initParticlesEngine`), `@formkit/auto-animate` (smooth college-grid filtering).
Local dev run: backend `python -m uvicorn main:app --port 8000`, web `npm run dev` (localhost:3000).
Remaining screens (SAT bank/analytics/vocab/mock, IELTS sub-pages) not yet upgraded — apply the kit.

## Site-wide theme toggle + responsive fixes (web, 2026-07-18)
- **Dark/light toggle everywhere:** new `src/components/ThemeToggle.tsx` (sun/moon button on
  `useTheme().setThemeMode`) added to the landing nav (always visible, beside the hamburger), the
  dashboard header, the SAT/IELTS/College layout mobile top bar, and login/signup. Previously the
  theme was only changeable in settings.
- **Responsive navbar fix:** the landing nav wrapped into a broken multi-row on tablets. Fixed in
  `globals.css`: `.nav`/`.nav-links` set to `flex-wrap: nowrap`, and the mobile-hamburger media
  query raised from `max-width: 900px` → `1024px` so all tablets get the clean hamburger. Note the
  dashboard has its OWN Tailwind responsive system (`md:hidden`, 768px) — independent of that media
  query; the `.dash-layout`/`.sidebar` rules in globals.css are legacy/unused.
- **Global overflow guards** in `globals.css`: `body { overflow-x: hidden; max-width: 100vw }`,
  `img/video/canvas/svg { max-width: 100% }`, `* { min-width: 0 }` — nothing forces horizontal scroll.

## Deployment (state as of 2026-07-18)
All three repos pushed to GitHub `main` (owner: `UMIDABDURAZZOQOV/{ilm-ai, ilm-ai-frontend,
ilm-ai-flutter}`). **Frontend** auto-deploys to Vercel; live prod domain is **`ilm-ai-edu.vercel.app`**
(also `ilm-ai.vercel.app`; the old `ilm-ai-frontend.vercel.app` is DEAD/404). **Backend** auto-deploys
to Render; the real service URL is **`https://ilm-ai-backend-256x.onrender.com`** (NOT
`ilm-ai-backend.onrender.com` — that's a different/old service). Verified live: `/health` ok, all
**12 subjects** served, CORS already allows `ilm-ai-edu.vercel.app`. Two prod-only gotchas handled/known:
- **Postgres schema:** Render's start command doesn't run Alembic and `create_all()` never ALTERs
  existing tables, so new `users` columns (xp_total/referral_code/referred_by) wouldn't appear on
  prod. Fixed with `services/db.py::migrate_postgres_columns()` (idempotent `ADD COLUMN IF NOT
  EXISTS`, runs every startup). Add future prod column changes there too.
- **Google OAuth `redirect_uri_mismatch`:** the frontend sends `redirect_uri =
  <origin>/auth/google-callback`, which must be registered EXACTLY in Google Cloud Console → OAuth
  client → Authorized redirect URIs (+ origin in Authorized JavaScript origins). When the domain
  changed to `ilm-ai-edu.vercel.app`, the console still only had the old dead domain → login broke.
  Fix is console-only (owner action): add `https://ilm-ai-edu.vercel.app/auth/google-callback` etc.
- **Seeding caveat:** `seed_skilltree_if_empty()` only seeds when `SkillSubject` is empty; if prod
  already had subjects, newly-added ones won't auto-load and need a manual sync.
- **SAT question bank returned 500 on prod:** same root cause as the users table — `sat_ielts_questions`
  was missing columns added after its table was first created (`skill`, `image_url`, `rubric`, `tags`,
  `source_filename`, `created_by`), and a single missing mapped column makes the whole SELECT fail.
  Fixed by adding those `ADD COLUMN IF NOT EXISTS` statements to `migrate_postgres_columns()`. Verified
  live: SAT bank now serves 500+ questions (IELTS ~20). **Rule of thumb:** any new column on a
  pre-existing table must be added to `migrate_postgres_columns()` or prod breaks.

### Email verification (prod) — Render blocks SMTP
- **Root cause:** Render's free tier blocks outbound SMTP ports (25/465/587), so Gmail SMTP fails on
  prod with `[Errno 101] Network is unreachable` (works locally). Diagnosed via a temporary
  `GET /auth/_diag/email` endpoint (reports provider-config booleans + password length + attempts a
  self-send, no secrets exposed — **remove it once email is sorted**).
- **Fix:** `services/email.py` now tries providers over HTTP (port 443, not blocked): **Brevo**
  (`BREVO_API_KEY`, `BREVO_FROM_EMAIL` defaults to `GMAIL_ADDRESS`; free ~300/day, single-sender
  verification, no domain needed — but its signup wants phone SMS which is flaky for +998) → **Resend**
  (`RESEND_API_KEY`; no phone, but needs a verified domain to send to arbitrary recipients) → **Gmail**
  SMTP (only works off-Render). Owner sets one provider's env vars on Render.
- **Brevo WAS wired up (2026-07-20)** — `BREVO_API_KEY` set on Render, sender `yaktusecho9@gmail.com`
  verified in Brevo, `/auth/_diag/email` returned `brevo_send: ok`. But it **does not deliver**: the
  Brevo event log shows Gmail **deferring** every message — `421-4.7.28 ... mail from your domain
  [brevosend.com] has been temporarily rate limited ... Bulk Email Senders Guidelines`. Root cause is
  the **freemail sender**: you can't SPF/DKIM-align a `gmail.com` from address on a shared IP, so
  Google rate-limits/soft-bounces it. **No config fixes this — it needs a real sending domain.**
- **Decision (2026-07-20): verification turned OFF** — `REQUIRE_EMAIL_VERIFICATION=false` on Render.
  `/auth/signup` auto-verifies + returns tokens immediately (no code); login stops blocking unverified
  users. The frontend "we'll send a 6-digit code / check spam" notices on `signup/page.tsx` and
  `login/page.tsx` were **removed** (commits on `ilm-ai-frontend@main`), but the i18n keys
  (`signup_verify_note`, `login_verify_note`), the `verify-email` page, and the whole backend flow are
  **kept intact** — nothing was deleted, only disabled.
- **To re-enable (when a domain exists):** authenticate a domain (SPF+DKIM) in Brevo/Resend, set
  `BREVO_FROM_EMAIL=noreply@thatdomain` (+ `RESEND_*` if using Resend), flip
  `REQUIRE_EMAIL_VERIFICATION=true`, and re-add the two note boxes on signup/login. The owner already
  owns `vakil-ai.com` (DNS currently broken — nameservers at IRANDNS don't answer); fixing that DNS +
  authenticating it is the zero-cost path.

### Session 2026-07-20 — localhost run, navbar polish, verification turned off
Switched over from the Vakil AI work to Ilm AI. Everything below was done this session.

**Running it locally (both halves):**
- Frontend: `cd ilm-ai-frontend && npm run dev` → http://localhost:3000 (Next 14). `node_modules`
  already present; `.env.local` has `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`. Harmless
  `Invalid Sentry Dsn` warning (placeholder DSN) — ignore.
- Backend: `cd ilm-ai && python -m uvicorn main:app --host 127.0.0.1 --port 8000`. The **global**
  Python 3.12 already has fastapi/uvicorn/sqlalchemy, so **no venv needed** (the `start_backend.ps1`
  points at a `.\venv` that doesn't exist — just call the module). `.env` `DATABASE_URL` targets a
  local Postgres that isn't running, so the backend **auto-falls back to SQLite** ("PostgreSQL is not
  available. Falling back to SQLite database...") — fine for local UI work; data is fresh/empty.

**Mobile navbar fixes** (`ilm-ai-frontend`, `globals.css` + `app/page.tsx`, deployed):
- The open mobile menu looked transparent (hero showed through). Cause: `.nav-sticky` has
  `backdrop-filter: blur(16px)`, which makes `position: fixed` on its descendant `.nav-links.mobile-open`
  resolve against the ~60px bar (its containing block), so `bottom:0` collapsed the overlay. Fix:
  `height: 100dvh` + an opaque premium background (solid `var(--bg)` + brand radial glows + blur) +
  `padding-top` to clear the logo/close button; the close (X) button got `position: relative` so its
  `z-index:101` actually applies (stays tappable above the overlay).
- The bar scrolled away instead of staying pinned — `position: sticky` was broken by an
  `overflow-x:hidden` ancestor. Changed `.nav-sticky` to **`position: fixed`** and added
  `pt-[72px]` on the page-root wrapper to offset its height.
- The page scrolled behind the open menu. Added a **scroll-lock**: a `useEffect` sets
  `document.body.style.overflow = "hidden"` while `mobileMenuOpen` (restores on close).

**Backend behavior change** (`routers/auth.py`, deployed): an unverified login (403 `email_not_verified`)
now calls `issue_code(...)` first, so the `/verify-email` screen the frontend redirects to always has a
fresh code (the signup one may have expired). `issue_code` is rate-limited, so this can't spam. Harmless
while verification is off (that branch never runs).

**Email verification:** wired Brevo, found it undeliverable from a gmail freemail sender, turned
verification OFF — full detail in the "Email verification" section above.

**Deploy mechanics (this project):** both repos auto-deploy from `main`.
- Frontend repo `ilm-ai-frontend` → Vercel project **`ilm-ai`** (`prj_…`, owner account
  `pubgmobile200820102009@gmail.com`) → **`ilm-ai-edu.vercel.app`**. `git push origin main` triggers it.
- Backend repo `ilm-ai` → Render service **`ilm-ai-backend`** (`srv-d99id4mcjfls738a8l80`) →
  **`https://ilm-ai-backend-256x.onrender.com`**. `git push origin main` triggers a build; but an
  **env-var change via the Render API does NOT auto-deploy** — you must POST a deploy
  (`/v1/services/<id>/deploys`) for it to take effect.
- Doc-only commits (like this CLAUDE.md) are committed but **not pushed alone** — pushing the backend
  repo forces a full Render rebuild, so let doc commits ride along with the next real backend change.
- Driven this session with the owner's **Render API key** (`rnd_…`) and **Vercel token** (`vcp_…`) —
  revoke them when CLI/API access is no longer wanted.

### Session 2026-07-21 — bug fixes, skill-tree gating, language level test, IELTS UI

**Bugs found & fixed**
- **Flashcards were 500-ing** (`routers/quiz.py`) and so was AI question generation
  (`services/question_bank.py`): both did `from services.quiz_engine import client`, but
  `quiz_engine` no longer defines `client` (it was refactored onto `services/gemini.py`). The
  runtime `ImportError` surfaced as "Kartochkalarni generatsiya qilib bo'lmadi". Both now call
  `services.gemini.generate_content` (multi-key rotation + timeout). **Rule: never import a raw
  Gemini `client` — always go through `services/gemini.py`.**
- **Everything looked "static"** — `apiFetch` (frontend `lib/api.ts`) had no cache control, so the
  browser replayed cached GETs (e.g. `/gaps/report/<id>`); freshly finished quizzes only appeared
  after a manual refresh. Fixed with `cache: "no-store"` on both fetch calls.

**Skill tree (Fanlar) — progression rules**
- **Star tiers + pass mark** (`routers/skills.py`): `STAR3_PCT=90 / STAR2_PCT=80 / STAR1_PCT=60`,
  `PASS_THRESHOLD_PCT = STAR1_PCT`. On a 10-question lesson: 10-9 → 3⭐, 8 → 2⭐, 7-6 → 1⭐, ≤5 → fail.
  `passed = stars >= 1`. **Failing no longer completes the lesson**, so the next node stays locked and
  the session screen says "yana bir marta o'rganing". An already-completed lesson is never downgraded.
- **Unit checkpoint exam** — new `UserUnitExam` table + `GET /skills/{id}/unit-exam?unit_id=` and
  `POST /skills/unit-exam/complete` (15 Q drawn from every lesson in the unit, 60% to pass, +50 XP).
  `services/skill_tree.py::build_tree` now gates each unit behind the previous unit's exam
  (`gate_open`), exposes `unit.exam.status` (`none|locked|unlocked|passed`), and **deliberately does
  not retro-lock** anyone who already has progress inside a unit (`started_here`).
- Renamed the section **"Milliy Sertifikat" → "Fanlar"** across nav, dashboard, marquee and i18n.

**Language placement test** — new `UserLanguageLevel` table, `GET /skills/{id}/level-test?subject=`
(15 Q sampled across easy/medium/hard) + `POST /skills/level-test/complete`. CEFR mapping
90/75/60/40 → C1/B2/B1/A2/A1. Only for `ingliz_tili | koreys_tili | fransuz_tili`; the card appears
above the path on those subjects.

**IELTS — full exam UI rebuilt (frontend), content deliberately NOT included**
Modelled on the UX of jumpinto.com. New under `ilm-ai-frontend/src/components/ielts/`:
`ReadingExam` (split pane, MCQ/TFNG/YNNG/completion/matching/heading, grouped instructions, guided
highlight, localStorage autosave, Answer-Keys drawer with My/Correct + band), `ListeningExam`
(audio + collapsible speaker-tagged audioscript), `WritingExam` (boxed prompt, figure, live word
count, Submit-for-Feedback, 4-criteria bands, sample answer), `SpeakingExam` (cue card +
MediaRecorder + timer), `ExamShell` (bottom `Listening · 1 · 2 · 3 · Writing · Speaking` nav) and
`TestBrowser` (book → test cards with band chips). `src/lib/ieltsBand.ts` holds the official
raw→band tables (Listening and Academic Reading differ) and IELTS rounding (.25/.75 round up).
- **Wired so far:** `/sat/ielts/reading` (uses the bundled sample passages) and the new
  `/sat/ielts/dictionary`. Listening/Writing/Speaking pages are **not wired yet** — their grading
  endpoints need a real `task_id` and `ielts_writing/listening/speaking` are still empty, so wiring
  them now would ship a button that 500s. Seed those tables first.
- **New `routers/vocab.py`** — IELTS dictionary: `GET /vocab/define` (free dictionaryapi.dev, i.e.
  Wiktionary data — deliberately not a commercial dictionary), `GET /vocab/examples` (sentences
  mined from OUR OWN passages/transcripts), and starred words (`UserStarredWord`,
  `GET /vocab/{id}/starred`, `POST|DELETE /vocab/starred`).

> **Content note (important, decided with the owner):** the IELTS *interface* is modelled on
> jumpinto.com, but its **content is Cambridge IELTS 18–21, which is copyrighted** and hosted there
> without a licence. We did **not** copy, scrape or ingest any of it, and repeated requests to do so
> (including via uploaded PDFs) were declined — for a startup applying to UzCombinator that is a
> deal-breaking IP risk. The owner will source content himself (licence from Cambridge, own
> item-writers, or openly-licensed texts). Every component above is content-agnostic and matches the
> DB shape, so licensed material drops straight in.

### ▶ PICK UP HERE (state at end of 2026-07-21) — read this first after a context reset

**Everything below in this session is already committed AND deployed AND verified live.**
- Backend `ilm-ai@main` → Render `ilm-ai-backend` (`srv-d99id4mcjfls738a8l80`) →
  https://ilm-ai-backend-256x.onrender.com — deploy `live`, `/health` 200, `/vocab/define` 200.
- Frontend `ilm-ai-frontend@main` → Vercel project `ilm-ai` → https://ilm-ai-edu.vercel.app —
  `Ready`, `/` and `/sat/ielts` both 200.
- Both repos push to `main` and auto-deploy. A Render **env-var change does NOT auto-deploy** —
  POST `/v1/services/<id>/deploys` afterwards.
- Owner-supplied credentials were used this session: Render API key `rnd_…`, Vercel token `vcp_…`,
  Brevo key `xkeysib-…`, Gemini key. They still work; tell the owner to revoke when done.
- Local dev during the session: frontend `npm run dev` (:3000), backend
  `python -m uvicorn main:app --port 8000` (global Python 3.12, no venv; Postgres unreachable →
  auto SQLite fallback, so local IELTS/skill data is the SQLite copy, not prod).

**THE ONE OPEN TASK: Cambridge IELTS 21 content extraction.**
The owner **has bought a licence** for the official book + audio, so ingesting them is legitimate
(this reverses the earlier "don't touch Cambridge content" stance — that only applied while there
was no licence). A first extraction pass was done by the owner's other tooling and **it is broken**:
`ielts_questions` is **0 rows**, 12 of 16 reading passages contain only the 30–36-char instruction
line, every listening transcript is hard-cut at exactly 800 chars, speaking bullets are mojibake
(`�`), and `ielts_writing.task` is `None`. Audio is the one good part: 26 MP3s in
`ilm-ai-frontend/public/audio/listening/` and all 16 listening rows link to them.

**Full details, source paths, PDF page map and the rewrite plan are in
`scripts/IELTS21_EXTRACTION_NOTES.md`** — open that file first, it is written for exactly this
situation. Short version: book is `C:/Users/Page/Downloads/IELTS_21.pdf` (146 pages, clean text
layer), only `pypdf` is installed, and questions must be extracted first because nothing works
without them.

**Frontend is ready and waiting for that content:** `src/components/ielts/` holds `ReadingExam`,
`ListeningExam`, `WritingExam`, `SpeakingExam`, `ExamShell` + `TestBrowser`, and
`src/lib/ieltsBand.ts` has the official raw→band tables. `/sat/ielts/reading` (on bundled samples)
and `/sat/ielts/dictionary` are wired; **Listening / Writing / Speaking pages are intentionally NOT
wired** because their grading endpoints need a real `task_id` and the tables are still wrong —
wire them only after the re-extraction lands.

### Test-mode notice
- Frontend: `components/TestModeBanner.tsx` — slim dismissible amber bar at the top of every page
  (rendered in `app/layout.tsx`, uz/ru/en, sessionStorage-dismissed). Backend: root `/` returns a
  `status: test_mode` + `warning` field. Remove both when the site leaves test mode.

## Flutter port of the full skill-tree suite — BUILT 2026-07-18
The whole Milliy Sertifikat suite is now on the Flutter app too (`ilm-ai-flutter`), not just web.
New data layer: `lib/features/skills/data/skill_extras_models.dart` (DTOs for practice/mock/class/
parent/profile/league/referral/leaderboard/achievements) + `skill_extras_repository.dart`
(`skillExtrasRepositoryProvider`, every `/skills`, `/classes`, `/parent` endpoint incl. the AI
tutor). `GamificationSummary` gained `todayXp`/`dailyGoalXp`. New screens under
`lib/features/skills/presentation/`:
- `skills_hub_screen.dart` — replaces the old plain subject picker at route `/skills`: daily-goal
  bar + 8-subject grid + 11 feature cards (daily/mistakes/lightning/marathon/mock/leaderboard/
  referral/profile/achievements/classes/parent). Marathon & mock open a subject-pick bottom sheet.
- `skill_practice_screen.dart` — one runner for daily/mistakes/lightning(60s timer)/marathon, with
  inline AI tutor on wrong answers.
- `ai_tutor_widget.dart` — the on-demand "🤔 Tushuntirib ber" button (calls `/skills/tutor/explain`).
- `mock_exam_screen.dart` (overview→timed runner→grade+prediction+review), `class_mode_screen.dart`
  (+ `ClassDetailScreen` roster/assignments), `parent_dashboard_screen.dart`, `skill_profile_screen.dart`
  (12-week heatmap + per-subject bars), `skill_leaderboard_screen.dart`, `skill_achievements_screen.dart`,
  `skill_referral_screen.dart` (Telegram share via url_launcher).
- `skill_ui.dart` — shared helpers: `str3(lang,uz,ru,en)` trilingual inline strings (no new i18n
  keys), `skillColor`, `gradeColor`, `subjectIcons` (all 8 slugs).
Routes wired in `core/router/app_router.dart` under `/skills/*` (practice, marathon, mock, classes,
parent, profile, leaderboard, achievements, referral). `flutter analyze` clean (only the pre-existing
quiz_repository.dart info-lint). Not yet driven on a device/emulator — backend endpoints already
verified via curl; mobile UI is a manual smoke-test away.

## Milliy Sertifikat — planned next (not built yet)
Lower priority / later: streak-freeze mechanic, PWA/installable/offline, deeper Telegram
(daily-challenge inside the bot), and a premium/monetization tier.

## Status (as of 2026-07-18)
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

### Phase 10 — Mobile: full React Native → Flutter rewrite (2026-07-16)
- User decided to fully replace `ilm-ai-mobile` (React Native/Expo) with a new Flutter app,
  `ilm-ai-flutter`, going forward. Reason: liked Flutter's animation consistency / no-JS-bridge
  model; the RN app itself had no blocking defect. Old repo kept untouched as reference/fallback.
- Rebuilt all **27 screens** with full feature parity, phase by phase (scaffold+nav shell → auth
  → core tabs → 9 flagged high-complexity screens → platform config/notifications/QA), verified
  live against the real backend on an Android emulator at every phase, not just `flutter analyze`.
- Stack: Riverpod (non-codegen), `go_router` (`StatefulShellRoute.indexedStack` for the 6 bottom
  tabs), `dio` with a queued/deduped token-refresh interceptor, `flutter_secure_storage` (upgrade
  from RN's plaintext AsyncStorage), `freezed` for auth DTOs, `CustomPainter` for all charts (math
  function plot, dashboard sparkline, SAT bell curve) — no charting library, matching RN's
  hand-rolled SVG approach.
- Ported `theme.ts`/`i18n.ts` (328 keys)/`colleges.ts` (44 curated entries) via one-off Node.js
  scripts that `eval()`'d the JS literal and emitted the Dart/JSON, instead of manual transcription
  — eliminates a whole class of silent porting bugs.
- **One backend change**, additive only: `services/push.py` gained an FCM-sending branch
  (`firebase-admin`) alongside the existing Expo path, since a plain Flutter app can't obtain an
  Expo push token. `requirements.txt` gained `firebase-admin`. Token-register endpoint unchanged.
- Deliberately dropped native file-picker (`file_picker`) after an extended AGP9/Kotlin-built-in
  toolchain incompatibility (documented battle in the Flutter repo's own history) — Knowledge Base
  upload is text-paste-only in the Flutter app for now. Everything else has full parity.
- Fixed a real bug found only via live testing (not static analysis): `QuizSessionScreen` crashed
  with a `RangeError` when the backend returned `{"error": ...}` with no `questions` key.
- Final QA pass caught and fixed one parity gap: `TelegramScreen` had several strings hardcoded in
  English where RN used inline uz/ru/en ternaries (and was missing RN's "what can the bot do?"
  command list entirely) — rewritten to match RN exactly, verified on-device.
- **Result: migration complete**, `flutter analyze` clean project-wide. Remaining item is external,
  not a code gap (see Open items below).

### Immediate next steps
1. IELTS → prod: dedupe local content, run `scripts/sync_ielts_to_prod.py`, confirm listening
   audio serves on Vercel, then generate more ORIGINAL content and verify AI grading live.
2. `services/gemini.py` round-robin load-balancing before advertising.
3. Flutter push notifications can't be tested end-to-end until real Firebase project files are
   supplied: `google-services.json` (Android), `GoogleService-Info.plist` (iOS), and a
   service-account JSON path set as `FIREBASE_SERVICE_ACCOUNT_PATH` on the backend. Everything is
   wired and waiting — this is a credentials gap, not missing code.


