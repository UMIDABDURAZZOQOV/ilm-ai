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


## 2026-10-22 — 2-bosqich, 6-sinf §1–7 doirasidagi qayta tekshiruv

Asl `fizika_6_uzb.pdf`ning **PDF/bosma3–16** to‘liq matni va barcha 14 sahifa
asl tasviri dars yozishdan oldin qayta ko‘rildi; source byte/text/render SHA’lari
ham amalda solishtirildi. Frozen darslar va tasvir evidence hash’lari:
`grade6_batch1.json`, `grade6_batch1_review.json`. PDF/rasm/to‘liq OCR Gitga kirmaydi.

31 karta, 8 original misol, 43 topshiriq, 5 FRQ lokal sinov uchun yozilgan.
§1–5 konseptual; §6–7 dagi besh hisoblash qoidasigina runtime graderga kiritilgan.
Boshqa sinf/fakt/formulalar to‘liq ekspertizadan o‘tdi deyilmaydi.

Ilmiy istisnolar: PDF7 tarixiy nationality/telescope-priority iboralari va qadimgi
atom «bo‘linmasligi» zamonaviy fakt sifatida o‘rgatilmaydi; PDF10–11 Piza rivoyati
universal qoida qilinmaydi; PDF13 tarixiy metr etaloni joriy SI ta’rifi emas.
PDF14 dagi «ichki chiziqchalar» soni bilan ko‘rsatilgan formula tafovuti sabab
**teng oraliqlar** aniq sanaladi. PDF15–16 yarim-bo‘linma xatoligi faqat oddiy
shkala modeli, ikki o‘lchov o‘rtachasi barcha xatoni yo‘qotish kafolati emas.
Bularning hech biri sun’iy yangi o‘quv mavzusi yoki tashqi kontentga aylantirilmadi.

Manbani qayta ko‘rish va deterministik arifmetika mustaqil fan/pedagog eksperti
imzosini anglatmaydi: `independent_subject_expert=not_claimed`, umumiy nashr o‘chiq.
Raqamli faoliyat haqiqiy fizik tajriba bajarilganini tasdiqlamaydi.
To‘liq yangi bosqich hisoboti: [STAGE2_GRADE6_BATCH1.md](STAGE2_GRADE6_BATCH1.md).


## 2026-10-22 — §8–35 authored review davomi

Jami35 lokal dars/faoliyat; dastlabki7 bytes/revisionlar saqlandi.82 asl
sahifa to‘liq matn/tasvir bilan qayta ko‘rildi va original PDF/text/PNG
fingerprintlari tekshirildi. Bu barcha316 bo‘limning fan ekspertizasi emas.
Yangi ilmiy tafovutlar, ehtiyotkor shartlar, misol/savollar va testlar
`grade6_batch2..5_review.json` hamda `STAGE2_PROGRESS.md` da.

Aniq map chegarasi: §32 oxirgi formula qutisi PDF90 boshida §33 dan
oldin. Source-only end89 arxivi saqlandi; v2 faqat page90 uchun
`extent_note=original_image_continues_before_next_heading` bilan
explicit continuation qabul qiladi. Tasodifiy page91 yoki umumiy
manbasiz sahifa ruxsati yo‘q.

Muhim yangi tafovutlar: PDF69 suzish/ko‘tarilish farqi; PDF94 g9,81
berilib9,8 hisob ishlatilgani; PDF95 real/ideal FIK farqi. Ular
xato javob kalitiga aylantirilmagan. §36 va keyingi281 bo‘lim
hali authored tayyorlikka kiritilmagan.

## 2026-10-26 — 9-sinf kalorimetriya erratumi (2-bosqich)

Yuqoridagi0interaktivdars holati 1-bosqich tarixiy auditidir. Joriy kontent
qamrovi `STAGE2_PROGRESS.md` va `GRADE9_STAGE2_PROGRESS.json`da.

