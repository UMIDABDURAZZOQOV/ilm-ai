# Manba review — hozirgi chegaralar

## 2026-11-04 — III qism23–26/30, PDF46–55

To‘liq asl tasvirlar ko‘rildi.23asl sarlavha «Shartni yetishmayotgan ma’lumotlar bilan to‘ldirish»; oldingi93dars checkpointi davom sarlavhasidagi «Murakkab...» nomi xato bo‘lgan. Applicationda u payt23dars hali yo‘q edi; eski93dars kontenti o‘zgarmagan.
PDF53/bosma51 footer **29-dars.O‘yin-dars**, TOC81 esa **28-dars.O‘yin-dars** deydi. Source-map TOClabel28va footer29ni alohida provenance bilan saqlaydi; alohida29tana yoki tayyor dars yaratilmagan. Footer53pini original26mavzu reviewida ham tekshiriladi; validator tafovut yashirilmasligini tekshiradi.
24juftliklarda tartib/takror qoidasi ochiq.25ribbon mashqidagi6bo‘sh shablonning o‘zi6yagona javob isboti deb olinmagan: original karta tanlovi «tartib ahamiyatsiz» deb belgilangan.26uchidagi hafta sikli va nisbiy kunlar matematik tekshirilgan.30cm modelida oraliqlar sanaladi, fizik ekran o‘lchovi da’vo qilinmaydi; tarixiy tana bilan taxmin qilish zamonaviyinch/foot standartlari o‘zgaruvchan degan da’voga aylantirilmagan.


## 2026-11-04 — III qism18–22: to‘liq asl tasvirlar

PDF36–45/bosma34–43 o‘qildi.23–26 va30–42 hali mualliflik reviewidan o‘tmagan.

- Source18: ko‘p/kam,farq,complement,count/order/chain. Harbiy tasvirlar va sana
  umumiy fakt bo‘lib ko‘chirilmagan; original rasm guruhlari ishlatilgan.
- Source19 PDF38–39: yo‘ldoshlar soni vaqtga bog‘liq. Kitobdagi Yupiter79/Saturn82
  qiymatlari amaldagi2026 statistika sifatida tasdiqlanmagan; yangi raqamlar
  ham taxmin qilinmagan. Nomlangan original maket jadvali28/15/0/0 bilan ayni
  arifmetika o‘rgatiladi. Ikki nol va bir xil/katta miqdor aniq tekshiriladi.
- Source20 PDF40–41: yorqinlik rasmi sharoitsiz fizik o‘lchov emas; astronomik
  turkumdagi nuqtalar umumiy populyatsiya deb olinmaydi. Original7/9/7sanash
  belgilaridan foydalanildi. Kitobning rasm/uzun matni Gitga ko‘chirilmagan.
- Source21 PDF42–43: birinchi parvoz yoshlariga mustaqil tarixiy tasdiq yo‘q;
  tekshirilmagan tuzatish ham da’vo qilinmaydi. Original taqqoslash masalalari,
  bir xil katak bir xil son bo‘lishi sharti va qavslar ishlatilgan. Bu CAS emas.
- Source22 PDF44–45: uch qism,ikki bosqich,bir xil farq,shakllar bog‘lanishi
  mustaqil hisoblandi.6uchburchak uchun5doira va7kvadrat; boshlang‘ich3/4dan
  qo‘shimcha2doira/3kvadrat. Teskari tekshiruvlar original,ko‘chirilmagan.

Source pins va har birlikning PDF/bosma sahifalari batch4_review.json va
batch4.jsonda. Bu manbaga sodiq original lokal kontent; mustaqil pedagogik
review,realAndroid,pilot hamda2026–27rasmiy dasturga moslik hali tasdiqlanmagan.


## 2026-11-04 — II qismning barcha mavjud32 mavzusi: jami73 lokal dars

1-sinf I qismning **41/41** darsi saqlandi. Shu sessiyada II qismning42–73
raqamli barcha **32 mavjud mavzusi**6partiyada qo‘shildi:192 karta,32 original
misol/96qadam,256 topshiriq va62 sonli tenglik. **IIqism33mavzudan32ta**:
74«Misol va masalalar yechish»ning bosma68–69sahifalari PDFda yo‘q.
Uning kontenti yoki progressi yaratilmagan. Butun1–11-sinf kursi hali tugallanmagan;
umumiy mavzular/qolganlar soni noma’lum. Faqat `local_test_preview_only`, `course_ready=false`.

