# Matematika engine — real poydevor va qolgan ishlar

## 2026-11-04 — III qism integratsiyasi

Jami78 lokal dars/70 model. III qism uchun37body-map,5dars.
[Explicit lokal source-gap QA flag siyosati va regressiyalar](RESUME_CHECKPOINT.md).
`available_books.source_body_topic_count`, `previous_book_navigation_ready`,
`source_gap_bridge` qo‘shimcha public fieldlar; eski DTOlar orqaga mos.
Snapshotda QA provenance saqlanadi; flagoff unfinished attemptni bloklaydi,
immutable MathLesson hujjati/progress/XPni o‘zgartirmaydi. No migration.


## 2026-11-03 — joriy checkpoint

1-sinf I qism: 41/41 dars, 230 karta, 288 topshiriq. Butun 1–11-sinf kursi hali tugallanmagan.
Math: 65 passed. Alohida PG: 1 passed. Flutter: 440 passed. Analyze: 0 muammo.
II qism: 33 mundarija bo‘limi, 32 native lokator, 0 tayyor dars. 74-mavzuning bosma 68–69-sahifalari yo‘q.
Bu status oldingi checkpointlardan yangiroq. [To‘liq dalil va texnik davom](FIRST_BOOK_COMPLETION.md),
[machine checkpoint](checkpoints/grade1_part1_batch8.json).

## Hozir ishlaydi

- `mathematics_grading.exact_number`: closed recursive-descent parser; +−×÷, qavs, unary sign va exact Fraction. O‘nli vergul/nuqta qabul qilinadi.1/2=2/4=0.5, ammo1/3 !=0.333. Token80, matn160, chuqurlik12, literal40belgi, ratio256bit; zero division rad. eval/exec/Python AST execution/sympify/CAS/arbitrary funksiyalar yo‘q.
- Explicit concept/alias, o‘zbek apostrofi normalizatsiyasi; o‘ va o tenglashtirilmaydi. Fuzzy matching yo‘q.
- Original shape-properties, aligned-length bars, relative-position, count-once, flat/solid illustration modellarining Flutter boshqaruvi. Canvas o‘lchovlari bir doska masshtabida; bar nisbati testlanadi. Kub/shar modeli 2D chizma,3D geometriya renderer emas.
- Alohida `/preview/mathematics/v1` authenticated router,4opt-in Math jadval. Snapshotdagi grading mijozga yuborilmaydi. Har requestga UUID, 24h attempt, ordered retry, monoton answer sequence, immutable import/revision, old account XP + once-only reward ledger.
- Public DTOdan tashqari server kalitlari UIga chiqmaydi. Flutter pending answer UUID/payloadni tarmoq xatosida saqlaydi;422dan keyin tahrirlash mumkin. Qoralama API origin+UID+lesson bo‘yicha ajratilgan. Server draftdan mustaqil ravishda baholaydi.

## Hali implementatsiya qilinmagan imkoniyatlar

| Oilalar | Texnik qaror | Holat |
|---|---|---|
| Aralash kasr, yaxlitlash/tolerance | yangi versionlangan syntax + explicit exact/approx spec | planned |
| Polynomial ekvivalentlik | allowlist parser → bounded rational-coefficient polynomial normal form; numeric-sample equality proof emas | planned |
| Ratsional ifoda/domain | numerator/denominator va asl excluded points saqlash; cancel domainni yo‘qotmasin | planned |
| Tenglama/ildizlar | explicit domain, complete root-set equality, substitution, extraneous roots | planned |
| Interval/tengsizlik | ordered exact endpoints, open/closed, union, empty/all-domain; unsupported radical/trigni fail closed | planned |
| Bosqichli yechim/isbot | authored permitted transformations + shartlar; alternative valid paths graphi, isbotga rubrika | planned |
| Grafik/parametrlar | testable model, real coordinate transform, discontinuity clipping, labelled axes/domain/asymptote, tap/slider, textual equivalent | planned |
| Geometriya/statistika/integral | source-specific constraints; chart normalization, exact dataset math, signed area/bounds, lightweight3D with invariant tests | planned |

Hech bir planned imkoniyat tayyor deb e’lon qilinmaydi. Bir nechta numeric samples yoki oddiy matn solishtirish orqali general symbolic equivalence tasdiqlanmaydi. CPU/memory budget, token/degree limits va unsupported javobga halol feedback har yangi oilada majburiy. Public API v1 yonida yangi response kind faqat version/capability kelishuvi bilan qo‘shiladi; eski MCQ/Fizika gradingga tegilmaydi.

Normal backend router, mobil fan katalogi, Google login, Ilmo assetlari, shared Gradle va frontend o‘zgartirilmagan. Full course publication integratsiyasi keyingi bosqich; hozir faqat explicit local/test flag+host guard.
