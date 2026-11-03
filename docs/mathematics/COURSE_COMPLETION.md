# Matematika kursi — hali tugallanmagan

## 2026-11-03 — 1-sinf I qism: 41/41 mavzu

**Birinchi kitobning mavzulari qamrab olindi. Butun 1–11-sinf Matematika kursi hali tugallanmagan.**
Faqat lokal test uchun: 41 dars, 230 karta, 41 original misolning 123 qadami va 288 topshiriq.
Bosqichlar: 144 guided, 41 MCQ, 41 FRQ va 62 transfer. Javob turlari: 113 variantli,
24 aniq atama, 144 sonli va 7 tartiblash topshirig‘i. 37 turdagi boshlang‘ich interaktiv model bor.
46 ta sonli misol tengligi import paytida aniq arifmetika bilan tekshiriladi.
Umumiy algebra/CAS, ilg‘or grafik va haqiqiy 3D o‘lchash mexanizmi hali tayyor emas.

Dastlabki 5 dars va ularning review fayllari o‘zgarmadi. Yangi 6–41-darslar qo‘shildi;
import eski mazmun yoki progressni qayta yozmaydi. Har bir kartaning, misol qadamining,
savolning va izohning manba havolasi reviewdagi kitob/sinf/qism/mavzu/sahifaga mos bo‘lishi shart.
Birinchi PDFning 94 sahifasi ko‘rildi, 82 ta dars sahifasi tasvirlari pin bilan bog‘landi.
PDF 55–56 takror skan; qo‘shimcha dars emas. Bosma/PDF sahifalar uchun yagona offset ishlatilmadi.
Qo‘lyozma javoblar tekshirilgan javob kaliti sifatida olinmadi.

Amalda bajarilgan yakuniy tekshiruvlar:

- Math: **65 passed, 1 skipped, 44.82 s**. Skip — alohida ishga tushiriladigan PostgreSQL testi.
- Alohida loopback PostgreSQL 16: **1 passed, 18.83 s**; barcha 41 dars, parallel birinchi XP, replay va immutable import.
- To‘liq Flutter: **440 passed, 2 min 7 s**; analyze — **0 muammo, 2.2 s**.
- Debug JS web build: **35.7 s**. Flag, lokal API URL va test UID berildi; haqiqiy JWT ishlatilmadi.
  Bu natija haqiqiy brauzer/API yoki Android sinovi emas.
- Biology completion/curriculum, Physics course va mobil OAuth himoya regressiyasi: **46 passed, 112.33 s**.
- 23 ta mavjud PDF va 2 958 sahifaning hash auditi o‘tdi. Bu barcha kitoblar mazmuni to‘liq o‘qilganini anglatmaydi.

Lokal test akkauntining eski 137 XP qiymati saqlanib, 547 XP bo‘ldi; 41 progress yozuvi bor.
Boshqa akkaunt XPsi o‘zgarmadi. Qayta bajarish 0 XP berdi. Bu test ma’lumoti, mahsulot uchun soxta statistika emas.
Ilmo, brend, normal app/API/auth, frontend, umumiy Gradle, production va boshqa fanlar fayllari o‘zgarmadi.
Himoyalangan beshta worktree avvalgi HEADda va toza qoldi. Yangi to‘liq backend regressiyasi da’vo qilinmaydi;
eski keng natija birinchi checkpointda, hozirgi Math va himoya sinovlari esa alohida qayd etilgan.

Yangi interaktivlik: vaqt tartibi, guruh tarkibi/miqdori, sonlar qatori, qo‘shish/ayirish,
butun–qism, juftlash, natural sonlar, nuqta/chiziq/kesma, siniq yo‘l, noma’lum had,
qo‘shiluvchilar o‘rnini almashtirish, jadval, taqqoslash va bosqichli ifoda.
Oqimlar 320 px, 200% matn va Reduce Motion bilan tekshirildi. Xatoda bosqichli ishora,
tartiblashda to‘liq ID permutatsiyasi, timeoutda saqlangan UUID bilan qayta yuborish ishlaydi.

### II qismda aniqlangan manba kamchiligi

II qismda 42–74 raqamli **33 ta mundarija bo‘limi**, 32 ta native sarlavha lokatori va **0 tayyor dars** bor.
PDF 68 / bosma 67 dan PDF 69 / bosma 70 mundarijaga o‘tiladi.
**74 «Misol va masalalar yechish» mavzusining bosma 68–69-sahifalari yo‘q.** Mazmuni taxmin qilinmadi.
`grade1_part2_map.json`da gap va tasvir SHA dalillari saqlandi. Faqat 42 va 73-mavzuning tana tasvirlari o‘qildi;
qolgan 30 mavzuning tanasi to‘liq tekshirilmagan. Mundarija yoki lokator tayyor dars hisoblanmaydi.
9-sinf Algebra va 11-sinf I qism transferda 32 MiB bilan bloklangan. 6-sinf II qism va 7–10-sinf Geometriya manbalari ham yo‘q.