Jami **73 dars,422 karta,73misol/219qadam,544 topshiriq,108 sonli tenglik**.
Bosqichlar:272 guided,73 MCQ,73 FRQ,126 transfer. Javoblar:172 choice,
24 short_text,334 exact_number,14 ordering.65 turdagi boshlang‘ich model;
ular umumiyCAS, ilg‘or grafik yoki haqiqiy3D tizimi degani emas.

Oxirgi69–73partiya PDF59–68/bosma58–67: teskari qo‘shish/ayirish,
ko‘p komponentli qo‘shish, guruhlash, jadvaldagi noma’lum va qavsli ifodalar.
Har karta, misol qadami, sonli tenglik, savol va feedback manbaga bog‘langan.
Yangi5dars30 karta/5misolning15qadami/40 topshiriq/12 tenglikdan iborat.
Qo‘shishning guruhlash xossasi ayirishga asossiz tatbiq qilinmaydi;
chapdan-o‘ngga qoida faqat hozir o‘rgatilgan+va−uchun ishlatiladi.
Darslikdagi noto‘g‘ri tenglikli true/false va xato-topish mashqlari tayyor
javob kaliti sifatida olinmadi. Mamlakatlar soni, fazogirlar jadvali,
nafas olish me’yorlari va boshqa mustaqil tasdiqlanmagan tashqi faktlar
arifmetik ko‘nikmaga mos, aniq shartli original masalalar bilan almashtirildi.
Kitobning uzun matni yoki rasmi Gitga ko‘chirilmagan.

Texnika: MathAPIga faqat import qilingan kitoblar ro‘yxati, haqiqiy
bibliografiya, part-local`sequence`dan alohida`source_number`, manbadagi
jami mavzu soni va gaplar qo‘shildi. Iqism41mavzusi tugamaguncha IIqism
serverda ham yopiq. IIqism32/33holati keyingi qismni soxta to‘liq deb ochmaydi.
Import immutable/additive; yangiDBmigration yo‘q. Javob kalitlari/private
rubric mijozga yuborilmaydi; baholash serverda. Flutterda kitob tanlash,
o‘nlik/birlik,100jadvali,cho‘t,ikki xonali amallar,jadval va qavs modellari
qo‘shildi. Kitob almashish timeoutida eski tanlov saqlanadi;422dan keyin
javob tahrirlanadi. Yopiq kitobda avval prerequisite sababi, mavjud kitobda
esa yetishmagan manba qaydi ko‘rsatiladi.200%matnda gap xabari sabab yopilish
sababi ekrandan surilib ketgan holat yakuniy regressionda tuzatildi.

Amalda tekshirildi:

- Math: **100 passed,1 skipped,123.48 s**; skip — alohida ishga tushirilganPGtest.
- OwnloopbackPostgreSQL16: **1passed,24.42 s**. Barcha73 dars, UUIDreplay,
  parallel birinchi mukofot, immutable reimport; old137XP→867/73progress,
  boshqaUIDXP0, qayta bajarish0XP. Bu izolyatsiyalangan test ma’lumoti.
- To‘liq Flutter: **491 passed,2:36**. Oldingi yakuniy urinish490pass/1failure
  bo‘ldi; prerequisite xabari ustuvorligi tuzatilib,18targeted va butun491test
  qayta o‘tdi.320px/200%matn/ReduceMotion bilan barcha32yangi oqim tekshirildi.
- Analyze: **0 muammo,1.3 s**. DebugJS Mathpreview build: **33.7 s**,
  lokalAPI/testUID/invalidcompile-onlytoken bilan. HaqiqiyJWT buildga kiritilmadi.
  Bu haqiqiy brauzer/API yoki Android sinovi emas.
- Biology/Physics/mobileOAuth himoyasi: **46 passed,102.78 s**.
- 23 asl PDF/2958 sahifa SHA va73mavzu/146 dars tanasi tasvir/native-text auditi o‘tdi.
  IIIqismning7 boshlang‘ich pinlari ham alohida qayta tekshirildi, ammo u yerda0 dars.
- IqismningbarchaJSON/map/reviewlari sessiya oldingi`0a367e0`bilan bir xil;
  beshta himoyalangan worktree avvalgiHEADda va toza. Normalapp/auth/Gradle,
  frontend, boshqa fanlar va production o‘zgarmadi. Yangi to‘liq backend da’vosi yo‘q.

