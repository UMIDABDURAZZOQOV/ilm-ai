# Davom checkpointi — 2026-10-27

2026-10-27. **Kurs tugallanmagan: 122/172 o‘quv birligi lokal/test preview’da.** Jami 937 karta, 755 topshiriq (447 MCQ / 242 qisqa FRQ / 66 xronologiya), 122 original misol va 122 avtomatik baholanmaydigan refleksiya. 7-sinf42/42 immutable;8-sinf40paragraf+1raqamsizyakuniyfaoliyat=41/41 saqlandi.

| Sinf | Bob | O‘quv birligi | Lokal/test dars | Qolgan | Karta | Savol | Qisqa FRQ |
|---|---:|---:|---:|---:|---:|---:|---:|
| 7 | 6 | 42 | 42 | 0 | 325 | 280 | 83 |
| 8 | 4 | 41 | 41 | 0 | 319 | 245 | 82 |
| 9 | 9 | 39 | 39 | 0 | 293 | 230 | 77 |
| 10 | 6 | 28 | 0 | 28 | 0 | 0 | 0 |
| 11 | 9 | 22 | 0 | 22 | 0 | 0 | 0 |

**Keyingi: 10-sinf §1, PDF 5, bosma 5 — Turkiston o‘lkasi 1917-yil fevral – oktyabr oralig‘ida.** Yo‘ldagi sequence=1.

Backend va Flutter branchi: feat/uzbekistan-history-curriculum. Worktreelar: /workspace/ilm-ai-uzbekistan-history va /workspace/ilm-ai-flutter-uzbekistan-history. Avval git status/worktree/log va remote SHA tekshirilsin; saqlanmagan ishlar overwrite yoki reset qilinmasin. Tayyor R1 darslarni qayta yaratmang.

PDF manbalar /workspace/attachments ichida, xususiy sahifa tasvirlari /workspace/.setup/uzbekistan-history ichida mavjud. Yangi muhitda ularni mavjud deb taxmin qilmang, katalog SHA bilan tekshiring. Yangi darsdan oldin uning barcha asl sahifalarini va chegaralarini o‘qing. OCR faqat locator. PDF, tasvir, OCR yoki transkriptni Gitga qo‘shmang.

Har 5–10 dars: original manba, karta/MCQ/FRQ, mustaqil literal javob orakuli, validator, SQLite/API, lokal PostgreSQL fresh schema, yangi public DTO capture, Flutter widget/analyze/full, hujjat, commit/push. Capture tugamasdan Flutter fixture testini kengaytirmang. Javob kaliti va tokenlar mijozga chiqarilmasin. Oddiy partiyalarda tasdiq kutmang. Boshqa fanlar, veb, production va main mergega tegmang.

- backend: `233 passed, 3 skipped in 187.00s (0:03:07)`.
- postgres: `3 passed, 171 deselected in 63.95s (0:01:03)`.
- flutter: `01:29 +317: All tests passed!`.
- flutter_history: `00:17 +163: All tests passed!`.
- analyze: `No issues found! (ran in 1.5s)`.

## Tekshiruv chegaralari

Barcha5kitobning769PDFsahifasi va172asosiy sarlavhasi kataloglangan. Bu hali yaratilmagan darslarning faktlari tekshirildi degani emas. 8-sinf scanned:4ta40sahifalik segment SHA,160asl sahifa pixel SHA va printed mapping saqlangan;original unsplit SHA taxmin qilinmagan. PDF3–158printed=PDF;1,2,159,160raqamsiz. OCR faqat private locator.9-sinf§4–5 va§35–36birlashtirilgan, ikki marta sanalmaydi.

Joriy targeted to‘plam eski7/8kontent/API/progress/XP hamda Biology validatorlarini ham bajaradi. 8-sinf83darsdagi keng backend:2429passed/6opt-inPGskipped/2sandboxdeselected/13existingwarning599.35s;Flutter277passed/analyze0/debugJSwebbuildpassed. [Frozen validation](checkpoints/grade8_validation.json). Bu keyingi9-sinf kontentiga full test o‘tdi degani emas. Xavfsiz lokal PGfreshschema testlari joriy partiya bilan qayta bajariladi.

Mustaqil tarix o‘qituvchisi, rasmiy2026–2027dastur tasdig‘i va realAndroidQA bajarilmagan. AndroidSDK/adb yo‘q;GradleidentitypatchfaqatFlutterhandoffda. Normalmobil/productionroutergaulanmagan. Bobyakunimarkerlarialohidacheckpointquizemas;teacherworkflow/r1revisionpromotion/publicreleasehaliqolgan. AI Tutor/Explainyo‘q. SandboxCLI tashqi-Gitguardchetlabo‘tilmagan.

Biology406/Physics316 va552eski backend fayli,7-sinf42r1 hamda oldingi4sourcebookobyekti SHA bilan himoyalangan. Kimyo/Jahontarixibranchlarigategilmadi. Vebsayt/productionDB/deploy/mainmergeyo‘q. PDF/OCR/rasm/transkriptGitgakiritilmadi.
