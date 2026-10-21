# Fizika — manba xaritalari va lokal interaktiv sinov

**Davom etayotgan ish — 2026-10-22:** barcha 316 bo‘lim uchun mualliflik ruxsati
berilgan. Hozir **24 lokal dars/faoliyat**, 99 karta / 158 topshiriq / 38 FRQ;
**292 bo‘lim qolgan**. Oraliq tasdiq kutilmaydi. Joriy sanoqlar, manba/ilmiy
qarorlar va testlar: [STAGE2_PROGRESS.md](STAGE2_PROGRESS.md).
Quyidagi birinchi partiya va source-only yozuvlar saqlangan tarixdir.

**2026-10-22 — 2-bosqichning birinchi partiyasi:** 6-sinf §1–7 uchun 7 dars,
31 karta, 8 misol, 43 topshiriq (5 FRQ) va alohida server/Flutter **lokal test preview**
yozildi. Fizika umumiy foydalanuvchilarga e’lon qilinmagan. V1/Biology API va 406
manifest saqlangan. Keyingi §8–17 hali boshlanmagan; foydalanuvchi tasdig‘i kerak.

Amaldagi holat, sahifalar, testlar, xavfsizlik va ishga tushirish:
[STAGE2_GRADE6_BATCH1.md](STAGE2_GRADE6_BATCH1.md).

## 1-bosqich yakunining saqlangan hisoboti — cb46a02

Quyidagi «0 dars/runtime yo‘q» jumlalari **2026-10-21 xaritalash yakuni** haqida.
Hozirgi lokal partiya alohida yuqorida; stage-one katalog/publication metadata
va olti sinfning source yozuvlari qayta generatsiya qilinmagan.

Sana: **2026-10-21**. **Olti sinfning mavjud manba doirasidagi barcha 316 raqamlangan
bo‘limi xaritalangan. To‘liq fan-fakt/formula tekshiruvi hali yakunlanmagan.**
Fizika e’lon qilinmagan; **0 tayyor interaktiv dars, 0 yangi savol**. Runtime FRQ,
AI Explain, DB import/migratsiya va production o‘zgarishi yo‘q. Keyingi bosqich
foydalanuvchi tasdig‘ini kutadi.

## Saqlangan ishlar va chegaralar

- Backend: **`feat/physics-curriculum-map`**, oldingi **`29e7d1e`** ustidan davom etildi;
  6/7/10/11-sinfning 197 bo‘lim yozuvi, sahifa auditi, supplement/reference yozuvlari
  va dastlabki 37 formula transkripsiyasi canonical SHA-256 bilan saqlangan.
- Flutter **`79608c2aa2795b24c3dcce0684298bb98868da90`**, `feat/biology-curriculum`;
  Next.js **`054f0cea9b78a9c791cba5aa478fc3769cbd85b8`** — o‘zgartirilmagan.
- Biologiya **355 nazariya + 51 raqamli faoliyat + 47 checkpoint / 2 527 karta /
  2 609 savol**, progress, XP, xavfsizlik va mobil nashr qoidalari saqlangan.
- PDF, sahifa rasmlari, to‘liq OCR matni private; Gitga kiritilmaydi.
- `MOBILE_PUBLISHED_SUBJECTS=biologiya`, Flutter `BIOLOGY_ONLY=true` va
  `SUBJECTS_ONLY=true` kengaytirilmagan. Eski AI fanlari qayta yoqilmagan.

## Qamrov va haqiqiy sanoq

| Sinf | PDF sahifa | Bob | Raqamlangan bo‘lim | Nazariya | Lab | Amaliy / uy amaliyoti | Masala yechish bo‘limi | Rasmdan tekshirilgan formula yozuvi |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [6](grade_6_map.md) | 176 | 7 | 61 | 53 | 7 | 0 / 1 | 0 | 13 |
| [7](grade_7_map.md) | 170 | 7 | 46 | 41 | 5 | 0 / 0 | 0 | 5 |
| [8](grade_8_map.md) | 176 | 5 | 60 | 41 | 5 | 2 / 0 | 12 | 41 |
| [9](grade_9_map.md) | 176 | 6 | 59 | 37 | 6 | 2 / 0 | 14 | 67 |
| [10](grade_10_map.md) | 178 | 9 | 45 | 40 | 5 | 0 / 0 | 0 | 7 |
| [11](grade_11_map.md) | 193 | 7 | 45 | 42 | 3 | 0 / 0 | 0 | 12 |
| Jami | **1 069** | **41** | **316** | **254** | **31** | **4 / 1** | **26** | **145** |

