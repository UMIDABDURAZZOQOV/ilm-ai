# Davom checkpointi — 2026-10-27

2026-10-27. **Kurs tugallanmagan: 127/172 o‘quv birligi lokal/test preview’da.** Jami 965 karta, 780 topshiriq (462 MCQ / 252 qisqa FRQ / 66 xronologiya), 127 original misol va 127 avtomatik baholanmaydigan refleksiya. 7-sinf42/42 immutable;8-sinf40paragraf+1raqamsizyakuniyfaoliyat=41/41 saqlandi.

| Sinf | Bob | O‘quv birligi | Lokal/test dars | Qolgan | Karta | Savol | Qisqa FRQ |
|---|---:|---:|---:|---:|---:|---:|---:|
| 7 | 6 | 42 | 42 | 0 | 325 | 280 | 83 |
| 8 | 4 | 41 | 41 | 0 | 319 | 245 | 82 |
| 9 | 9 | 39 | 39 | 0 | 293 | 230 | 77 |
| 10 | 6 | 28 | 5 | 23 | 28 | 25 | 10 |
| 11 | 9 | 22 | 0 | 22 | 0 | 0 | 0 |

**Keyingi: 10-sinf §6, PDF 31, bosma 31 — Buxoro amirligida islohotlar uchun kurash hamda qizil armiya tomonidan amir hokimiyatining ag‘darilishi. BXSRning tashkil topishi va faoliyati.** Yo‘ldagi sequence=6.

Backend va Flutter branchi: feat/uzbekistan-history-curriculum. Worktreelar: /workspace/ilm-ai-uzbekistan-history va /workspace/ilm-ai-flutter-uzbekistan-history. Avval git status/worktree/log va remote SHA tekshirilsin; saqlanmagan ishlar overwrite yoki reset qilinmasin. Tayyor R1 darslarni qayta yaratmang.

PDF manbalar /workspace/attachments ichida, xususiy sahifa tasvirlari /workspace/.setup/uzbekistan-history ichida mavjud. Yangi muhitda ularni mavjud deb taxmin qilmang, katalog SHA bilan tekshiring. Yangi darsdan oldin uning barcha asl sahifalarini va chegaralarini o‘qing. OCR faqat locator. PDF, tasvir, OCR yoki transkriptni Gitga qo‘shmang.

Har 5–10 dars: original manba, karta/MCQ/FRQ, mustaqil literal javob orakuli, validator, SQLite/API, lokal PostgreSQL fresh schema, yangi public DTO capture, Flutter widget/analyze/full, hujjat, commit/push. Capture tugamasdan Flutter fixture testini kengaytirmang. Javob kaliti va tokenlar mijozga chiqarilmasin. Oddiy partiyalarda tasdiq kutmang. Boshqa fanlar, veb, production va main mergega tegmang.

- backend: `239 passed, 4 skipped in 208.51s (0:03:28)`.
- postgres: `4 passed, 177 deselected in 72.66s (0:01:12)`.
- flutter: `01:31 +323: All tests passed!`.
- flutter_history: `00:18 +169: All tests passed!`.
- analyze: `No issues found! (ran in 1.5s)`.

## Tekshiruv chegaralari

Barcha5kitobning769PDFsahifasi va172asosiy sarlavhasi kataloglangan. Bu hali yaratilmagan darslarning faktlari tekshirildi degani emas. 8-sinf scanned:4ta40sahifalik segment SHA,160asl sahifa pixel SHA va printed mapping saqlangan;original unsplit SHA taxmin qilinmagan. PDF3–158printed=PDF;1,2,159,160raqamsiz. OCR faqat private locator.9-sinf§4–5 va§35–36birlashtirilgan, ikki marta sanalmaydi.

Joriy targeted to‘plam eski7/8kontent/API/progress/XP hamda Biology validatorlarini ham bajaradi. 8-sinf83darsdagi keng backend:2429passed/6opt-inPGskipped/2sandboxdeselected/13existingwarning599.35s;Flutter277passed/analyze0/debugJSwebbuildpassed. [Frozen validation](checkpoints/grade8_validation.json). 9-sinf122darsdagi yangi keng backend:2469passed/7opt-inPGskipped/2sandboxdeselected/13oldwarning641.83s;Flutter317passed/history163/analyze0. [9-sinf frozen validation](checkpoints/grade9_validation.json). Bu keyingi10/11-sinf kontentiga full test o‘tdi degani emas. Xavfsiz lokal PGfreshschema testlari joriy partiya bilan qayta bajariladi.

Mustaqil tarix o‘qituvchisi, rasmiy2026–2027dastur tasdig‘i va realAndroidQA bajarilmagan. AndroidSDK/adb yo‘q;GradleidentitypatchfaqatFlutterhandoffda. Normalmobil/productionroutergaulanmagan. Bobyakunimarkerlarialohidacheckpointquizemas;teacherworkflow/r1revisionpromotion/publicreleasehaliqolgan. AI Tutor/Explainyo‘q. SandboxCLI tashqi-Gitguardchetlabo‘tilmagan.

Biology406/Physics316 va552eski backend fayli,7-sinf42r1 hamda oldingi4sourcebookobyekti SHA bilan himoyalangan. Kimyo/Jahontarixibranchlarigategilmadi. Vebsayt/productionDB/deploy/mainmergeyo‘q. PDF/OCR/rasm/transkriptGitgakiritilmadi.
