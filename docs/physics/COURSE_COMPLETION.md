# Fizika 6–11-sinflar: yakuniy qamrov — 2026-10-26

**316/316 raqamlangan bo‘lim original interaktiv kontent bilan qamrab olindi; yozilishi qolgan bo‘lim yo‘q.** Nashr holati: **faqat lokal/test preview**. Mustaqil fan/pedagogik ekspertizasi va haqiqiy Android sinovi o‘tkazilmagan. Bu hisobot ommaviy release tayyorligini tasdiqlamaydi.

| Sinf | Tayyor / jami | Qolgan | Karta | Formula | Namuna | Topshiriq | FRQ | Lab / amaliy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 6 | 61/61 | 0 | 254 | 74 | 67 | 394 | 88 | 7/1 |
| 7 | 46/46 | 0 | 196 | 90 | 47 | 304 | 133 | 5/0 |
| 8 | 60/60 | 0 | 253 | 129 | 70 | 419 | 134 | 5/2 |
| 9 | 59/59 | 0 | 271 | 202 | 61 | 461 | 205 | 6/2 |
| 10 | 45/45 | 0 | 214 | 160 | 46 | 373 | 161 | 5/0 |
| 11 | 45/45 | 0 | 225 | 125 | 45 | 354 | 127 | 3/0 |

Jami **1 413 karta, 780 formula yozuvi, 336 namuna va 2 305 topshiriq**, shundan **848 FRQ**. 31 raqamli laboratoriya, 5 boshqa amaliy faoliyat va 26 masala mashqi bo‘limi 316 bo‘limning ichida. Nazariy bo‘limlar soni 254 ta. Formula yozuvlari soni bajariladigan qoida oilalari soni emas: jami 665 oila — 660 ta reviewed va 5 ta saqlangan legacy v2 oila.

## Manbalar

[COURSE_COVERAGE_316.md](COURSE_COVERAGE_316.md) har bir bo‘limning dars nomi, turi, PDF/bosma sahifasi va kontent sonlarini beradi. Har karta, formula, namuna, savol va yechimning alohida `source_refs` metadata’si bor. Manba katalogida asl kitob/qism SHA256 identifikatorlari; review fayllarida native matn va asl tasvir identifikatorlari saqlangan.

Original fayllar bilan **924 sahifa tekshiruvi / 890 noyob sahifa** tasdiqlandi. Takror sahifa tekshiruvlari yangi noyob sahifa sifatida sanalmadi. PDF, OCR va sahifa tasvirlari Gitga qo‘shilmagan.

Qamrov xaritadagi 316 raqamlangan bo‘limga tegishli. Kitobdagi har qo‘shimcha yakuniy masala alohida darsga aynan ko‘chirildi degan da’vo yo‘q. Uzoq kitob matnlari ko‘chirilmagan; tushuntirish va masalalar original. 7-sinfning qabul qilingan §1–46 doirasidan tashqaridagi yo‘q kirish sahifalari taxminan to‘ldirilmagan.

[SOURCE_REVIEW.md](SOURCE_REVIEW.md) aniqlangan ilmiy tafovutlar, tuzatish asoslari va qo‘llanish chegaralarini saqlaydi. Tarixiy stage 1 `--require-complete` butun fakt/formula inventari uchun alohida qat’iy gate bo‘lib qoladi; uni 316 darsning amaldagi kontent validatori bilan tenglashtirmaymiz. Mustaqil ekspert tasdig‘i hanuz kerak.

## Amalda bajarilgan testlar

| Tekshiruv | Haqiqiy natija |
|---|---|
| Backend suite | **2272 passed**, 4 PG opt-in skipped, **2 sandbox deselected**, 13 mavjud warning; 568.38 s |
| Alohida lokal PostgreSQL 16 | **1 passed**, 130.25 s |
| Oxirgi §41–45 testlari | **39 passed**, 3.09 s |
| To‘liq qamrov va yo‘q import testlari | **4 passed**, 32.01 s |
| To‘liq Flutter suite | **154 passed**, 117 s |
| Flutter analyze | **No issues found (1.9s)** |
| Lokal Physics preview web build | **Passed**, 59.9 s |
| Native Android/APK | **Bajarilmagan: SDK va adb yo‘q** |

Backend buyrug‘i: `python -m pytest -q -k 'not sandbox' --basetemp /tmp/ilm-physics-final316`.

PostgreSQL testi alohida lokal schema’da assessment v2 migratsiyasi, 316 darsni import/reimport qilish, barcha 2 305 javob, 3 160 XP va replay idempotency’ni tekshirdi. Eski 137 XP / 3 streak / 2 stars saqlandi. Bu production migratsiyasi emas; barcha to‘rtta opt-in PG testi alohida qayta bajarildi degan da’vo yo‘q.

