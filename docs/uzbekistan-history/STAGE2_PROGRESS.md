# O‘zbekiston tarixi — interaktiv kurs checkpointi

2026-10-26. Kurs tugallanmagan. 7-sinf §1–15 lokal/test adapteri uchun yozildi: 114 tushuntirish kartasi, 15 original misol, 60 MCQ, 30 obyektiv qisqa FRQ, 10 xronologiya topshirig‘i va 15 baholanmaydigan tahlil/rubrika. Manbali original topshiriqlar soni 100.

| Sinf | Bob | Katalogdagi mavzu guruhi | Interaktiv dars | Qolgan |
|---|---:|---:|---:|---:|
| 7 | 6 | 42 | 15 | 27 |
| 8 | Noma’lum | Noma’lum | 0 | Noma’lum: PDF olinmagan |
| 9 | 9 | 39 (§1–41, ikkita birlashtirilgan mavzu) | 0 | 39 |
| 10 | 6 | 28 | 0 | 28 |
| 11 | 9 | 22 | 0 | 22 |

To‘rtta mavjud kitobda 131 mavzu guruhi kataloglangan, 116 tasi hali darsga aylantirilmagan. Beshala kitobning jami dars soni noma’lum. Bu 131 ta dars tayyor degani emas.

| 7-sinf mavzusi | PDF va bosma manba sahifalari | Holat |
|---|---|---|
| §1 Ijtimoiy-iqtisodiy o‘zgarishlar | 6–8, §2 boshlanishigacha | JSON, javoblar, lokal API va Flutter testlari |
| §2 Ilk o‘rta asrlarda davlatlar | 8–10 | Xuddi shu tekshiruvlar |
| §3 Eftallar davlati | 11–13 | Xuddi shu tekshiruvlar |
| §4 O‘rta Osiyo xalqlari Turk xoqonligi davrida | 14–16 | Xuddi shu tekshiruvlar |
| §5 G‘arbiy Turk xoqonligi | 16–18; §6 boshlanadigan 19-sahifadagi oldingi jadval yangi faktga aylantirilmagan | Xuddi shu tekshiruvlar |

Aniq sarlavha, fakt darajasidagi sahifalar va sahifa ichidagi chegaralar `grade7_batch1.json` hamda `sources.json`da. Kitob sahifasi bilan PDF raqami alohida saqlanadi. Birinchi partiyada ular mos keladi; boshqa kitoblarda ham avtomatik teng deb olinmaydi.

§6–10 uchun `grade7_batch2.json`: 39 karta, 20 MCQ, 10 qisqa FRQ, 2 xronologiya; 5 misol va 5 refleksiya. Fakt manbalari: §6 PDF/bosma 19–22, §7 22–26, §8 27–30, §9 31–33, §10 33–37. Sahifa ichidagi chegaralar saqlangan. Bob I uchun tugallanish belgisi faqat barcha §1–7 o‘tilganda ochiladi; alohida checkpoint quiz hali mavjud emas.

§11–15 (`grade7_batch3.json`) uchun 41 karta, 34 topshiriq: 20 MCQ, 10 qisqa FRQ, 4 xronologiya, 5 misol va 5 refleksiya. §11 fakt manbalari PDF/bosma38–40, §12 41–44, §13 45–47, §14 48–52, §15 53–54. Oldingi partiyalar o‘zgartirilmadi. Murakkab tarixiy xulosalar avtomatik matn kaliti bilan baholanmaydi.

Joriy backend: 52 passed/1 PG skipped (6.33s). Real lokal PostgreSQL fresh schema: 1 passed (6.68s), 15 dars/150 XP, 137→287, replay/parallel completion. Barcha uch partiyada 49 to‘liq asl dars sahifasi tasviri qayta tekshirildi. Flutter yangi partiya va legacy regression sinovlari bajarilmoqda; tugamaguncha passed deb hisoblanmasin. Avvalgi to‘liq backend: 2314 passed/5 skipped/2 sandbox deselected (536.55s); Flutter §1–10:176passed (87s).

Keyingi ish: **7-sinf §16, PDF/bosma55 — “Qoraxoniylar”**. §16–20 uchun asl55–74ko‘rildi, JSON hali yo‘q. 59-sahifadagi 1141 jangdan keyingi “davlat tugatiladi” iborasi siyosiy qaramlik va sulola tugashini aralashtirishi mumkin: ekspert tekshiruvisiz bu tugash sanasini kalitga aylantirmang. Chingizxon tug‘ilgan yilidagi bahs, ommaviy qurbonlar soni va rivoyatdagi aniq iqtiboslarni isbotlangan yagona dalil sifatida testlamang.

8-sinf uchun 32 MiB’dan kichik, uzluksiz PDF segmentlari kerak. To‘liq kitob 32 MiB transfer chegarasidan o‘tmadi; sahifalari, SHA va mavzulari taxmin qilinmagan. 2026–2027 rasmiy dastur manbalariga real proxy 403 sabab kirilmadi. Mustaqil tarix o‘qituvchisi tekshiruvi va haqiqiy Android sinovi bajarilmagan.