Bu ustunlar tayyor darslar soni emas. Raqamlangan laboratoriya, amaliyot va
`Masalalar yechish` bo‘limlari nazariya sifatida qayta sanalmaydi. 6-sinf §13 —
uy amaliyoti. 6-sinfdagi dastlabki yetti mavzu va 10-sinf §1 kirish tartibida qolgan.
Bob yakunlari, nazoratlar, qo‘shimcha mashqlar va ishlangan misol anchorlari ham
saqlangan; ular jadvalga yangi nazariy mavzu sifatida qo‘shilmagan.

145 soni **transkripsiya yozuvlari**, noyob fizik qonunlar emas: ekvivalent yozuvlar,
birlik tengliklari va laboratoriya hisoblashlari ham bor. Hammasida
`ready_for_publication=false`, `executable_grading_rule=false`.
`full_formula_inventory_complete=false` barcha olti sinf uchun saqlangan.

## Manba sahifalari va tekshirish chegarasi

- 8-sinf **88 + 88**, 9-sinf **44 + 44 + 44 + 44** sahifali barcha olti qism ochildi.
  Har ikkisi asl PDF **1–176** ni uzilish/kesishishsiz qamraydi. Qism fayllari SHA-256,
  hajmi/sahifa soni, tartibi, asl va qism ichidagi sahifa bog‘lanishi tekshirildi.
  Manifest hash’i butun birlashtirilgan PDF hash’i deb ko‘rsatilmaydi.
- Yangi **352 sahifa** rastrlash va OCRdan o‘tdi. 8/9-sinfning **119 sarlavhasi**
  mundarija va asosiy sahifa tasviri bilan solishtirildi; mavjud bosma sahifa yorliqlari
  rasmlardan tekshirildi. OCR qidirish vositasi, fakt/formula tasdig‘i emas.
- 9-sinf mundarijasida **PDF171 = bosma173; PDF172 = bosma171; PDF173 = bosma172**.
  Asl PDF tartibi o‘zgartirilmadi. Mundarija o‘qish tartibi 172→173→171.
  8-sinf PDF174 mundarija oxirida ko‘rinadigan bosma raqam yo‘q; `null` saqlandi.
- 7-sinf **PDF1 = bosma8**, §1 «Jismlarning harakati». Foydalanuvchi yakuniy qarori:
  mavjud **§1–46** to‘liq xaritalanadi va ketma-ket ishlatiladi; bosma1–7 kirish
  sahifalari **blok emas**, izlash majburiy emas, mazmuni to‘qilmaydi.
  `source_complete=false` butun kitob nusxasi haqida, `mapping_scope_complete=true`
  shu qabul qilingan doira haqida. Nashr qaydidagi uchinchi/to‘rtinchi nashr tafovuti
  va aniqlanmagan ISBN yashirilmagan.
- 6-sinfda bosma ≈ PDF; 7-sinfda bosma = PDF+7; 10/11 asosiy body’da bosma = PDF−1.
  Raqamsiz muqova/imprintga raqam to‘qilmagan. 11-sinf III bob kirishi PDF42/bosma41,
  §11 esa PDF43/bosma42 bo‘lib qoladi.
- Bir sahifadagi chegaralar eski raqamli kitoblarda matn offseti, yangi skanlarda
  **rastr koordinatalari va kesilgan source region hash’lari** bilan saqlanadi.
  Masalan 9-sinf PDF97dagi sirt energiyasi §31ga, pastda boshlangan ho‘llash §32ga
  tegishli; butun sahifadagi formulalar ikkalasiga ko‘r-ko‘rona biriktirilmaydi.

