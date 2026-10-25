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
| 6 | 61 | 56 | 5 | 234 | 68 | 62 | 365 | 79 | 7 / 1 |
| 7 | 46 | 0 | 46 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 8 | 60 | 0 | 60 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 9 | 59 | 0 | 59 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 10 | 45 | 0 | 45 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 11 | 45 | 0 | 45 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| Jami | 316 | 56 | 260 | 234 | 68 | 62 | 365 | 79 | 7 / 1 |

Formula yozuvlari dars ichidagi izohlangan formulalardir, noyob fizik qonunlar
soni emas. 56 executable qoida oilasi bor: dastlabki 5 + keyingi 51.
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


## Keyingi saqlangan partiya — §18–24

Yana 7 dars/faoliyat: 27 karta, 15 formula yozuvi, 8 misol, 48 topshiriq,
16 FRQ. PDF/bosma45–61: §18 45–46, §19 47–48, §20 49–51,
§21 52–55, §22 55–57, §23 57–59, §24 60–61.
17 sahifaning to‘liq matni va tasviri qayta ko‘rildi; jami53 original sahifa
text/render hash tekshiruvlari o‘tdi. `grade6_batch3.json` va `_review.json`.

Yangi model/domains: yo‘l/sanoq jismi, qadamdan taxminiy masofa, vaqt birliklari,
km/h↔m/s, butun yo‘l/butun vaqt, g=9,81 N/kg bilan kuch/massa, N va kg farqi,
tekis tortishdagi dinamometr ko‘rsatishi, tik kuch/yuza, cm²↔m², ideal press.
PDF48 yulduz masofasi/farsaxdagi bahsli sonlar va PDF55 dagi g=9,8 bilan
yaxlitlangan tayyor javoblar ko‘chirilmagan. Paskal tashqi bosim ortishini
uzatadi; har xil chuqurlikdagi umumiy bosimlar teng degan noto‘g‘ri xulosa yo‘q.
§22 — raqamli ko‘rsatish/reja/tartiblash; sun’iy hisoblash formulasi kiritilmagan.

Physics jami118 passed (19.21s); yangi16 sonli topshiriqda mustaqil aniq javoblar,
muqobil formulalar/birliklar, g domeni, nol yuza/vaqt va kasr qadam soni rad etildi.
Barcha24 darsning HTTP javob/replay/complete va240 XP oqimi o‘tdi.
Flutter haqiqiy public payloadlarida N/Pa/m²/s, massa/hajm/zichlik/tezlik chiplarini
320px/200% da sinadi:16 passed. Source audit53 sahifa.

Haqiqiy holat24/316, qolgan292. Keyingi nuqta §25 PDF62.
§25–29 manba sahifalari62–76 ko‘rildi; dars muallifligi keyingi partiyada.


## Saqlangan navbatdagi partiya — §25–29

5 original dars:22 karta/12 formula yozuvi/7 misol/39 topshiriq/15 FRQ.
PDF/bosma: §25 62–64, §26 64–67, §27 67–70, §28 70–72, §29 73–76.
`grade6_batch4.json` va `_review.json`; 15 to‘liq matn/tasvir ko‘rildi; jami68
asl sahifa text/render hash auditidan o‘tdi. Hozir29/316,287 qolgan.

Muhim ilmiy chegaralar: p=rho*g*h — bir jinsli ustun hissasi, tashqi bosim
qo‘shilmagan. Butun atmosfera doimiy zichlikli ustun emas.1atm=101325Pa exact
konversiya; kitobdagi133,3Pa/mmHg yaxlitlash global exact unit registryga
kiritilmagan. Arximed kuchida rho muhitniki, V siqib chiqarilgan hajm;
sirtida tinch suzishda FA=mg. PDF69 dagi FA>mg ko‘tarilishdan ajratilgan.
A=F*s faqat parallel o‘zgarmas kuchda; tik kuchning ishi nol. Ep ning nol sathi
va Ek=m*v²/2 tekshirildi. Quvvatdagi N bilan kuch birligi N farqlanadi.
J.Uatt «birinchi bug‘ mashinasi» va universal kunlik oziqa energiyasi kabi
bahsli umumlashtirishlar olinmadi. Simob/igna/balandlikka chiqish tajribasi yo‘q.