**Keyingi:1-sinf III qism,1-dars«Masalaning tarkibi»,PDF6–7/bosma4–5.**
Bu2024yilgi qayta ishlangan2-nashr; I/IIqism2023. Raqamlash1dan qaytadi,
uni75deb davom ettirmang. Keyingi sarlavhaPDF8/bosma6. IIIqismning to‘liq
tana xaritasi hali yo‘q; TOCdagi takror28/nazorat/o‘yin bloklarini taxminan
sanamang. [Aniq texnik handoff](PART3_SOURCE_HANDOFF.md).
9-sinfAlgebra/11-sinfIqismtransferi32MiBchegarasida;6-sinfIIva7–10Geometriya
manbalari yo‘q. Bu cheklovlar mavjud kitoblardagi mualliflikni to‘xtatmaydi.

RealAndroid/SDK, mustaqil o‘qituvchi/pilot va rasmiy2026–27moslik hali
**not_verified**. Cloudstandalone CLI positive-run Git-directoryguard sabab hali
sinovdan o‘tmagan; himoya chetlab o‘tilmagan. O‘zimizningPGkonteyneri testdan
so‘ng to‘xtatiladi; restartda privateURL porti own containerdan yangilansin,
credential logga chiqmasin. Ikkala repo uchun yangi`gh pr list`hamGitHub GraphQL
`Forbidden`qaytardi; PR yaratilmagan yoki bor deb da’vo qilinmagan.
Merge/deploy/productionimport/nashr bajarilmadi.

[Checkpoint](checkpoints/grade1_part2_batch6.json),
[32 mavzuning to‘liq ro‘yxati](PART2_PROGRESS.md).


## 2026-11-03 — 1-sinf I qism: 41/41 mavzu

**Birinchi kitobning mavzulari qamrab olindi. Butun 1–11-sinf Matematika kursi hali tugallanmagan.**
Faqat lokal test uchun: 41 dars, 230 karta, 41 original misolning 123 qadami va 288 topshiriq.
Bosqichlar: 144 guided, 41 MCQ, 41 FRQ va 62 transfer. Javob turlari: 113 variantli,
24 aniq atama, 144 sonli va 7 tartiblash topshirig‘i. 37 turdagi boshlang‘ich interaktiv model bor.
46 ta sonli misol tengligi import paytida aniq arifmetika bilan tekshiriladi.
Umumiy algebra/CAS, ilg‘or grafik va haqiqiy 3D o‘lchash mexanizmi hali tayyor emas.

Dastlabki 5 dars va ularning review fayllari o‘zgarmadi. Yangi 6–41-darslar qo‘shildi;
import eski mazmun yoki progressni qayta yozmaydi. Har bir kartaning, misol qadamining,
savolning va izohning manba havolasi reviewdagi kitob/sinf/qism/mavzu/sahifaga mos bo‘lishi shart.
Birinchi PDFning 94 sahifasi ko‘rildi, 82 ta dars sahifasi tasvirlari pin bilan bog‘landi.
PDF 55–56 takror skan; qo‘shimcha dars emas. Bosma/PDF sahifalar uchun yagona offset ishlatilmadi.
Qo‘lyozma javoblar tekshirilgan javob kaliti sifatida olinmadi.

Amalda bajarilgan yakuniy tekshiruvlar:

- Math: **65 passed, 1 skipped, 44.82 s**. Skip — alohida ishga tushiriladigan PostgreSQL testi.
- Alohida loopback PostgreSQL 16: **1 passed, 18.83 s**; barcha 41 dars, parallel birinchi XP, replay va immutable import.
- To‘liq Flutter: **440 passed, 2 min 7 s**; analyze — **0 muammo, 2.2 s**.
- Debug JS web build: **35.7 s**. Flag, lokal API URL va test UID berildi; haqiqiy JWT ishlatilmadi.
  Bu natija haqiqiy brauzer/API yoki Android sinovi emas.
- Biology completion/curriculum, Physics course va mobil OAuth himoya regressiyasi: **46 passed, 112.33 s**.
- 23 ta mavjud PDF va 2 958 sahifaning hash auditi o‘tdi. Bu barcha kitoblar mazmuni to‘liq o‘qilganini anglatmaydi.

