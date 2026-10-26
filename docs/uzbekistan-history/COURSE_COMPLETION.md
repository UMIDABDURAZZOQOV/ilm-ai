# O‘zbekiston tarixi — tugallanmagan kurs, birinchi interaktiv checkpoint

2026-10-26. **To‘liq kurs tayyor emas.** 7-sinfning §1–5 mavzusi uchun 5 dars yozildi: 34 karta, 5 original misol, 20 MCQ, 10 qisqa FRQ va 4 xronologiya topshirig‘i; 5 tahlil/rubrika avtomatik baholanmaydi.

| Sinf | Bob | Kataloglangan mavzu | Interaktiv dars | Qolgan mavzu |
|---|---:|---:|---:|---:|
| 7 | 6 | 42 | 5 | 37 |
| 8 | ? | ? | 0 | PDF transferi bloklangan |
| 9 | 9 | 39 | 0 | 39 |
| 10 | 6 | 28 | 0 | 28 |
| 11 | 9 | 22 | 0 | 22 |

Mavjud 4 kitobda 131 ta o‘quv mavzu guruhi bor; beshala kitobning jami soni hali noma’lum. §4–5 va §35–36 birlashtirilgan 9-sinf mavzulari ikki marta sanalmagan. Barcha 609 mavjud PDF sahifasining native xeshlari, 131 sarlavha tasviri va birinchi darslarda ishlatilgan 13 to‘liq asl sahifa tasviri audit qilindi. Metadata yoki sarlavha auditi kitobdagi barcha tarixiy faktlar tekshirildi degani emas.

## Bajarilgan tekshiruvlar

- Manba va interaktiv backend testlari: **42 passed, 1 opt-in PostgreSQL skipped, 3.42 s**.
- Alohida real lokal PostgreSQL fresh schema: **1 passed, 26 deselected, 3.86 s**; 5 dars, qayta import/replay, 50 XP, yakunda 137→187 va parallel completion sinovi. Faqat yangi test schema yaratilib, so‘ng o‘chirildi; productionga tegilmadi.
- Flutter: **169 passed, 90 s**, shundan 15 ta yangi History testi. 320×568 va 200% matn, qisqa FRQ inputi, xronologiya, sinf tanlash, 8-sinf empty state, source dialog, internet xatosi va retry tekshirildi. **Analyze: No issues found, 1.9 s.**
- Source validator: 4 kitob / 609 sahifa / 131 sarlavha tasviri / 13 dars manba sahifasi; 34 topshiriq. Ruff toza. Mavjud 552 backend fayli xeshi saqlandi.
- To‘liq backend regression sinovi shu checkpoint yozilayotganida hali ishlamoqda; natijasini keyingi checkpointda qayd etish kerak. Hozir muvaffaqiyatli deb hisoblanmaydi.

## Chegaralar va ochiq masalalar

8-sinf 45.4 MB skaner PDF’i 32 MiB transfer limitidan o‘tmadi. Uzluksiz kichik segmentlar kerak; OCR/manba tasviri hali olinmagan. 2026–2027 rasmiy dastur bilan moslik real proxy 403 sabab tasdiqlanmadi. Mustaqil tarix o‘qituvchisi, real Android, native accessibility va umumiy foydalanuvchi release’i hali tasdiqlanmagan. Bob belgisi alohida checkpoint testi emas.

History faqat izolyatsiyalangan lokal/test router va Flutter entrypointda. Production app/router/katalog, Google login, veb-sayt, Biology/Physics kontenti o‘zgarmadi. Chemistry va Jahon tarixi alohida ref/worktree holida saqlandi, bu branchga merge qilinmadi; bitta integrated branchda ularning regressioni tekshirildi deb da’vo qilinmaydi. Baza va server production import/deploy qilinmadi; main merge yo‘q.

Git: backend/Flutter `feat/uzbekistan-history-curriculum`; dastlabki manba checkpointi `d7d0510`. Ushbu partiya commit SHA sini `git log` orqali tekshiring (hujjat ichiga o‘z commit xeshini qo‘yish mumkin emas). Davom nuqtasi va aniq source chegaralari: [STAGE2_PROGRESS.md](STAGE2_PROGRESS.md). Lokal ishga tushirish chegaralari: [LOCAL_QA.md](LOCAL_QA.md).
