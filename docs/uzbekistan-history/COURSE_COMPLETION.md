# O‘zbekiston tarixi — darslik qamrovi yakuni

2026-10-27. **172/172 haqiqiy o‘quv birligi uchun original, manbaga bog‘langan interaktiv kontent yaratildi va lokal/test rejimida tekshirildi. Qolgan mavzu: 0.** Mustaqil pedagogik tasdiq va ommaviy mobil release hali olinmagan.

## Sinflar va kontent

| Sinf | Bob | Manba birligi | Tayyor lokal/test dars | Qolgan | Karta | MCQ | Qisqa FRQ | Xronologiya | Jami topshiriq |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 6 | 42 | 42 | 0 | 325 | 168 | 83 | 29 | 280 |
| 8 | 4 | 41 | 41 | 0 | 319 | 140 | 82 | 23 | 245 |
| 9 | 9 | 39 | 39 | 0 | 293 | 139 | 77 | 14 | 230 |
| 10 | 6 | 28 | 28 | 0 | 184 | 84 | 56 | 15 | 155 |
| 11 | 9 | 22 | 22 | 0 | 159 | 66 | 44 | 7 | 117 |
| **Jami** | **34** | **172** | **172** | **0** | **1280** | **597** | **342** | **88** | **1027** |

Jami **172 original misol** va **172 avtomatik baholanmaydigan refleksiya** ham bor. 8-sinfning 41 birligi — 40 raqamlangan paragraf va 1 raqamsiz yakuniy faoliyat. 9-sinfdagi 41 paragraf raqami 39 darsga to‘g‘ri keladi: §4–5 va §35–36 kitobda birlashtirilgan. Sun’iy mavzu yoki takroriy sanoq kiritilmadi.

## Manba va pedagogika

Beshta kitob kataloglangan: **769 PDF sahifasi, 34 bob, 172 o‘quv sarlavhasi**. Bosma/PDF sahifasi, book/grade/chapter/topic/fact identifikatorlari, kitob SHA-256, native matn/tasvir SHA va paragraf chegaralari kontentga bog‘langan. 8-sinfning to‘rtta 40 sahifalik segmenti uzluksiz 160 sahifa sifatida tekshirildi. Asl bo‘linmagan fayl SHA’si taxmin qilinmadi. 1, 2, 159, 160-sahifalar bosma raqamsiz; 3–158 oralig‘ida bosma va PDF raqami teng.

Kartalar → original misol → MCQ/qisqa FRQ/xronologiya → oldindan yozilgan feedback → natija → XP/progress oqimi mavjud preview adapterida ishlaydi. Savol va izohlar manba sahifalariga bog‘langan. Avtomatik validator bog‘lanish, hesh, chegara, alias va tartib kalitlarini tekshiradi; u mustaqil tarixiy ekspertiza o‘rnini bosmaydi. Bahsli siyosiy/diniy talqin uchun yagona avtomatik «to‘g‘ri fikr» kaliti yo‘q. Etnik yoki diniy jamoaga kollektiv ayb qo‘yilmaydi.

## Haqiqiy test natijalari

- **backend_full**: `2524 passed, 9 skipped, 2 deselected, 13 warnings in 829.05s (0:13:49)`.
- **postgres**: `5 passed, 223 deselected in 100.80s (0:01:40)`.
- **whole_course**: `3 passed in 35.72s`.
- **flutter_history**: `00:23 +215: All tests passed!`.
- **flutter_analyze**: `No issues found! (ran in 1.6s)`.
- **flutter_full**: `01:27 +369: All tests passed!`.

- Debug JavaScript preview build: **passed, 41.7 s**. Haqiqiy token o‘rniga yaroqsiz compile-only placeholder ishlatilgan. Yakuniy Dart application va pubspec hashlarining build bilan tengligi tekshirildi.
- Source audit: **769 asl PDF sahifasi**, **172 sarlavha**, **746 partiya-sahifa tasviri**. Oxirgi sanoq chegara sahifalarining partiyalar orasidagi takrorlarini ham hisoblaydi; bu noyob sahifa yoki faktlar soni emas.
- Full backend’dagi opt-in PostgreSQL testlari default run’da skip. **5 ta History PostgreSQL testi alohida amalda o‘tdi.** Ikki positive sandbox testi chiqarildi; 13 oldingi warning saqlangan. Barcha test bazalari production’dan ajratilgan.

### Bitta akkaunt bilan butun kurs

Izolyatsiyalangan SQLite/ASGI testida barcha **172 dars va 1 027 javob** tugatildi. Eski **137 XP** saqlanib, **1 720 yangi XP** bilan jami **1 857 XP** bo‘ldi. Shu kuni mavjud **3 kunlik streak** saqlandi. Barcha **34 bob belgisi** ochildi. Yangi client’da qayta ochilganda 172 progress saqlangan; qayta urinish **0 XP** berdi. Javob va complete replay ayni natijani qaytardi. Boshqa test akkauntining XP’si 0 qoldi. Bu real foydalanuvchi statistikasi emas, avtomatik QA dalilidir.