Lokal test akkauntining eski 137 XP qiymati saqlanib, 547 XP bo‘ldi; 41 progress yozuvi bor.
Boshqa akkaunt XPsi o‘zgarmadi. Qayta bajarish 0 XP berdi. Bu test ma’lumoti, mahsulot uchun soxta statistika emas.
Ilmo, brend, normal app/API/auth, frontend, umumiy Gradle, production va boshqa fanlar fayllari o‘zgarmadi.
Himoyalangan beshta worktree avvalgi HEADda va toza qoldi. Yangi to‘liq backend regressiyasi da’vo qilinmaydi;
eski keng natija birinchi checkpointda, hozirgi Math va himoya sinovlari esa alohida qayd etilgan.

Yangi interaktivlik: vaqt tartibi, guruh tarkibi/miqdori, sonlar qatori, qo‘shish/ayirish,
butun–qism, juftlash, natural sonlar, nuqta/chiziq/kesma, siniq yo‘l, noma’lum had,
qo‘shiluvchilar o‘rnini almashtirish, jadval, taqqoslash va bosqichli ifoda.
Oqimlar 320 px, 200% matn va Reduce Motion bilan tekshirildi. Xatoda bosqichli ishora,
tartiblashda to‘liq ID permutatsiyasi, timeoutda saqlangan UUID bilan qayta yuborish ishlaydi.

### II qismda aniqlangan manba kamchiligi

II qismda 42–74 raqamli **33 ta mundarija bo‘limi**, 32 ta native sarlavha lokatori va **0 tayyor dars** bor.
PDF 68 / bosma 67 dan PDF 69 / bosma 70 mundarijaga o‘tiladi.
**74 «Misol va masalalar yechish» mavzusining bosma 68–69-sahifalari yo‘q.** Mazmuni taxmin qilinmadi.
`grade1_part2_map.json`da gap va tasvir SHA dalillari saqlandi. Faqat 42 va 73-mavzuning tana tasvirlari o‘qildi;
qolgan 30 mavzuning tanasi to‘liq tekshirilmagan. Mundarija yoki lokator tayyor dars hisoblanmaydi.
9-sinf Algebra va 11-sinf I qism transferda 32 MiB bilan bloklangan. 6-sinf II qism va 7–10-sinf Geometriya manbalari ham yo‘q.

**Keyingi: 1-sinf II qism, 42 «11 dan 20 gacha bo‘lgan sonlar», PDF 5–6 / bosma 4–5.**
[Texnik handoff](FIRST_BOOK_COMPLETION.md), [dalil](checkpoints/grade1_part1_batch8.json).
Backend kod: `b29fff9858d0f6dc6fbc3b0d6cf252d0d5a3f53f`. Flutter: `f69de9b0accb1cda6835e0858a355a07d68ec280`. Ikkala feature branch GitHubga push qilindi.
GitHub GraphQL 403 qaytardi; PR yaratilmagan. Merge/deploy/nashr bajarilmadi.
Android SDK yo‘q; real telefon, mustaqil o‘qituvchi, pilot va rasmiy dastur mosligi tekshirilmagan.
`course_ready=false` va `publication=local_test_preview_only` saqlandi.

## 2026-11-03 — 35 darslik tekshirilgan checkpoint

**1-sinf I qism: 35/41 mualliflik darsi**, 194 karta, 35 original
misol/105 qadam, 240 topshiriq. Butun1–11kurs tugallanmagan;
umumiy mavzular/qolganlar soni hali noma’lum. Nashr: faqat lokal test.

31–35: kesma oxirlari/bo‘g‘inlar/nuqtalar, qo‘shish/ayirish hadlari, noma’lum qo‘shiluvchi va kamayuvchi. Original siniq chiziq modeli va ma’lum had o‘zgarganda yechimni qayta ochish modeli bor. FRQ sonli yoki aniq atama bilan serverda baholanadi; umumiy symbolicCAS deb ko‘rsatilmaydi. AB va BA ayni kesma; nuqta sanog‘i bilan bo‘g‘in sanog‘i ajratiladi.

Yangi partiya manbalari:

| Mavzu | PDF | Bosma |
|---|---|---|
| 31 To‘g‘ri chiziq kesmasi. Siniq chiziq | 67–68 | 64–65 |
| 32 Qo‘shish hadlari | 69–70 | 66–67 |
| 33 Ayirish hadlari | 71–72 | 68–69 |
| 34 Noma’lum qo‘shiluvchini topish | 73–74 | 70–71 |
| 35 Noma’lum kamayuvchini topish | 75–76 | 72–73 |

Haqiqiy sinovlar:

