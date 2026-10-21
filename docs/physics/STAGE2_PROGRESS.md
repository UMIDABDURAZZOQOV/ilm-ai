# Fizika 2-bosqich — davom etayotgan haqiqiy kontent

2026-10-22 (Asia/Tashkent). Foydalanuvchi barcha **316 bo‘limni** ketma-ket
yaratishga ruxsat berdi; partiyalar orasida yangi tasdiq talab qilinmaydi.
Bu ruxsat production deploy yoki ommaviy nashr uchun ruxsat emas.

## Tekshirilgan partiyalar

Boshlang‘ich backend `986efa7`, Flutter `9f152f0`; GitHub HEADlar qayta tekshirildi.
§1–7 JSON va review fayllari qayta yaratilmagan. `physics_sources.json`, formula
review va source-map audit — saqlangan 1-bosqich arxivi; undagi «0 dars» tarixiy.
Joriy mualliflik sanoqlari `python -m scripts.audit_physics_course` orqali olinadi.

| Sinf | Jami bo‘lim | Yozilgan lokal dars/faoliyat | Qolgan | Karta | Formula yozuvi | Misol | Topshiriq | FRQ | Lab / uy amaliyoti |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 6 | 61 | 17 | 44 | 72 | 19 | 20 | 110 | 22 | 2 / 1 |
| 7 | 46 | 0 | 46 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 8 | 60 | 0 | 60 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 9 | 59 | 0 | 59 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 10 | 45 | 0 | 45 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 11 | 45 | 0 | 45 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| Jami | 316 | 17 | 299 | 72 | 19 | 20 | 110 | 22 | 2 / 1 |

Formula yozuvlari dars ichidagi izohlangan formulalardir, noyob fizik qonunlar
soni emas. 17 executable qoida oilasi bor: dastlabki 5 + yangi 12.
Hisoblash mavjud bo‘lmagan mavzularga sun’iy formula kiritilmagan.

## 6-sinf §8–17: yangi 10 bo‘lim

| § | Qisqa nom | PDF = bosma sahifa | Karta | Formula | Misol | Topshiriq | FRQ |
|---|---|---|---:|---:|---:|---:|---:|
| 8 | Modda tuzilishi ta’limotlari | 18–19 | 4 | 0 | 1 | 5 | 0 |
| 9 | Molekulalar va o‘lchamlari | 20–21 | 4 | 1 | 1 | 7 | 2 |
| 10 | O‘zaro ta’sir va Broun harakati | 22–24 | 4 | 0 | 1 | 6 | 0 |
| 11 | Diffuziya | 24–25 | 4 | 0 | 1 | 6 | 0 |
| 12 | Moddaning uch holati | 26–28 | 4 | 0 | 1 | 6 | 0 |
| 13 | Uy amaliyoti: diffuziya | 28 | 4 | 1 | 1 | 6 | 2 |
| 14 | Massa | 29–31 | 4 | 3 | 1 | 7 | 3 |
| 15 | Lab: shayinli tarozi | 31–33 | 4 | 2 | 1 | 7 | 2 |
| 16 | Zichlik | 33–36 | 5 | 4 | 2 | 9 | 4 |
| 17 | Lab: qattiq jism zichligi | 37–39 | 4 | 3 | 2 | 8 | 4 |

Jami yangi: **41 karta, 14 formula yozuvi, 12 original misol, 67 topshiriq,
17 FRQ**. Har fakt/karta/formula/misol/bosqich/savol/izohda aniq paragraf va
sahifa SHA bilan `source_refs` bor. 22 asl sahifa to‘liq matn va tasvir orqali
qayta ko‘rildi. Barcha 36 eski+yangi sahifaning original PDF/text/render hash’i
amalda qayta tekshirildi. PDF, to‘liq matn va rasmlar Gitga kiritilmaydi.

## Ilmiy qarorlar va halol cheklovlar

- Demokrit, Ar-Roziy, Beruniy/Ibn Sino qarashlari tarixiy; hozirgi tajriba natijasi
  yoki cheksiz bo‘linish isboti sifatida o‘rgatilmaydi.
- Molekula misollari molekulyar moddalarga tegishli; NaCl alohida molekula modeli
  deb berilmagan. P21 optik mikroskop aniqligi va oqsil o‘lchami haqidagi bahsli
  sonlar savolga kiritilmagan. Bir qatlamli parda V/S — taxminiy model.
