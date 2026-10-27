# O‘zbekiston tarixi — joriy checkpoint

2026-10-27. **Kurs tugallanmagan: 83/172 o‘quv birligi lokal/test preview’da.** 7-sinf42/42 o‘zgarmadi; 8-sinf41/41. Jami 644 karta, 525 topshiriq (308 MCQ / 165 qisqa FRQ / 52 xronologiya), 83 original misol va 83 baholanmaydigan refleksiya.

| Sinf | Bob | O‘quv birligi | Lokal/test dars | Qolgan |
|---|---:|---:|---:|---:|
| 7 | 6 | 42 | 42 | 0 |
| 8 | 4 | 41 | 41 | 0 |
| 9 | 9 | 39 | 0 | 39 |
| 10 | 6 | 28 | 0 | 28 |
| 11 | 9 | 22 | 0 | 22 |

## Haqiqiy test natijalari

- backend: `193 passed, 2 skipped in 111.24s (0:01:51)`.
- postgres: `2 passed, 131 deselected in 41.45s`.
- flutter: `01:27 +277: All tests passed!`.
- flutter_history: `00:13 +123: All tests passed!`.
- analyze: `No issues found! (ran in 1.5s)`.
- biology_targeted: `included in current combined backend command: test_biology_curriculum.py + test_biology_segments.py`.

Source audit: 769 asl PDF sahifasi, 172 original sarlavha tasviri; 317 partiya-sahifa tasviri tekshiruvi. `--require-complete` endi haqiqatan exit0: yetishmagan8-sinf manbasi olindi. Bu kurs tayyorligi mezoni emas.

7-sinfdagi oldingi full backend2366passed/5skipped/2deselected/13warning; bu tarixiy checkpoint. Yangi8-sinf kontenti uchun yuqoridagi joriy targeted testlar haqiqiy bajarildi. Flutter full to‘plami eski Physics/brand testlarini ham o‘z ichiga oladi. Mustaqil fan branchlari integrated regressiondan o‘tdi deb aytilmaydi.

## Chegaralar

Barcha besh manba kataloglangan; bu barcha darslar yaratilgan degani emas. 8-sinf40raqamlangan paragraf va alohida yakuniy mustaqil dars jami41o‘quv birligi. 9-sinf§4–5 va§35–36 birlashtirilgan mavzular ikki marta sanalmaydi. Asl8-sinfning segmentlanmagan PDF SHA noma’lum; to‘rtta yuklangan qismning haqiqiy SHA va ulardan yig‘ilgan lokal fayl SHA alohida saqlangan.

Manba tasviri birlamchi; OCR faqat private locator.8-sinf native text watermark bo‘lib, dars matni emas. Har faktga asl sahifa tasviri SHA ham bog‘langan. O‘qituvchi ekspertizasi,2026–2027rasmiy dastur tasdig‘i va real Android QA bajarilmagan. Normal mobil katalog/productionga ulanmagan. Bob yakuni markerlari alohida checkpoint quiz emas; teacher workflow va r1dan keyingi revision promotion ham qolgan. AI Tutor/Explain yo‘q.

Biology406/Physics316 va552eski backend fayli,7-sinfning42r1darsi hamda oldingi4source book objekti xeshdan himoyalangan. Kimyo/Jahon tarixi branchlari merge yoki tahrir qilinmagan. Veb-sayt, production DB/import/deploy va main merge yo‘q. PDF/OCR/kitob tasvirlari Gitga qo‘shilmagan. Android QA Gradle patch faqat handoffda, SDKda build qilinmagan.

## Git va davom

Ikkala repo branchi `feat/uzbekistan-history-curriculum`. Avvalgi7-sinf backend `e293e48`,Flutter `f90637e` saqlandi. Ushbu checkpoint commitini remote SHA bilan tekshiring. **Keyingi: 9-sinf §1, PDF/bosma 5 — XIX asr o‘rtalarida O‘rta Osiyo davlatlarining hududi va aholisi (asl sahifalarni tekshirib davom eting).** Partiyalar orasida ruxsat talab qilinmaydi. [Manba auditi](GRADE8_SOURCE_REVIEW.md), [to‘liq xarita](COURSE_MAP.md), [davom](STAGE2_PROGRESS.md).


## 8-sinf to‘liq regression dalili

2429 passed, 6 skipped, 2 deselected, 13 warnings in 599.35s (0:09:59). Alohida PG2passed; Flutter277passed/analyze0. DebugJSwebbuildpassed; Android va teacher tasdig‘i yo‘q. [Logxeshlar va frozen content commitlar](checkpoints/grade8_validation.json).