- math: `61 passed, 1 skipped in 45.77s`.
- postgres: `1 passed in 26.13s`.
- flutter_math: `01:10 +60: All tests passed!`.
- analyze: `No issues found! (ran in 1.3s)`.

Manba auditi:23PDF/2958sahifa va70tana sahifasi tasviri/hash.
SQLite va o‘zimizning alohida loopbackPG16 sxemasi: barcha35dars, idempotent
import, progress, replay0XP,137oldXP→487; parallel birinchi completion bitta mukofot.
Birinchi5kontent/review o‘zgarmagan. Boshqa fanlar, auth, frontend, umumiy Gradle,
normal app va production o‘zgartirilmagan. Android va pedagogik mustaqil ekspertiza yo‘q.
Manba transferidagi2kattaPDF va yetishmayotgan5manba cheklovi saqlangan.

Keyingi: **36 «Noma’lum ayriluvchini topish»,PDF77–78/bosma74–75**.
1-sinf I qismning6mavzusi hali yozilmagan.
Backend `3aada2e0de32efe3fff9e71352a229068a626bf5`; Flutter `aa9df2e8f9bdcba6a90f52ff91ff3d1820d4e4dc`. [Dalil](checkpoints/grade1_part1_batch7.json).

## 2026-11-03 — 30 darslik tekshirilgan checkpoint

**1-sinf I qism: 30/41 mualliflik darsi**, 164 karta, 30 original
misol/90 qadam, 200 topshiriq. Butun1–11kurs tugallanmagan;
umumiy mavzular/qolganlar soni hali noma’lum. Nashr: faqat lokal test.

26–30: 10ning ikki raqamli yozuvi, o‘sish/kamayish, natural sonlar kelishuvi, juft/toq va nuqta/chiziqlar. 0ning natural emasligi shu darslik kelishuvi sifatida beriladi; juftlik bilan aralashtirilmaydi. 10elementli tartiblash serverda to‘liq permutatsiya bilan tekshiriladi. Noma’lum explorer client/serverda fail-closed rad etiladi. Original to‘g‘ri/egri chiziq modeli va nuqta semantikasi qo‘shildi.

Yangi partiya manbalari:

| Mavzu | PDF | Bosma |
|---|---|---|
| 26 10 soni | 57–58 | 54–55 |
| 27 1 dan 10 gacha bo‘lgan sonlar. Sonlarni taqqoslash | 59–60 | 56–57 |
| 28 Natural sonlar | 61–62 | 58–59 |
| 29 Juft va toq sonlar | 63–64 | 60–61 |
| 30 Nuqta. To‘g‘ri va egri chiziq | 65–66 | 62–63 |

Haqiqiy sinovlar:

- math: `60 passed, 1 skipped in 25.13s`.
- postgres: `1 passed in 12.81s`.
- flutter_math: `00:41 +52: All tests passed!`.
- analyze: `No issues found! (ran in 1.6s)`.

Manba auditi:23PDF/2958sahifa va60tana sahifasi tasviri/hash.
SQLite va o‘zimizning alohida loopbackPG16 sxemasi: barcha30dars, idempotent
import, progress, replay0XP,137oldXP→437; parallel birinchi completion bitta mukofot.
Birinchi5kontent/review o‘zgarmagan. Boshqa fanlar, auth, frontend, umumiy Gradle,
normal app va production o‘zgartirilmagan. Android va pedagogik mustaqil ekspertiza yo‘q.
Manba transferidagi2kattaPDF va yetishmayotgan5manba cheklovi saqlangan.

Keyingi: **31 «To‘g‘ri chiziq kesmasi. Siniq chiziq»,PDF67–68/bosma64–65**.
1-sinf I qismning11mavzusi hali yozilmagan.
Backend `ad35c8e5d73011157d9c82b4a573d2f4fb34009c`; Flutter `1f15a4a4c7f882448310a51dab49b97fc2fe1ccf`. [Dalil](checkpoints/grade1_part1_batch6.json).

## 2026-11-03 — 25 darslik tekshirilgan checkpoint

**1-sinf I qism: 25/41 mualliflik darsi**, 134 karta, 25 original
misol/75 qadam, 160 topshiriq. Butun1–11kurs tugallanmagan;
umumiy mavzular/qolganlar soni hali noma’lum. Nashr: faqat lokal test.

