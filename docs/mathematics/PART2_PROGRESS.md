# Matematika II qism — joriy davom

## 2026-11-04 — II qism42–46: jami46 tekshirilgan dars

I qismning41 darsi va barcha JSON/reviewlari byte-for-byte saqlandi. II qismning birinchi5 mavzusi qo‘shildi:30 karta,5 original misol/15 qadam,40 topshiriq va9 sonli tenglik. Jami46 dars,260 karta,328 topshiriq; butun1–11kurs tugallanmagan, jami/qolgan mavzu soni noma’lum. Nashr faqat lokal test, `course_ready=false`.

| № | Mavzu | PDF | Bosma |
|---|---|---|---|
|42|11 dan20 gacha bo‘lgan sonlar|5–6|4–5|
|43|11 dan20 gacha sonlarning o‘nlikda yozilishi|7–8|6–7|
|44|11 va12 sonlari|9–10|8–9|
|45|13 va14 sonlari|11–12|10–11|
|46|15 va16 sonlari|13–14|12–13|

Manbalar asl tasvir/native-text SHA bilan tekshirildi; qo‘lyozma javoblar kalit emas. Kitobdagi hayvonlarning yo‘qolish tezligi va terak/archa kislorod nisbati mustaqil tasdiqlanmagan; ilmiy fakt sifatida darsga kiritilmadi. Yomg‘irli kunlarda quyosh paneli umuman ishlamaydi degan xulosa qo‘llanilmadi. Uch bolaning1/2/3 miqdori kimga tegishliligini qo‘shimcha shartsiz aniqlab bo‘lmasligi ko‘rsatildi. Daraxtning ekilganidan beri vaqt uning to‘liq biologik yoshi deb olinmadi.

API: katalog faqat import qilingan kitoblarni `available_books` bilan qaytaradi. `source_number`42–46 part-local`sequence`1–5dan alohida. IIqism Iqismning barcha41mavzusi tugamaguncha serverda ham403`finish_previous_book` bilan yopiq. Kitob va mavzu ichki prerequisite birgalikda tekshiriladi; takror bajarish0XP. Source auditor reviewlarni haqiqiy `book_id` bo‘yicha ajratadi; birinchi kitobga tegishli ilk10formulasiz qoida endi faqat Iqismga scoped. Takror grade/part/sequence importda rad etiladi. DBschema yoki public normalappAPI o‘zgarmadi.

Flutter: alohida Math previewda kitob tanlash, haqiqiy IIqism ISBN/yil/sahifalar, o‘nlik/birlik va sonni qismlarga ajratish modellari.20 ikkita to‘liq o‘nlik va0 ortiqcha birlik bilan ko‘rsatiladi. Kitob almashish timeoutida eski katalog/tanlov saqlanadi va xato ko‘rinadi.422dan keyin tahrirlash qayta ochiladi, ekran javobdan uzoqqa sakramaydi. Ilmo/brend, UID/origin/draft va idempotency himoyalari saqlangan.

Haqiqiy testlar: Math **67passed,1skipped42.08s**; alohida loopbackPG16 **1passed11.93s**; to‘liq Flutter **449passed1:47**, analyze **0issue1.7s**;22targetedwidgettest o‘tdi.320px/200%matn/ReduceMotion bilan5yangi to‘liq oqim. Lokal UID1 eski137XP→597,46progress; UID2XP0/IIqismyopiq; parallel firstreward/replay/immutable import o‘tdi.23PDF/2958sahifa,46mavzu/92tana sahifasi hash auditi o‘tdi. Bu partiyada yangi web build yoki to‘liq backend to‘plami bajarilmadi; oldingi keng natijalar alohida tarixda.

IIqism74ning bosma68–69sahifalari hali yo‘q:33TOCmavzudan32bodymavjud,5tayyor,27mavjudbodyqolgan,1blocked. Keyingi47«17 va18sonlari»PDF15–16/bosma14–15;47–51PDF15–24tasvirlari ko‘rildi, hali bu checkpointda import qilinmagan.9-sinfAlgebra/11-sinfIqism32MiB transfer va6-sinfII/7–10Geometriya manba cheklovlari saqlangan.

Frontend, boshqa fanlar, Googlelogin, umumiyGradle va production o‘zgarmadi. AndroidSDK/realtelefon, mustaqil o‘qituvchi/pilot/rasmiy2026–27moslik not_verified. PostgreSQL konteyneri restartida dinamik port o‘zgargani sabab dastlab connectionrefused bo‘ldi; privateURL faqat owncontainerning yangi loopbackportiga yangilanib test qayta o‘tdi. Credential logga chiqarilmadi. Cloud Git-directoryguard chetlab o‘tilmadi; standaloneCLIpositive-run sinovi hali ochiq. [Machine checkpoint](checkpoints/grade1_part2_batch1.json).

