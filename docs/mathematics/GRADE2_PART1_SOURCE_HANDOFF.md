# 2-sinf I qism — yo‘q sahifadan keyingi xavfsiz davom

## Joriy checkpoint186 — 2026-11-05

186lokal dars,1 120karta,1 466savol.2-sinf Iqismning barcha43mavjud bodybirligi yaratildi.
44dan1birlik —yo‘q§25/path26/bosma54–55—yaratilmadi,unga progress/XPyo‘q.
Yakuniy26mashq bitta to‘plamdagi26original raqamli moslashtirish,26alohida dars emas.
KeyingiIIqism§42,PDF5–6/bosma4–5;faqat preflight,0dars va34TOCnomzodi,hali fullmap emas.
Butun1–11kurs,realAndroid,pedagog/physicalskill/pilot/2026–27tasdiqlanmagan.
[Testlar](QA_REPORT.md),[checkpoint](checkpoints/grade2_part1_batch8.json),
[26mashq qamrovi](GRADE2_PART1_PRACTICAL_COVERAGE.md),[keyingiIIqism](GRADE2_PART2_PREFLIGHT.md).
Quyidagi oldingi yozuvlar tarix sifatida saqlandi.

### Oldingi checkpointlar (saqlangan tarix)

## Joriy checkpoint178 — 2026-11-05

178lokal dars,1 052karta,1 384savol.2-sinf Iqism35/44birlik,9qolgan:
8mavjud tana va1yo‘q§25/bosma54–55. Keyingi§36,path37,PDF75–76/bosma76–77.
§31–35ning asl sahifalari asosida5yangi dars va yig‘indidan ayirish modeli qo‘shildi.
173oldingi dars saqlandi;global1–11kurs tugallanmagan. [Haqiqiy testlar](QA_REPORT.md),
[checkpoint](checkpoints/grade2_part1_batch7.json),[ilmiy review](GRADE2_PART1_SCIENTIFIC_REVIEW.md),
[keyingi manba](GRADE2_PART1_NEXT_SOURCE.md). Quyidagi oldingi yozuvlar tarix sifatida saqlandi.


## Joriy checkpoint — 2026-11-05

173lokal dars,1 022karta,1 344savol.2-sinf Iqism§26–30/path27–31yaratildi:
30/44birlik tayyor,14qolgan (13mavjud tana,1yo‘q§25/bosma54–55).
Keyingi§31,path32,PDF65–66/bosma66–67. §25uchun dummyprogress/XPyo‘q;
keyingi mavjud mavzularga alohida default-off lokalQAflag va25haqiqiy prerequisite talab qilinadi.
Bu butun1–11kurs tugallanganini anglatmaydi.
[Yangi partiya/testlar](QA_REPORT.md),[checkpoint](checkpoints/grade2_part1_batch6.json),
[lokalQA](GRADE2_PART1_LOCAL_QA.md). Oldingi yozuvlar quyida tarix sifatida saqlandi.

§26–30hozir dars/test partiyasida;§31esa faqat manba ko‘rigi. Quyidagi dastlabki handoff tarixi saqlandi.


2026-11-05. §21–24 yangi partiya testlarida. Tayyor darslar deb faqat yakuniy tekshiruvlaridan o‘tgan checkpoint sonlari olinadi.

§25ning bosma54–55 sahifalari manbada yo‘q. Buni §26 bilan almashtirish, path26ga dummy dars/progress/XP yozish yoki keyingi pathlarni yashirincha siljitish mumkin emas.

Keyingi mavjud manba **§26 «Sonlarni qo‘shish (28 + 14)», path27, PDF55–56/bosma56–57**.
§26–31ning PDF55–66/bosma56–67 to‘liq asl tasvirlari ko‘rildi. Ular hali dars yoki testlangan interaktiv kontent emas.
Hash pinlari va review qaydlari `scripts/curriculum/mathematics/grade2_part1_source_handoff.json`da saqlandi; PDF/rasmlar private joyda qoladi.

| Manba | Path | PDF | Bosma | Kerakli yo‘nalish |
|---|---|---|---|---|
|26|27|55–56|56–57|Ikki xonali qo‘shish, o‘nlikdan tashqari birliklar, aniq qoida bilan zanjir|
|27|28|57–58|58–59|Ustunda birlik/o‘nlikni moslash, birliklar va perimetr|
|28|29|59–60|60–61|Ikki xonali umumiy ayirishda o‘nlikni ochish, bog‘liq guruhlar|
|29|30|61–62|62–63|Ayriluvchini qismlab olish, qoldiq va boshlang‘ichlar jadvali|
|30|31|63–64|64–65|Ustunda carry va qolgan birlik, diagramma, cm/dm|
|31|32|65–66|66–67|Qo‘shishning o‘rin almashtirish/guruhlash xossalari|

Hozirgi qat’iy preview prerequisite tartibi yo‘q path26dan keyingi darsni ochmaydi. Mazmunni yaratish davom etishi mumkin, lekin uni ishlaydigan dars deb ko‘rsatishdan oldin quyidagilar alohida testlanishi kerak:

- Faqat lokal/test, odatda o‘chiq, aniq2-sinf Iqism/SHA/gapga bog‘langan konfiguratsiya.
- Barcha25oldingi haqiqiy dars tugallangan; yo‘q mavzuga progress yoki XP berilmaydi.
- O‘quvchi so‘rovi yoki umumiy missing metadata ruxsat bermaydi.
- Keyingi mavjud darslarda odatiy ketma-ketlik, UID himoyasi, replay0XP saqlanadi.
- Konfiguratsiya o‘chsa tugallanmagan urinishlar bloklanadi, tugallangan natijalar saqlanadi.
- Flutter manba kamchiligini ochiq ko‘rsatadi; course_ready=false qoladi.

Bu hujjat keyingi lokal siyosat uchun handoff. Ushbu partiyada bunday yangi ruxsat yoki production policy yaratilmagan. Raqamlash, eski darslar va ma’lumotlar o‘zgarmagan.

## Kelgusi ruxsat doirasi bo‘yicha aniqlik

Bu faqat oldindan ruxsat berilgan lokal/test ishlab chiqish doirasi uchun talablar. Production prerequisite o‘zgarmaydi. Yangi urinishlar va qayta mashq ham odatda o‘chiq source-gap konfiguratsiyasini talab qilishi kerak; tugallangan eski natijani o‘qish esa saqlanadi. Faqat katalogda completed holati borligi yangi unfinished urinishni konfiguratsiya o‘chiqligida ochib yubormasin.

Siyosatni katalog, start, answer, complete va snapshot/revocation bo‘yicha birgalikda sinang. Source25body yo‘qligi, barcha25haqiqiy oldingi dars, aniq sourceSHA, UID va replay0XP uchun salbiy holatlar ham yozilsin. Mavjud version1API va boshqa kitoblarning lokalQAflaglari buzilmasin.