21–25: olti–to‘qqiz va nol. Ikki tomondan sanoqda o‘rindagi belgi bir marta hisoblanadi; kun/mashg‘ulot, jami/yonma-yon joy va turli yil boshlanishlari ajratildi. Nol — aniq javob; bo‘sh input422bilan rad etiladi. Katta guruhlar Wrap orqali kichik ekranga moslashadi. PDF55–56 takror hisoblanmaydi; keyingi26mavzu PDF57dan, bosma54dan boshlanadi.

Yangi partiya manbalari:

| Mavzu | PDF | Bosma |
|---|---|---|
| 21 6 soni va raqami | 45–46 | 44–45 |
| 22 7 soni va raqami | 47–48 | 46–47 |
| 23 8 soni va raqami | 49–50 | 48–49 |
| 24 9 soni va raqami | 51–52 | 50–51 |
| 25 0 soni va raqami | 53–54 | 52–53 |

Haqiqiy sinovlar:

- math: `57 passed, 1 skipped in 18.20s`.
- postgres: `1 passed in 7.32s`.
- flutter_math: `00:34 +43: All tests passed!`.
- analyze: `No issues found! (ran in 1.8s)`.

Manba auditi:23PDF/2958sahifa va50tana sahifasi tasviri/hash.
SQLite va o‘zimizning alohida loopbackPG16 sxemasi: barcha25dars, idempotent
import, progress, replay0XP,137oldXP→387; parallel birinchi completion bitta mukofot.
Birinchi5kontent/review o‘zgarmagan. Boshqa fanlar, auth, frontend, umumiy Gradle,
normal app va production o‘zgartirilmagan. Android va pedagogik mustaqil ekspertiza yo‘q.
Manba transferidagi2kattaPDF va yetishmayotgan5manba cheklovi saqlangan.

Keyingi: **26 «10 soni»,PDF57–58/bosma54–55**.
1-sinf I qismning16mavzusi hali yozilmagan.
Backend `246f41ef6f711707e3a83a18076a291ac570c124`; Flutter `c5d8e3a88770059b27eeb1d872db6e65a266fe51`. [Dalil](checkpoints/grade1_part1_batch5.json).

## 2026-11-03 — 20 darslik tekshirilgan checkpoint

**1-sinf I qism: 20/41 mualliflik darsi**, 104 karta, 20 original
misol/60 qadam, 120 topshiriq. Butun1–11kurs tugallanmagan;
umumiy mavzular/qolganlar soni hali noma’lum. Nashr: faqat lokal test.

16–20: uch/to‘rt/besh tarkibi, juft bilan buyum sanog‘i, butun–qism, qo‘shni oraliqlar bo‘ylab qo‘shish/ayirish. Har bir guruhlashda narsalar bir marta hisoblanadi. Boshlanish nuqtasi qadam hisoblanmaydi. Qo‘lyozma noto‘g‘ri javoblar kalit sifatida ishlatilmadi.

Yangi partiya manbalari:

| Mavzu | PDF | Bosma |
|---|---|---|
| 16 3 soni va raqami | 35–36 | 34–35 |
| 17 4 soni va raqami | 37–38 | 36–37 |
| 18 5 soni va raqami | 39–40 | 38–39 |
| 19 1 dan 5 gacha bo‘lgan sonlar | 41–42 | 40–41 |
| 20 1 dan 5 gacha bo‘lgan sonlar bilan amallar bajarish | 43–44 | 42–43 |

Haqiqiy sinovlar:

- math: `55 passed, 1 skipped in 12.00s`.
- postgres: `1 passed in 5.65s`.
- flutter_math: `00:25 +35: All tests passed!`.
- analyze: `No issues found! (ran in 1.8s)`.

Manba auditi:23PDF/2958sahifa va40tana sahifasi tasviri/hash.
SQLite va o‘zimizning alohida loopbackPG16 sxemasi: barcha20dars, idempotent
import, progress, replay0XP,137oldXP→337; parallel birinchi completion bitta mukofot.
Birinchi5kontent/review o‘zgarmagan. Boshqa fanlar, auth, frontend, umumiy Gradle,
normal app va production o‘zgartirilmagan. Android va pedagogik mustaqil ekspertiza yo‘q.
Manba transferidagi2kattaPDF va yetishmayotgan5manba cheklovi saqlangan.

Keyingi: **21 «6 soni va raqami»,PDF45–46/bosma44–45**.
1-sinf I qismning21mavzusi hali yozilmagan.
Backend `304226e1b3840db7123489e025055df8e1defa8a`; Flutter `3c3ee6f3d12492a9606aad81a38fc3ae38ebb105`. [Dalil](checkpoints/grade1_part1_batch4.json).

