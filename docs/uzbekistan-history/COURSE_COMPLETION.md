# O‘zbekiston tarixi — joriy kurs checkpointi

2026-10-26. **Kurs tugallanmagan.** 7-sinf §1–25: **25 dars**, 191 karta, 25 original misol, 168 topshiriq (100 MCQ / 49 qisqa FRQ / 19 xronologiya), 25 avtomatik baholanmaydigan refleksiya/rubrika.

| Sinf | Bob | Katalogdagi mavzu | Interaktiv dars | Qolgan |
|---|---:|---:|---:|---:|
| 7 | 6 | 42 | 25 | 17 |
| 8 | ? | ? | 0 | Noma’lum: PDF olinmagan |
| 9 | 9 | 39 | 0 | 39 |
| 10 | 6 | 28 | 0 | 28 |
| 11 | 9 | 22 | 0 | 22 |

To‘rtta mavjud darslikda 131 ta mavzu guruhi kataloglangan; 106 tasi hali darsga aylantirilmagan. Beshala kitob jami **noma’lum**. 9-sinf §4–5 va §35–36 birlashtirilgan bo‘limlar alohida ikki marta sanalmaydi. Manba inventari tayyor darslar soni emas.

## Haqiqiy test natijalari

- backend: `66 passed, 1 skipped in 10.97s`.
- postgres: `1 passed, 50 deselected in 9.46s`.
- flutter: `01:34 +204: All tests passed!`.
- analyze: `No issues found! (ran in 1.5s)`.
- legacy_selected: `530 passed in 197.87s (0:03:17)`.
- legacy_full: `2314 passed, 5 skipped, 2 deselected, 13 warnings in 536.55s (0:08:56)`.

Source audit: 609 asl native sahifa, 131 sarlavha tasviri va **85 to‘liq dars manba sahifasi tasviri** xeshdan tekshirildi. Bu barcha kitoblardagi har bir tarixiy da’vo mustaqil ekspert tomonidan tasdiqlandi degani emas. `legacy_full` birinchi5dars checkpointida; `legacy_selected` §1–15ustida; eng yangi partiya `backend/postgres/flutter` bilan keyin tekshirildi.

## Tekshiruv chegaralari

8-sinfning 45.4 MB skanerlangan PDF’i 32 MiB executor transfer limitidan o‘tmadi; uni to‘liq olingan, OCR qilingan yoki SHA tekshirilgan deb hisoblamaymiz. Sahifalar tartibi aniq ko‘rsatilgan, 32 MiB’dan kichik uzluksiz segmentlar kerak. 2026–2027 rasmiy dasturga moslik real proxy403 sabab tasdiqlanmadi. Mustaqil tarix o‘qituvchisi va real Android sinovi bajarilmagan. Android SDK/adb yo‘q; Gradle alohida History QA application ID integratsiyasi ham qolgan.

Barcha yangi darslar **lokal/test preview**, `course_ready=false`. Bob tugallanish belgisi alohida checkpoint quiz emas; alohida bob testlari hali yozilmagan. Erkin tarixiy tahlil uchun rubrika bor, lekin teacher workflow yoki avtomatik esse bahosi yo‘q. Hozirgi import faqat immutable `r1` darslar uchun; kelajak revision aktivlashtirish/unique constraint strategiyasi alohida integratsiya va migratsiya review talab qiladi. Mavjud revision yoki foydalanuvchi progressi qayta yozilmaydi.

Production router, fanlar katalogi, Google login, veb-sayt, Biology406 va Physics316 kontenti o‘zgartirilmagan. 552 mavjud backend fayli xeshi tekshiriladi. Kimyo268 va Jahon tarixi parallel remote branchlari saqlandi, ushbu Physics-base branchga merge qilinmagan; barcha fanlar bitta integration branchida testlandi deb aytilmaydi. PDF/OCR/kitob tasviri/transkript Gitga qo‘shilmagan. Main merge, production DB/import/deploy va AI Tutor/Explain yo‘q.

## Git va davom

Backend va Flutter: `feat/uzbekistan-history-curriculum`. Source checkpoint `d7d0510`; oldingi partiyalar `bf98c8c`/`a11c97d`/`4b51213`, Flutter `8490036`/`86402fc`/`bfef1a9`. Joriy partiya commitini `git log -1` va `git ls-remote` bilan tekshiring. Keyingi: **7-sinf §26, PDF/bosma 91 — Movarounnahr va Xorazmning madaniy hayoti**.

[Davom va dars manbalari](STAGE2_PROGRESS.md), [manba tafovutlari](SOURCE_REVIEW.md), [lokal QA chegaralari](LOCAL_QA.md).