**Keyingi: 1-sinf II qism, 42 «11 dan 20 gacha bo‘lgan sonlar», PDF 5–6 / bosma 4–5.**
[Texnik handoff](FIRST_BOOK_COMPLETION.md), [dalil](checkpoints/grade1_part1_batch8.json).
Backend kod: `b29fff9858d0f6dc6fbc3b0d6cf252d0d5a3f53f`. Flutter: `f69de9b0accb1cda6835e0858a355a07d68ec280`. Ikkala feature branch GitHubga push qilindi.
GitHub GraphQL 403 qaytardi; PR yaratilmagan. Merge/deploy/nashr bajarilmadi.
Android SDK yo‘q; real telefon, mustaqil o‘qituvchi, pilot va rasmiy dastur mosligi tekshirilmagan.
`course_ready=false` va `publication=local_test_preview_only` saqlandi.

## 2026-11-03 — 35 darslik tekshirilgan checkpoint

**1-sinf I qism: 35/41 mualliflik darsi**, 194 karta, 35 original
misol/105 qadam, 240 topshiriq. Butun1–11kurs tugallanmagan;
umumiy mavzular/qolganlar soni hali noma’lum. Nashr: faqat lokal test.

31–35: kesma oxirlari/bo‘g‘inlar/nuqtalar, qo‘shish/ayirish hadlari, noma’lum qo‘shiluvchi va kamayuvchi. Original siniq chiziq modeli va ma’lum had o‘zgarganda yechimni qayta ochish modeli bor. FRQ sonli yoki aniq atama bilan serverda baholanadi; umumiy symbolicCAS deb ko‘rsatilmaydi. AB va BA ayni kesma; nuqta sanog‘i bilan bo‘g‘in sanog‘i ajratiladi.

Yangi partiya manbalari:

| Mavzu | PDF | Bosma |
|---|---|---|
| 31 To‘g‘ri chiziq kesmasi. Siniq chiziq | 67–68 | 64–65 |
| 32 Qo‘shish hadlari | 69–70 | 66–67 |
| 33 Ayirish hadlari | 71–72 | 68–69 |
| 34 Noma’lum qo‘shiluvchini topish | 73–74 | 70–71 |
| 35 Noma’lum kamayuvchini topish | 75–76 | 72–73 |

Haqiqiy sinovlar:

- math: `61 passed, 1 skipped in 45.77s`.
- postgres: `1 passed in 26.13s`.
- flutter_math: `01:10 +60: All tests passed!`.
- analyze: `No issues found! (ran in 1.3s)`.

Manba auditi:23PDF/2958sahifa va70tana sahifasi tasviri/hash.
SQLite va o‘zimizning alohida loopbackPG16 sxemasi: barcha35dars, idempotent
import, progress, replay0XP,137oldXP→487; parallel birinchi completion bitta mukofot.
Birinchi5kontent/review o‘zgarmagan. Boshqa fanlar, auth, frontend, umumiy Gradle,
normal app va production o‘zgartirilmagan. Android va pedagogik mustaqil ekspertiza yo‘q.
Manba transferidagi2kattaPDF va yetishmayotgan5manba cheklovi saqlangan.

Keyingi: **36 «Noma’lum ayriluvchini topish»,PDF77–78/bosma74–75**.
1-sinf I qismning6mavzusi hali yozilmagan.
Backend `3aada2e0de32efe3fff9e71352a229068a626bf5`; Flutter `aa9df2e8f9bdcba6a90f52ff91ff3d1820d4e4dc`. [Dalil](checkpoints/grade1_part1_batch7.json).

## 2026-11-03 — 30 darslik tekshirilgan checkpoint

**1-sinf I qism: 30/41 mualliflik darsi**, 164 karta, 30 original
misol/90 qadam, 200 topshiriq. Butun1–11kurs tugallanmagan;
umumiy mavzular/qolganlar soni hali noma’lum. Nashr: faqat lokal test.

26–30: 10ning ikki raqamli yozuvi, o‘sish/kamayish, natural sonlar kelishuvi, juft/toq va nuqta/chiziqlar. 0ning natural emasligi shu darslik kelishuvi sifatida beriladi; juftlik bilan aralashtirilmaydi. 10elementli tartiblash serverda to‘liq permutatsiya bilan tekshiriladi. Noma’lum explorer client/serverda fail-closed rad etiladi. Original to‘g‘ri/egri chiziq modeli va nuqta semantikasi qo‘shildi.

