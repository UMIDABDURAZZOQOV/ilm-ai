# Fizika manba auditi — 2026-10-21

## Qabul qilingan doira va natija

`feat/physics-curriculum-map`, boshlang‘ich `29e7d1e` saqlangan. 6–11-sinfdagi mavjud
**316/316 raqamlangan bo‘lim** asosiy manba sahifalariga bog‘langan. Bu **254 nazariya,
31 laboratoriya, 4 amaliy mashg‘ulot, 1 uy amaliyoti, 26 masala yechish bo‘limi**.
Bundan tashqari bob kirish/yakunlari, nazorat, qo‘shimcha mashq va namuna anchorlari
bor. **Tayyor interaktiv dars/savol: 0.**

7-sinfning qabul qilingan doirasi §1–46, PDF1/bosma8 dan boshlanadi. Bosma1–7 ning
yo‘qligi, foydalanuvchining yakuniy qaroriga ko‘ra, blok emas. `source_complete=false`
saqlanishi butun kitob nusxasi yo‘qligini yashirmaydi. `--require-mapped` ham,
kelajakdagi `--require-complete` ham shu qabul qilingan doirani ishlatadi; yo‘q kirish
sahifalari sababli kursni doimiy bloklash yo‘q.

## Yangi PDF qismlari qanday tekshirildi

- 8-sinf: 1–88 va 89–176, har biri 88 sahifa.
- 9-sinf: 1–44, 45–88, 89–132, 133–176, har biri 44 sahifa.
- Oltita faylning haqiqiy SHA-256si, real sahifa soni va gap/overlap/tartibi tekshirildi.
  Manba fayli nomlari qism tartibi uchun ishlatiladi; tasodifiy upload kataloglari
  alifbo tartibida birlashtirilmaydi.
- Asl PDF88/89, 44/45, 88/89 va 132/133 chegaralarining sahifa tasvirlari ko‘rildi.
  Barcha mavjud bosma sahifa yorliqlari original rastrdan solishtirildi.
- Har bir yangi sahifa PyMuPDF **1.26.6**, scale **2.2** bilan dekodlandi;
  Tesseract **5.5.0**, `eng`, PSM3 bilan OCR qilindi. Uzbek OCR modeli yo‘q;
  OCRni to‘g‘ri fakt/formula deb avtomatik qabul qilish yo‘q.
- 8-sinf rangli sarlavha panellari umumiy OCRda tushib qolishi aniqlandi. Barcha
  **60** panel tasviri alohida mundarija bilan ko‘rildi. 9-sinfdagi **59** sarlavha
  ham body tasviri bilan tekshirildi. Demak xarita faqat mundarijadan tuzilmagan.
- 9-sinfning TOC sahifalari asl faylda bosma173,171,172 tartibida: PDF171,172,173.
  Hech qanday asl PDF sahifa raqami o‘zgartirilmadi; TOC o‘qish tartibi 172→173→171.
- 8-sinf PDF174 mundarija oxirida ko‘rinadigan bosma raqam yo‘q: `printed_page=null`.
- Yangi sahifalarda raw PDF matn qatlami, OCR matni va original RGB rastr uchun
  alohida fingerprintlar bor. `source_regions` chegara sahifalarini sarlavhadan
  oldin/keyin kesadi; region OCR va piksel hash’lari ham tekshiriladi.

PDFlar, rasmlar, sarlavha kontakt rasmlari, OCR va crop matnlari **private**.
Gitda faqat qisqa sarlavhalar, metadata, tekshiruv holati, formulalar va hashlar bor.
`source_set_sha256` segment manifestiga tegishli; u birlashtirilgan PDF hash’i emas.

## Formula inventari nimani tasdiqlaydi

| Sinf | Saqlangan / yangi | Jami rasmdan tekshirilgan yozuv | To‘liq formula/fakt review |
|---|---:|---:|---|
| 6 | 13 / 0 | 13 | Tugallanmagan |
| 7 | 5 / 0 | 5 | Tugallanmagan |
| 8 | 0 / 41 | 41 | Tugallanmagan |
| 9 | 0 / 67 | 67 | Tugallanmagan |
| 10 | 7 / 0 | 7 | Tugallanmagan |
| 11 | 12 / 0 | 12 | Tugallanmagan |
| Jami | 37 / 108 | **145** | **To‘liq inventar deb belgilanmagan** |

Yozuv — alohida transkripsiya, mustaqil fizik qonunlar soni emas. Ekvivalent
ifodalar va birlik tengliklari ham hisobga kiradi. Har yangi yozuv original PDF,
bosma sahifa, qismning SHA-256si va qism ichidagi sahifani beradi. Miqdor ma’nosi,
birlik, qo‘llanish sharti, indeks, vektor/modul va yaxlitlash qayd etilgan.

Ko‘rilgan formulalar orasida Kulon, elektr maydon, tok/kuchlanish/qarshilik,
ketma-ket/parallel ulash, sig‘im, tok ishi/quvvati, Faradey, Amper/Lorens,
molekulyar kattaliklar, ideal gaz/izojarayonlar, termodinamika, issiqlik,
sirt taranglik/elastiklik, namlik, sinish/qaytish va linza hisoblari bor.
Bu ularning barchasi executable graderga tayyor degani emas. Har yozuvda
`ready_for_publication=false`, `executable_grading_rule=false`.