### API va mavjud ishlarning saqlanishi

`course_content_complete=true` faqat barcha besh sinf ketma-ketligi DBga haqiqatan import qilingan va barcha manbalar mavjud bo‘lsa qaytadi. Bitta import/manba yetishmasa false. `grade_content_complete` tanlangan sinfga tegishli. `course_complete=false`, `course_ready=false`, `independent_review_pending=true` va `publication=local_test_preview_only` nashr tasdig‘i yo‘qligini saqlaydi. Eski v2 maydonlar olib tashlanmagan. Boshlang‘ich public DTO’da grading kalitlari yo‘q. MCQ va qisqa FRQ serverda baholanadi; ochiq esse uchun LLM yoki bitta satr kaliti ishlatilmaydi.

7-sinfning 42 r1 va 8-sinfning 41 r1 JSON/review Git bloblari oldingi checkpoint bilan bir xil. 552 old backend fayli source-preservation testlari bilan himoyalangan. Biologiya va Fizika regressionlari umumiy test to‘plamida o‘tdi. Asl Physics backend/Flutter hamda frontend worktreelari toza va boshlang‘ich HEADlarida. Kimyo va Jahon tarixi branchlariga yozilmadi. Veb, main, production DB, production migratsiya/deploy va ommaviy nashr bajarilmadi. PDF, OCR, asl rasm, transkript yoki credential Gitga kiritilmadi. Ilmo, brend va normal OAuth saqlandi.

## Qolgan review va release ishlari

1. Mustaqil tarix o‘qituvchisining faktologik va pedagogik ko‘rigi bajarilmagan. [Umumiy manba tafovutlari](SOURCE_REVIEW.md) va [11-sinf auditi](GRADE11_SOURCE_REVIEW.md)dagi bahsli da’volar avtomatik kalitga kiritilmadi. Ular uchun taxminiy tuzatish yozilmadi.
2. Rasmiy 2026–2027 dastur bilan to‘liq qiyos tasdiqlanmagan. 27-oktabrda gov.uz va uzbmb.uz qayta so‘raldi; proxy 403 qaytardi. Eski nashrlarni amaldagi dasturga avtomatik tenglashtirmaymiz. [Dastur auditi](CURRICULUM_ALIGNMENT_2026_2027.md).
3. Haqiqiy Android, TalkBack, native lifecycle va APK sinovi yo‘q: Android SDK/adb mavjud emas. History uchun alohida Android QA identity patchi Flutter branchidagi handoffda saqlangan, shared Gradle fayliga qo‘llanmagan. Telefon va real Google login sinovi bajarildi deyilmaydi.
4. Kurs alohida lokal/test preview rejimida. Normal mobil/production router va ommaviy fan katalogiga ulanmagan. Reviewer/teacher workflow, kontent revisionlarini ko‘tarish va umumiy integratsiya alohida bosqichlar.
5. 34 bob belgisi progress asosida ishlaydi; ular alohida checkpoint quiz emas. 172 ochiq refleksiya self/teacher rubrikasida, avtomatik esse baholash yoki teacher submission workflow yaratilmagan. Matnli xarita tahlili manba sahifalariga tayanadi; yangi interaktiv kartografik renderer yaratilgani da’vo qilinmaydi.
6. Standalone yangi sandbox CLI bu muhitdagi Git markerlari sabab to‘liq tekshirilmagan. Ikki positive sandbox testi full suite’dan chiqarildi; guard chetlab o‘tilmadi. SQLite ASGI/API va real loopback PostgreSQL sinovlari o‘tdi. Production migratsiya yoki deploy bajarilmadi.

## Git va hujjatlar

Ikkala repo branchi: `feat/uzbekistan-history-curriculum`.

- Tekshirilgan backend code: [1409236](https://github.com/UMIDABDURAZZOQOV/ilm-ai/commit/1409236526e5e5e2609125bfe72f668a99caa643).
- Tekshirilgan Flutter contract: [fa6c305](https://github.com/UMIDABDURAZZOQOV/ilm-ai-flutter/commit/fa6c305c4a56b16f397aa5d73f40b8040f016ed3).
- [Mashina o‘qiydigan yakuniy dalil](checkpoints/final_validation.json), [davom nuqtasi](RESUME_CHECKPOINT.md), [lokal QA](LOCAL_QA.md).

Mualliflik qamrovi tugadi. Keyingi sessiya 172 darsni qayta yaratmasin; ochiq review va integratsiya ishlarini yuqoridagi chegaralarda davom ettirsin. Production release/main merge uchun alohida ruxsat kerak.