Flutter’da 11-sinfning 127 ta public FRQ drafti 320 px / 200% matn sharoitida tekshirildi. Manfiy energiya, ildiz, scientific notation, birlik, fokus/semantika va tap-target regressiyalari bor. To‘g‘ri `PHYSICS_PREVIEW=true` va `API_URL=http://127.0.0.1:8887` bilan `lib/main.dart` web bundle yig‘ildi. Bu compile tekshiruvi; joriy 316 dars uchun jonli TCP/brauzer OAuth yoki real telefon sinovi emas.

Biology auditi: **355 nazariy + 51 raqamli = 406 dars/faoliyat, 2 527 karta, 2 609 savol** saqlandi. Boshlang‘ich `9e2b73e` dagi 113 eski Physics JSON fayli byte-for-byte saqlangan. Veb-sayt va Kimyo fayllariga tegilmagan.

### Ikki sandbox testining cheklovi

Ikki o‘zgarmagan test Gitdan tashqari temp katalogni talab qiladi. Cloud muhiti `/tmp` va `/workspace` ostida read-only `.git` mount yaratadi. Oldingi outside-Git bajarish avtomatik approval-review xizmatining usage limiti sabab amalga oshmadi; bu amal xavfli deb topilgan qaror emas. Guardlar chetlab o‘tilmadi yoki yumshatilmadi. Shu ikki testning oldingi o‘tishi joriy running o‘tishi deb ko‘rsatilmaydi.

## Backend/Flutter kontrakti

Assessment v2 eski Biology/MCQ API’dan ajratilgan opt-in namespace va jadvallarda ishlaydi. Son, formula, birlik, ishora, aniqlik va ruxsatli alternativalar serverda tekshiriladi. Umumiy CAS, `eval` yoki AI Explain qo‘shilmagan. Javob kaliti/private grading qoidasi public DTO’ga chiqmaydi. Qayta answer/complete bir xil natija va bir martalik XP beradi.

`course_complete` barcha olti sinfning **import qilingan kontent qamrovi**ni bildiradi. Bu o‘quvchi kursni tugatgani yoki release tasdiqlanganini bildirmaydi. Har sinfda aynan `1..N` ketma-ketligi talab qilinadi. Oxirgi yoki o‘rtadagi bir dars importi yo‘q bo‘lsa overall complete false, tegishli `grade_content_complete` false bo‘ladi. Prerequisite va foydalanuvchi progress qoidalari saqlangan.

Yangi `allow_variable_power=true` faqat ikki yopiq decay formulasida ishlatiladi. Cheklangan AST shakli taqqoslanadi, o‘quvchi ifodasi bajarilmaydi. Serverning alohida `Fraction` hisobi faqat butun `0..4096` yarim davrni qabul qiladi; umumiy kasr darajali exponential solver da’vosi yo‘q. Bq aktivlik birligi Hz chastotasidan ajratilgan; `decayRate` berilgani reciprocal-second `1/s` bilan keladi.

## Keyingi bosqich

Mualliflik uchun keyingi bo‘lim qolmagan. [ANDROID_QA_316.md](ANDROID_QA_316.md) Windows PowerShell orqali lokal sandbox, USB reverse va alohida debug APK buyruqlarini beradi. Real Android’da qayta ochish, offline/retry, klaviatura, katta matn, TalkBack, Ilmo animatsiyalari va XP/progressni tekshirish kerak. Laboratoriyalar raqamli faoliyat bo‘lib qoladi; haqiqiy tajriba bajarilgani tasdiqlanmaydi.

Mustaqil ilmiy/pedagogik ekspertiza va native QA’dan keyin ommaviy nashr uchun foydalanuvchining alohida tasdig‘i olinadi. Google OAuth, push notification yoki imzolangan release bu kontent bosqichida qayta tekshirildi deb ko‘rsatilmaydi.

## Git

Backend: `feat/physics-curriculum-map`. Flutter: `feat/physics-first-batch`. Oldingi tekshirilgan checkpointlar `a0c21c7` va `0c97fca`; yakuniy kod/kontent/test/hujjatlar ushbu hisobotni saqlagan feature commit ichida. Pushdan so‘ng remote HEAD solishtiriladi; aniq final SHA chat hisobotida beriladi. PR merge qilinmagan.

Production deploy/import/migratsiya, `main` merge va Play Market nashri bajarilmagan. Fizika umumiy foydalanuvchi katalogida yoqilmagan. Biology progress/XP/streak, Ilmo, Flutter brendi va veb-sayt saqlangan.
