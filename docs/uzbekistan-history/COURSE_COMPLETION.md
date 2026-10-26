# O‘zbekiston tarixi — joriy kurs checkpointi

2026-10-27. **Kurs tugallanmagan.** 7-sinf §1–42: **42 dars**, 325 karta, 42 original misol, 280 topshiriq (168 MCQ / 83 qisqa FRQ / 29 xronologiya), 42 avtomatik baholanmaydigan refleksiya/rubrika.

| Sinf | Bob | Katalogdagi mavzu | Interaktiv dars | Qolgan |
|---|---:|---:|---:|---:|
| 7 | 6 | 42 | 42 | 0 |
| 8 | ? | ? | 0 | Noma’lum: PDF olinmagan |
| 9 | 9 | 39 | 0 | 39 |
| 10 | 6 | 28 | 0 | 28 |
| 11 | 9 | 22 | 0 | 22 |

To‘rtta mavjud darslikda 131 ta mavzu guruhi kataloglangan; 89 tasi hali darsga aylantirilmagan. Beshala kitob jami **noma’lum**. 9-sinf §4–5 va §35–36 birlashtirilgan bo‘limlar alohida ikki marta sanalmaydi. Manba inventari tayyor darslar soni emas.

## Haqiqiy test natijalari

- backend: `94 passed, 1 skipped in 23.72s`.
- backend_full_current: `2366 passed, 5 skipped, 2 deselected, 13 warnings in 505.90s (0:08:25)`.
- sandbox_negative_guard: `1 passed in 0.81s`.
- postgres: `1 passed, 78 deselected in 14.19s`.
- flutter: `01:19 +235: All tests passed!`.
- analyze: `No issues found! (ran in 1.5s)`.
- legacy_selected: `530 passed in 197.87s (0:03:17)`.
- legacy_full: `2335 passed, 5 skipped, 2 deselected, 13 warnings in 553.66s (0:09:13)`.
- flutter_history: `00:08 +81: All tests passed!`.
- web_build: `debug JS build/web passed; compile-only invalid placeholder, no browser/Android run`.
- web_limit: `existing flutter_tts JS interop/Wasm dry-run warnings; Wasm not validated`.

Source audit: 609 asl native sahifa, 131 sarlavha tasviri va **150 partiya-sahifa tasviri tekshiruvi (148 noyob manba sahifasi)** xeshdan tekshirildi. Bu barcha kitoblardagi har bir tarixiy da’vo mustaqil ekspert tomonidan tasdiqlandi degani emas. `legacy_full` §1–25 checkpointida; `legacy_selected` §1–15 ustida; eng yangi partiya `backend/postgres/flutter` bilan keyin tekshirildi.

## Tekshiruv chegaralari

8-sinfning 45.4 MB skanerlangan PDF’i 32 MiB executor transfer limitidan o‘tmadi; uni to‘liq olingan, OCR qilingan yoki SHA tekshirilgan deb hisoblamaymiz. Sahifalar tartibi aniq ko‘rsatilgan, 32 MiB’dan kichik uzluksiz segmentlar kerak. 2026–2027 rasmiy dasturga moslik real proxy403 sabab tasdiqlanmadi. Mustaqil tarix o‘qituvchisi va real Android sinovi bajarilmagan. Android SDK/adb yo‘q; Gradle alohida History QA application ID integratsiyasi ham qolgan.

Barcha yangi darslar **lokal/test preview**, `course_ready=false`. Bob tugallanish belgisi alohida checkpoint quiz emas; alohida bob testlari hali yozilmagan. Erkin tarixiy tahlil uchun rubrika bor, lekin teacher workflow yoki avtomatik esse bahosi yo‘q. Hozirgi import faqat immutable `r1` darslar uchun; kelajak revision aktivlashtirish/unique constraint strategiyasi alohida integratsiya va migratsiya review talab qiladi. Mavjud revision yoki foydalanuvchi progressi qayta yozilmaydi.

Production router, fanlar katalogi, Google login, veb-sayt, Biology406 va Physics316 kontenti o‘zgartirilmagan. 552 mavjud backend fayli xeshi tekshiriladi. Kimyo268 va Jahon tarixi parallel remote branchlari saqlandi, ushbu Physics-base branchga merge qilinmagan; barcha fanlar bitta integration branchida testlandi deb aytilmaydi. PDF/OCR/kitob tasviri/transkript Gitga qo‘shilmagan. Main merge, production DB/import/deploy va AI Tutor/Explain yo‘q.

## Git va davom

Oxirgi kontent checkpointlari: backend **`7644bec6ff10a0cec60eb2daab7bd9a86b3dcc86`**, Flutter **`f90637ed39e2a2e58ad7d0601a4a5a0ab8b8501d`**; ikkala remote SHA `ls-remote` bilan tekshirildi. Bu hujjatning keyingi commitida kontent qayta yozilmadi.

Backend va Flutter: `feat/uzbekistan-history-curriculum`. Source checkpoint `d7d0510`; oldingi backend partiyalari `bf98c8c`/`a11c97d`/`4b51213`/`e9c8c9e`/`606d17d`/`4fdcc56`/`717d5ae`/`0661754`; Flutter `8490036`/`86402fc`/`bfef1a9`/`adaa2bb`/`0379d6b`/`eff2654`/`bdfa3ad`/`248e6e9`. Joriy partiya commitini `git log -1` va `git ls-remote` bilan tekshiring. Keyingi: **8-sinf: manba PDF segmentlari olinmaguncha bloklangan**.

[Davom va dars manbalari](STAGE2_PROGRESS.md), [manba tafovutlari](SOURCE_REVIEW.md), [lokal QA chegaralari](LOCAL_QA.md), [8-sinf manba handoffi](SOURCE_HANDOFF.md).

## Yakuniy regression qaydi

2366-testli full run7-sinf42dars va yangi backend validator/grader/runtime bilan bajarildi.5PostgreSQL opt-in holati oddiy run’da skip; History uchun alohida real lokal PostgreSQL fresh-schema testi1passed.2sandbox-nomli test full commandda deselect qilingan: tashqi Gitdan tashqarida yangi sandbox yaratadigan ijobiy CLI sinovi bu muhitda bajarilmaydi; guardning salbiy testi esa alohida1passed. Guard chetlab o‘tilmadi.13oldingi Pydantic/FastAPI/SQLAlchemy deprecation/query warning saqlandi.

`--require-complete` ham joriy42dars bilan real ishga tushirilib kutilgan exit2 qaytardi:8-sinf yo‘qligi yashirilmaydi. Buyruqning muvaffaqiyatsiz completeness natijasi to‘liq kurs tayyor degan da’voni to‘sadi. [Mashina o‘qiydigan dalillar](checkpoints/grade7_validation.json).