## 2026-11-03 — 15 darslik tekshirilgan checkpoint

**1-sinf I qism: 15/41 mualliflik darsi**, 79 karta, 15 original
misol/45 qadam, 90 topshiriq. Butun1–11kurs tugallanmagan;
umumiy mavzular/qolganlar soni hali noma’lum. Nashr: faqat lokal test.

11–15: qo‘shish/ayirish, >/< /= yo‘nalishi, 1 va2, buyum bilan bo‘lak sanog‘i. To‘rtta original tenglik yozuvi exact parser bilan importda tekshiriladi. Bu umumiy algebra CAS emas. Ayirishning oldin/keyin holatlari alohida; hali o‘rgatilmagan nol modelga kiritilmadi. Qo‘lda raqam yozish sifati avtomatik baholanmaydi.

Yangi partiya manbalari:

| Mavzu | PDF | Bosma |
|---|---|---|
| 11 Qo‘shish | 25–26 | 24–25 |
| 12 Ayirish | 27–28 | 26–27 |
| 13 Sonlarni taqqoslash | 29–30 | 28–29 |
| 14 1 soni va raqami | 31–32 | 30–31 |
| 15 2 soni va raqami | 33–34 | 32–33 |

Haqiqiy sinovlar:

- math: `53 passed, 1 skipped in 7.97s`.
- postgres: `1 passed in 4.69s`.
- flutter_full: `01:42 +396: All tests passed!`.
- analyze: `No issues found! (ran in 1.6s)`.

Manba auditi:23PDF/2958sahifa va30tana sahifasi tasviri/hash.
SQLite va o‘zimizning alohida loopbackPG16 sxemasi: barcha15dars, idempotent
import, progress, replay0XP,137oldXP→287; parallel birinchi completion bitta mukofot.
Birinchi5kontent/review o‘zgarmagan. Boshqa fanlar, auth, frontend, umumiy Gradle,
normal app va production o‘zgartirilmagan. Android va pedagogik mustaqil ekspertiza yo‘q.
Manba transferidagi2kattaPDF va yetishmayotgan5manba cheklovi saqlangan.

Keyingi: **16 «3 soni va raqami»,PDF35–36/bosma34–35**.
1-sinf I qismning26mavzusi hali yozilmagan.
Backend `5e7bcc45529e4074d6698294af65d34e05ec8724`; Flutter `9b1ed1529985b3f0a372238a1b0677ce1011105d`. [Dalil](checkpoints/grade1_part1_batch3.json).

## 2026-11-03 — ikkinchi tekshirilgan partiya

1-sinf I qism **1–10: 10 dars, 54 karta, 10 original misol/30 qadam, 60 topshiriq**.
6 «Vaqt bo‘yicha ketma-ketlik» PDF15–16/bosma14–15; 7 «Narsalar guruhi»17–18/16–17;
8 «Guruhlarni taqqoslash»19–20/18–19; 9 «1 dan10gacha bo‘lgan sonlar»21–22/20–21;
10 «Narsalar sanog‘i»23–24/22–23. Har bir asl tana tasviri qayta o‘qildi.
Guruh tarkibi bilan teng miqdor farqlanadi; qo‘shni-son topshiriqlari ko‘rsatilgan1–10
qatorining ichki2–9sonlari bilan cheklangan. Qo‘lyozma kalit emas.

Yangi ordering javobi yagona to‘liq ID permutatsiyasini serverda tekshiradi. Noto‘g‘ri
haqiqiy tartib feedback/ishora oladi; dublikat/noma’lum/to‘liqmas ID422bilan rad etiladi.
Mavjud MCQ/FRQ va birinchi5JSON/review o‘zgarmadi; import immutable/additive.
Flutter timeline, tarkib/miqdor taqqoslash va chegaralangan sonlar qatori bilan boyitildi.
Bir xil nomli4/10mavzular endi tartib raqami va barqaror key bilan ajraladi.

Testlar: Math **50 passed,1 skipped5.50s**; alohida haqiqiyPG16 **1passed3.08s**
(all10,parallel firstXP,replay); Flutter Math **20passed13s**, analyze **0issue1.6s**.
137oldXP→237; barcha10progress; qayta bajarish0XP. 23PDF/2958sahifa hash auditi o‘tdi;
20tana sahifasi/10mavzu image pinlari tasdiqlandi. Bu partiyada to‘liq backend/Flutter
regressiyasi qayta bajarilmadi; oldingi keng natijalar birinchi checkpointda saqlandi.
Android/o‘qituvchi/pilot/rasmiy dastur holati o‘zgarmagan.