Yangi partiya manbalari:

| Mavzu | PDF | Bosma |
|---|---|---|
| 26 10 soni | 57–58 | 54–55 |
| 27 1 dan 10 gacha bo‘lgan sonlar. Sonlarni taqqoslash | 59–60 | 56–57 |
| 28 Natural sonlar | 61–62 | 58–59 |
| 29 Juft va toq sonlar | 63–64 | 60–61 |
| 30 Nuqta. To‘g‘ri va egri chiziq | 65–66 | 62–63 |

Haqiqiy sinovlar:

- math: `60 passed, 1 skipped in 25.13s`.
- postgres: `1 passed in 12.81s`.
- flutter_math: `00:41 +52: All tests passed!`.
- analyze: `No issues found! (ran in 1.6s)`.

Manba auditi:23PDF/2958sahifa va60tana sahifasi tasviri/hash.
SQLite va o‘zimizning alohida loopbackPG16 sxemasi: barcha30dars, idempotent
import, progress, replay0XP,137oldXP→437; parallel birinchi completion bitta mukofot.
Birinchi5kontent/review o‘zgarmagan. Boshqa fanlar, auth, frontend, umumiy Gradle,
normal app va production o‘zgartirilmagan. Android va pedagogik mustaqil ekspertiza yo‘q.
Manba transferidagi2kattaPDF va yetishmayotgan5manba cheklovi saqlangan.

Keyingi: **31 «To‘g‘ri chiziq kesmasi. Siniq chiziq»,PDF67–68/bosma64–65**.
1-sinf I qismning11mavzusi hali yozilmagan.
Backend `ad35c8e5d73011157d9c82b4a573d2f4fb34009c`; Flutter `1f15a4a4c7f882448310a51dab49b97fc2fe1ccf`. [Dalil](checkpoints/grade1_part1_batch6.json).

## 2026-11-03 — 25 darslik tekshirilgan checkpoint

**1-sinf I qism: 25/41 mualliflik darsi**, 134 karta, 25 original
misol/75 qadam, 160 topshiriq. Butun1–11kurs tugallanmagan;
umumiy mavzular/qolganlar soni hali noma’lum. Nashr: faqat lokal test.

21–25: olti–to‘qqiz va nol. Ikki tomondan sanoqda o‘rindagi belgi bir marta hisoblanadi; kun/mashg‘ulot, jami/yonma-yon joy va turli yil boshlanishlari ajratildi. Nol — aniq javob; bo‘sh input422bilan rad etiladi. Katta guruhlar Wrap orqali kichik ekranga moslashadi. PDF55–56 takror hisoblanmaydi; keyingi26mavzu PDF57dan, bosma54dan boshlanadi.

Yangi partiya manbalari:

| Mavzu | PDF | Bosma |
|---|---|---|
| 21 6 soni va raqami | 45–46 | 44–45 |
| 22 7 soni va raqami | 47–48 | 46–47 |
| 23 8 soni va raqami | 49–50 | 48–49 |
| 24 9 soni va raqami | 51–52 | 50–51 |
| 25 0 soni va raqami | 53–54 | 52–53 |

Haqiqiy sinovlar:

- math: `57 passed, 1 skipped in 18.20s`.
- postgres: `1 passed in 7.32s`.
- flutter_math: `00:34 +43: All tests passed!`.
- analyze: `No issues found! (ran in 1.8s)`.

Manba auditi:23PDF/2958sahifa va50tana sahifasi tasviri/hash.
SQLite va o‘zimizning alohida loopbackPG16 sxemasi: barcha25dars, idempotent
import, progress, replay0XP,137oldXP→387; parallel birinchi completion bitta mukofot.
Birinchi5kontent/review o‘zgarmagan. Boshqa fanlar, auth, frontend, umumiy Gradle,
normal app va production o‘zgartirilmagan. Android va pedagogik mustaqil ekspertiza yo‘q.
Manba transferidagi2kattaPDF va yetishmayotgan5manba cheklovi saqlangan.

Keyingi: **26 «10 soni»,PDF57–58/bosma54–55**.
1-sinf I qismning16mavzusi hali yozilmagan.
Backend `246f41ef6f711707e3a83a18076a291ac570c124`; Flutter `c5d8e3a88770059b27eeb1d872db6e65a266fe51`. [Dalil](checkpoints/grade1_part1_batch5.json).

## 2026-11-03 — 20 darslik tekshirilgan checkpoint