Partiya Physics119 passed (20.90s): barcha29 dars/197 javob/290 XP, replay va
15 qo‘shimcha mustaqil sonli oracle o‘tdi. Flutter to‘liq142 passed, analyze toza.
Yangi alohida loopback PostgreSQL16 sinovlari2 passed (12.13s): eski7 darsning
migratsiya/concurrency testi va mustaqil schemada yangi29 dars/import/reimport,
legacy137 XP/3 streak/2 stars saqlandi. Dastlab testlar bir schemani bo‘lishib
to‘qnashgan; alohida test moduli/schemalar bilan tuzatildi, application
migratsiyasini idempotent deb soxtalashtirish yoki eski7-dars testini susaytirish yo‘q.

Muhit qayta ishga tushganda keng backend va preview web build uzilgan; bu
ikki jarayon muvaffaqiyatli deb e’lon qilinmagan, yakuniy holatda qayta bajariladi.
Keyingi nuqta §30 PDF84; §30–35 PDF84–97 matn/tasvirlari keyingi mualliflik
uchun ko‘rildi. §32 ning yakuniy formula qutisi PDF90 boshiga o‘tgan: eski
map end89 buni qamramaydi; authored citationdan oldin explicit qayd kerak.


## §30–35 — 6 yangi dars/faoliyat

| § | Mavzu | PDF/bosma | Karta | Formula yozuvi | Misol | Topshiriq | FRQ |
|---|---|---|---:|---:|---:|---:|---:|
|30|Massa markazi va muvozanat|84–86|4|0|1|6|0|
|31|Moment va richag|87–89|4|3|1|7|3|
|32|Raqamli richag laboratoriyasi|89–90|3|2|1|5|2|
|33|Oddiy mexanizmlar|90–93|6|4|1|8|4|
|34|Ideal ishlar tengligi|93–95|3|2|1|6|3|
|35|Oltin qoida va FIK|95–97|4|3|1|7|3|

Jami24 karta/14 formula yozuvi/6 original misol/39 topshiriq/15 FRQ.
To‘liq14 sahifa matn/tasviri qayta ko‘rildi; barcha5 partiya bo‘yicha82
asl sahifa PDF/text/render hash auditidan o‘tdi. Har birlik tegishli
paragraf va sahifaga bog‘langan. Mustaqil ekspert tasdig‘i da’vo qilinmaydi.

§32 ning l2/l1=F1/F2 formula qutisi PDF90 boshida, §33 sarlavhasidan oldin
davom etadi. Eski digital source map end89 saqlandi; `SOURCE_CONTINUATIONS`
faqat shu bitta page90 uchun `extent_note` bilan explicit v2 citationga
ruxsat beradi. Boshqa sahifalarga umumiy chekinish yo‘q; bu note olib
tashlansa validator rad etadi. Review JSONda `source_extent_corrections` bor.

Ilmiy qarorlar: geometrik/massa markazi faqat bir jinsli simmetrik misolda mos;
kuchlar yig‘indisi nol bo‘lishi aylanish muvozanati uchun yolg‘iz mezon emas.
Moment yelkasi ta’sir chizig‘iga tik masofa. N*m moment uchun conventional
unit; J bilan bir xil SI bazaviy o‘lchamiga ega bo‘lsa ham shu quantity
topshirig‘ida N*m yozuvi talab qilinadi. Bitta ko‘char blokning ikki vertikal
ip/og‘irliksiz/ishqalanishsiz shartlari aytilgan. Umumiy polispast2n/2^n
qoidasi ulanishdan tashqarida qo‘llanmagan. PDF94 dagi g=9,81/9,8 tafovutli
tayyor yechim ko‘chirilmagan. FIK nisbat0..1, foiz1/100; ideal100% chegarasi
real yo‘qotishlardan ajratiladi. Raqamli lab real bajarilganlik emas.

Physics120 passed24.27s; har15 yangi FRQ uchun mustaqil javob, muqobil
formula/birlik; noto‘g‘ri geometrik h>s va Af>Au rad etiladi. Barcha35 darsni
actual localhost HTTP orqali yakunlash:236 to‘g‘ri javob/68 sonli FRQ/350 XP,
javob+complete replay bir xil; start paytida private rubric/expected qiymat yo‘q.
Flutter142 passed, analyze toza, standalone preview JS web build48.0s o‘tdi.
WASM paketlari uchun oldingi dry-run warning bor; WASM success deyilmaydi.
Keng backend/PG va actual Chromium natijasi yakuniy tekshiruv qaydida beriladi.

