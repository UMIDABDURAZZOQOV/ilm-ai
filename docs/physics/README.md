# Fizika — 1-bosqich: manba xaritasi va texnik loyiha

Sana: **2026-10-21**. Holat: **qisman xaritalangan; to‘liq olti sinf xaritasi hali tayyor emas**.
Fizika e’lon qilinmagan, dars/savol yozilmagan, DB importi va migratsiya bajarilmagan.
Keyingi implementatsiya bosqichi foydalanuvchi tasdig‘ini kutadi.

## Tekshirilgan mavjud asos

- Backend boshlang‘ich commit: `c0f84d0603905393904083f59f5d2a61a125c9bd`.
- Flutter: `79608c2aa2795b24c3dcce0684298bb98868da90`, `feat/biology-curriculum`; o‘zgartirilmagan.
- Ushbu source-only ish backendning **`feat/physics-curriculum-map`** branchida.
- `CLAUDE.md`ning curriculum, arxitektura, baholash va oxirgi mobil nashr bo‘limlari o‘qildi.
- `services/curriculum.py`, `curriculum_validation.py`, `models.py`, `study.py`,
  `mobile_publication.py`, Flutter curriculum modellari, question modeli, repository
  va lesson ekrani tekshirildi. Runtime’ga ulanish qo‘shilmadi.
- Biologiya **355 nazariya + 51 raqamli faoliyat + 47 checkpoint / 2 527 karta / 2 609 savol**
  holatida saqlandi. Eski Fizika AI seedlari manba sifatida ishlatilmadi va o‘chirilmadi.
- Next.js repozitoriyasiga tegilmadi; asl PDF, rasmlar va to‘liq matn Gitga kiritilmaydi.

## Manbalar va aniq qamrov

| Sinf | PDF sahifa | Bob | Raqamlangan bo‘lim | Nazariya | Laboratoriya | Uy amaliy ishi | Tayyor dars |
|---|---:|---:|---:|---:|---:|---:|---:|
| [6](grade_6_map.md) | 176 | 7 | 61 | 53 | 7 | 1 | **0** |
| [7](grade_7_map.md) | 170 | 7 | 46 | 41 | 5 | 0 | **0** |
| 8 | O‘qilmadi | Noma’lum | Noma’lum | Noma’lum | Noma’lum | Noma’lum | **0** |
| 9 | O‘qilmadi | Noma’lum | Noma’lum | Noma’lum | Noma’lum | Noma’lum | **0** |
| [10](grade_10_map.md) | 178 | 9 | 45 | 40 | 5 | 0 | **0** |
| [11](grade_11_map.md) | 193 | 7 | 45 | 42 | 3 | 0 | **0** |
| O‘qilgan fayllarda jami | **717** | **30** | **197** | **176** | **20** | **1** | **0** |

Raqamlangan laboratoriyalar nazariy mavzu sifatida qayta sanalmaydi. 6-sinf §13 uyda
bajariladigan diffuziya amaliyoti; u alohida nazariya emas. Bobdagi kirish/yakuniy
suhbat, qo‘shimcha mashq va nazoratlar ham raqamlangan darslar ustiga nazariya sifatida
qo‘shilmagan. 6-sinf boshidagi 7 mavzu va 10-sinf §1 manbadagi kirish tartibida saqlangan.

**Bu jadval kontent tayyorligi emas.** 717 PDF sahifaning matn qatlami chiqarildi va
fingerprintlandi; 197 raqamlangan sarlavhaning body sahifasi mundarija bilan solishtirildi.
Bob yakuni, masala yechish namunasi, mashq va amaliy topshiriq belgilari body bo‘ylab
qidirildi. Barcha 717 sahifadagi fan faktlari yoki barcha formulalar vizual/pedagogik
tekshiruvdan o‘tdi degan da’vo yo‘q. Hech qanday interaktiv dars tayyor deb belgilanmagan.

### Transfer bloklari

`fizika_8_uzb.pdf` va `fizika_9_uzb.pdf` uchun real yuklab olish natijasi:
**`file exceeds the executor transfer limit of 32 MiB`**.
Bu ikkala kitobning boblari, mualliflari, yili va mavzu sonlari taxmin qilinmadi.
PDF sahifa ketma-ketligini saqlagan, har biri 32 MiB’dan kichik qismlar kerak.
Qism nomida **asl PDF** sahifa oralig‘i bo‘lishi kerak; bosma sahifa bilan almashtirmang.

7-sinf faylining **PDF1 sahifasi bosma8** sahifadir. Bosma1–7, jumladan mundarijada
bosma3 deb ko‘rsatilgan `Kirish`, mavjud faylda yo‘q. Shu yetti bosma sahifa yoki
to‘liq to‘g‘ri kitob nusxasi talab qilinadi. PDF168/170 imprintida to‘rtinchi nashr,
PDF170 yuqoridagi bibliografik satrda esa uchinchi nashr yozilgan; bu tafovut saqlandi.
ISBN mavjud sahifalardan olinmadi. 46 ta raqamlangan paragraf body’da mavjudligi bu
fayl to‘liq kitob ekanini anglatmaydi.

### Sahifa raqamlari