**1-sinf I qism: 20/41 mualliflik darsi**, 104 karta, 20 original
misol/60 qadam, 120 topshiriq. Butun1–11kurs tugallanmagan;
umumiy mavzular/qolganlar soni hali noma’lum. Nashr: faqat lokal test.

16–20: uch/to‘rt/besh tarkibi, juft bilan buyum sanog‘i, butun–qism, qo‘shni oraliqlar bo‘ylab qo‘shish/ayirish. Har bir guruhlashda narsalar bir marta hisoblanadi. Boshlanish nuqtasi qadam hisoblanmaydi. Qo‘lyozma noto‘g‘ri javoblar kalit sifatida ishlatilmadi.

Yangi partiya manbalari:

| Mavzu | PDF | Bosma |
|---|---|---|
| 16 3 soni va raqami | 35–36 | 34–35 |
| 17 4 soni va raqami | 37–38 | 36–37 |
| 18 5 soni va raqami | 39–40 | 38–39 |
| 19 1 dan 5 gacha bo‘lgan sonlar | 41–42 | 40–41 |
| 20 1 dan 5 gacha bo‘lgan sonlar bilan amallar bajarish | 43–44 | 42–43 |

Haqiqiy sinovlar:

- math: `55 passed, 1 skipped in 12.00s`.
- postgres: `1 passed in 5.65s`.
- flutter_math: `00:25 +35: All tests passed!`.
- analyze: `No issues found! (ran in 1.8s)`.

Manba auditi:23PDF/2958sahifa va40tana sahifasi tasviri/hash.
SQLite va o‘zimizning alohida loopbackPG16 sxemasi: barcha20dars, idempotent
import, progress, replay0XP,137oldXP→337; parallel birinchi completion bitta mukofot.
Birinchi5kontent/review o‘zgarmagan. Boshqa fanlar, auth, frontend, umumiy Gradle,
normal app va production o‘zgartirilmagan. Android va pedagogik mustaqil ekspertiza yo‘q.
Manba transferidagi2kattaPDF va yetishmayotgan5manba cheklovi saqlangan.

Keyingi: **21 «6 soni va raqami»,PDF45–46/bosma44–45**.
1-sinf I qismning21mavzusi hali yozilmagan.
Backend `304226e1b3840db7123489e025055df8e1defa8a`; Flutter `3c3ee6f3d12492a9606aad81a38fc3ae38ebb105`. [Dalil](checkpoints/grade1_part1_batch4.json).

## 2026-11-03 — 15 darslik tekshirilgan checkpoint

**1-sinf I qism: 15/41 mualliflik darsi**, 79 karta, 15 original
misol/45 qadam, 90 topshiriq. Butun1–11kurs tugallanmagan;
umumiy mavzular/qolganlar soni hali noma’lum. Nashr: faqat lokal test.

11–15: qo‘shish/ayirish, >/< /= yo‘nalishi, 1 va2, buyum bilan bo‘lak sanog‘i. To‘rtta original tenglik yozuvi exact parser bilan importda tekshiriladi. Bu umumiy algebra CAS emas. Ayirishning oldin/keyin holatlari alohida; hali o‘rgatilmagan nol modelga kiritilmadi. Qo‘lda raqam yozish sifati avtomatik baholanmaydi.

Yangi partiya manbalari:

| Mavzu | PDF | Bosma |
|---|---|---|
| 11 Qo‘shish | 25–26 | 24–25 |
| 12 Ayirish | 27–28 | 26–27 |
| 13 Sonlarni taqqoslash | 29–30 | 28–29 |
| 14 1 soni va raqami | 31–32 | 30–31 |
| 15 2 soni va raqami | 33–34 | 32–33 |

Haqiqiy sinovlar:

- math: `53 passed, 1 skipped in 7.97s`.
- postgres: `1 passed in 4.69s`.
- flutter_full: `01:42 +396: All tests passed!`.
- analyze: `No issues found! (ran in 1.6s)`.

Manba auditi:23PDF/2958sahifa va30tana sahifasi tasviri/hash.
SQLite va o‘zimizning alohida loopbackPG16 sxemasi: barcha15dars, idempotent
import, progress, replay0XP,137oldXP→287; parallel birinchi completion bitta mukofot.
Birinchi5kontent/review o‘zgarmagan. Boshqa fanlar, auth, frontend, umumiy Gradle,
normal app va production o‘zgartirilmagan. Android va pedagogik mustaqil ekspertiza yo‘q.
Manba transferidagi2kattaPDF va yetishmayotgan5manba cheklovi saqlangan.

