# O‘zbekiston tarixi — joriy kurs checkpointi

2026-10-27. **Kurs tugallanmagan.** 7-sinf §1–40: **40 dars**, 307 karta, 40 original misol, 267 topshiriq (160 MCQ / 79 qisqa FRQ / 28 xronologiya), 40 avtomatik baholanmaydigan refleksiya/rubrika.

| Sinf | Bob | Katalogdagi mavzu | Interaktiv dars | Qolgan |
|---|---:|---:|---:|---:|
| 7 | 6 | 42 | 40 | 2 |
| 8 | ? | ? | 0 | Noma’lum: PDF olinmagan |
| 9 | 9 | 39 | 0 | 39 |
| 10 | 6 | 28 | 0 | 28 |
| 11 | 9 | 22 | 0 | 22 |

To‘rtta mavjud darslikda 131 ta mavzu guruhi kataloglangan; 91 tasi hali darsga aylantirilmagan. Beshala kitob jami **noma’lum**. 9-sinf §4–5 va §35–36 birlashtirilgan bo‘limlar alohida ikki marta sanalmaydi. Manba inventari tayyor darslar soni emas.

## Haqiqiy test natijalari

- backend: `92 passed, 1 skipped in 22.08s`.
- postgres: `1 passed, 76 deselected in 13.74s`.
- flutter: `01:20 +229: All tests passed!`.
- analyze: `No issues found! (ran in 1.4s)`.
- legacy_selected: `530 passed in 197.87s (0:03:17)`.
- legacy_full: `2335 passed, 5 skipped, 2 deselected, 13 warnings in 553.66s (0:09:13)`.
- flutter_history: `00:07 +77: All tests passed!`.

Source audit: 609 asl native sahifa, 131 sarlavha tasviri va **143 to‘liq dars manba sahifasi tasviri** xeshdan tekshirildi. Bu barcha kitoblardagi har bir tarixiy da’vo mustaqil ekspert tomonidan tasdiqlandi degani emas. `legacy_full` §1–25 checkpointida; `legacy_selected` §1–15 ustida; eng yangi partiya `backend/postgres/flutter` bilan keyin tekshirildi.

## Tekshiruv chegaralari

8-sinfning 45.4 MB skanerlangan PDF’i 32 MiB executor transfer limitidan o‘tmadi; uni to‘liq olingan, OCR qilingan yoki SHA tekshirilgan deb hisoblamaymiz. Sahifalar tartibi aniq ko‘rsatilgan, 32 MiB’dan kichik uzluksiz segmentlar kerak. 2026–2027 rasmiy dasturga moslik real proxy403 sabab tasdiqlanmadi. Mustaqil tarix o‘qituvchisi va real Android sinovi bajarilmagan. Android SDK/adb yo‘q; Gradle alohida History QA application ID integratsiyasi ham qolgan.

Barcha yangi darslar **lokal/test preview**, `course_ready=false`. Bob tugallanish belgisi alohida checkpoint quiz emas; alohida bob testlari hali yozilmagan. Erkin tarixiy tahlil uchun rubrika bor, lekin teacher workflow yoki avtomatik esse bahosi yo‘q. Hozirgi import faqat immutable `r1` darslar uchun; kelajak revision aktivlashtirish/unique constraint strategiyasi alohida integratsiya va migratsiya review talab qiladi. Mavjud revision yoki foydalanuvchi progressi qayta yozilmaydi.

Production router, fanlar katalogi, Google login, veb-sayt, Biology406 va Physics316 kontenti o‘zgartirilmagan. 552 mavjud backend fayli xeshi tekshiriladi. Kimyo268 va Jahon tarixi parallel remote branchlari saqlandi, ushbu Physics-base branchga merge qilinmagan; barcha fanlar bitta integration branchida testlandi deb aytilmaydi. PDF/OCR/kitob tasviri/transkript Gitga qo‘shilmagan. Main merge, production DB/import/deploy va AI Tutor/Explain yo‘q.

## Git va davom

Backend va Flutter: `feat/uzbekistan-history-curriculum`. Source checkpoint `d7d0510`; oldingi partiyalar `bf98c8c`/`a11c97d`/`4b51213`, Flutter `8490036`/`86402fc`/`bfef1a9`. Joriy partiya commitini `git log -1` va `git ls-remote` bilan tekshiring. Keyingi: **7-sinf §41, PDF/bosma 150 — Adabiyot**.

[Davom va dars manbalari](STAGE2_PROGRESS.md), [manba tafovutlari](SOURCE_REVIEW.md), [lokal QA chegaralari](LOCAL_QA.md).
