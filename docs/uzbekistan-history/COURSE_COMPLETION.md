# O‘zbekiston tarixi — joriy checkpoint

2026-10-27. **Kurs tugallanmagan: 47/172 o‘quv birligi lokal/test preview’da.** 7-sinf42/42 o‘zgarmadi; 8-sinf5/41. Jami 358 karta, 310 topshiriq (183 MCQ / 93 qisqa FRQ / 34 xronologiya), 47 original misol va 47 baholanmaydigan refleksiya.

| Sinf | Bob | O‘quv birligi | Lokal/test dars | Qolgan |
|---|---:|---:|---:|---:|
| 7 | 6 | 42 | 42 | 0 |
| 8 | 4 | 41 | 5 | 36 |
| 9 | 9 | 39 | 0 | 39 |
| 10 | 6 | 28 | 0 | 28 |
| 11 | 9 | 22 | 0 | 22 |

## Haqiqiy test natijalari

- backend: `112 passed, 2 skipped in 42.13s`.
- postgres: `2 passed, 87 deselected in 20.27s`.
- flutter: `01:24 +241: All tests passed!`.
- flutter_history: `00:10 +87: All tests passed!`.
- analyze: `No issues found! (ran in 1.5s)`.
- biology_targeted: `36 passed in 21.46s`.

Source audit: 769 asl PDF sahifasi, 172 original sarlavha tasviri; 165 partiya-sahifa tasviri tekshiruvi. `--require-complete` endi haqiqatan exit0: yetishmagan8-sinf manbasi olindi. Bu kurs tayyorligi mezoni emas.

7-sinfdagi oldingi full backend2366passed/5skipped/2deselected/13warning; bu tarixiy checkpoint. Yangi8-sinf kontenti uchun yuqoridagi joriy targeted testlar haqiqiy bajarildi. Flutter full to‘plami eski Physics/brand testlarini ham o‘z ichiga oladi. Mustaqil fan branchlari integrated regressiondan o‘tdi deb aytilmaydi.

## Chegaralar

Barcha besh manba kataloglangan; bu barcha darslar yaratilgan degani emas. 8-sinf40raqamlangan paragraf va alohida yakuniy mustaqil dars jami41o‘quv birligi. 9-sinf§4–5 va§35–36 birlashtirilgan mavzular ikki marta sanalmaydi. Asl8-sinfning segmentlanmagan PDF SHA noma’lum; to‘rtta yuklangan qismning haqiqiy SHA va ulardan yig‘ilgan lokal fayl SHA alohida saqlangan.

Manba tasviri birlamchi; OCR faqat private locator.8-sinf native text watermark bo‘lib, dars matni emas. Har faktga asl sahifa tasviri SHA ham bog‘langan. O‘qituvchi ekspertizasi,2026–2027rasmiy dastur tasdig‘i va real Android QA bajarilmagan. Normal mobil katalog/productionga ulanmagan. Bob yakuni markerlari alohida checkpoint quiz emas; teacher workflow va r1dan keyingi revision promotion ham qolgan. AI Tutor/Explain yo‘q.

Biology406/Physics316 va552eski backend fayli,7-sinfning42r1darsi hamda oldingi4source book objekti xeshdan himoyalangan. Kimyo/Jahon tarixi branchlari merge yoki tahrir qilinmagan. Veb-sayt, production DB/import/deploy va main merge yo‘q. PDF/OCR/kitob tasvirlari Gitga qo‘shilmagan. Android QA Gradle patch faqat handoffda, SDKda build qilinmagan.

## Git va davom

Ikkala repo branchi `feat/uzbekistan-history-curriculum`. Avvalgi7-sinf backend `e293e48`,Flutter `f90637e` saqlandi. Ushbu checkpoint commitini remote SHA bilan tekshiring. **Keyingi: 8-sinf §6, PDF/bosma 19 — Abdullaxon II davrida Buxoro xonligining yuksalishi.** Partiyalar orasida ruxsat talab qilinmaydi. [Manba auditi](GRADE8_SOURCE_REVIEW.md), [to‘liq xarita](COURSE_MAP.md), [davom](STAGE2_PROGRESS.md).
