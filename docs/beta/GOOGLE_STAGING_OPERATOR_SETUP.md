# Google OAuth — yangi bepul staging uchun operator qadamlari

Staging: https://ilm-ai-103-stage-8b0727.onrender.com

## 2026-11-08 — configured, two real accounts accepted

Real HTTPS staging on Samsung SM-A125F now accepts two owner-approved Google
accounts, independent onboarding, restart/session restoration, A→B→A logout/login,
MCQ/FRQ and saved progress. A returned to30 XP/two lessons/20-XP goal; B independently
started atzero and completed Chemistry7 at12/12,+20 XP/one lesson/10-XP goal.
A's Chemistry result was11/12 and Physics5/6; correct/incorrect feedback and
optional reviewed explanations were observed. No identities or tokens are reported.

Three real fixes are accepted: route-extra restoration (`e3571d3`), reviewed
profile404 (`d587f9b`) and native FRQ semantics (`23f696f`, following470313d).
Current Flutter source23f696f: **1375 full tests passed** (serial38:33),105 default
targeted/10 reviewed contracts passed, full analyze **No issues found**.
Backend Live d587f9b: **5334 passed,65 skipped,21 warnings**, import/Docker passed
in CI42395951490. Awake exact-Live public preflight9/9 passed. Counts overlap and
must not be summed; the earlier interrupted Flutter attempt is retained separately.

Current installed artifact: `ILM-AI-Staging-1.0.3-code4-23f696f.apk`,180506516 bytes
(172.14 MiB), SHA2560268df56e4bee55d097dbb885a3b46c0ade13dd04322eda463257419c430abe2.
Separate staging package, install-r Success, no clear/uninstall, bounded credential
scan zero matches. Private OAuth file still has the doubled.json.json extension
and matches active staging. Free hosting/DB, auto-deploy off, deletion/test-auth/
preview flags off; no external AI key. Verified fallback works.

**Production NO-GO**: Live e97c029/main remains unchanged. Production baseline/
verified backup restore/migration/import/deploy approval, actual deletion sender/
policy/storage acceptance, Play-signed1.0.2 update/OAuth compatibility, provider
audience/configuration, exposed operator-key rotation and stable performance/
final production artifact acceptance remain. Free idle wake/timeouts are retained
as failures; no current cold-start SLA or artificial keepalive is claimed.
See backend `docs/beta/GOOGLE_STAGING_ACCEPTANCE_20261107.md` and
`docs/beta/PRODUCTION_READINESS_20261108.md` for current evidence and release gates.


The original setup below is for deliberate future client rotation only.
Production OAuth remains unchanged.

## Google Cloud’da

1. Production’dan alohida staging loyiha yoki tasdiqlangan test resursida Google
   Auth Platform consent/audience sozlamalarini tayyorlang. Testing holatida
   faqat o‘zingiz boshqaradigan test akkauntlarini qo‘shing.
2. OAuth client turini **Web application** deb tanlang. Bu ilovadagi brauzer orqali
   OAuth + backend callback oqimi uchun; API kaliti emas.
3. Authorized redirect URI aynan quyidagicha bo‘lsin:

   `https://ilm-ai-103-stage-8b0727.onrender.com/auth/google-callback-mobile`

   Scope: `openid email profile`. Production callback’ni almashtirmang.
4. Client JSON faylini yuklab, Git checkout’laridan tashqarida saqlang, masalan:

   `C:\Users\Page\.config\ilm-ai\staging-google.private.json`

5. Agentga **faqat fayl yo‘lini** yuboring. Client secret, token yoki JSON
   mazmunini chatga/Git’ga yubormang.

[Google rasmiy Web OAuth ko‘rsatmasi](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred).

## Agent keyin bajaradigan amallar

- Fayldagi client ID/redirect va uning production clientdan alohidaligini
  qiymatlarni oshkor qilmasdan tekshirish.
- Faqat yangi staging servisga `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` qo‘yish;
  `STAGING_AUTH_SETUP_PENDING=false`. Test-login/preview himoyalarini ochmaslik.
- Qat’iy staging validatorini qayta ishlatish va faqat stagingni deploy qilish.
  Render env-var PUT barcha qiymatlarni almashtiradi: tasodifan boshqa sozlamalar
  o‘chib ketmasin; production servis ID’sini qat’iy rad etish.
- Public PKCE/config preflightdan so‘ng haqiqiy test akkaunt bilan yangi/qaytgan
  akkaunt, boshqa akkaunt, cancellation, session/refresh/logout, progress va
  tarmoq uzilishi holatlarini tekshirish. Unit testni haqiqiy Google sinovi deb
  belgilamaslik.
- Zarur bo‘lganda `com.ilmai.app.staging`/`ilmai-staging` va aynan HTTPS API_URL
  bilan alohida Android build tayyorlash. Secret APK ichiga kiritilmaydi.
- ADB telefonni ko‘rsa o‘rnatish; ko‘rmasa o‘rnatilgan deb yozmaslik. Lokal Beta
  `com.ilmai.app.beta` va production `com.ilmai.app` ma’lumotlarini tozalamaslik.

Account deletion uchun alohida test mailbox/policy/storage va HTTPS tekshiruv
hali kerak. Hozir uni yoqish yoki production deploy/Play upload qilishga ruxsat
berilmagan. Chatda oshkor bo‘lgan Render kalitini chiqarishdan oldin almashtirish
talabi ham saqlanadi.
