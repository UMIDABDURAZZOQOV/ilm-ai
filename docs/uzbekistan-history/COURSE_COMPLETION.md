# O‘zbekiston tarixi — joriy checkpoint

2026-10-27. **Kurs tugallanmagan: 165/172 o‘quv birligi lokal/test preview’da.** Jami 1230 karta, 989 topshiriq (576 MCQ / 328 qisqa FRQ / 85 xronologiya), 165 original misol va 165 avtomatik baholanmaydigan refleksiya. 7-sinf42/42 immutable;8-sinf40paragraf+1raqamsizyakuniyfaoliyat=41/41 saqlandi.

| Sinf | Bob | O‘quv birligi | Lokal/test dars | Qolgan | Karta | Savol | Qisqa FRQ |
|---|---:|---:|---:|---:|---:|---:|---:|
| 7 | 6 | 42 | 42 | 0 | 325 | 280 | 83 |
| 8 | 4 | 41 | 41 | 0 | 319 | 245 | 82 |
| 9 | 9 | 39 | 39 | 0 | 293 | 230 | 77 |
| 10 | 6 | 28 | 28 | 0 | 184 | 155 | 56 |
| 11 | 9 | 22 | 15 | 7 | 109 | 79 | 30 |

## Joriy testlar

- backend: `278 passed, 5 skipped in 277.13s (0:04:37)`.
- postgres: `5 passed, 216 deselected in 94.79s (0:01:34)`.
- flutter: `01:23 +362: All tests passed!`.
- flutter_history: `00:22 +208: All tests passed!`.
- analyze: `No issues found! (ran in 1.6s)`.

Source audit: 769 asl sahifa, 172 sarlavha va 707 partiya-sahifa tasviri. `--require-complete` manbalar mavjudligi uchun exit0, kurs/publicrelease tasdig‘i emas.

## Tekshiruv chegaralari

Barcha5kitobning769PDFsahifasi va172asosiy sarlavhasi kataloglangan. Bu hali yaratilmagan darslarning faktlari tekshirildi degani emas. 8-sinf scanned:4ta40sahifalik segment SHA,160asl sahifa pixel SHA va printed mapping saqlangan;original unsplit SHA taxmin qilinmagan. PDF3–158printed=PDF;1,2,159,160raqamsiz. OCR faqat private locator.9-sinf§4–5 va§35–36birlashtirilgan, ikki marta sanalmaydi.

Joriy targeted to‘plam eski7/8kontent/API/progress/XP hamda Biology validatorlarini ham bajaradi. 8-sinf83darsdagi keng backend:2429passed/6opt-inPGskipped/2sandboxdeselected/13existingwarning599.35s;Flutter277passed/analyze0/debugJSwebbuildpassed. [Frozen validation](checkpoints/grade8_validation.json). 9-sinf122darsdagi yangi keng backend:2469passed/7opt-inPGskipped/2sandboxdeselected/13oldwarning641.83s;Flutter317passed/history163/analyze0. [9-sinf frozen validation](checkpoints/grade9_validation.json). 10-sinf150darsdagi yangi keng backend:2498passed/8opt-inPGskipped/2sandboxdeselected/13oldwarning767.30s;Flutter346passed/history192/analyze0. [10-sinf frozen validation](checkpoints/grade10_validation.json). Bu keyingi11-sinf kontentiga full test o‘tdi degani emas. Xavfsiz lokal PGfreshschema testlari joriy partiya bilan qayta bajariladi.

Mustaqil tarix o‘qituvchisi, rasmiy2026–2027dastur tasdig‘i va realAndroidQA bajarilmagan. AndroidSDK/adb yo‘q;GradleidentitypatchfaqatFlutterhandoffda. Normalmobil/productionroutergaulanmagan. Bobyakunimarkerlarialohidacheckpointquizemas;teacherworkflow/r1revisionpromotion/publicreleasehaliqolgan. AI Tutor/Explainyo‘q. SandboxCLI tashqi-Gitguardchetlabo‘tilmagan.

Biology406/Physics316 va552eski backend fayli,7-sinf42r1 hamda oldingi4sourcebookobyekti SHA bilan himoyalangan. Kimyo/Jahontarixibranchlarigategilmadi. Vebsayt/productionDB/deploy/mainmergeyo‘q. PDF/OCR/rasm/transkriptGitgakiritilmadi.

## Git va davom

Ikkala repo branchi `feat/uzbekistan-history-curriculum`. Partiya commitini remote SHA bilan tekshiring. **Keyingi: 11-sinf §16, PDF 102, bosma 102 — O‘zbekistonda madaniyat va san’at.** Oddiy partiyalar uchun qayta ruxsat talab qilinmaydi.