Mavzulardagi `*_candidate` sahifalari va `quantity_term_candidates` OCR orqali
qidirilgan manba joylari; barcha ta’rif, qonun, birlik yoki yechim tasdiqlangan
emas. Tenglama raqamlari matnda qayta kelishi mumkin; nomzod soni formula soni
sifatida e’lon qilinmaydi. Matnda `=` topilmagani formula yo‘q degani emas.

## Dars yoki graderdan oldin hal qilinadigan manba tafovutlari

| Manba | Aniqlangan holat | Keyingi qaror |
|---|---|---|
| 8-sinf §28, PDF82 (1), PDF83 (5) | C₃/U₃ oldida minus, izoh va sxema esa yig‘indini aytadi | Noto‘g‘ri umumiy yozuv ko‘chirilmaydi; fan review bilan to‘g‘ri qoida va manba tafovuti alohida yoziladi |
| 8-sinf §43, PDF124 (3)–(4) | A «atom massasi» deb atalgan, F esa C/mol | Atom/molyar massa va birlik konvensiyasi aniq kelishilmaguncha grader yo‘q |
| 9-sinf §37, PDF109, 1-masala | Shart 4 mm / 5%; yechim jadvali 3 mm / 0,15% | Bu shartga jadvaldagi javob berilmaydi; keyinchalik original namuna mustaqil tekshiriladi |
| 9-sinf §50–51, PDF145–147 | F,f manfiy degan matn bilan −1/F=1/d−1/f yozuvining konvensiyasi noaniq | Modullar va ishorali masofalar aralashtirilmaydi; fan review zarur |
| 9-sinf §50, PDF145; §54, PDF153 | Radiuslar ishorasi va mikroskopdagi l ning model talqini | Formula konteksti/chegarasi tasdiqlanmaguncha umumiy qoida sifatida nashr qilinmaydi |
| 7-sinf PDF168/170 | Imprint «to‘rtinchi», bibliografik satr «uchinchi»; ISBN olinmagan | Ikkala qayd saqlangan; mavjud §1–46 xaritasini bloklamaydi |

Bu tafovutlar taxminiy yangi dars mazmuni bilan to‘ldirilmagan. Darslikning uzun
matni yoki tayyor masalalari ko‘chirilmagan; keyingi mualliflik original bo‘ladi.

## Validator va test dalillari

- `audit_physics_sources.py --require-mapped`: **exit0**, olti sinf qabul qilingan doirada.
- Private tekshiruv: **1 069 PDF sahifa**, **352 OCR sahifa**, yangi sarlavha va barcha
  kesilgan regionlar hash’lari mos. Bu avtomatik matematik ekspertiza emas.
- `--require-complete`: **kutilgan exit2**, `complete_source_and_formula_review_blocked`.
  Sabab — tugallanmagan fakt/formula inventari; 7-sinf kirish sahifalari blok emas.
- Physics: **39 passed (2.64s)**. Segment gap/overlap/tartib/hash, qism ichidagi
  sahifa, asl/bosma TOC istisnosi, kesilgan umumiy sahifa, baseline saqlanishi,
  source-only nashr qoidalari, formula va saved audit drift tekshirildi.
- Yakuniy keng regression: **565 passed, 1 warning (234.79s)** — 39 Physics testi
  va 526 Biology/mobil regression holati. Barcha tanlangan testlar yakuniy kodda qayta o‘tdi.
- Biologiya completion audit: **355 nazariya, 51 faoliyat, 2 527 karta, 2 609 savol**;
  testlar barcha **406 mobil dars/faoliyat va 47 checkpoint**ni ham yakunlaydi.
- Bir mavjud SQLAlchemy `SAWarning`, `routers/skills.py:931`: Subquery `IN()` ichida
  selectga avtomatik o‘raladi. Runtime kod bu source-only bosqichda o‘zgartirilmadi.
- Ruff to‘liq tekshiruv va `git diff --check`: o‘tdi.
- Flutter/Next.js kodi o‘zgarmagan; bu bosqichda Flutter/native Android, PostgreSQL
  staging yoki yangi FRQ runtime testlari bajarilmadi. Oldingi sessiya natijalari
  bu ishda qayta bajarilgan deb ko‘rsatilmaydi.

[Audit snapshot](../../scripts/curriculum/physics/physics_map_audit.json) faqat
source-only holat va tekshiruv natijalarini saqlaydi. Xarita/sonlar uning testida
joriy katalog bilan solishtiriladi. Audit ORM yoki production DBga ulanmaydi.

## Keyingi aniq nuqta

**Foydalanuvchi tasdig‘ini kutish.** 6-sinf §1–7 dan boshlanadi; 176 sahifali
manba, bob/paragraf tartibi va dastlabki texnik reja tayyor. Har partiyadagi
fakt/formula/birlik/namuna/javoblar asl sahifalaridan qayta tekshiriladi, original
kartalar va savollar yaratiladi. Formula kerak bo‘lmagan mavzuga FRQ hisoblash
sun’iy kiritilmaydi. Laboratoriya raqamli faoliyati haqiqiy tajriba bajarilganini
anglatmaydi. FRQ runtime va mobil nashr hozir boshlanmagan.
