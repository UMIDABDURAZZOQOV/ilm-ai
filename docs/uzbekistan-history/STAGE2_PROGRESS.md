# O‘zbekiston tarixi — interaktiv kurs checkpointi

2026-10-26. Kurs tugallanmagan. 7-sinf §1–10 lokal/test adapteri uchun yozildi: 73 tushuntirish kartasi, 10 original misol, 40 MCQ, 20 obyektiv qisqa FRQ, 6 xronologiya topshirig‘i va 10 baholanmaydigan tahlil/rubrika. Manbali original topshiriqlar soni 66.

| Sinf | Bob | Katalogdagi mavzu guruhi | Interaktiv dars | Qolgan |
|---|---:|---:|---:|---:|
| 7 | 6 | 42 | 10 | 32 |
| 8 | Noma’lum | Noma’lum | 0 | Noma’lum: PDF olinmagan |
| 9 | 9 | 39 (§1–41, ikkita birlashtirilgan mavzu) | 0 | 39 |
| 10 | 6 | 28 | 0 | 28 |
| 11 | 9 | 22 | 0 | 22 |

To‘rtta mavjud kitobda 131 mavzu guruhi kataloglangan, 121 tasi hali darsga aylantirilmagan. Beshala kitobning jami dars soni noma’lum. Bu 131 ta dars tayyor degani emas.

| 7-sinf mavzusi | PDF va bosma manba sahifalari | Holat |
|---|---|---|
| §1 Ijtimoiy-iqtisodiy o‘zgarishlar | 6–8, §2 boshlanishigacha | JSON, javoblar, lokal API va Flutter testlari |
| §2 Ilk o‘rta asrlarda davlatlar | 8–10 | Xuddi shu tekshiruvlar |
| §3 Eftallar davlati | 11–13 | Xuddi shu tekshiruvlar |
| §4 O‘rta Osiyo xalqlari Turk xoqonligi davrida | 14–16 | Xuddi shu tekshiruvlar |
| §5 G‘arbiy Turk xoqonligi | 16–18; §6 boshlanadigan 19-sahifadagi oldingi jadval yangi faktga aylantirilmagan | Xuddi shu tekshiruvlar |

Aniq sarlavha, fakt darajasidagi sahifalar va sahifa ichidagi chegaralar `grade7_batch1.json` hamda `sources.json`da. Kitob sahifasi bilan PDF raqami alohida saqlanadi. Birinchi partiyada ular mos keladi; boshqa kitoblarda ham avtomatik teng deb olinmaydi.

§6–10 uchun `grade7_batch2.json`: 39 karta, 20 MCQ, 10 qisqa FRQ, 2 xronologiya; 5 misol va 5 refleksiya. Fakt manbalari: §6 PDF/bosma 19–22, §7 22–26, §8 27–30, §9 31–33, §10 33–37. Sahifa ichidagi chegaralar saqlangan. Bob I uchun tugallanish belgisi faqat barcha §1–7 o‘tilganda ochiladi; alohida checkpoint quiz hali mavjud emas.

Keyingi ish: **7-sinf §11, PDF/bosma 37 — “Abbosiylar davrida Xuroson va Movarounnahr”**. §11–15 uchun asl 37–55-sahifalar ko‘rildi, ammo hozircha ularning interaktiv JSON’i yo‘q. Manbada 749/750 sulola almashish qaydlari bir-biriga mos emas; bu sanani avtomatik test kalitiga aylantirmang. Source review qaydlarini o‘qing.

Tekshiruvlar: joriy 47 passed/1 PG skipped (4.21s), alohida PostgreSQL 1 passed (5.47s), barcha 10 dars/100 XP/replay/parallel yozuv. Flutter full 176 passed (87s), history 22 passed (3s). To‘liq backend regression birinchi partiya ustida 2314 passed/5 opt-in skipped/2 sandbox deselected (536.55s); ikkinchi partiyaning manba/API sinovlari keyin alohida o‘tkazilgan. Har ikki partiya uchun 32 asl to‘liq sahifa tasviri + 609 native sahifa xeshi + 131 heading tasviri tekshirildi.

8-sinf uchun 32 MiB’dan kichik, uzluksiz PDF segmentlari kerak. To‘liq kitob 32 MiB transfer chegarasidan o‘tmadi; sahifalari, SHA va mavzulari taxmin qilinmagan. 2026–2027 rasmiy dastur manbalariga real proxy 403 sabab kirilmadi. Mustaqil tarix o‘qituvchisi tekshiruvi va haqiqiy Android sinovi bajarilmagan.
