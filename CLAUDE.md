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
- Frontend (prod): **https://ilm-ai-edu.vercel.app**  ← the Vercel project was renamed;
  `ilm-ai-frontend.vercel.app` is gone and now 404s, including for the audio files.
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
  A gamified, learn-then-test course for Uzbekistan's Milliy Sertifikat exam. **12 subjects, 814
  lessons, ~8200 questions** (was 253 lessons / ~2500 until 2026-07-21 — see "Syllabus depth"
  below; do NOT quote the old numbers, and do not describe the tree as a finished course while
  `fill_content.sh` still reports lessons without questions). All Gemini-generated then committed
  as static seed fixtures (never
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

### ▶ PICK UP HERE (state at end of 2026-07-22) — read this first after a context reset

**Two Cambridge books are loaded: 21 and 20.** 320 questions each, every answer keyed,
twelve passages apiece. Book 20 has **Listening and Reading only** — the edition the owner
bought prints no audioscripts and no Writing or Speaking papers, so those two are greyed out
on its cards and its overall band averages over two skills, not four.

Adding a third book is now a two-command job, and neither is edited first:

```
IELTS_BOOK=19 IELTS_PDF=<file> python scripts/parse_ielts21.py   # → scripts/seeds/ielts19.json
IELTS_BOOK=19 python scripts/seed_ielts21.py
```

Copy the recordings to `ilm-ai-frontend/public/audio/listening/` named `C19T<test>P<part>`
(`.mp3` or `.m4a`; split rips take `.1`/`.2` before the extension). The startup seeder loads
every `scripts/seeds/ielts*.json` it finds and checks each volume against its own fixture,
so a new book needs no code change here at all.

The parser handles two physical layouts and picks between them from `/Rotate`, not from the
book number: book 21 is rotated publisher typesetting, book 20 is upright and re-typeset.
**If a third book parses to green counts, still read some of the output** — the failure that
cost the most time was Test 3's Passage 2, whose thirteen questions all parsed while the
article itself came out empty, because the paper prints its questions first.

**What is NOT verified for book 20:** that each recording matches its section. They arrived
named `T1S1.m4a`…`T4S4.m4a` and were copied straight across on that reading; the durations
(6.8-9.5 min) are right for a Listening section, but nobody has listened to one against its
questions.

**Skill-tree content is DONE: 836 of 836 lessons answerable in production, 12441 questions,
all twelve subjects at 100%** (it was 253 lessons / 2526 on the morning of 2026-07-21). The
placement bank is complete too — 1797 questions covering every level of every subject, so the
level test works everywhere: 35 questions over 5 `daraja_*` levels for the academic subjects,
42 over 6 CEFR bands for the three languages.

Two checks back this, and both are scripts you can re-run:
- `python scripts/coverage_check.py` — greps *lesson* titles for ~80 required topics across all
  twelve subjects, each under several spellings. **Do not trust an LLM audit for this**:
  `scripts/audit_units.py` called 62 of 74 units complete, Matematika among them, while it had
  no calculus at all. The 14 topics this found (calculus, Archimedes, halogens, selective
  breeding, word formation, Homer, Hemingway, Korean honorifics, …) are the ones now filled.
- Lesson **order** is a teaching sequence, not the order lessons were assembled in
  (`scripts/reorder_lessons.py` → `_order` in `skilltree_outline.json` → applied by
  `scripts/apply_lesson_order.py`). 68 of 74 units were resequenced; six answers were rejected
  for not being a true permutation and those units kept their previous order untouched.

**What is NOT verified:** the wording of 12441 questions. Sampling looked good; nobody has read
them all. If a lesson reads badly, regenerate that one with
`python scripts/seed_skilltree.py --subject <slug> --regen-questions`.

`GET https://ilm-ai-backend-256x.onrender.com/skills/subjects` reports the live state with no
auth — check it before quoting any number. To add more:

```
bash scripts/fill_content.sh              # resumes; exits 3 when every key is dry
python scripts/dump_skilltree_fixtures.py # prod seeds from fixtures, NOT from the DB
git add scripts/seeds && git commit && git push   # Render auto-deploys
```

**Never edit a script a background job is executing.** The generation loop was running from a
copy in /tmp and that file was rewritten underneath it; bash reads a script incrementally, so it
hit a syntax error mid-run and the batch died silently. That is why the runner lives in the repo
as `scripts/fill_content.sh`.

**A new lesson's unit slug must exist in the spine.** Two fluid-mechanics lessons were written
into `fizika/molekulyar-issiqlik`; the real slug is `molekulyar-fizika`, and
`skilltree_taxonomy.py::_merge_expansion()` only touches units it recognises, so they vanished
without an error. Check against `[u['slug'] for u in SKILLTREE_OUTLINE[subject]['units']]` — the
guard caught the same mistake again the next day (`qadimgi-adabiyot` for `antik-adabiyot`).

**Reordering a unit needs two things that are easy to miss.** `(unit_id, order_index)` is UNIQUE,
so a unit cannot be renumbered a row at a time — the first move collides with whoever holds the
slot; park the whole unit at `10_000 + n` first, then assign the real indices. And the
prerequisite chain must be **rebuilt**, not added to, or a lesson stays locked behind one that
now comes after it. Both `scripts/seed_skilltree.py::upsert_structure` and
`services/seed_skilltree_bank.py::_upsert_structure_only` do this; they mirror each other and
must be changed together.

**Provider is switchable** (`services/llm_provider.py`, `SEED_PROVIDER`). Gemini's free tier is
~20 requests/day/key — with ten keys, ~640/day. Mistral's free "Experiment" tier
(`OPENAI_BASE_URL=https://api.mistral.ai/v1`, `mistral-large-latest`) is ~1 req/sec and was used
for the last batch; its Uzbek is good, slightly more formal in register than Gemini's. OpenAI
needs paid credit — data sharing grants free daily tokens only from usage Tier 1, which a $0
account is not, so a brand-new key answers `insufficient_quota`.

**Read "Syllabus depth and the placement test" below before answering any question about how much
content the app has.** The owner was, in their words, misled about this — CLAUDE.md recorded
"~253 lessons" accurately but the tree was presented as a complete course when a subject could be
finished in under an hour. Quote the real counts, and say plainly what is not done yet.

**The same failure showed up three times on 2026-07-21, and the shape of it is worth remembering:
a check that passes because it cannot see the thing that is wrong.** The placement test reported a
CEFR band from an uncalibrated bank; the IELTS parser printed `missing=[]` while question text was
mangled (a broken question is still a question, so the count stayed green); and two startup seeders
skipped their update because rows already existed. Whenever a check goes green here, ask what it
would fail to notice.

**A "seed only if needed" guard has now held back a correction three times** — questions that
were mangled but countable, audio URLs that were NULL, and tables on a field the check did not
look at. `services/seed_ielts21.py` compares the question count, the audio links, a sample of
question *text*, and the number of sections with a table. Extend it whenever the fixture gains a
field, or production will keep serving the old shape while everything looks green locally.

The Cambridge IELTS 21 extraction is finished, deployed and verified (details below).

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

**Cambridge IELTS 21 extraction — DONE 2026-07-21, live and verified. Do not redo it.**
The owner **has bought a licence** for the official book + audio, so ingesting them is legitimate
(this reverses the earlier "don't touch Cambridge content" stance — that only applied while there
was no licence).

The first extraction pass (by the owner's other tooling) was broken: `ielts_questions` was **0
rows**, 12 of 16 reading passages held only the 30–36-char instruction line, every transcript was
hard-cut at exactly 800 chars, speaking bullets were mojibake, `ielts_writing.task` was `None`.
**Root cause: every page of the PDF is `/Rotate 90`.** pypdf's plain `extract_text()` then emits
glyph runs in an order that interleaves columns — the answer keys came out as
`"1 10/ten 21 &22 IN EITHER ORDER"` and the audioscripts lost speaker attribution entirely.

The forensic record of what the broken first pass produced is kept in
`scripts/IELTS21_EXTRACTION_NOTES.md` (marked DONE at the top).
`scripts/parse_ielts21.py` fixes this by collecting each run with its text-matrix position and
rebuilding the lines itself: **with the rotation, `tm[4]` (x) runs *down* the page = line order,
and `tm[5]` (y) runs *across* it = column order.** Keep that in mind before touching it.
- `page_lines()` — normal pages. `page_segments()` — answer keys only; splits at bare-number runs
  that sit in a **frequent** across-page position (≥5 hits), so numeric answers like `3 250` are
  not mistaken for question numbers.
- Running heads are dropped **case-sensitively** ("Listening" is a head, "LISTENING" is the section
  heading we must keep).
- Verify with the script's own report: it must print `missing=[]` for all 8 skill/test pairs.

Result, all committed: **320/320 questions + 320/320 answer keys**, 12 passages of 750–960 words,
untruncated speaker-tagged transcripts, clean Part 1/2/3 speaking, Task 1/Task 2 writing.
- Fixture: `scripts/seeds/ielts21.json` (332 KB, committed). Regenerate with
  `python scripts/parse_ielts21.py`; load with `python scripts/seed_ielts21.py --purge-legacy`.
- **Production seeds itself**: `services/seed_ielts21.py::seed_ielts21_if_needed()` runs from
  `main.py` and reseeds whenever the question count ≠ 320 **or** any listening part lacks audio.
  (The audio check exists because an earlier fixture resolved mp3 paths by globbing the frontend's
  `public/` dir, which does not exist on Render — prod seeded 320 questions with every
  `audio_url` NULL. Paths are now baked into the JSON at parse time.)
- New column **`ielts_listening.audio_parts` (JSON)** — 9 of the 16 parts were ripped as two files
  that must play back to back. Added via `services/db.py`'s `migrate_*_columns()`, which is this
  project's real migration mechanism (**alembic/ is vestigial and is not run on Render**).
- Audio: 26 MP3s, **179 MB, committed to `ilm-ai-frontend/public/audio/listening/`** on the owner's
  explicit go-ahead after weighing repo bloat vs. external hosting. Served from Vercel's CDN.
- Known gap: Test 2 Listening Q15-20 is a **map-labelling** task whose labels live inside vector
  artwork with no text layer. Those items are emitted with `needs_figure: true` and placeholder
  text so the 1–40 numbering stays intact.

**All four IELTS pages are now wired to the API** (they previously ran on the bundled samples in
`src/lib/ielts.ts`; Listening even read its script aloud with `speechSynthesis`). Rows are grouped
into "Cambridge IELTS 21 Academic → Test 1-4" by parsing the seeder's title format via
`src/lib/cambridge.ts` — reading/listening carry the tag in `title`, speaking in `topic`, writing
in `category`. **Speaking deliberately passes no `onSubmit`**: `/ielts/speaking/submit` cannot
transcribe audio, so it would invent a band score; the recorder is for self-review only.

## Syllabus depth and the placement test — REWORKED 2026-07-21

Two things the owner found and was right about. Both are recorded here because both were
misrepresented before, not merely incomplete.

### 1. The tree was a demo presented as a course

Every unit had 3-5 lessons: **the whole of Uzbek history was 27 lessons** ("Qadimgi davr" was
four), the whole English language 22, Korean 14. A learner finished a subject in under an hour and
found nothing after it. CLAUDE.md's "~253 lessons" was numerically true, but 253 across 12 subjects
is 21 each — calling that a full course was wrong.

- `scripts/expand_taxonomy.py` asks Gemini for the lessons each unit actually needs at DTM/Milliy
  Sertifikat depth and writes **`services/skilltree_outline.json`**, which
  `skilltree_taxonomy.py` merges over the hand-authored spine at import time (`_merge_expansion()`).
  Result: **814 lessons**, 11 per unit.
- **The merge only ever APPENDS, and never reorders or renames an existing slug.**
  `UserLessonProgress` rows point at those slugs, so moving one silently repoints somebody's
  completed lesson at a different lesson. Any future expansion must keep this property.
- `scripts/fill_content.sh` is the runner: resume, then **exit as soon as a whole pass adds
  nothing**, which means every key is out of daily quota. It does not idle overnight — the
  machine is not always on.
- `scripts/dump_skilltree_fixtures.py` re-exports the fixtures straight from the DB.
  `seed_skilltree.py` only writes a subject's fixture when it *finishes* that subject, so a
  quota-stopped run leaves the committed fixtures behind the database — and **production seeds
  from the fixtures, not the database**. Run the dump before every deploy.
- `scripts/coverage_check.py` is the check that actually works: it greps *lesson* titles for each
  required topic under several spellings. Reading the seven **unit** titles of Matematika, I told
  the owner it lacked trigonometry, logarithms, progressions and vectors — all four were there as
  lessons. A unit title is a summary, and a summary cannot be checked against a syllabus. One
  keyword is not enough either: `article` misses the lesson called "Otlar va artikllar".
- `scripts/audit_units.py` and `scripts/fill_syllabus_gaps.py` ask a model the same question, and
  **it rubber-stamps** — 62 of 74 units came back "complete" including the one with no calculus.
  Useful for suggestions, never for assurance.

**Quota reality:** the Gemini free tier is ~20 requests/day/key/model. With the 10 keys in
`GEMINI_API_KEYS` that is roughly 600-800 successful calls a day; a full lesson costs 2 (theory +
questions). Adding keys scales it linearly. `_generate_round_robin` sweeps the whole ring three
times with a pause between sweeps — bailing after one sweep threw away a lesson over what was
usually a one-minute limit. `SLEEP_BETWEEN_CALLS` (env `SEED_SLEEP`, default 0.4s) replaced a fixed
3s pause between every call: with one key that mattered, with ten it only added an hour across the
~1100 calls this needed.

**Catalogue counts:** `GET /skills/subjects` returns `lesson_count` and `ready_lessons` per subject
(one grouped query each, not one per subject). `ready_lessons` counts only lessons that actually
have questions — a lesson exists in the tree as soon as the outline is merged, well before it is
answerable, and the catalogue must not claim it. **This is the quickest way to see what is really
live**, with no auth needed.

### 2. `seed_skilltree_if_empty()` meant none of this could ever ship

It returned early whenever the tree had any subject at all. Production has been seeded since July,
so **the expansion from 253 to 814 lessons would have stayed invisible there forever** no matter
how much was generated locally. It is incremental now and safe on every boot: structure upsert
creates only missing slugs, and questions/theory attach only to lessons that have none (verified: a
second run added 8 missing lessons and 0 duplicate questions). `services/seed_placement_bank.py` is
the matching loader for the placement bank, keyed on question text so a generator re-run across
several days never duplicates.

### 3. The placement test reported a level it had not measured

It drew 15 questions from the ordinary lesson bank and mapped the raw percentage onto a CEFR band
(90 → C1, 75 → B2, …). Wrong twice over:

- **The lesson bank is not calibrated.** Its `easy/medium/hard` is relative to each lesson, so a
  "hard" question in the A1 unit is still an A1 question. The test never measured CEFR at all —
  users got B2 here and B1 elsewhere, which is worse than no result.
- **One percentage cannot separate** "mastered A1, nothing above" from "half of everything".
  Answering 57% at every level scored B1 under the old rule; that is the profile of a guesser.

Now: **`PlacementQuestion`** is a separate bank whose rows are authored AT a level, with the prompt
spelling out what the band means (an A1 row asks "I ___ a student", a C1 row wants inversion after
"Only after …"). **`services/placement.py`** walks the scale bottom-up and stops at the first level
not mastered (75%), with partial credit (45%) only for the one level directly above — a high score
low down can never buy a level the learner has not shown. The 57%-everywhere learner now places A1.
The level is resolved server-side from each question's own `level` column, so a client cannot award
itself C1.

- 7 questions per level, spread across skills, so grammar alone cannot carry a level.
- Extended to **every subject**, not just the three languages: languages on CEFR **A1-C2**, the
  rest on a Milliy Sertifikat **`daraja_1`..`daraja_5`** scale (`levels_for()` picks).
- Generator: `scripts/seed_placement.py` (12 per level×skill bucket, 6 per Gemini call — a dozen
  at once blew the 60s client timeout). Fixture `scripts/seeds/placement_bank.json`.
- Frontend `components/skills/LevelTest.tsx` shows the **per-level breakdown**, because a bare
  "B2" is only believable if you can see which levels were cleared. A subject with no bank yet
  answers 404 and the dialog says "still being prepared", not "could not load".

## Session 2026-07-21/22 — what was actually done, and what it cost

Recorded in full because most of the day's work was undoing claims that had been made
without checking, and the same failure kept coming back in new clothes.

### The one pattern behind almost every bug

**A check passed because it could not see the thing that was wrong.** Five times:

| The check | What it missed |
|---|---|
| `missing=[]` from the IELTS parser | A mangled question is still a question — the count stayed green while the text lost its tail |
| "seed only if the table is empty" | Rows existed, so 253→836 lessons would never have reached production |
| Question count + audio + sampled text | `tables` was a new field; the grids never shipped |
| `order_index` written only at creation | A resequenced unit kept its old order in the database |
| Seven unit titles | Read as the syllabus; the 77 lesson titles underneath said otherwise |

When something here goes green, ask what it structurally cannot notice.

### Syllabus: 253 → 836 lessons

- `scripts/expand_taxonomy.py` filled each unit out to 11 lessons.
- `scripts/coverage_check.py` then found 14 genuinely missing topics across the twelve
  subjects; those were added by hand and generated.
- `scripts/reorder_lessons.py` + `apply_lesson_order.py` put each unit into teaching
  order. Appending had left Tarix teaching the Mongols before the Ephthalites.
- `scripts/fill_content.sh` is the runner: resumes, and **exits when every key is out
  of quota** rather than idling overnight, because the owner's machine is not always on.

### Placement test: rebuilt from scratch

It drew 15 questions from the lesson bank and mapped a percentage onto CEFR. The lesson
bank is not calibrated, so it was never measuring CEFR — users got B2 here and B1
elsewhere. `PlacementQuestion` + `services/placement.py` replace it: rows authored AT a
level, scored by walking up the scale and stopping at the first level not mastered.
A learner answering 57% at every level used to score B1; they now place A1.

### IELTS: extraction and Jumpinto parity

Every page of the PDF is `/Rotate 90`, which is what defeated the first attempt — see
the IELTS section below for the parser, the tables, and the four coordinate traps.
On the UI side: full-viewport exam, answer boxes inline where the gap is printed, the
home page as book → test → four skills, and **one band per skill over all 40 questions**
instead of a separate mark per part.

### Providers

`services/llm_provider.py` — `SEED_PROVIDER` picks Gemini or any OpenAI-compatible
endpoint. Gemini free tier ≈ 640 calls/day across ten keys; Mistral's free tier is
~1 req/sec and carried the last batches. OpenAI was tried and abandoned: its free daily
tokens require usage Tier 1, so a $0 account answers `insufficient_quota` no matter what
data-sharing is enabled.

### Deployment facts worth keeping

- **Production seeds from `scripts/seeds/*.json`, never from the local database.** Run
  `python scripts/dump_skilltree_fixtures.py` before every deploy — `seed_skilltree.py`
  only writes a subject's fixture when it *finishes* that subject.
- **Never edit a script a background job is executing.** A generation loop running from
  /tmp was rewritten underneath itself; bash reads scripts incrementally and it died
  mid-batch with a syntax error and no other sign.
- `GET /skills/subjects` returns `lesson_count` and `ready_lessons` per subject with no
  auth. Quote that, not a remembered number.

## IELTS section — must be indistinguishable from jumpinto.com

The owner's standing bar, in their words: *"men kirganimda IELTS Sectionga bu Jumpintomi
yoki Ilm ai mi deb so'rashim kerak … bitta logodan qolgan"* — opening it should be
indistinguishable apart from the logo. They send screenshots of both side by side.
**Treat every structural difference in such a screenshot as in scope, not only the one
they name.** Content is theirs to fill (*"UI/UX zo'r bo'lsa bo'ldi, materiallarni o'zim
hal qilaman"*); layout and behaviour are ours.

Done 2026-07-21:
- **`components/ielts/FullScreenExam.tsx`** — an open exam takes the whole viewport. It
  used to render inside the dashboard layout, so the 252px sidebar stayed put and the
  split view had half the width. The exam opens from page state, not a route, so the
  layout cannot know about it — hence a fixed overlay rather than a flag. Escape exits.
- **Answer boxes render inline**, where the gap is printed (`GAP_MARK` in
  `ReadingExam.tsx`), not in a column down the right edge.
- **`/sat/ielts` is a test browser**: book → card per test → its four skills, and a skill
  link carries `?test=` so the page opens that test's paper. Skills with no material are
  greyed, not hidden.
- **The four skills are NOT in the sidebar** (`app/sat/layout.tsx`, `IELTS_NAV`). A skill
  only means something inside a test; listing it separately let someone open one detached
  from any test. Sidebar is Tests / Dictionary / Score Calculator.

**Table questions — DONE.** `scripts/ielts_tables.py` is wired into `parse_ielts21.py`
(`attach_tables`), the grids ride to production in `ielts21.json` → `ielts_listening.tables` /
`ielts_reading.tables`, and `components/ielts/QuestionTable.tsx` renders a real `<table>` with
the input dropped in wherever a cell holds `[[7]]`. Three tables in this book: Listening T1P1,
Listening T2P1, Reading T2P1.

Why it needed its own extractor: **pypdf returns a whole table row as one text run** —
`"Taster day introduction to sailing £120 if booking one small groups (max"` — so the cell
boundaries are not in its output at all. pdfplumber gives per-word boxes. Four non-obvious things
came out of getting it right:
- The **first column's header is a single word**, so it never reaches the popularity threshold
  that finds the other column edges; without seeding it from the leftmost word, every left-hand
  cell collapsed into column two.
- The **dot leader interleaves with the word beside it**: `"....................a..v..a..il.a"` +
  `"ble"` is `"…… available"`. `clean_token()` strips the dots and keeps the letters.
- A gap is **"3" followed by a leader wide enough to cross into the next column**, which put the
  number in one cell and its marker in another — question 3 of Test 1 had no box anywhere. The
  pair is resolved while reading order is intact and placed in the *number's* cell.
- Matching a grid to a section must be **scoped to one skill's pages**. Listening and Reading both
  number from 1, so a Reading table matched a Listening part just as well.

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


