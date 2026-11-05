# IV qism — faqat lokal QA

2026-11-05:joriy IV10/33, jami120lokal dars. [Batch2dalili](checkpoints/grade1_part4_batch2.json).
Keyingi122/PDF25–26/bosma24–25. Quyidagi112–116raqamlari birinchi partiya tarixi.

2026-11-04. Hozir 112–116 / path1–5 interaktiv; keyingi117, PDF15–16/bosma14–15.
Qolgan28 mavzu header/footer xaritasi bilan cheklangan, tayyor dars emas.
IV qism 2023-yilgi nashr; III qism 2024 qayta ishlangan nashr.
Publisher raqami112 boshlanishini oldingi qismga moslab almashtirmang.

## Default va ruxsat doirasi

Server default strict: III qismdagi5schedule-only nazorat/o‘yin tanasi yo‘qligi
uchun IV ochilmaydi. Bu qatorlar va II74 tugallangan deb belgilanmagan.
`MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE=true` faqat alohida lokal/test muhitida,
`MATHEMATICS_QA_SOURCE_GAP_BRIDGE=true` bilan birga va oldingi110mavjud darsning
barchasi shu akkauntda bajarilgan bo‘lsa, IVni sinashga imkon beradi.

Manba juftligining SHA-256lari, aynan37IIIkey/sequence, avvalgi73darsning
prerequisitelari va5schedule-onlylabel tekshiriladi. Boshqa sinf/qism yoki
o‘zgargan manba uchun umumiy exception berilmaydi. Request orqali yoqish mumkin emas.
`previous_book_complete=false`, `course_ready=false` saqlanadi; UI sababi va
ikki nashrning raqam farqini ko‘rsatadi. Bu production flagi emas.

Flag o‘chirilsa tugallanmagan IVurinishga start/answer403qaytadi. Tayyor
natija, foydalanuvchi progressi va XP o‘chirilmaydi. Urinishni qayta tekshirish
endi snapshotdagi haqiqiy grade/partni ishlatadi; IIIga hardcode qilinmaydi.
Umumiy Google login, normal app/katalog, boshqa fanlar yoki frontend o‘zgarmagan.

## Lokal buyruq

Faqat o‘zingizning barcha Git repositorylardan tashqaridagi yangi papkangizda:

```powershell
python -m scripts.serve_mathematics_preview --directory C:\ILM-local\mathematics_staging --allow-known-part2-source-gap --allow-known-part3-schedule-gap
```

Qayta ochishda `--resume` va ikkala kerakli flag aniq beriladi. Private
`flutter-defines.json` ichidagi bir soatlik test JWTni Git yoki logga kiritmang.

```powershell
flutter run -d chrome -t lib/mathematics_preview_main.dart --dart-define-from-file=C:\ILM-local\mathematics_staging\flutter-defines.json
```

Bu Windows buyruqlari hali o‘sha kompyuterda tekshirilmagan. Cloud `/workspace`
va `/tmp` Git ancestor guardi sabab standalone positive-run bajarilmagan;
guard chetlab o‘tilmagan. Authenticated TestClient/SQLite va faqat o‘zimizning
loopback PostgreSQL sxemasi sinovlar uchun ishlatiladi. Help/parser tekshirildi.

## Model chegaralari

Raqamli chizg‘ich cm yorliqlari bilan intervalni tekshiradi; telefon pikseli
fizik santimetrga teng deyilmaydi. Kesma chizish mahorati yoki qo‘lyozma
modeldagi muvaffaqiyatdan avtomatik tasdiqlanmaydi. Bo‘g‘inlar jami uchlar
orasidagi to‘g‘ri kesma uzunligi deb olinmaydi. Oddiy yopiq3–6uchli shakllar
ishlatiladi; umumiy topologiya/CAS/yuza formulalari qo‘shilmagan.

Mustaqil o‘qituvchi, real Android, TalkBack va o‘quvchilar bilan pilot
tekshiruvi hali bajarilmagan. Haqiqiy avtomatik natijalar [QA_REPORT.md](QA_REPORT.md)
va tegishli checkpointda saqlanadi. Faqat debug/local preview.