## Formulalar, birliklar va manbadagi noaniqliklar

[Mashina o‘qiydigan xarita](../../scripts/curriculum/physics/physics_sources.json)
har mavzuning nazariya/ta’rif/qonun/birlik, miqdor atamalari, tenglama, ishlangan
misol, mustaqil mashq va amaliy ko‘rsatma sahifalarini saqlaydi. Yangi skanlardagi
`*_candidate` yozuvlari OCR nomzodi ekanligi aniq belgilangan. Hech narsa topilmagani
«formula/masala yo‘q» degani emas; konseptual mavzuga sun’iy hisoblash kiritilmaydi.

[Formula inventari](../../scripts/curriculum/physics/physics_formula_review.json)
**108 yangi + 37 saqlangan = 145** original tasvirdan tekshirilgan yozuvni beradi.
Belgi, birlik, shart, indeks, modul/vektor, yaxlitlash va manba PDF/bosma/qism
havolalari bor. **Barcha formula, ilmiy fakt, namunaviy yechim yoki javob tekshirilgan
emas.** Quyidagilar keyingi dars/FRQ yozilishidan oldin hal qilinadi:

- 8-sinf PDF82–83: umumiy C/U yig‘indisidagi minus belgilar matn va sxemaga zid.
- 8-sinf PDF124: A atom/molyar massa talqini va Faradey doimiysi birliklari.
- 9-sinf PDF109: §37 1-masala sharti va yechim jadvalidagi sonlar turlicha.
- 9-sinf PDF145–147: linza radiusi, ishorali masofa/modul va sochuvchi linza yozuvi.
- 9-sinf PDF153: mikroskop modelidagi l talqini va qo‘llanish chegarasi.

Tafsilotlar: [SOURCE_REVIEW.md](SOURCE_REVIEW.md). Texnik reja:
[FRQ_AND_IMPLEMENTATION_PLAN.md](FRQ_AND_IMPLEMENTATION_PLAN.md).

## Qayta tekshirish

Backend ildizidan, DB/production credentiallarsiz:

```bash
python scripts/audit_physics_sources.py --require-mapped
# Private original fayllar; PyMuPDF 1.26.6:
python scripts/audit_physics_sources.py --require-mapped --pdf-dir /workspace/attachments \
  --ocr-dir /workspace/.setup/physics-sources
# Qasddan exit2: barcha fakt/formula review hali tugamagan:
python scripts/audit_physics_sources.py --require-complete
python scripts/audit_biology_completion.py
```

Oddiy audit ichki izchillikni, `--require-mapped` qabul qilingan barcha bo‘limlar
qamrovini tekshiradi. `--require-complete` esa barcha fan-fakt/formula review va
qabul qilingan manba doirasi uchun qat’iy, alohida gate; hozir o‘tmaydi. Bu gate ham
7-sinfning qabul qilingan §1–46 doirasini ishlatadi: yo‘q kirish sahifalari sabab
doimiy blok qo‘yilmaydi. Hozirgi to‘siq — tugallanmagan fakt/formula review.

Private tekshiruv **1 069 PDF sahifa**, yangi **352 OCR sahifasi**, barcha yangi
sarlavha va kesilgan region hash’lari mosligini tekshirdi. Hash tasdiqi matematik
haqiqatning ekspert tasdig‘i emas. Testlarning joriy natijalari [SOURCE_REVIEW.md](SOURCE_REVIEW.md)da.

## 6-sinfni boshlashga tayyorlik

Manba va tartib tayyor: **176 sahifa, 7 bob, 61 bo‘lim**, mavjud Biologiya/runtime’dan
ajratilgan. Birinchi partiya §1–7; **foydalanuvchi tasdig‘idan so‘ng** ularning to‘liq
matni, tushunchalari, birliklari va topshiriq dalillari tekshirilib original darslar
muallifligi boshlanishi mumkin. To‘liq formula/FRQ banki yoki ishlaydigan yangi input
UI hozir tayyor emas. 7-sinfning yo‘q kirish sahifalari boshqa sinflarni bloklamaydi.
