# Davom ettirish checkpointi — 2026-10-27

Bu yakuniy qabul yoki ommaviy release tasdig‘i emas. Keyingi sessiya ushbu ishni qayta boshlamasin.

## Bajarilgan qamrov

- 7-sinf: 42/42 dars. R1 fayllari va review xeshlari o‘zgarmagan.
- 8-sinf: 40 raqamlangan paragraf va bitta raqamsiz yakuniy mustaqil faoliyat, jami 41/41.
- 9-sinf: dastlabki 20 o‘quv birligi, asl §1–21. §4–5 birlashtirilgani uchun yo‘l raqami paragraf raqamiga teng emas.
- 10-sinf: 0/28; 11-sinf: 0/22. Manba kataloglari mavjud, interaktiv darslar hali yaratilmagan.
- Jami 103/172; 69 birlik qoladi: 9-sinf 19, 10-sinf 28, 11-sinf 22.

**Aniq keyingi joy: 9-sinf §22 — «Soliq va majburiyatlar. Xalq qo‘zg‘olonlari», PDF/bosma 78-sahifa. Yo‘ldagi sequence=21.**

78-sahifaning yuqorisi oldingi §21 davomi, pastidagi sarlavhadan §22 boshlanadi. Oldingi dars havolalaridagi end_before_y saqlansin. Keyingi paragrafning barcha sahifalarini va zarur tasvirlarini o‘qimasdan dars yaratilmang. 9-sinf §35–36 ham bitta o‘quv birligidir.

## Git va xavfsiz davom

Ikkala izolyatsiyalangan worktree ham feat/uzbekistan-history-curriculum branchida:

- Backend: /workspace/ilm-ai-uzbekistan-history
- Flutter: /workspace/ilm-ai-flutter-uzbekistan-history

Avval git status, worktree list, log va origin branch SHA tekshirilsin. Hech qanday reset --hard, force push yoki saqlanmagan ishni overwrite qilish kerak emas. Partiya4 kontenti va testlari shu branch checkpointida saqlanadi; aniq natijalar checkpoints/grade9_batch4.json ichida. Muhit vaqtincha uzilgan, qayta ulanganida barcha saqlanmagan fayllar joyida edi; o‘tgan testlar loglardan tekshirildi. Uzilishning o‘zi push muvaffaqiyati deb qabul qilinmagan.

7-sinfni qayta yaratmang. Boshqa fan branchlari, original worktreelar, veb-sayt va production bazaga tegmang. Oldingi foydalanuvchi progressi, XP, streak va sessiyalarni qayta hisoblamang. AI Tutor/Explain qo‘shmang.

## Manbalar

8-sinfning to‘rtta qismi ochilgan, har birida 40 sahifa, umumiy 1–160 tartibi uzluksiz. Segment SHA va bosma/PDF mappingi grade8_segments.json hamda GRADE8_SOURCE_REVIEW.md ichida. Yig‘ilgan lokal PDF SHA asl segmentlanmagan fayl SHA emas. PDF 1, 2, 159, 160 raqamsiz; 3–158 da printed=PDF. OCR yordamchi, fakt tasdig‘i uchun asl tasvir ishlatiladi.

PDF, asl sahifa tasviri, OCR va transkriptlar faqat xususiy manba papkalarida. Ularni Gitga qo‘shmang. Joriy muhitda /workspace/attachments va /workspace/.setup/uzbekistan-history/grade9 ichida fayllar bor; yangi muhitda avtomatik mavjud deb taxmin qilmang. Katalogdagi SHA bilan qayta tekshiring. 9-sinfning 5–78-sahifalari o‘qilgan; keyingi sahifalar qayta manba tekshiruvini talab qiladi.

## Tekshirish tartibi

Har 5–10 darsda original sahifa → original karta/mashq → literal mustaqil javob orakuli → validator → SQLite/API → lokal PostgreSQL fresh schema → haqiqiy public DTO capture → Flutter widget/analyze/full → hujjat → commit/push.

Eski R1 JSON va urinish snapshotlarini qayta yozmang. Yangi batchni BATCHES ga faqat manba tekshiruvi bilan ro‘yxatlang. Flutter fixture testini kengaytirishdan oldin yangi DTOlar haqiqatan capture qilingan bo‘lsin. Javob kalitlari, token va private grading_spec fixture yoki mijozga chiqmasin.

## Ochiq chegaralar

Mustaqil tarix o‘qituvchisi, rasmiy 2026–2027 dastur tekshiruvi va real Android QA bajarilmagan. Android SDK/adb yo‘q. Bob yakuni markerlari alohida checkpoint quiz emas. Teacher workflow, revision promotion va normal mobil/production integratsiyasi yakunlanmagan. Erkin tarixiy tahlil bitta matn kaliti bilan avtomatik baholanmaydi.

8-sinf yakunida keng backend 2429 passed / 6 opt-in PostgreSQL skipped / 2 sandbox deselected / 13 mavjud warning edi; bu keyingi 9-sinf kontenti uchun qayta o‘tgan full backend natijasi emas. Yangi partiyalarning targeted, PostgreSQL, Flutter va manba auditi natijalari alohida checkpointlarda. [Joriy hisobot](COURSE_COMPLETION.md), [davom](STAGE2_PROGRESS.md), [manba tafovutlari](SOURCE_REVIEW.md).