Keyingi: **11 «Qo‘shish»,PDF25–26/bosma24–25**; Iqismning31mavzusi hali yozilmagan.
Butun1–11kursning jami/qolganlari noma’lum; manba cheklovlari saqlangan.
[Dalil](checkpoints/grade1_part1_batch2.json). Backend `71c22693e9574ecee0f4cca2fb3c31fee53d667f`,Flutter `5c4d030c1ef7c86b68bc48609dd53c87f8193e23`.

1-sinf I qism PDF3 bibliografiya va PDF5–14ning har bir asl tasviri o‘qildi. Bosma4–13ga mos.1–5mavzu sarlavhasi va keyingi chegaralari tekshirildi. Review JSONda original SHA, page-nativeSHA,1.3RGBPNG SHA, fact/page mapping saqlangan. Original diagramma va mashqlar qayta yozildi, uzun kitob matni/rasmi ko‘chirilmadi.

Dars1: shakl/rang/o‘lchamni ajratish. Dars2: bitta tayanchdan uzunlik/balandlik/kenglik taqqosi. Dars3: ekranga qarayotgan o‘quvchining chap/o‘ngi, tayanch va oraliq. Dars4: one-to-one sanash, miqdor/tartib, guruh, joy almashishi. Dars5: yassi model va hajmli buyum modeli farqi. Bu mavzularga sun’iy formula va hajm hisoblash qo‘shilmadi.

Muhim scope: kub/shar2D proyeksiyasi hajmli buyumni ko‘rsatadi; ekrandagi rasm haqiqiy hajm emas. Fizik qutilarning ideal shaklga yaqinligi haqida so‘z yuritiladi. Doira/shar yoki kvadrat/kub bir xil deb baholanmaydi. Chap/o‘ng bolaga nisbatan aniqlanadi; boshqa qarash nuqtasi jim almashtirilmaydi. Count input son yozishni yangi o‘rgatadigan alohida dars o‘rnini bosmaydi;1-sinf keyboard/reading mosligi pedagogik pilotda tekshirilsin.

8-sinf PDF1–2 asl bibliografiya tasvirlari tekshirildi. Native matn ko‘rinishidagi eduportal watermark o‘quv matni sifatida hisoblanmaydi. Butun240sahifa OCR/diagramma/tana tekshiruvi **hali bajarilmagan**. OCR yordamchi locator; hech qanday formula OCR natijasi bilangina reviewdan o‘tdi deyilmaydi.

Qolgan23PDFning hammasi to‘liq o‘qilgan emas. Katalogdagi ayrim ISBNlar OCR yoki source-placeholder ko‘rinishida; checksum/visual review maydoni alohida. 10-sinf ISBN noldan iborat placeholder bo‘lishi mumkin;1-sinfIVqismda «Nashriyot nomi» bosma placeholderi bor. Ularni taxminiy haqiqiy raqam/nashriyotga almashtirmang.

9-sinf va11-sinfIpart transferda bloklangan, SHA noma’lum.6IIva7–10Geometriya manbalari berilmagan. Bu manbalar bor deb, yoki11IIprerequisitelari Iqismsiz to‘liq ekanini taxmin qilmang.2026–2027rasmiydastur, mustaqil matematik/pedagog ekspertiza va real Android/bolalar sinovi not_verified.

## PDF sahifa mappingi: topilgan takror

1-sinfIpart PDF53–54 va55–56 asl tasvirlari ko‘rildi: ikkalasi ham25 «0 soni va raqami», bosma52–53ning takror skanlari. Pixel va nativeSHA boshqa, lekin topshiriq va qo‘lyozma javoblari bir xil.55–56 alohida mavzu yoki yangi bilim sifatida sanalmaydi. Bosma86mundarija PDF89da. Shuning uchun barcha sahifaga bir xil offset qo‘llash xato. Qo‘lyozma o‘quvchi javoblari darslikning tasdiqlangan javob kaliti emas.

`grade1_part1_map.json`:41TOCbirligi asl mundarija tasviri bilan nomlangan va native tana sarlavhalari lokatoriga bog‘langan. Faqat1–5tana sahifalari authored lesson reviewdan o‘tgan; qolgan36hali body review/content pending. Duplicate investigation25mavzuni tayyor dars qilmaydi.
