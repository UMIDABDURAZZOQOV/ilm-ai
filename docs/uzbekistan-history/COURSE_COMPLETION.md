# O‘zbekiston tarixi — joriy checkpoint

2026-10-27. **Kurs tugallanmagan: 137/172 o‘quv birligi lokal/test preview’da.** Jami 1033 karta, 837 topshiriq (492 MCQ / 272 qisqa FRQ / 73 xronologiya), 137 original misol va 137 avtomatik baholanmaydigan refleksiya. 7-sinf42/42 immutable;8-sinf40paragraf+1raqamsizyakuniyfaoliyat=41/41 saqlandi.

| Sinf | Bob | O‘quv birligi | Lokal/test dars | Qolgan | Karta | Savol | Qisqa FRQ |
|---|---:|---:|---:|---:|---:|---:|---:|
| 7 | 6 | 42 | 42 | 0 | 325 | 280 | 83 |
| 8 | 4 | 41 | 41 | 0 | 319 | 245 | 82 |
| 9 | 9 | 39 | 39 | 0 | 293 | 230 | 77 |
| 10 | 6 | 28 | 15 | 13 | 96 | 82 | 30 |
| 11 | 9 | 22 | 0 | 22 | 0 | 0 | 0 |

## Joriy testlar

- backend: `249 passed, 4 skipped in 206.55s (0:03:26)`.
- postgres: `4 passed, 187 deselected in 70.76s (0:01:10)`.
- flutter: `01:26 +333: All tests passed!`.
- flutter_history: `00:20 +179: All tests passed!`.
- analyze: `No issues found! (ran in 1.5s)`.

Source audit: 769 asl sahifa, 172 sarlavha va 553 partiya-sahifa tasviri. `--require-complete` manbalar mavjudligi uchun exit0, kurs/publicrelease tasdig‘i emas.

## Tekshiruv chegaralari

Barcha5kitobning769PDFsahifasi va172asosiy sarlavhasi kataloglangan. Bu hali yaratilmagan darslarning faktlari tekshirildi degani emas. 8-sinf scanned:4ta40sahifalik segment SHA,160asl sahifa pixel SHA va printed mapping saqlangan;original unsplit SHA taxmin qilinmagan. PDF3–158printed=PDF;1,2,159,160raqamsiz. OCR faqat private locator.9-sinf§4–5 va§35–36birlashtirilgan, ikki marta sanalmaydi.

Joriy targeted to‘plam eski7/8kontent/API/progress/XP hamda Biology validatorlarini ham bajaradi. 8-sinf83darsdagi keng backend:2429passed/6opt-inPGskipped/2sandboxdeselected/13existingwarning599.35s;Flutter277passed/analyze0/debugJSwebbuildpassed. [Frozen validation](checkpoints/grade8_validation.json). 9-sinf122darsdagi yangi keng backend:2469passed/7opt-inPGskipped/2sandboxdeselected/13oldwarning641.83s;Flutter317passed/history163/analyze0. [9-sinf frozen validation](checkpoints/grade9_validation.json). Bu keyingi10/11-sinf kontentiga full test o‘tdi degani emas. Xavfsiz lokal PGfreshschema testlari joriy partiya bilan qayta bajariladi.

Mustaqil tarix o‘qituvchisi, rasmiy2026–2027dastur tasdig‘i va realAndroidQA bajarilmagan. AndroidSDK/adb yo‘q;GradleidentitypatchfaqatFlutterhandoffda. Normalmobil/productionroutergaulanmagan. Bobyakunimarkerlarialohidacheckpointquizemas;teacherworkflow/r1revisionpromotion/publicreleasehaliqolgan. AI Tutor/Explainyo‘q. SandboxCLI tashqi-Gitguardchetlabo‘tilmagan.

Biology406/Physics316 va552eski backend fayli,7-sinf42r1 hamda oldingi4sourcebookobyekti SHA bilan himoyalangan. Kimyo/Jahontarixibranchlarigategilmadi. Vebsayt/productionDB/deploy/mainmergeyo‘q. PDF/OCR/rasm/transkriptGitgakiritilmadi.

## Git va davom

Ikkala repo branchi `feat/uzbekistan-history-curriculum`. Partiya commitini remote SHA bilan tekshiring. **Keyingi: 10-sinf §16, PDF 87, bosma 87 — Ikkinchi jahon urushining boshlanishi hamda O‘zbekistonning urush girdobiga tortilishi.** Oddiy partiyalar uchun qayta ruxsat talab qilinmaydi.
