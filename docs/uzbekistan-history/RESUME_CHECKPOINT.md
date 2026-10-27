# Davom checkpointi — 2026-10-27

2026-10-27. **Kurs tugallanmagan: 132/172 o‘quv birligi lokal/test preview’da.** Jami 999 karta, 809 topshiriq (477 MCQ / 262 qisqa FRQ / 70 xronologiya), 132 original misol va 132 avtomatik baholanmaydigan refleksiya. 7-sinf42/42 immutable;8-sinf40paragraf+1raqamsizyakuniyfaoliyat=41/41 saqlandi.

| Sinf | Bob | O‘quv birligi | Lokal/test dars | Qolgan | Karta | Savol | Qisqa FRQ |
|---|---:|---:|---:|---:|---:|---:|---:|
| 7 | 6 | 42 | 42 | 0 | 325 | 280 | 83 |
| 8 | 4 | 41 | 41 | 0 | 319 | 245 | 82 |
| 9 | 9 | 39 | 39 | 0 | 293 | 230 | 77 |
| 10 | 6 | 28 | 10 | 18 | 62 | 54 | 20 |
| 11 | 9 | 22 | 0 | 22 | 0 | 0 | 0 |

**Keyingi: 10-sinf §11, PDF 61, bosma 61 — O‘zbekistonda qishloq xo‘jaligini kollektivlashtirish siyosati hamda quloqlarning surgun qilinishi.** Yo‘ldagi sequence=11.

Backend va Flutter branchi: feat/uzbekistan-history-curriculum. Worktreelar: /workspace/ilm-ai-uzbekistan-history va /workspace/ilm-ai-flutter-uzbekistan-history. Avval git status/worktree/log va remote SHA tekshirilsin; saqlanmagan ishlar overwrite yoki reset qilinmasin. Tayyor R1 darslarni qayta yaratmang.

PDF manbalar /workspace/attachments ichida, xususiy sahifa tasvirlari /workspace/.setup/uzbekistan-history ichida mavjud. Yangi muhitda ularni mavjud deb taxmin qilmang, katalog SHA bilan tekshiring. Yangi darsdan oldin uning barcha asl sahifalarini va chegaralarini o‘qing. OCR faqat locator. PDF, tasvir, OCR yoki transkriptni Gitga qo‘shmang.

Har 5–10 dars: original manba, karta/MCQ/FRQ, mustaqil literal javob orakuli, validator, SQLite/API, lokal PostgreSQL fresh schema, yangi public DTO capture, Flutter widget/analyze/full, hujjat, commit/push. Capture tugamasdan Flutter fixture testini kengaytirmang. Javob kaliti va tokenlar mijozga chiqarilmasin. Oddiy partiyalarda tasdiq kutmang. Boshqa fanlar, veb, production va main mergega tegmang.

- backend: `244 passed, 4 skipped in 203.54s (0:03:23)`.
- postgres: `4 passed, 182 deselected in 70.89s (0:01:10)`.
- flutter: `01:24 +328: All tests passed!`.
- flutter_history: `00:18 +174: All tests passed!`.
- analyze: `No issues found! (ran in 1.5s)`.

## Tekshiruv chegaralari

Barcha5kitobning769PDFsahifasi va172asosiy sarlavhasi kataloglangan. Bu hali yaratilmagan darslarning faktlari tekshirildi degani emas. 8-sinf scanned:4ta40sahifalik segment SHA,160asl sahifa pixel SHA va printed mapping saqlangan;original unsplit SHA taxmin qilinmagan. PDF3–158printed=PDF;1,2,159,160raqamsiz. OCR faqat private locator.9-sinf§4–5 va§35–36birlashtirilgan, ikki marta sanalmaydi.

Joriy targeted to‘plam eski7/8kontent/API/progress/XP hamda Biology validatorlarini ham bajaradi. 8-sinf83darsdagi keng backend:2429passed/6opt-inPGskipped/2sandboxdeselected/13existingwarning599.35s;Flutter277passed/analyze0/debugJSwebbuildpassed. [Frozen validation](checkpoints/grade8_validation.json). 9-sinf122darsdagi yangi keng backend:2469passed/7opt-inPGskipped/2sandboxdeselected/13oldwarning641.83s;Flutter317passed/history163/analyze0. [9-sinf frozen validation](checkpoints/grade9_validation.json). Bu keyingi10/11-sinf kontentiga full test o‘tdi degani emas. Xavfsiz lokal PGfreshschema testlari joriy partiya bilan qayta bajariladi.

Mustaqil tarix o‘qituvchisi, rasmiy2026–2027dastur tasdig‘i va realAndroidQA bajarilmagan. AndroidSDK/adb yo‘q;GradleidentitypatchfaqatFlutterhandoffda. Normalmobil/productionroutergaulanmagan. Bobyakunimarkerlarialohidacheckpointquizemas;teacherworkflow/r1revisionpromotion/publicreleasehaliqolgan. AI Tutor/Explainyo‘q. SandboxCLI tashqi-Gitguardchetlabo‘tilmagan.

Biology406/Physics316 va552eski backend fayli,7-sinf42r1 hamda oldingi4sourcebookobyekti SHA bilan himoyalangan. Kimyo/Jahontarixibranchlarigategilmadi. Vebsayt/productionDB/deploy/mainmergeyo‘q. PDF/OCR/rasm/transkriptGitgakiritilmadi.
