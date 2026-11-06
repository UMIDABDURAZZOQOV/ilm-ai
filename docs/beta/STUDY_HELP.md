# Beta: fan almashtirish va manbali izoh — 2026-10-31

## Latest provider update — NVIDIA trial

The user supplied the official NVIDIA Muse Glimmer page, superseding the earlier
issuer guesses below. Read [NVIDIA_TRIAL_SETUP.md](NVIDIA_TRIAL_SETUP.md).
An optional internal-test-only adapter supports source-bound selection and up
to8 authorized standby keys; quota never switches accounts. Real NVIDIA private
credentials have not been supplied; no live provider call/restart occurred.
Hosted free trial is not production access. Combined regression152 passed,
6 PostgreSQL cases deselected/1 existing warning; no app/APK or progress change.

## 2026-11-06 — Free-only/provider correction

Latest requirements and actual credential status are in
[AI_PROVIDER_READINESS.md](AI_PROVIDER_READINESS.md). The user corrected the
issuer to Hugging Face; the supplied credential format has not been verified.
No provider is activated. An optional Cloudflare Free adapter is implemented
and tested, but the user has no Cloudflare account. It is not a live integration
or an automatically selected substitute. The historical config below remains
superseded; do not copy exposed credentials into it. New regression102 passed,
5 PostgreSQL cases deselected/1 existing warning; no Flutter/APK change.


## 2026-11-06 - Provider configuration supersedes historical single-key instructions

The user supplied Google AI Studio credentials. They were not used or saved;
Gemini's under-18 client restriction prevents activating them in this school app.
The optional existing OpenAI selector now requires a reviewed private config,
not the historical api_key/model pair below. It never forwards student free-form
messages/answers/IDs or accepts generated prose. Bounded standby on authorized
transport/service failures is tested; quota/rate errors pause/fall back instead
of sweeping accounts. Read [AI provider readiness](AI_PROVIDER_READINESS.md)
for exact configuration, limits, migration and production blockers. Older
configuration/inference statements below are historical and superseded.

## Audit va qabul qilingan yo‘l

Branch: `feat/beta-subject-switch-ai-help`, backend va Flutter alohida beta
worktreelarida. Boshlang‘ich commitlar `eb04a8d` / `0e508ef` saqlangan.
Normal Learn: SubjectHome → CurriculumLearning → SkillPath. Avval aktiv yo‘ldan
fan almashtirish sinf katalogiga qaytishni talab qilardi. Endi ko‘rinadigan
**Fanlar** tugmasi bir sheetda fan va sinfni tanlaydi. Qamrov backend katalogidan;
tegishli sinfda yo‘q fanlar va “Tez kunda” fanlari bosilmaydi. Tanlov oddiy
LearningPreferences orqali per-account saqlanadi; dars qoralamalari va progress
formatlari o‘zgarmagan. Bekor qilish yozuv yaratmaydi.

To‘rtta fan umumiy AssessmentLessonScreen/avvalgi editorlarda, Biologiya avvalgi
SkillLesson/SkillPractice ekranlarida qolgan. Yangi help shu ekranlarga ulanadi.
Biologiyada mavjud bo‘lmagan FRQ yaratilmagan. SAT/IELTS va veb tutor o‘zgarmagan.

Eski AiTutorWidget serverga client savol va javob kalitini yuborar edi;
AiExplainSheet umumiy `/assistant/ask` promptidan foydalanardi. Ular ushbu
manbali fan oqimiga ulanmagan. Eski `/tutor` beta middleware blokini saqlaydi.

## Yangi API va qat’iy manba chegarasi

`POST /beta/study-help`: subject, grade (questionli Biologiyada server aniqlashi
mumkin), lesson_key/attempt_id/question_key, language, ixtiyoriy message.
Begona maydonlar va 1000 belgidan uzun xabar rad etiladi. UID access tokendan.
Client savol matni, to‘g‘ri javob yoki rubricni authoritative qilib yubora olmaydi.
Response attempt_id/question_key qaytaradi; Flutter subject/grade/lesson/attempt/
question mosligini tekshiradi. Ushbu session identifikatorlari modelga berilmaydi.

- V2: asli runtime preview gate, get_session ownership/expiry, issued snapshot,
  public_attempt va qabul qilingan feedback. Javobdan avval grading_spec,
  expected qiymat yoki private yechim chiqmaydi. Javobdan keyin aynan graderning
  feedback/solution/source_refs qiymatlari qaytariladi; help graderni chaqirib
  natija yozmaydi. Har ikkala correctness holati qo‘llanadi.
- Biologiya: mobile_publication qat’iy hash/source/subject filtri va
  resolve_session. Savol faqat tegishli akkauntga chiqarilgan snapshotdan olinadi.
  V1 lokal tekshirishi uchun checked/selected_answer maslahat qiymatlari tekshiriladi;
  ular XP yoki attemptga yozilmaydi. Grade/source haqiqiy curriculum joinidan.
- Fan chatida faqat ochilgan/tugallangan darslar. Boshqa sinf, locked dars,
  begona savol/attempt va o‘chirilgan preview guard rad etiladi.
- Har bir ko‘rsatiladigan parcha haqiqiy source_refs bilan beriladi. Manba yoki
  izoh yo‘q bo‘lsa 409; AI bilan bo‘shliq to‘ldirilmaydi. Kitobdagi faktlar,
  manba validatorlari, mavjud erratum mexanizmi o‘zgarmaydi.
- Har UID uchun process ichida 20/min so‘rov; ro‘yxat tozalanadi va chegaralangan.
  Timeout, error yoki noto‘g‘ri provider natijasi maxfiy matnni logga chiqarmaydi.

## Tokensiz va tokenli rejimning aniq farqi