Keyingi: **16 «3 soni va raqami»,PDF35–36/bosma34–35**.
1-sinf I qismning26mavzusi hali yozilmagan.
Backend `5e7bcc45529e4074d6698294af65d34e05ec8724`; Flutter `9b1ed1529985b3f0a372238a1b0677ce1011105d`. [Dalil](checkpoints/grade1_part1_batch3.json).

## 2026-11-03 — ikkinchi tekshirilgan partiya

1-sinf I qism **1–10: 10 dars, 54 karta, 10 original misol/30 qadam, 60 topshiriq**.
6 «Vaqt bo‘yicha ketma-ketlik» PDF15–16/bosma14–15; 7 «Narsalar guruhi»17–18/16–17;
8 «Guruhlarni taqqoslash»19–20/18–19; 9 «1 dan10gacha bo‘lgan sonlar»21–22/20–21;
10 «Narsalar sanog‘i»23–24/22–23. Har bir asl tana tasviri qayta o‘qildi.
Guruh tarkibi bilan teng miqdor farqlanadi; qo‘shni-son topshiriqlari ko‘rsatilgan1–10
qatorining ichki2–9sonlari bilan cheklangan. Qo‘lyozma kalit emas.

Yangi ordering javobi yagona to‘liq ID permutatsiyasini serverda tekshiradi. Noto‘g‘ri
haqiqiy tartib feedback/ishora oladi; dublikat/noma’lum/to‘liqmas ID422bilan rad etiladi.
Mavjud MCQ/FRQ va birinchi5JSON/review o‘zgarmadi; import immutable/additive.
Flutter timeline, tarkib/miqdor taqqoslash va chegaralangan sonlar qatori bilan boyitildi.
Bir xil nomli4/10mavzular endi tartib raqami va barqaror key bilan ajraladi.

Testlar: Math **50 passed,1 skipped5.50s**; alohida haqiqiyPG16 **1passed3.08s**
(all10,parallel firstXP,replay); Flutter Math **20passed13s**, analyze **0issue1.6s**.
137oldXP→237; barcha10progress; qayta bajarish0XP. 23PDF/2958sahifa hash auditi o‘tdi;
20tana sahifasi/10mavzu image pinlari tasdiqlandi. Bu partiyada to‘liq backend/Flutter
regressiyasi qayta bajarilmadi; oldingi keng natijalar birinchi checkpointda saqlandi.
Android/o‘qituvchi/pilot/rasmiy dastur holati o‘zgarmagan.

Keyingi: **11 «Qo‘shish»,PDF25–26/bosma24–25**; Iqismning31mavzusi hali yozilmagan.
Butun1–11kursning jami/qolganlari noma’lum; manba cheklovlari saqlangan.
[Dalil](checkpoints/grade1_part1_batch2.json). Backend `71c22693e9574ecee0f4cca2fb3c31fee53d667f`,Flutter `5c4d030c1ef7c86b68bc48609dd53c87f8193e23`.

| Qabul mezoni | Holat | Haqiqiy qamrov |
|---|---|---|
| Context completeness | partial | 23 PDF inventari, birinchi qismda 41 mundarija lokatori, 5 dars; 7 ta manba cheklovi |
| Explanation completeness | partial | 29 original karta, 5 misol va 15 action/why qadam |
| Visual completeness | partial | 5 boshlang‘ich interaktiv model; umumiy grafik/geometriya/statistika/integral/3D tizimi hali yo‘q |
| Practice completeness | partial | 15 guided, 5 MCQ, 5 FRQ, 5 transfer; qolgan mavzular kutilmoqda |
| Mathematical correctness | partial | Birinchi 5 dars va chegaralangan exact parser testlangan; umumiy kurs ekspertizasi olinmagan |
| Product quality | partial | Widget/API/SQLite/PG/web build tekshirildi; real Android va normal mobil integratsiya yo‘q |
| Educational effectiveness | not_verified | O‘qituvchi ko‘rigi va rozilikli bolalar piloti o‘tkazilmagan |

**Umumiy kurs tugallanmagan. Jami haqiqiy mavzular va qolgan mavzular soni hali aniqlanmagan.** Dars soni butun bilim qamrovi yoki ta’lim samarasi isboti emas. Publication `local_test_preview_only`, `course_ready=false`. Ikki PDF transferda bloklangan, beshta manba `source_missing`; ularning mazmuni taxmin bilan yaratilmaydi.

[Manba inventari](SOURCE_CATALOG.md), [qamrov](CURRICULUM_COVERAGE.md), [testlar](QA_REPORT.md), [davom nuqtasi](RESUME_CHECKPOINT.md).