Original **9-sinf PDF/bosma64**, laboratoriya20ning8-bandi suratida
`m_s*c_s - m_k*c_k` yozilgan. Original **PDF/bosma58**, formula6 esa issiqlik
balansidan kelib chiqadigan to‘g‘ri **plus**ni ko‘rsatadi. Suv ham,kalorimetr
ham Tc danTf gacha isiyapti;ikkalasining qabul qilgan energiyasi qo‘shiladi:

`ch = (mw*cw + mc*cc)*(Tf-Tc)/(mh*(Th-Tf))`, `Tc<Tf<Th`.

Ikkala original tasvir ko‘rildi. Hisobiy regressiya: suvning mc ko‘paytmasi
210J/K,kalorimetrniki178J/K,Tf-Tc10K,mh0.2kg,Th-Tf50K. To‘g‘ri
natija **388J/(kg*K)**;minus varianti **32J/(kg*K)** chiqardi. Validator va
server testlari minus formulani ham,uning sonli javobini ham rad qiladi.
Ikkala manba sahifasi dars20ga bog‘langan;PDF va frozen xarita o‘zgarmadi.

Bu agent bajargan manba/energiya-balans tekshiruvidir;mustaqil kalorimetriya
mutaxassisi tasdig‘i bajarildi deyilmaydi. General publication oldidan shu
review talab qilinadi. Raqamli laboratoriya jismoniy tajriba tasdig‘i emas.

## 9-sinf §26–30 — issiqlik dvigatellari va manba tafovutlari (2026-10-26)

PDF/bosma81–90 asl tasvirlari, formulalar va split-PDF88/89 chegarasi ko‘rildi.
§26 va §29 konseptual; manbada bo‘lmagan formula yoki to‘rt takt diagrammasi
qo‘shilmadi.81-sahifadagi qisqa so‘rish/yondirish bayoni to‘liq takt jadvali
sifatida olinmadi; «oktan yonuvchi gaz» degan tasnif ham takrorlanmadi.

84-sahifadagi siqilish ishining belgilari gaz BY ishi bilan tashqi kuch ON
ishini aralashtirmasdan izohlandi. To‘liq siklda DU=0, A_BY=Qh-Qc; Qh/Qc
musbat modullar. Karno ikki izoterma va ikki adiabatadan iborat qaytar model.
85-sahifadagi FIK «faqat temperatura farqiga proporsional» jumlasi to‘liq emas:
eta_max=(Th-Tc)/Th, Th ham kerak. Masalan,600/300K uchun0.5,1200/900K
uchun0.25, farq ikkalasida300K. Bu ixtiyoriy real dvigatelning aynan FIK’i
emas.86-sahifadagi273 yaqinlashuvi aniq273.15 bilan yashirin aralashtirilmadi;
yangi masalalar Kelvin qiymatlarida.

87–88-sahifalardagi tarixiy global sarf, quvvat va chiqindi raqamlari hozirgi
statistika yoki yangi iqlim qonuni sifatida ishlatilmadi. Quyoshni barcha
vaziyatda yagona yechim, barcha sovitkich moddalarini bir xil ozon yemiruvchi
deb ko‘rsatadigan umumlashtirishlar ko‘chirilmadi. Asosiy ekologik tushunchalar
manbaga bog‘langan; mustaqil ekologiya mutaxassisi review’i bajarildi deyilmaydi.

89-sahifadagi kerosin q=46MJ/kg 66-sahifadagi42MJ/kg jadval bilan farq qiladi.
Yangi suv isitish masalasida noma’lum turdagi yoqilg‘i uchun q=40MJ/kg **berilgan
hisobiy parametr**; kerosin uchun yangi universal konstanta yaratilmagan.
Foydali isitish energiyasi mexanik ish bilan teng nomlanmaydi.90-sahifadagi
P=eta*rho*V*q*v/s o‘zgarmas tezlik/o‘rtacha foydali quvvat modelida qo‘llanadi.
PDF, frozen xarita, oldingi darslar va Biology o‘zgartirilmadi. Barchasi lokal/test
preview; mustaqil fan/pedagogik review va Android sinovi hali bajarilmagan.