**Haqiqiy holat35/316;281 bo‘lim qolgan.** 6-sinfda30 nazariya+4 lab+1 uy
amaliyoti authored; qolgan23 nazariya+3 lab. Boshqa sinflar manba xaritasi
saqlangan, interaktiv darslari hali0. 7-sinf yo‘q kirish sahifalari blok emas.
Keyingi aniq nuqta: **6-sinf §36, PDF/bosma102, «Issiqlikni hosil qiluvchi
manbalar. Issiqlik qabul qilish»**. Uning to‘liq sahifalarini qayta ko‘rishdan
davom etiladi; hali authored/publish-ready deb belgilanmaydi. Oraliq tasdiq
so‘ralmaydi; production/nashr uchun alohida ruxsat zarur.


## Yakuniy tekshiruv qaydi — 2026-10-22

- To‘liq backend: **702 passed/4 opt-in skipped/13 oldingi warning**,283.83s.
- Alohida actual PostgreSQL16 staging: **4 passed**,318.26s;35 Physics dars,
  eski7 migration/concurrency, OAuth hamda Biology406+47 checkpoint.
- Flutter: **143 passed**, analyze toza. Physics3D tugmalariga alohida
  semantik boundary/label/tap qo‘shildi: uzun matn bilan aralashmaydi.
  Widget regression bu label va tapni tasdiqlaydi. Boshqa global UI o‘zgarmagan.
- CDN’siz JS preview34.9s; actual Chromium §35 to‘rtta konseptual va
  eta=Af/Au /80 /% javobini server bilan tekshirdi;390x844/640x320
  rasmlari ko‘rildi, JS error yo‘q. CanvasKit CDN domeni bloklanganida
  `--no-web-resources-cdn` bilan lokal SDK resursi ishlatiladi.
- Actual HTTP35 lesson/236 answer/68 numeric/350 XP; retry bir xil.
- Original82 sahifa hash audit, Biology355+51/2527/2609 va oldingi7 dars
  bytes/progress saqlangan; veb-sayt054f0ce toza.

To‘liq316 bo‘lim va mustaqil ekspert/real telefon tekshiruvi hali yakunlanmagan.
Keyingi bo‘lim §36/PDF102; qolgan281 bo‘limning hech biri tayyor deb sanalmadi.


Yakuniy normal `main.dart` release JS web build ham o‘tdi (49.3s,
`--no-web-resources-cdn --no-wasm-dry-run`). Current build/web/main.dart.js
private sandbox JWT’ni o‘z ichiga olmaydi. Bu production deploy yoki WASM/native
Android build emas. Temporary QA server/konteynerlari tekshiruvdan keyin to‘xtatiladi.


## Davom — §36–42, 2026-10-22

GitHub branch HEADlari qayta tekshirildi: backend861bdd8 / Flutter4002bca;
mavjud35 dars qayta yozilmadi. Yangi7 dars:29 karta,7 original misol,42
topshiriq (39 konseptual+3 tartiblash). Sun’iy formula/FRQ qo‘shilmadi.
Manbalar: §36 PDF102–104; §37 104–106; §38 106–108; §39 108–110;
§40 110–112; §41 112–114; §42 114. Barchasida PDF=bosma.
13 sahifaning to‘liq matni va asl tasviri qayta ko‘rildi; jami95 asl sahifa
PDF/text/render hash auditidan o‘tdi. `grade6_batch6.json`/`_review.json`.

Muhim aniqliklar: issiqlik modda emas; ish ichki energiyani o‘zgartirishi
mumkin, erishda temperatura har doim ortmaydi. Suvning4°C istisnosi,
modda oqimli konveksiya, vakuumdan o‘tadigan nurlanish va termosning
yaltiroq sirti alohida o‘rgatiladi. Ibn Sinoning tarixiy havo taxmini
zamonaviy muz suzishi sababi sifatida berilmaydi. Selsiy tayanchida
toza suv/normal bosim sharti bor. §42 faqat raqamli qayd va reja;
real tajriba bajarilganlik yoki aralashma uchun sun’iy o‘rtacha formula yo‘q.

Amaldagi testlar: Physics **89 passed (21.49s)**, yangi semantik javob
kalitlari va barcha chalg‘ituvchi variantlar/tartiblar tekshirildi. To‘liq42
darsning HTTP/javob/replay/complete oqimi **420 XP** bilan o‘tdi. Flutter
Physics **17 passed**; backend boshlang‘ich cheklangan socket muhiti va
Flutter socket testi bloklangach, ruxsatli muhitda qayta bajarildi.
Biology curriculum/completion regressionlari **22 passed (3.39s)**.
Keng backend/haqiqiyPG/native Android natijasi bu partiya uchun yangidan
da’vo qilinmaydi. GitHub tekshiruvi dastlab approval-review usage limitiga
uchradi, keyingi urinishda ishladi; xavfsizlik cheklovi chetlab o‘tilmadi.