Hozirgi build/serverda haqiqiy token **yo‘q**. UI “AI hozir ulanmagan” deb aytadi
va tayyor, tekshirilgan dars izohini ko‘rsatadi. Follow-up shu dars kontekstida
ishlaydi; tokensiz javoblar tayyor manbali materialdan iborat. Bu erkin generativ
chat yoki yangi ilmiy javob degani emas. Kontent o‘zbekcha; UI uz/ru/en, til
farqi ochiq ko‘rsatiladi. Yechimlar manbali bosqichlar bilan, MCQ variantlari
tekshirilgan javobga mos/mos emas belgilari bilan solishtiriladi. Har distractor
uchun darslikda yozilmagan yangi sabab o‘ylab topilmaydi.

Keyingi tokenli adapter ham faqat tasdiqlangan evidence IDlarini tanlaydi va
tartiblaydi. JSON schema natijasi whitelist/unikallik/hajm bo‘yicha tekshiriladi;
notanish ID, refusal, timeout yoki API xatosida tayyor izohga qaytiladi. Model
prozasini ilmiy fakt sifatida o‘quvchiga uzatish yo‘li yo‘q. Grader feedbacki
provider tanlovidan qat’i nazar saqlanadi. Internet/general chat ochilmagan;
keyingi bunday scope uchun alohida manba/review siyosati va testlar zarur.

Provider kontrakti uchun rasmiy asos:
[OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=chat).
Haqiqiy tarmoqli AI chaqiruvi bu ishda sinovdan o‘tkazilmagan; faqat mock adapter.

## Keyinchalik private konfiguratsiya

Hozir buning uchun fayl yoki kalit yaratish shart emas. Keyin server egasi Git
worktree tashqarisidagi faqat o‘ziga o‘qiladigan private JSONga `api_key` va
`model` stringlarini joylaydi. Environmentdagi OPENAI_API_KEY/API_KEYS avtomatik
olinmaydi. Kalitni chatga, APKga, dart-definega, Gitga yoki build receiptga qo‘ymang.

```powershell
Set-Location 'C:\Users\Page\Desktop\Projects\ilm-ai-beta'
python -u -X utf8 scripts/serve_mobile_beta.py `
  --directory 'C:\Users\Page\Desktop\Projects\ilm-ai-beta-local' --resume `
  --port 8930 --ai-config-file 'C:\private\ilm-beta-ai.json'
```

Faqat token keyin kiritilganda tasdiqlangan savol/dars konteksti va yozilgan
follow-up tashqi providerga yuboriladi; user ID, JWT va credential yuborilmaydi.
Model IDni server egasi o‘z API hisobida mavjud modelga mos tanlaydi.
APKni qayta build qilish talab qilinmaydi. HTTPS/OAuth talablari LOCAL_BETA.md’da.

## O‘zgargan fayllar

Backend: `services/study_help.py`, `routers/beta_mobile.py`,
`scripts/serve_mobile_beta.py`, `tests/test_study_help.py`, `CLAUDE.md`, ushbu hujjat.

Flutter: `features/study_help/study_help.dart` (DTO/repository/provider/sheet),
`subject_switch_sheet.dart`, `subject_home_screen.dart`,
`curriculum_learning_screen.dart`, `assessment_lesson_screen.dart`,
`skill_lesson_screen.dart`, `skill_practice_screen.dart`, `lesson_feedback_panel.dart`,
tegishli widget testlar, `scripts/build_integrated_beta.ps1`, docs/CLAUDE.
Builder faqat avvalgi beta va yangi aniq feature branchni qabul qiladi.

## Tekshiruv

Disposable SQLite nusxasi; telefon bazasiga testlar yozmaydi:

```powershell
$env:ILM_BETA_REVIEWED_DB_FILE='C:/Users/Page/Desktop/Projects/ilm-ai-beta-local/chemistry_staging_world_history_staging_uzbekistan_history_staging_beta_staging.db'
python -m pytest tests/test_study_help.py -q -k 'not postgres'
```

Natija: 6 passed, 4 deselected (PostgreSQL variantlari bu yangi testlarda
ishga tushirilmagan). To‘rtta fan, Biologiya lesson/daily, ownership, wrong grade,
locked/foreign context, no-token, yaroqsiz provider ID, eski tutor guardi,
asl Physics MCQ/numeric FRQ correct/wrong, aniq yechim bosqichlari, XP yozilmasligi.
Baseline integratsiyada SQLite va PostgreSQL allaqachon 16 test bilan tekshirilgan.

Yakuniy yangi va avvalgi integratsiya regressiyasi birga: **14 passed,
12 deselected, 1 warning in 32.14s** (SQLite nusxalari). 1 381 birlik katalogi,
barcha besh fan graderlari, bir martalik XP va server auth/source guardlari ham o‘tdi.

Flutter: `flutter analyze --no-pub`; beta define bilan study_help_test,
integrated_beta_test va beta_shell_test. Yakuniy natija Flutter CLAUDE.md’da.
360px/200% text, light/dark, keyboard, cancel/retry, savol konteksti, to‘rtta FRQ
editori, normal onboarding/login/session va fan almashtirish saqlanishi tekshiriladi.

31-oktabr tekshiruv vaqtida `adb devices -l` bo‘sh. Yangi buildning haqiqiy
telefondagi smoke-testi hozir bajarildi deb ko‘rsatilmaydi. Oldingi beta APK
Samsungga o‘rnatilgani yangi feature acceptance hisoblanmaydi. Yangilash
`adb install -r` bilan, app data o‘chirilmaydi. APK/commit/hajm/hash uchun yonidagi
`integrated-beta-build.json` ishlatiladi; bu hali production reliz emas.