| Sinf | Tekshirilgan bog‘lanish | Muhim misol |
|---|---|---|
| 6 | Asosiy bosma sahifa = PDF sahifa | §16: bosma33 / PDF33 |
| 7 | Mavjud body’da bosma sahifa = PDF + 7 | §9: bosma37 / PDF30; formula bosma38 / PDF31 |
| 10 | Asosiy bosma sahifa = PDF − 1 | §1: bosma3 / PDF4 |
| 11 | Asosiy bosma sahifa = PDF − 1 | §1: bosma4 / PDF5 |

Har sahifadagi mavjud bosma raqam alohida tekshirildi va `page_audit`da saqlandi;
raqamsiz muqova/imprintga soxta bosma raqam berilmadi. 11-sinf III bob kirishi
bosma41/PDF42, birinchi mavzusi esa bosma42/PDF43 — ular bitta sahifa deb olinmagan.
Bir sahifada ikki mavzu boshlansa, **matn boshlanish/tugash offsetlari** ham saqlanadi.
Masalan 6-sinf PDF147 yuqorisidagi `D = 1/F` §53ga tegishli; pastda boshlanadigan §54ga
bu formula avtomatik bog‘lanmaydi. Sahifa diapazoni fakt yoki javobning tasdig‘i emas.

## Formulalar va fizik kattaliklar

- [Mashina o‘qiydigan xarita](../../scripts/curriculum/physics/physics_sources.json):
  barcha 197 bo‘lim tartibi, bob egasi, kitob/PDF sahifasi, manba SHA-256, body sarlavha
  tekshiruvi, manba matni chegarasi, mashq/namuna/amaliyot sahifalari.
- [Formula transkripsiyalari](../../scripts/curriculum/physics/physics_formula_review.json):
  **37 tanlangan formula**, asl sahifa tasviri bilan tekshirilgan. Bu to‘liq formula
  banki emas; executable grader yoki tekshirilgan savol ham emas.
- Har mavzuda formulaga o‘xshash belgilar topilgan sahifalar va raqamlangan tenglama
  nomzodlari bor. Tenglama raqami havolada qayta uchrashi mumkin; ular noyob
  formulalar soni deb hisoblanmaydi. Kasr, indeks, vektor, daraja va minus ishoralari
  asl rasmdan tekshirilmaguncha `formula_inventory_complete: false` qoladi.
- `quantity_term_candidates` faqat shu mavzu matnida topilgan fizik atamalar va
  sahifalarni ko‘rsatadi. Ta’rif, o‘lcham yoki birlik tekshirilganini anglatmaydi.
- Hisoblash yo‘nalishlari uchun darslikdagi ishlangan misol/mashq sahifalari alohida
  ko‘rsatilgan; bunday belgilar topilmagani «mavzuda hech qanday hisoblash yo‘q» degani emas.
- Tarix, diffuziya, konveksiya, elektrlanish va boshqa konseptual mavzularga sun’iy
  formula kiritilmaydi. Modalitetni tanlashdan oldin mavzuning to‘liq body’si qayta o‘qiladi.

To‘liq texnik loyiha va 6-sinf partiyalari: [FRQ_AND_IMPLEMENTATION_PLAN.md](FRQ_AND_IMPLEMENTATION_PLAN.md).

## Qayta tekshirish

Backend ildizidan, DB va production credentiallarsiz:

```bash
python scripts/audit_physics_sources.py
# Faqat private original fayllar bilan; PyMuPDF 1.26.6 talab qilinadi:
python scripts/audit_physics_sources.py --pdf-dir /workspace/attachments
# Qasddan exit 2: hozircha to‘liq qamrov va barcha formula tekshiruvi mavjud emas:
python scripts/audit_physics_sources.py --require-complete
```

Oddiy audit exit0 — **qisman katalog ichki izchil** degani. Bu full curriculum,
tekshirilgan savollar, barcha formulalar yoki release tayyor degani emas. `--pdf-dir`
717 haqiqiy sahifaning hashini va mavjud bosma raqamlarini, 197 body sarlavha
markerini tekshiradi; u rasmdagi formulani matematik jihatdan tushunib tasdiqlamaydi.

Amaldagi avtomatik tekshiruv: Physics uchun **15 yangi test**; mavjud Biology
curriculum/segment regressionlari bilan jami **51 passed (25.27s)**. Biologiya
completion auditi **355/51/2 527/2 609** sonlarini tasdiqladi. Ruff critical va
whitespace tekshiruvi toza. Flutter va website kodi o‘zgarmagani uchun ushbu
source-only bosqichda build/native testlar qayta bajarilmadi.

## Davom ettirish chegarasi

1. 8/9-sinfning kichik PDF qismlari va 7-sinfning yetishmagan old sahifalarini olish.
2. Har segmentning fayl SHA, sahifa soni, asl PDF oralig‘i va ketma-ketligini tekshirish.
3. Oltita kitob xaritasini to‘ldirish, bibliografik tafovutni aniqlashtirish.
4. Barcha formula/miqdor/birlik va masala yo‘nalishlarini sahifa tasviridan tekshirish.
5. Yakuniy 1-bosqich natijasini foydalanuvchiga taqdim etish.
6. **Faqat foydalanuvchi tasdig‘idan so‘ng** FRQ implementatsiyasi va 6-sinf darslariga o‘tish.

`MOBILE_PUBLISHED_SUBJECTS=biologiya`, Flutter `BIOLOGY_ONLY=true` va `SUBJECTS_ONLY=true`
holati o‘zgarmagan. Fizika uchun runtime endpoint, migratsiya, import, generatsiya,
AI Explain yoki mobil nashr ushbu bosqichda qo‘shilmagan.