**42/316;274 qolgan. Keyingi nuqta: 6-sinf §43, PDF/bosma118.**
Keyingi elektr manba sahifalari118–128 matn/tasvirlari o‘qildi; mualliflik
keyingi partiyada. Boshqa sinflar0 authored; oraliq tasdiq kutilmaydi.


## Davom — §43–46: elektrga kirish

Yangi4 dars:18 karta/1 birlik formulasi/4 misol/24 topshiriq(2 FRQ).
Manba PDF=bosma: §43 118–121, §44 121–124, §45 124–126, §46 127–128.
11 asl sahifa matn/tasvirlari qayta tekshirildi; jami106 sahifa hash audit.
`grade6_batch7.json`/`_review.json`; eski42 dars o‘zgarmadi.

Elektrostatika belgisi va neytral metallning zaryad qayta taqsimlanishi
farqlandi: tortilish oldindan qarama-qarshi net zaryad borligini isbotlamaydi.
Erkin elektronlar metallga xos misol; barcha muhitdagi yagona tashuvchi
deb berilmagan. Voltmetr parallel, ampermetr ketma-ket: chizmalar tekshirildi.
Faqat manbadagi1V=1000mV birlik almashtirish qoidasi qo‘shildi; Ohm qonuni
yoki qarshilik formulasi majburlanmadi. V/mV/kV server exact SI registry;
case-sensitive va noto‘g‘ri fizik kattalik rad etiladi. Uy tarmog‘ida tajriba,
«36V dan pasti doim xavfsiz» yoki universal tejash foizi yo‘q.

Physics+Biology tanlangan regressionlari **116 passed(27.02s)**; barcha46
dars HTTP/replay/complete bilan460XP.2 mustaqil sonli oracle va22 konseptual/
tartib topshirig‘i semantik javoblar bilan tekshirildi. Flutter Physics
**17 passed**, haqiqiy yangi public payloadlardan mV chipi320px/200% da sinaldi.
Public fixturega private grading/expected qiymatlar kiritilmadi.

**46/316;270 qolgan. Keyingi nuqta §47, PDF/bosma132.**
§47–56 sahifalari132–151 matn/tasvir bilan ko‘rildi; darslari navbatda.
PG/full backend/build/native Android natijasi yangi partiya uchun hali
qayta tasdiqlanmagan; Fizika faqat lokal/test preview, AI Explain yo‘q.


## 2026-10-25 — Optika §47–56 saqlanmagan ishlarini yakunlash

Worktree va GitHub HEAD07f748b qayta tekshirildi; hech qanday reset/overwrite
yo‘q. Oldingi46 dars saqlandi.10 yangi dars:42 karta/7 formula yozuvi/10 misol/
63 topshiriq(9 FRQ). Manba PDF=bosma:§47 132–134;48 134–135;49 135–137;
50 138–140;51 140–142;52 142–145;53 146–147;54 147–149;55 149–150;56 150–151.
20 asl sahifa matn/tasviri tekshirildi; review JSONda hash/ilmiy qarorlar bor.
Yangi5 executable oila: flat image, spherical focus, real concave image, lens
power/focal distance. d>F>0 paraksial ko‘zgu va havodagi musbat yig‘uvchi linza
doiralari aniq; virtual/singular branchni musbat formula bilan baholamaymiz.
km/s,dptr,1/m exact birliklari;9 mustaqil sonli oracle.

Kitob tafovutlari:PDF145 mashq2 d250cm/F245cm natijasi12250cm, berilgan124cm
kalit emas; parallel2ko‘zgu uchun universal2tasvir kaliti ham ko‘chirilmagan.
PDF141 kamalak yoyini Yer sferikligi bilan izohlash ilmiy qoida sifatida
berilmaydi; tomchi/sinish/qaytish ishlatiladi. PDF137 tanga/qora ko‘zoynak
bilan Quyoshga qarash topshirig‘i kiritilmadi. Sferik qonunlar paraksial;
7 rang nomi shartli, spektr uzluksiz. Raqamli2lab real tajriba emas.

Optika11 yangi source-semantic/domain testi o‘tdi; tanlangan Physics/Biology
suite **127 passed(26.76s)**; barcha56 dars HTTP/replay/560XP. Flutter Physics
**17 passed**; dptr/km public birliklar320px/200% da tekshirildi. Jami126 asl
sahifa hash auditidan o‘tdi. Flutter branch commitbefb294. **56/316;260 qolgan.**
Keyingi **§57,PDF/bosma156**. Native Android/mustaqil ekspert tasdig‘i yo‘q.