- Broun zarrasi molekulaning o‘zi emas. Piramida va teri orqali kislorod haqidagi
  umumlashtirishlar ishlatilmagan; zararli modda tatish/shisha kesish topshirig‘i yo‘q.
- §13 dagi `D≈h/t` umumiy diffuziya koeffitsiyenti emas. `v=h/t` faqat berilgan
  kuzatuvdagi rangli qatlamning o‘rtacha siljish ko‘rsatkichi sifatida izohlanadi.
- Qattiq jismlarning hammasi kristall emas. Tarixiy kilogramm etaloni joriy SI
  ta’rifi emas. «Shakar eriganda hajm mutlaqo o‘zgarmaydi» va «barcha qattiq jismlar
  barcha suyuqliklardan zichroq» degan umumlashtirishlar yo‘q. P38 Quyosh markazi
  zichligi haqidagi bahsli son ishlatilmagan.
- Menzurka modeli to‘liq botgan/erimaydigan jism, suv to‘kilmasligi va pufaklar
  bo‘lmasligini talab qiladi. Lab va uy amaliyoti raqamli: haqiqiy tajriba bajarildi
  deb tasdiqlanmaydi. Mustaqil fan/pedagog ekspert imzosi **da’vo qilinmaydi**.

## Muhandislik o‘zgarishlari

- Faqat explicit reviewed batch registry yuklanadi; tasodifiy JSON/glob import yo‘q.
  Immutable eski kontent, token, progress, StudySession snapshot va birinchi-yakun XP
  qoidalari saqlanadi. `--all-reviewed` barcha tasdiqlangan manbali partiyalarni
  qo‘shadi. Sandbox `--resume` ham yangi kontentni qo‘shib, eski XP/progressni saqlaydi.
- Massa, yuza, hajm, zichlik va siljish tezligi birliklari; cheklangan `cm³/cm^3`,
  `kg/m³`, reciprocal integer-power formula variantlari. `eval`/CAS yo‘q, eski
  parser hajm/chuqurlik/daraja chegaralari saqlanadi.
- Har FRQ javobi structured givens dan exact Fraction orqali qayta hisoblanadi.
  Noto‘g‘ri birlik o‘lchami/formula/son/manfiy yoki noldagi domain rad etiladi.
  Javob kaliti va private rubric mijozga berilmaydi.
- Catalog grade parametri 6–11, faqat import qilingan darslar. Yo‘q prerequisite
  keyingi bo‘limni ochmaydi. `course_complete=false`; source-map soni tayyor dars
  deb ishlatilmaydi. §1–7 default API/import testlari saqlangan.
- Flutter dars oralig‘ini katalogdan oladi; FRQ birlik chip/hintlari mavzuning
  public `unit_choices` ro‘yxatidan. Massa/zichlikda «m, cm, mm» majburlanmaydi.
  Ilmo, brand, draft/retry/account isolation va Biologiya UI o‘zgarmagan.

## Ushbu partiyada amalda bajarilgan tekshiruvlar

- Oldingi v2 + source-map testlari: **99 passed**; yangi kurs testlari:
  **12 passed (4.34s)**. Yangi 17 sonli topshiriq uchun alohida yozilgan javob
  orakullari; barcha 17 darsni HTTP orqali tugatish, append/reimport, private-rubric
  yo‘qligi, har javob va complete replay, jami **170 XP** tekshirildi.
- Yangi Flutter Physics testlari: **16 passed** (oldingi 15 + birlik/320px/200% test).
  Flutter analyze toza. To‘liq suite/build va PG shu davomning yakunida qayta
  bajariladi; oldingi sessiya natijasi yangi kod natijasi deb ko‘rsatilmaydi.
- Biology completion audit: **355 nazariya + 51 faoliyat / 2 527 karta / 2 609 savol**.
- Android SDK mavjud emas; real telefon, native APK va TalkBack sinovi hali ochiq.

Keyingi aniq mualliflik nuqtasi: **6-sinf §18, PDF/bosma45**. Navbatdagi
manba sahifalari 45–61 o‘qildi va tasviri ko‘rildi; bu hali authored lesson emas.
Ish keyingi partiyada davom etadi, foydalanuvchidan oraliq tasdiq kutilmaydi.
