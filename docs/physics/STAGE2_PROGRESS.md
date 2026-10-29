# Fizika 2-bosqich — davom etayotgan haqiqiy kontent

2026-10-25 (Asia/Tashkent). Foydalanuvchi barcha **316 bo‘limni** ketma-ket
yaratishga ruxsat berdi; partiyalar orasida yangi tasdiq talab qilinmaydi.
Bu ruxsat production deploy yoki ommaviy nashr uchun ruxsat emas.

## Tekshirilgan partiyalar

Boshlang‘ich backend `986efa7`, Flutter `9f152f0`; GitHub HEADlar qayta tekshirildi.
§1–7 JSON va review fayllari qayta yaratilmagan. `physics_sources.json`, formula
review va source-map audit — saqlangan 1-bosqich arxivi; undagi «0 dars» tarixiy.
Joriy mualliflik sanoqlari `python -m scripts.audit_physics_course` orqali olinadi.

| Sinf | Jami bo‘lim | Yozilgan lokal dars/faoliyat | Qolgan | Karta | Formula yozuvi | Misol | Topshiriq | FRQ | Lab / uy amaliyoti |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 6 | 61 | 61 | 0 | 254 | 74 | 67 | 394 | 88 | 7 / 1 |
| 7 | 46 | 15 | 31 | 63 | 25 | 15 | 98 | 39 | 1 / 0 |
| 8 | 60 | 0 | 60 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 9 | 59 | 0 | 59 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 10 | 45 | 0 | 45 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| 11 | 45 | 0 | 45 | 0 | 0 | 0 | 0 | 0 | 0 / 0 |
| Jami | 316 | 76 | 240 | 317 | 99 | 82 | 492 | 127 | 8 / 1 |

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


## 2026-10-25 — §57–61: 6-sinf muallifligi61/61

Yangi5 dars:20 karta/6 formula yozuvi/5 misol/29 topshiriq(9 FRQ).
Manba PDF=bosma:§57 156–158;58 159–161;59 161–163;60 163–165;61 165–167.
12 asl sahifa to‘liq matn/tasvir bilan tekshirildi; barcha9partiya bo‘yicha
**138 original sahifa** PDF/text/render hash auditidan o‘tdi.
`grade6_batch9.json`/`_review.json`; oldingi56 dars qayta yozilmadi.
Yangi3 executable oila: chastota n/t, borish-qaytishdan h=v*t/2,
tovush yutilishi Ea/Ei; jami65 oila. Hz/kHz birliklari serverda.
Chastotada musbat butun tebranish soni va musbat vaqt, yutilishda
0≤Ea≤Ei/Ei>0 talab qilinadi. Chaqmoqdagi bir tomon vaqti aks sado
bilan almashtirilmaydi.9 sonli javob mustaqil oracleda tekshirildi.

Ilmiy qarorlar: PDF157 ovozning asosiy manbaini til deb atash olinmagan;
7–9Hz halokat haqidagi tasdiqlanmagan hikoya/individual eshitish testi yo‘q.
Tovush tezligi faqat zichlik funksiyasi emas;99,9% suv/havo qaytish raqami
umumiy universal qoida emas. Jadvaldagi gaz0°C/suyuqlik20°C sarlavhasi
matndagi umumiy0°C jumlasidan ajratildi. Qattiqlik, ton balandligi va
tembr farqlandi; og‘riq chegarasi/vokal diapazon universal son sifatida
berilmadi. Yutilish jadvali500Hz va material sharoitiga tegishli.
Tuxumsimon ship har joyga teng yo‘l beradi degan universal da’vo yo‘q.

Amaldagi tekshiruvlar:
- Yangi sound+course **27 passed18.22s** (avvalgi bitta outdated
  grade_content_complete=false kutish61dars tugashi sabab yangilandi).
- Actual localhost HTTP **61dars/394javob/88FRQ/610XP**; javob/complete
  replay bir xil, startda private rubric/expected qiymat yo‘q.
- Flutter **143 passed**, analyze0issue, normal releaseJS web build51.5s.
  Hz/kHz yangi public fixture, Hz chip320px/200% testda.
- To‘liq backend va haqiqiy PG rehearsal shu checkpoint paytida davom
  etmoqda; yakuniy log natijasi keyingi qaydda. Native Android/ekspert yo‘q.

**Haqiqiy umumiy holat61/316;255 qolgan.**6-sinf53nazariya+7raqamli lab+
1uy amaliyoti;254karta/74formula yozuvi/67misol/394topshiriq(287konseptual,
19tartiblash,88FRQ). Boshqa sinflar hali0 authored. Biologiya406+47
checkpoint/source kontenti o‘zgarmadi. Veb054f0ce toza. Flutterac9b3e0.

**Aniq davom nuqtasi:7-sinf §1 «Jismlarning harakati»,PDF1–4/bosma8–11.**
Manba `/workspace/attachments/e0ae04db-aceb-4d4e-8e34-944009b3c9e0/fizika_7_uzb.pdf`,
SHAbdd4fbfc0fdc48957e36663219777d9ce64efe2939190ccc1b34fee4881f8367.
Yetishmayotgan kirish bosma1–7 foydalanuvchi qaroriga ko‘ra blok emas.
§1dan oldin asl matn/tasvirni qayta ko‘rish, grade7 authoring helper va
review yaratish kerak. Hozir Flutter preview sarlavha/bibliografiya va
repository catalog chaqiruvi6-sinfga bog‘langan;7-sinf darsi qo‘shilganda
grade tanlash va to‘g‘ri bibliografiya bilan testlang. Sonli oracles hozir
(sequence,qN) bilan kalitlanadi:7-sinf qo‘shilishidan OLDIN grade kalitini
qo‘shing, aks holda sinflar savol kalitlari to‘qnashadi. Runtime catalog
grade6..11 parametri mavjud. Production/AIExplain/yashirin fanlar yoqilmasin.
Oldingi partiyalarni qayta yaratish yoki ommaviy PDF commit qilish kerak emas.


## Saqlangan checkpoint va keng tekshiruv — 2026-10-25

Backend **047c639**, Flutter **ac9b3e0** GitHub feature HEADlari; optics
backend6305313/Flutterbefb294. Branchlar oldingidek; main/productionga tegilmadi.
Haqiqiy PostgreSQL16: **4 passed292.04s** — eski7 migratsiya/concurrency,
barcha61 import/reimport/610XP, legacy137XP/3streak/2stars hamda
OAuth/Biology406+47checkpoint tekshirildi. HTTP61/394/88FRQ/610XP o‘tdi.

Birinchi keng backend run **731passed/1failed/4skipped/13warning268.50s**:
faqat yangi61dars sabab grade_content_complete=true bo‘lganini eskicha
false kutgan test yiqildi. Bu test tuzatilib sound/course27passed bilan
qayta tasdiqlandi. To‘liq run ham tuzatishdan keyin yana ishga tushirildi;
uning natijasi alohida final tekshiruv qaydida, tugashidan oldin success
deyilmaydi. Keng Flutter143passed, analyze0issue, webbuild51.5s.

Oldingi35 kontent/review fayli, source-map va Biology kontent diffi bo‘sh.
`--dry-run --all-reviewed`61lessonni validatsiya qildi.7-sinf§1–2
PDF1–7/bosma8–14 to‘liq matn/tasviri ko‘rildi, lekin darslar hali
yozilmadi; **61/316** sanoq o‘zgarmadi. Yangi `GRADE7_NEXT_REVIEW.md`
PDF5/bosma12dagi4300yil vs4,32millionyil arifmetik tafovuti, cheksiz fazo
da’vosi va tarixiy sekund ta’rifi kabi muammolarni aniq saqlaydi.

Keyingi sessiya avval GitHub/worktree va shu hujjatning eng oxirgi
qaydini tekshirsin; backend test logi private
`/workspace/.setup/physics-stage2/backend-grade6-retest.log`, PG
`postgres-grade6-final.log`, audit `audit-grade6-final.json`. Eski sessiya
logini yangi test natijasi deb sanamang. PrivatePDF, QAJWT yoki
DB credential commit qilinmasin.7-sinf§1 muallifligidan davom etilsin;
§1–61 qayta yaratilmasin. Flutter gradepicker/bibliografiya va grade-aware
numeric oracle keylari birinchi7-sinf importidan oldin zarur.


## Yakunlangan6-sinf QA qayta yurishi — 2026-10-25

Tuzatilgan testdan keyin to‘liq backend qayta bajarildi: **732passed,
4opt-in skipped,13existing warning,249.54s**. Alohida actualPG16run
**4passed292.04s**; skipped testlar PG muvaffaqiyatiga o‘rniga taxmin
sifatida ishlatilmagan. Flutter143passed/analyze0issue/web51.5s va
HTTP61/394/88FRQ/610XP/replay natijalari saqlangan.
`GRADE6_VALIDATION.json` ushbu haqiqiy natijalar va barcha6sinf holatini
mashina o‘qiydigan shaklda beradi. Testlangan application commit047c639,
Flutterac9b3e0; keyingi commitlar shu qayd/evidence fayllari.
`GRADE7_SOURCE_PREFLIGHT.json`7asl sahifa text/render hashini saqlaydi,
lekin grade7authored0 ekanini aniq ko‘rsatadi.

QA test serveri va faqat shu ish uchun yaratilgan PostgreSQL konteyneri
to‘xtatildi; production/server/foydalanuvchiDBga tegilmadi. Sessiya
checkpointi: **61/316;255qolgan;7-sinf§1PDF1/bosma8**. 316/316
tugallandi deyilmasin. Keyingi davomda §1–61 noldan yozilmasin.


## 7-sinf oldidan sinflararo poydevor — 2026-10-25

Backend/FlutterHEADa40362a/ac9b3e0 va toza worktree tekshirildi.
Catalogda additive `book` bibliografiya allowlisti(id/grade/title/authors/
publisher/year) bor; OCR/privatepath/rubric chiqarilmaydi. Grade6 default
API saqlandi. Flutter repositorygrade6..11 queryparametrini yuboradi,
mos kelmaydigan grade/bookni rad etadi. Preview sinf tanlashni serverdagi
available_grades asosida ko‘rsatadi; hardcoded6-sinf bibliografiyasi olib
tashlandi. Sinf almashishda cancellation/generation guard, eski lesson
key asosidagi account/origin draft izolyatsiyasi saqlanadi.

Sonli test kaliti endi(grade,section,question). Boshqa sinfda bir xil
paragraf/raqam borligi grade6javobiga fallback qilmaydi. Test qasddan
grade7 uchun kalit yo‘qligini va mustaqil kalit ajratilishini sinaydi.
Bu bosqich **hali61/316**: grade7dars import qilinmadi. ManbaPDF1–21
matn/tasvirlari keyingi§1–5 muallifligi uchun qayta ko‘rildi.
BackendoldPhysics81passed25.12s, multigrade8passed1.22s. Flutter
analyze0issue; Physics18passed, gradepicker320px/200% regression o‘tdi.


## 7-sinf§1–5 — birinchi manbali partiya,2026-10-25

5dars/23karta/6formula yozuvi/5misol/32topshiriq(22konseptual,1tartib,9FRQ).
Manba PDF/bosma:§1 1–4/8–11;§2 4–7/11–14;§3 7–11/14–18;
§4 11–18/18–25;§5 19–21/26–28.21asl sahifa matn/tasviri qayta ko‘rildi;
jami159sahifa originalPDF/text/render hash auditidan o‘tdi.
`grade7_batch1.json`/`_review.json`.6-sinf9partiya/61dars baytlari saqlandi.

5yangi qoida:klassik bir yo‘nalishli tezliklar, kollinear bir/qarama-qarshi
ko‘chish modullari, musbat skalyar ko‘paytirish, teng vaqt oraliqlarida
takroriy yo‘l. Jami70executable oila. Qarama-qarshi branch a≥b; musbat k
sharti va butun oraliqlar soni tekshiriladi. Vector triangle/subtraction,
projection, reference frames, material point, path/displacement, coordinate
dimensions va uniform/straight farqi o‘rgatildi. Musbat k<1 modulni
kamaytiradi; to‘g‘ri chiziqda orqaga qaytishda yo‘l≠ko‘chish moduli.
§4ichidagi17–18PDF qo‘shimcha mashqlar ham manba sifatida ko‘rildi;
bosma24dagi Yer sharqdan g‘arbga aylanadi jumlasi ko‘chirilmagan.
Tarixiy metre/sekund ta’riflari joriy SI sifatida berilmaydi.

Amaldagi testlar:Physics/source/identity/Biology **117passed34.07s**;
serverHTTP66dars/replay660XP o‘tdi. Grade-default6API va grade7ning
prerequisite mustaqilligi tekshirildi. Alohida actual PostgreSQL16
**1passed14.76s**:barcha66lesson import/reimport,660XP, legacy137XP/3streak/
2stars saqlandi. Bu PGtest boshqa406kontent regressionini yangidan
uydirib tasdiqlamaydi; ular tanlangan Biologytestlarda tekshirildi.
FlutterPhysics **19passed**, yangi9publicFRQ320px/200% draft testi
o‘tdi; analyze0issue. FullFlutter **145passed**; normalJSreleasebuild natijasi keyingi qaydda.

**Haqiqiy holat66/316;250qolgan.7-sinf5/46,41qolgan.**
Keyingi **7-sinf§6«To‘g‘ri chiziqli tekis harakat tezligi»,PDF21/bosma28**.
§6–10PDF21–37 matnlari o‘qildi, rasmlari hali mualliflikdan oldin tekshirilsin.
Oraliq tasdiq so‘ralmaydi. Kimyo/Biology/veb/prod/PDFtarqatish/AIExplain yo‘q.


## 7-sinf§6–10 —2026-10-25

Yana5dars/20karta/8formula yozuvi/5misol/35topshiriq(20MCQ+15FRQ).
Manba PDF/bosma:§6 21–25/28–32;§7 25–27/32–34;§8 27–30/34–37;
§9 30–33/37–40;§10 33–37/40–44.17asl sahifa matn/tasvir bilan
tekshirildi; umumiy175noyob sahifa hash audit(sahifa21 oldingi partiyada
ham bor).`grade7_batch2.json` va `_review.json`.

Doimiy tezlanish, signeda, v=v0+a*t, endpointmean(onlyconstantaccel/no
reversal) qo‘shildi;73executable oila. m/s2 va cm/s2 exact birliklar,
manfiy sonli acceleration javobi qabul qilinadi; eski nonnegative
domenlar globally bo‘shatilmagan. Sonli velocity modeli to‘xtashgacha;
result<0 bo‘lsa source branch rad etiladi. O‘rtacha tezlik jami yo‘l/
jami vaqt; to‘xtash vaqti ham kiradi. Grafik o‘qlari/masshtabi va qisqa
oraliqdagi taqribiy oniy qiymat farqlandi. PDF29dagi6minvs10mingrafik
nomuvofiqligi vaPDF36dagi35/36rasm reference xatosi kalitga ko‘chirilmagan.

Physics/Biology/identity **123passed34.47s**, barcha71dars HTTP/replay
710XP. Alohida haqiqiyPG16 **1passed14.02s**:71lesson/import/reimport,
legacy137XP/3streak/2stars saqlandi. FlutterPhysics **19passed**;
24ta grade7publicFRQ320px/200% da manfiy sonli qoralamani saqladi.
Avvalgi partiya kengFlutter145passed, webrelease47.1s o‘tgan.
§6–10 uchun yangi nativeAndroid yoki mustaqil faneksperti da’vosi yo‘q.

**71/316;245qolgan.7-sinf10/46,36qolgan.**
Keyingi§11«Tekis o‘zgaruvchan harakatda bosib o‘tilgan yo‘l»
**PDF37/bosma44**.§11–15PDF37–52 matn/tasvirlari keyingi mualliflik
uchun qayta ko‘rilsin; hozir37–49matni o‘qildi, bu authoredemas.
6-sinf61dars va 7-sinfoldingi5dars qayta yaratilmaydi.


## 7-sinf§11–15 —2026-10-25

Yana5dars/faoliyat:20karta/11formula yozuvi/5misol/31topshiriq
(15MCQ+1tartiblash+15FRQ). Manba PDF/bosma:§11 37–39/44–46;
§12 40–41/47–48;§13 41–43/48–50;§14 43–45/50–52;§15 49–52/56–59.
13sahifa asl matn/tasviri qayta ko‘rildi; umumiy187originalsahifa hash
audit(37oldingi partiyada ham bor).§12raqamli lab real tajriba emas.
10qoidaoilasi qo‘shildi:jami83. Tezlanishli yo‘l faqat to‘xtashgacha;
lab2s/t² va uch aning o‘rtachasi; erkin tushish/yuqoriga otilishdagi
g explicit source modeli; yuqoriga musbat ishorali v cho‘qqidan keyin
manfiy bo‘lishi mumkin. h otilgan sathga nisbatan balandlik, jami yo‘l
emas. Ideal qaytish-sath/qarshiliksiz shartlar aniq.
Radian yoy/radius, omega phi/t; rad va rad/s birliklari. Kitobdagi
pi=3,14 exact emas, yaqinlashuv. PDF52minutmili30mm/10min berilishi
30mmradius uchun haqiqiy minutmili davriga mos emas:kalitga olinmadi.
PDF38yo‘l vaqtga proporsional deyilishi kvadratikformula bilan
almashtirilib aniqlashtirildi; barcha sourceqarorlari batchreviewda.

Amaldagi backendPhysics/Biology **129passed32.22s**; barcha76dars
HTTP/replay760XP. Sonli15oracle, wrongunit/formula/son, flighttime/g
model/radius/time/stopdomain tekshirildi. ActualPG16 **1passed16.67s**:
76lesson/import/reimport760XP/legacy137XPsaqlandi. FlutterPhysics
**19passed**,39ta publicFRQ320px/200%signeddraftsinovi o‘tdi.
Audit189pagechecks,187noyob(book,page); takroriy citationlar sanoqda
yangi sahifa sifatida yashirilmaydi. Oldingi6-sinf61 va7-sinf10dars
baytlari o‘zgarmadi. **76/316;240qolgan.7-sinf15/46,31qolgan.**
Keyingi **§16«Aylanma harakatni tavsiflaydigan kattaliklar orasidagi
munosabatlar»,PDF52/bosma59**. Oraliq tasdiq kutilmaydi.


## 7-sinf §16–20 — 2026-10-25

5dars,21karta,9formula yozuvi,5originalmisol,32topshiriq(19konseptual,
1tartib,12FRQ). Manba PDF/bosma:§16 52–55/59–62;§17 55–58/62–65;
§18 62–65/69–72;§19 65–68/72–75;§20 69–71/76–78.17asl sahifa
matn/tasviri qayta ko‘rildi; originalaudit206pagechecks,203noyob(book,page).
`grade7_batch4.json` va review. 9yangi qoida, jami92. 1/sfrequency
rad/sdan ajratildi; davr/butun aylanish, v=omegaR, ac=v²/R, kollinear
kuchlar va qismlar massasi. Pi p=3.14 sourceyaqinlashuv,0.005rad/s
aniqlik explicit va chegaralari testlangan. Inersiya darsiga sun’iyFRQyo‘q.
PDF58summarydagi phi=2piR/v birlik xatosi olinmadi; PDF54dagi erta
oraliq yaxlitlash ko‘chirilmagan. Qarama-qarshi aravacha tezlanishlari
vektorlari teng emas, faqat modul. Barcha qarorlar reviewda.

Backend Physics/source/identity/Biology **186passed39.89s**. Dastlab
185passed/1sandbox-resume fail: muhitdagi /tmp/.git belgisi private
sinovkatalogini Git deb blokladi. Xavfsizlik qoidasini bo‘shatmay,
/dev/shm alohida disposable basetempda barcha186test qayta o‘tdi.
ActualPG16 **1passed20.62s**,81lesson/import/reimport810XP, eski137XP/
3streak/2stars saqlandi. FlutterPhysics **19passed**,51publicFRQ
320px/200% signedqoralama; rubrikalar mijozga chiqarilmadi.
Biology kontenti/6-sinf61dars baytlari va website/Kimyo saqlandi.
**81/316;235qolgan.7-sinf20/46,26qolgan.** Keyingi
**§21«Nyutonning ikkinchi qonuni»,PDF71/bosma78**. §21–25ningPDF71–88
matn/tasvirlari yangi mualliflik uchun qayta o‘qildi; hali authoredemas.
Oraliq tasdiq kutilmaydi. NativeAndroid/mustaqil pedagogik tasdiq yo‘q.


## 7-sinf §21–25 — 2026-10-25

Yana5dars/faoliyat(1raqamli prujina lab),22karta,12formula yozuvi,
5originalmisol,35topshiriq(17konseptual,1tartib,17FRQ). PDF/bosma:
§21 71–74/78–81;§22 75–79/82–86;§23 79–81/86–88;
§24 81–86/88–93;§25 86–88/93–95.18asl sahifa matn/tasviri ko‘rildi;
audit224pagechecks/220noyob sahifa. 12yangi executable oila,jami104.
F=m*a dagi F bir jismning natijaviy kuchi; NewtonIII juftligi turli
jismlarda. Markazga kuch yangi interaction turi emas; sharchaga
ichkariga/tashqariga ikki kuchni qo‘yib bekor qilinmaydi. SourcePDF75
vektor ishora xatosi,PDF83muvozanatni NewtonIII deyishi va chiziqlik/
elastiklik chegarasi farqi reviewda ochiq qayd etildi. Prujina F=kx,
k=F/x,x=F/k va kichik aksial sterjen k=ES/l; E birligi dimensional
tekshirildi. N/m,kN/mexact registry. Raqamli lab g=10m/s2, alohida
har k keyin uch k o‘rtachasi; real tajriba bajarildi demaydi.

Backend Physics/source/identity/Biology **192passed47.94s**; barcha86dars
ASGIHTTP/replay860XP, mustaqil17oracle/wrongunit/formula/son/noldomen.
ActualPG16 **1passed26.47s**, import/reimport/860XP va old137XP/3streak/
2stars saqlandi. FlutterPhysics **19passed**,68publicFRQ320px/200%signed
qoralama. Oldingi61grade6/20grade7 JSON o‘zgarmadi, secrets/PDFGitga yo‘q.
**86/316;230qolgan.7-sinf25/46,21qolgan.** Keyingi
**§26«Butun olam tortishish qonuni»,PDF90/bosma97**. PDF90–105aslmatn/
tasvir keyingi§26–30 uchun qayta ko‘rildi, hali authoredemas.
NativeAndroid/mustaqil ekspert/prodrelease tasdiqlanmagan. Keyingi
partiyaga yangi ruxsat kutmasdan o‘tiladi.


## 7-sinf §26–30 — 2026-10-25

Yana5dars,20karta,11formula yozuvi,5originalmisol,31topshiriq
(15MCQ+16FRQ). PDF/bosma:§26 90–93/97–100;§27 93–95/100–102;
§28 95–98/102–105;§29 98–101/105–108;§30 101–105/108–112.
16asl sahifa matn/tasvir:240pagechecks/236noyob audit.11yangi executable
oila, jami115. G ning6.67e-11N*m2/kg2 yaqinlashuvi explicit; oddiy
SIlinear numeric parser va bounded formula whitelist o‘zgarmadi.
G/g, massa/kuch, jismga tortish/tayanchga P ajratildi. kg kalibrli
shkala kuchning kg birligi degani emas; prujina o‘tish jarayoni har doim
monoton deb olinmaydi. P=m(g±a) tezlanish tomoni uchun, pastga branch
0≤a≤g; vaznsizlikdaP0,Fmgsaqlanadi. Gorizontal s=v0t jami trayektoriya
yo‘li emas; h=gt²/2 verticalv0=0. gh=GM/(R+h)²/ideal v²=gr
shartlari aniq. Sqrt parserni yashirin kengaytirmasdan radius branchi
FRQ bilan tekshirildi; source7.9km/s ideal taxmin, release yo‘riqnomaemas.
Barcha ilmiy sourceqarorlar grade7_batch6_review.json da.

BackendPhysics/source/identity/Biology **198passed44.36s**; barcha91dars
ASGIHTTP/replay910XP.16mustaqil oracle, Gunit, tiny scientificnotation,
constants/radius/contactdomain tekshirildi. ActualPG16 **1passed21.86s**:
91lesson/import/reimport910XP/legacy137XP/3streak/2stars saqlandi.
FlutterPhysics **19passed**;84publicFRQ320px/200% qoralama. Eski
Biology406/grade6/grade7old25 JSON o‘zgarmadi, website/Kimyoga tegilmadi.
**91/316;225qolgan.7-sinf30/46,16qolgan.** Keyingi **§31«Yerning sun’iy
yo‘ldoshlari»,PDF105/bosma112**. PDF105–120matni keyingi§31–35 uchun
o‘qildi; rasmlar mualliflikdan avval tekshirilsin. NativeAndroid va
mustaqil pedagogik tasdiq yo‘q. Oraliq tasdiq kutmasdan davom etiladi.


## 7-sinf §31–35 — 2026-10-25

5dars/faoliyat(1raqamli lab),22karta,7formula yozuvi,5misol,31topshiriq
(18MCQ+3tartib+10FRQ). PDF/bosma:§31 105–108/112–115;
§32 108–111/115–118;§33 111–115/118–122;§34 115–116/122–123;
§35 116–120/123–127.16asl sahifa matn/tasvir tekshirildi;
audit256pagechecks/251noyob.7yangi executable oila,jami122.
Tinch ishqalanish f=F muvozanatda Fmaxgacha, f=k*F_applied universal
emas. Yo‘nalish nisbiy sirpanish/tendensiyaga qarshi, yurishda jismni
oldinga tezlatishi mumkin. Dumalash c uzunlik birligida, sirpanish mu
birliksiz. c doimradiusbilanortadi sourcexulosasi olinmadi. Labdagi
printed121(4) noto‘g‘ri dumalash havolasi o‘rniga PDF112/printed119
sirpanish formulasi aniq topic33 identifikatori bilan cited. Buning
uchun source validator istisnosi qo‘shilmadi. Real tajriba da’vosi yo‘q.
Satellite300km/7.7km/s universalminimum emas; shartli idealorbita
originalmisoli, tarix1957→1961→1969. SourceApolloqo‘nish/firststep
sana farqi kalitda aralashmadi. Qualitativeengineering darsida sun’iyFRQyo‘q.

BackendPhysics/source/identity/Biology **204passed48.91s**, barcha96dars
ASGIHTTP/replay960XP.10mustaqiloracle, staticchegaradan oshish, rolling
unit/radius, labmass/g va manba-topic identity tekshirildi. ActualPG16
**1passed26.99s**,96import/reimport960XP/legacy137XP/3streak/2stars.
FlutterPhysics **19passed**,94publicFRQ320px/200%signeddraft.
**96/316;220qolgan.7-sinf35/46,11qolgan.** Keyingi **§36«Impuls»,
PDF123/bosma130**. PDF123–136,140–145 aslmatn/tasvirlari keyingi
§36–40 muallifligi uchun ko‘rildi, hali authoredemas. Eski kontent
baytlari/406Biology/website/Kimyo saqlandi. NativeAndroid/independent
expert/prodclaim yo‘q. Navbatdagi partiyaga tasdiq kutmasdan o‘tiladi.


## 7-sinf §36–40 — 2026-10-25

5dars/faoliyat(1raqamli ish lab),22karta,9formula yozuvi,5misol,
34topshiriq(15MCQ+1tartib+18FRQ). PDF/bosma:§36 123–128/130–135;
§37 128–133/135–140;§38 133–136/140–143;§39 140–143/147–150;
§40 144–145/151–152.20asl sahifa matn/tasvir:276pagechecks/271noyob.
8yangi executable oila,jami130. F*t, m*v, m(v−v0), jami p va yopishish
umumiy v, ikki-qism recoil, Fprojection*s, ko‘tarish F*h. Signed
proyeksiyalar faqat aniq yangi qoidalarda; musbat massa/vaqt/yo‘l talab
bo‘shatilmadi. N*s va kg*m/s teng dimension, MJsourcebirligi qo‘shildi.
Tashqi netimpuls0, bitta o‘q/sistema, yopishish branchi va initialrest
recoil shartlari aniq; uzluksiz raketa tenglamasi deb berilmaydi. Gazning
raketaga nisbatan tezligi bilan inertialu aralashtirilmadi. Ish musbat,
manfiy yoki0bo‘lishi mumkin, tanlangan kuch alohida. Barcha ilmiy
qarorlar batchreviewda; xavfli ip/bolg‘a/berkprobirka topshirig‘i yo‘q.

BackendPhysics/source/identity/Biology **210passed50.48s**, barcha101dars
ASGIHTTP/replay1010XP.18mustaqiloracle va noto‘g‘ri ishora/birlik/formula,
zero/yopishish, mass/time/distancedomainlar. ActualPG16 **1passed27.02s**:
101import/reimport1010XP/legacy137XP/3streak/2stars. FlutterPhysics
**19passed**,112publicFRQ320px/200%signeddraft. Oldingi6-sinf61/7-sinf35
baytlari va Biology406 saqlandi; website/Kimyo/production/AIExplainyo‘q.
**101/316;215qolgan.7-sinf40/46,6qolgan.** Keyingi **§41«Potensial
energiya»,PDF145/bosma152**. §41–46PDF145–161aslmatn/tasvirlari
mualliflik uchun qayta ko‘rildi; hali authoredemas. NativeAndroid va
mustaqil ekspert tekshiruvi hali bajarilmagan. Tasdiq kutmasdan davom.


## 7-sinf §41–46 va sinf yakuniy QA — 2026-10-25

6yangi dars/faoliyat(1raqamli lab),26karta,17formula yozuvi,7misol,
43topshiriq(20MCQ+2tartib+21FRQ). PDF/bosma:§41 145–148/152–155;
§42 148–150/155–157;§43 150–155/157–162;§44 155–156/162–163;
§45 156–158/163–165;§46 159–161/166–168.17asl sahifa matn/tasvir;
audit293pagechecks/287noyob.9yangi executable oila,jami139. Gmgh va
gravitatsiya ishi−deltaEp,deltaEk netish, konservativ mechanicalbalance,
chiziqli kx²/2, N=Fv/Nv inverse va craneFIK. Kichik mW/kW/MW,
W*s=J registri. SourcePDF147ishora/prose,PDF153yopiqsistemadaharqanday
mexaniksaqlanish,PDF157gWprefix vaPDF160kran24/27mtafovutlari reviewda.
Raqamli rollinglab ilgarilanma mv²/2 ni barchaaylanish/urilish energiyasi
deb olmaydi. Qarshilikda mexanik qism kamayishi umumiyenergiya yo‘qolishiemas.

### Shu sinf uchun haqiqiy tekshiruvlar

- **To‘liq backend795passed/4opt-in skipped/13oldwarnings302.11s.** Dastlab
 794passed/1coverageassertfail304.58s: formatterdan so‘ng tuple101/215
 qolgan, haqiqiy content107/209 edi. Expectation tuzatildi, focusedtest
 o‘tdi va butun suite qayta795pass bo‘ldi; hech qanday runtimefail yashirilmadi.
- **ActualPG16 2passed39.55s:** alohida schemas, additivefirstbatchmigration,
 all107import/reimport,1070XP,replay va concurrentfirstpass XP1marta,
 eski137XP/3streak/2stars saqlandi. Boshqa2stagingtest bu sinfdaopt-in
 sifatida alohida qayta bajarilmadi; ular fullsuiteda skipped. ProductionDByo‘q.
- **ActualTCPHTTP107lesson(6:61,7:46)/698javob/221mustaqilsonlioracle/
 1070XP.** Bir javob/complete replay teng; maxfiyrubrika clientgachiqmadi.
 Server127.0.0.1:8889, disposableprivatedb, sinovdan so‘ng to‘xtatildi.
- **Flutter145passed**, analyze0issue2.2s; JSreleasewebbuild3.1s.133ta
 grade7publicFRQ320px/200% da signedqoralama. AndroidSDK/realAndroid
 test va mustaqil pedagogik ekspertiza bajarilmadi; WASM successda’vosi yo‘q.
- Source-map/batchhashaudit yuqoridagi287sahifa, grade6frozen61 va
 oldgrade7batchesbaytlari, Biology406/47checkpoint/2527karta/2609savol
 kontenti o‘zgarmadi. Website/Kimyo/production/AIExplainyo‘q.

**6-sinf61/61;7-sinf46/46. Umumiy107/316;209qolgan.**
7-sinf196karta/90formula yozuvi/47misol/304topshiriq/133FRQ/5raqamli lab.
Jami450karta/164formula yozuvi/114misol/698topshiriq/221FRQ.
8-sinf0/60,9-sinf0/59,10-sinf0/45,11-sinf0/45. 7-sinfmissingbosma1–7
foydalanuvchi qabul qilgan doiraga ko‘ra nonblocking, ularning mazmuni
o‘ylab topilmadi. NativeAndroid/independentexpert/generalpublicationyo‘q.

**Keyingi aniq nuqta:8-sinf§1«Jismlarning zaryadlanishi»,PDF/bosma4.**
Avval sourceidentityadapter:8/9books orderedPDFsegments, source_set_sha256
butunPDFhashi emas; nativeemptytext va cachedOCRdigest alohida. Mavjud
source maps/PDFqismlar/fingerprints saqlansin. Original8PDF4–22 rasmlari,
noaniq11/14/15/20sahifa to‘liq kattalashtirib ko‘rildi; barcha19OCR/nativeraster
hashlari tekshirildi. Bu darslari authored degani emas. Yangi ruxsat
kutmasdan8-sinf1–5partiya bilan davom etish. `GRADE7_VALIDATION.json`
saqlangan QAcheckpoint, Gitlog oxirgi featurecommitlarni ko‘rsatadi.


## 8/9-sinf segmentli manbalarga texnik tayyorgarlik — 2026-10-25

6/7 manbalari bitta PDF/native-text,8/9 esa orderedPDFsegments+OCR.
Oldv2validatorda book[sha256] talabi8/9da mavjud bo‘lmagan butunfaylhashini
kutgan edi. Endi legacysha va source_set_sha256 alohida qat’iy identity,
manifest uzluksizligi/tartibi/soni, har originalpage uchunsegmentfile,
localpage va partSHA tekshiriladi. Manifest hechqachon butunPDFdigestideb
yozilmaydi. Reviewda native layer hash/OCRhash/rastrdalillari alohida.
`services/physics_source_documents.py`, `scripts/audit_physics_source_pages.py`
va mavjud validator/auditCLIyangilandi. PDF/OCR/credentialsGityo‘q;
6/7darsJSONlari va Biology406baytlari o‘zgarmadi. No publication.

230tanlanganbackend/source/API/grading/Biologytest **52.75s** o‘tdi,
13yangi segmenttest ichida manifestgap/reorder/wronghash, originalfile
bytes, localbinding, native/OCR/render tamperlar bor. Private293oldpage
checks qayta o‘tdi. Fitztayyorbo‘lmaganQAvenv uchun optional
`requirements-source-review.txt` PyMuPDF1.26.6 pin qo‘shildi; uv bilan
QAvenvga o‘rnatilib barchasi real bajarildi. Pip buvenvdayo‘q; source
renderer prodwebrequirementga majburan qo‘shilmadi. Optionalrenderer
bo‘lmasa5PDFfixturetests skip va8metadata test ishlaydi, bu skiplar
passed deb aytilmaydi. Amaldagi natijada230/230pass, rendererbor.

Manbani tekshirish:
`python -m scripts.audit_physics_course --pdf-dir <private-pdfs> --ocr-dir <private-cache>`
OCRcacheichida`g8-ocr/p004.txt` kabi originalPDFindeks saqlanadi.
**Hali107/316;8-sinf0/60.** Sourceadapter tayyor; keyingi8-sinf§1–5,
PDF/bosma4–22. Noaniq exponent/symbol sahifalari11/14/15/20to‘liq
kattalashtirib tekshirildi, OCRning xatolari bilim manbasi deb olinmaydi.


## 8-sinf §1–5 — 2026-10-25

5 dars/faoliyat, 23 karta, 13 formula yozuvi, 6 original namuna,
36 topshiriq (19 MCQ + 2 tartiblash + 15 FRQ). Manba PDF/bosma:
§1 4–9, §2 9–12, §3 12–15, §4 15–18, §5 18–22. 19 asl sahifa
va cached OCR qayta tekshirildi; jami 312 page checks/306 noyob sahifa.
8-sinf manbasi ikki original PDF segmentidan iborat; segment manifesti
butun PDF hashiga aylantirilmadi. Har citation original va local sahifa,
part SHA, OCR/native text va render dalillari bilan tekshiriladi.

12 yangi executable oila, jami151. Charge C/µC/nC, forceµN va fieldN/C
birliklari; elementar musbat modul e=1.6e-19C, butun zarra soni,
particle mass, vakuum Kulon moduli, signed ikki bir xil shar taqsimoti,
kuch nisbati, E=F/q/kq/r² va dielektrik modeli. §1ga sun’iy FRQ yo‘q.
PDF11dagi elektron yo‘qotgan jism ishorasi xato, PDF9 orbit rasmi va
OCRdagi exponent/epsilon tafovutlari reviewda ochiq. Asl11/14/15/20
sahifalar kattalashtirib tekshirildi. Barcha tushuntirish/masalalar original.

Kvadrat ildiz faqat serverdagi yangi `equal_coulomb_charge` oilasi uchun
opt-in. `sqrt(...)`, `^0.5` va `^(1/2)` yopiq AST sifatida taniladi;
client flag bera olmaydi. Parser uzunlik/depth/bit/power chegaralari,
no-eval/no-CAS va eski qoida defaultlari saqlandi. Numeric ifodada faqat
aniq ratsional ildiz hisoblanadi. Bu partiyaning manbali masalalari shunga
mos; **umumiy irratsional ildizni aniqlik bilan yaxlitlash hali implement
qilingan deyilmaydi**. Ildiz, ishora, kichik birliklar va noto‘g‘ri function
chaqiruvlari alohida testlangan. Qoidalar/javob kalitlari clientga chiqmaydi.

To‘liq backend **815 passed,4 opt-in skipped,13 mavjud warning296.78s**.
Actual lokal PG16 **1 passed26.49s**: barcha112 dars import/reimport,
1120XP, replay, eski137XP/3streak/2stars saqlandi. Flutter **147 passed**,
Physics **21 passed**, analyze toza; grade8 bibliography/API query va
15 yangi FRQ320px/200% qoralama, root notation testlari o‘tdi. Native
Android va yangi actual TCPHTTP112 sinovi bu partiyada bajarilmadi;
oldingi actualHTTP107 natijasi sinf7checkpointida qoladi. Old6/7json va
Biology406 o‘zgarmadi; website/Kimyo/prod/import/AIExplain yo‘q.

**112/316;204 qolgan.**6:61/61,7:46/46,8:5/60,9:0/59,10:0/45,11:0/45.
Jami473karta/177formula yozuvi/120namuna/734topshiriq/236FRQ.
Keyingi **8-sinf§6«O‘tkazgichlarda elektr zaryadlarning taqsimlanishi»,
PDF/bosma22**. §6–10 PDF22–29/32–39 matn/tasvirlari qayta o‘qildi;
25/26dagi noaniq OCR asl tasvirda tekshirildi, keyingi darslar hali0.
Oraliq tasdiq kutilmaydi, §6–10 muallifligi bilan davom etiladi.


## 8-sinf §6–10 — 2026-10-25

5dars/faoliyat,22karta,5formula yozuvi,7originalnamuna,34topshiriq
(23MCQ+5tartib+6FRQ). PDF/bosma:§6 22–25;§7 25–27;§8 27–29;
§9 32–34;§10 34–39.16originalsahifa matn/tasvir;328pagechecks/321noyob.
Qaytadan yaratilgan eski dars yo‘q.5yangi executable oila,jami156.
q=F/E,n=F/(eE),eps=kq/(Er²),ideal muallaq q=mg/E va tayyor
tovush kechikishi s≈340t. nN aniqSIkoeffitsiyenti qo‘shildi.

Metall ichidagi ortiqcha zaryad bilan barcha zarralarni ajratish,
Faradeyqafasining yopiq/elektrostatik/ichkizaryadsiz shartlari,uchli
sirt taqsimoti va elektrshamol raqamli izohi. PDF25eps3.2ni OCR32deb
olinmadi,26dagi exponent tafovuti mustaqil hisob bilan aniqlandi.
Tomchi modelida kuchlar yo‘nalishi va g10 explicit. Chaqmoqmasofasi
faqat tayyorqayd/taxmin, haqiqiy bo‘ronda turish topshirig‘i yo‘q.
Tok tartibli zaryad oqimi; manba boshqa energiyadan zaryad ajratadi.
Kislota reaksiyasi/eskibiografiya/seriespower universalclaim ko‘chirilmagan.
§6,9,10konseptual, sun’iyformula/FRQyo‘q. §10ichidagi inclusivePDF39
aslida§11voltageboshlanishi: fakt/formulalari§10ga yozilmadi.

Physics/source/server/Biology **243passed,2opt-inPGskipped62.02s**.
Alohida actualPG16 **1passed30.71s**:117dars import/reimport1170XP,
replay,eski137XP/3streak/2stars.6mustaqil numericoracle va noto‘g‘ri
unit/formula/son, integercount/dielectric/fieldzero/g/soundmodeldomain
sinovlari. FlutterPhysics **21passed**,21publicgrade8FRQ320px/200%.
Avvalgi fullbackend815/4skipped/Flutter147 natijalari §1–5checkpointida;
bu partiyada qayta to‘liq821deb da’vo qilinmaydi. NativeAndroidyo‘q.
Biology406,old6/7hamda8old5baytlari,website/Kimyo/prod/AIExplain saqlandi.

**117/316;199qolgan.8-sinf10/60,50qolgan;9:59,10:45,11:45qolgan.**
Jami495karta/182formula yozuvi/127namuna/768topshiriq/242FRQ.
Keyingi **8-sinf§11«Elektr kuchlanish va uni o‘lchash»,PDF/bosma39**.
§11–15PDF39–52OCRmatni o‘qildi, originalrasmlar renderqilingan,
mualliflikdan oldin qayta ko‘rilsin. Oraliq tasdiq kutmasdan davom.


## 8-sinf §11–15 — 2026-10-25

5 yangi dars/faoliyat (1 raqamli laboratoriya),21 karta,16 formula yozuvi,
6 original namuna,39 topshiriq (18MCQ+5tartiblash+16FRQ). §11PDF39–42,
§12PDF42–45,§13PDF45–46,§14PDF46–47,§15PDF47–52;bosma raqamlar bir xil.
Barcha14 asl sahifa tasviri qayta o‘qildi,OCR/darajalar/qutblar/jadval
solishtirildi. 342pagechecks/334noyob original sahifa. 15yangi executable
oila,jami171. Amper,mA,µA/μA/uA,Ω/mΩ/kΩ/MΩ,Ω*m/ohm*m,mm² aniq
SI konversiyalari; eski MCQ/FRQ/parser defaultlari saqlandi.

U=A/q,I=q/t,A=UIt,m=It*m0/e,R=rho*l/S va manbali inverselar.
PDF40qutb satri/chizma fizik DC qutblanishiga mos tushuntirildi;PDF45dagi
nostandartnkg o‘rniga kg/g/mg. Nixrom1.1×10^-6Ω*m jadvalning asl
PDF51tasviridan tasdiqlandi. Uzunlik/kesim bog‘lanishida material/harorat
sharti aniq; mm²→m² mustaqil test. Haqiqiy o‘lchovlar uydirilmagan,
labda bo‘sh jadvalni to‘ldirish majburiy emas va real tajriba da’vosi yo‘q.
§15ga kelgusi Omqonuni,§14ga sun’iy FRQ qo‘shilmadi. Review barcha
fakt/karta/formula/misol/topshiriq/yechim manba bindingini qayd etadi.

Yangi ilmiy/domen/unit testlari18passed1.99s. Physics/source/server/Biology
**261passed,2opt-inPGskipped60.95s**. Alohida actualPG16 **1passed30.51s**:
122dars import/reimport/1220XP/replay va eski137XP/3streak/2stars.
FlutterPhysics **21passed**,37publicgrade8FRQ320px/200% qoralama/birliklar;
yangi klient grading yoki answerkey yo‘q. Oldingi full815backend/147Flutter
natijalari alohida; bu partiyada fullsuite deb da’vo qilinmaydi.

**122/316;194qolgan**.6:61/61,7:46/46,8:15/60,9:0/59,10:0/45,11:0/45.
Jami516karta/198formula yozuvi/133namuna/807topshiriq/258FRQ.
Keyingi **8-sinf§16«Rezistorlar.Reostatlar.Potensiometrlar»,PDF/bosma52**.
§16–20PDF52–64OCR/aslrasmlari tekshirildi;darslar hali yozilmagan.
Avtomatik davom, oraliq ruxsat kutilmaydi. Biology406/6–7frozen darslar/
old8§1–10/website/Kimyo/prod/AIExplain o‘zgarmadi. Fizika faqatlocaltest,
Android/independentexpert/prodnashr tasdig‘i yo‘q.


## 8-sinf §16–20 — 2026-10-26 (Asia/Tashkent)

5 yangi dars/faoliyat: rezistor/reostat/potensiometr, Om qonuni, masalalar,
1 raqamli laboratoriya va 1 raqamli amaliy ish. 20 karta,11 formula yozuvi,
6 original namuna,33 topshiriq (17MCQ+5tartib+11FRQ). §16 PDF52–56,
§17 PDF56–60,§18 PDF60–61,§19 PDF61–63,§20 PDF63–64; bosma raqamlar bir xil.
13 asl sahifa qayta o‘qildi:355pagechecks/346noyob. 9 yangi qoida,jami180.
I=U/R,U=IR,R=U/I va sim geometriyasi,zaryad/elektron soni,4 ta R o‘rtachasi.

Ohmik element va doimiy harorat/rho sharti aniq. R=U/I nisbatini universal
R∝U sababiy qonun deb o‘rgatilmaydi. PDF60 qizigan volfram misolining sovuq
jadval rho bilan soddalashtirilgani reviewda ochiq:original mashqlarda rho
sharti berilgan,haqiqiy qizigan spiral natijasi da’vo qilinmaydi. Reostatda
faol uch/surgich tekshiriladi,universal chap/o‘ng yodlash yo‘q. §16ga sun’iy
potensiometr formula,§20ga sonli tajriba uydirmasi qo‘shilmadi. Raqamli lab
misollari «shartli,haqiqiy tajriba emas» deb belgilangan;manba bo‘sh jadvali
real natija sifatida to‘ldirilmagan.

Dastlab yangi testda3 assertion xatosi (unknown_symbol kodi,aslida butun1
elektron bo‘lgan fractional probe,Shartli harf registri) tuzatildi;kontent
javoblari o‘zgartirilmadi. Yangi test17passed1.86s. Keng Physics/Biology
**278passed,2PGopt-in skipped63.04s**. Actual lokal PG16 **1passed28.65s**:
127dars/import/reimport/1270XP/replay/eski137XP/3streak/2stars. FlutterPhysics
**21passed**,48publicgrade8FRQ320px/200%. Oldingi full815backend/147Flutter
natijalari old checkpointda; yangi fullsuite/nativeAndroid da’vosi yo‘q.

**127/316;189qolgan.** 6:61/61,7:46/46,8:20/60,9:0/59,10:0/45,11:0/45.
Jami536karta/209formula yozuvi/139namuna/840topshiriq/269FRQ.
Keyingi **8-sinf§21«Iste’molchilarni ketma-ket ulash»,PDF/bosma64**.
§21–25PDF64–76aslrasm/OCR qayta o‘qildi;darslar yozilmagan. PDF76dagi
«har qanday» murakkab sxema series/parallelga keladi umumlashtirishi yangi
kontentda cheklanadi:faqat shu usul bilan qisqaradigan misollar. Oraliq
ruxsat kutilmaydi. Biology406/6–7/old8/website/Kimyo/prod/AIExplain saqlandi.


## 8-sinf §21–25 — 2026-10-26 (Asia/Tashkent)

Ketma-ket va parallel iste’molchilar, manbalarni ulash raqamli amaliyoti,
raqamli laboratoriya hamda aralash ulanish: 5 bo‘lim, 20 karta, 13 formula
yozuvi, 5 original namuna, 33 topshiriq (15 MCQ + 5 tartiblash + 13 FRQ).
§21 PDF64–67, §22 PDF67–71, §23 PDF71–72, §24 PDF72–75, §25 PDF75–76;
bosma sahifalar teng. Barcha13 asl sahifa tekshirildi:368pagechecks/358noyob.
11 yangi executable oila, jami191. Musbat rezistorlar, aniq ikki tugun va
umumiy/shoxobcha terminali shartlari bilan exact Fraction hisob.

Parallel qarshilik eng kichik shoxobchadan ham kichikligi, umumiy tok va
shoxobcha tok farqi tekshirildi. Lab formulalariga oldingi§21PDF65/§22PDF69
havolalari haqiqiy topic_id bilan qo‘shildi; manba labga noto‘g‘ri atalmadi.
Manbalar va labdagi sonlar faqat ochiq shartli misollar, real o‘lchov da’vosi
yo‘q. PDF66 mains-shoda ulash jumlasi amaliy topshiriqqa ko‘chirilmadi.
PDF76 «har qanday murakkab sxema» da’vosi series-parallelga qisqaradigan
sxemalar bilan cheklangan. Hech qanday yangi ko‘prik-zanjir mavzusi yo‘q.

Yangi semantik/topologiya/oracle/domen testlar15passed1.67s. Keng
Physics/Biology **293passed,2PGopt-in skipped66.02s**. Alohida actualPG16
**1passed32.01s**:132dars/import/reimport/1320XP/replay/legacy137XP3streak2stars.
FlutterPhysics **21passed**,61publicgrade8FRQ320px/200%. Old full815backend/
147Flutter natijalari tarixiy; nativeAndroid va ekspert sinovi da’vo qilinmaydi.

**132/316;184qolgan**.6:61/61,7:46/46,8:25/60,9:0/59,10:0/45,11:0/45.
Jami556karta/222formula yozuvi/144namuna/873topshiriq/282FRQ.
Keyingi **8-sinf§26«Masalalar yechish»,PDF/bosma76**. §26–30ning
PDF76–85/88–90OCR va asl tasvirlari o‘qildi,shu darslar hali yozilmagan.
86–87 raqamlanmagan chapter review,authored bo‘limlar sanog‘iga kiritilmadi.
PDF83 minus/plus tafovuti reviewga yozilsin. Oraliq tasdiq kutilmaydi.
Biology406/6–7/old8/veb/Kimyo/prod/AIExplain saqlandi;faqat lokal/test preview.


## 8-sinf §26–30 va to‘liq regression — 2026-10-26 (Asia/Tashkent)

5 bo‘lim: zanjir masalalari, sig‘im/kondensatorlar, kondensatorlarni ulash,
sig‘im masalalari va tok ishi. 21 karta,17 formula yozuvi,6 original namuna,
37 topshiriq (15MCQ+5tartib+17FRQ). §26PDF76–78,§27PDF78–82,§28PDF82–84,
§29PDF84–85,§30PDF88–90;bosma sahifalar bir xil.13asl sahifa qayta o‘qildi:
381pagechecks/370noyob.13yangi executable oila,jami204. F/µF/μF/uF/nF/pF
vaF/m aniqSI registry,eski MCQ/baholash/parser defaultlari saqlandi.

C=q/U,bitta qoplama zaryad moduli;parallel C yig‘indi,series reciprocal;
yassi model eps*e0*S/d,kvadrat qoplama oralig‘i,eps va aniq mixed topologiya.
e0=8.85e-12F/m va eps≥1 ushbu manba modeli bilan tekshirildi. §26da
parallel juftlik U_AB bilan butun mixedzanjir U si alohida;PDF77rasm
ko‘rildi. PDF83eq5dagi U3 oldidan bosilgan minus izchil yo‘nalish sharti
bilan tushuntirildi;figure84ikki element yig‘indisi tekshirildi. PDF80
«barcha klaviatura» umumlashtirishi cheklangan. PDF89I²Rt/U²t/R asl
segment89local1bilan bog‘langan,88/89orasida sahifaidentitysaqlandi.
Kondensatorning uzun matni ko‘chirilmadi;misollar/givens original.

Yangi semantik/independent oracle/domen/unit testlari **19passed1.83s**.
**To‘liq backend890passed,4PGopt-in skipped,13mavjud warning312.29s**.
Alohida actual lokalPG16 **1passed40.05s**:137dars/import/reimport/1370XP,
replay,eski137XP/3streak/2stars saqlandi. **To‘liq Flutter147passed**,78public
8FRQ320px/200%qoralama sinovlari;**flutter analyze No issues found1.8s**.
Bu partiyada actualTCPHTTP137,webbuild yoki nativeAndroid qayta bajarilmadi;
old actualHTTP107/webbuild natijalari tarixiy. Mustaqil ekspert tasdig‘i yo‘q.

**137/316;179qolgan**.6:61/61,7:46/46,8:30/60,9:0/59,10:0/45,11:0/45.
Jami577karta/239formula yozuvi/150namuna/910topshiriq/299FRQ.
Keyingi **8-sinf§31«Elektr tokining quvvati»,PDF/bosma90**. §31–35PDF90–102
OCR/aslrasm tekshirildi,originalmatn private authoringda tayyor,lekin runtime
JSON/registry/test hali qo‘shilmagan. PDF94erta yaxlitlashdan R489vs484Ω;
PDF96o‘rtacha quvvat formulasidagi minus belgisi reviewga yozilsin.
Oraliq tasdiq kutilmaydi. Biology406/6–7/old8/veb/Kimyo/prod/AIExplain saqlandi.


## 8-sinf §31–35 — 2026-10-26 (Asia/Tashkent)

Quvvat,quvvat masalalari,raqamli quvvat laboratoriyasi,Joul–Lens va FIK,
foydali ish masalalari:5bo‘lim/22karta/17formula yozuvi/5namuna/37topshiriq
(15MCQ+5tartib+17FRQ). §31PDF90–94,§32PDF94–96,§33PDF96–97,
§34PDF97–100,§35PDF100–102,bosma raqamlar teng.13aslrasm qayta o‘qildi;
394pagechecks/382noyob.16yangi executable oila,jami220. Wh,kWh,hWh,MWh,GJ
energiya va hW quvvat koeffitsiyentlari aniq;W energiya belgisi/W vatt
birligi tushuntirilgan. Meter subtraction no-reset va FIK0..1 tekshiriladi.

PDF94R1≈489Ω erta0.45A yaxlitlashidan;aniq220²/100=484Ω,originalmasalalar
oraliq aniqlikni saqlaydi. PDF96o‘rtacha P formulasidagi minus matematik
ravishda plusga tuzatildi;3ta original shartli qiymat bilan mustaqil test.
Q=I²Rt,heat≠temperature,FIK≠energiya yo‘qolishi;no-expansion/no-heat lamp
universalclaim takrorlanmagan. Yangi joule_current oilasigagina opt-in
exactrational sqrt(Q/(Rt));legacyrootdefault yopiq,irratsional rounding
umumiy qo‘llab-quvvatlandi deyilmaydi. Original1rootFRQ,xato/alternativ/
negative/injection/irrational testlari bor. Labsonlari haqiqiy o‘lchov emas.

Yangi test **22passed1.96s**. Keng Physics/Biology **334passed,
2PGopt-in skipped70.70s**. Alohida actualPG16 **1passed32.85s**142dars/
import/reimport/1420XP/replay/legacy137XP3streak2stars. FlutterPhysics
**21passed**,95public8FRQ320px/200%,Coulomb va Joule ildizli inputqoralama.
Old§26–30to‘liq890backend/147Flutter/analyze natijalari alohida saqlanadi;
bu partiyada full912deb da’vo qilinmaydi. NativeAndroid/ekspert yo‘q.

**142/316;174qolgan**.6:61/61,7:46/46,8:35/60,9:0/59,10:0/45,11:0/45.
Jami599karta/256formula yozuvi/155namuna/947topshiriq/316FRQ.
Keyingi **8-sinf§36«Joul–Lens qonunining amaliy tatbiqlari»,PDF/bosma102**.
§36–40PDF102–112/115–117OCR/aslrasm o‘qildi. §39asli112 yuqori qismda
21-mashq davom etadi:archive111end ni o‘zgartirmasdan exactpage continuation
ruxsati/evidence qo‘shilsin. §37–38neutral/switch/42V/live-insulation
jumlalari jiddiy xavfsizlik review talab qiladi;DIY yoki xavfsizlikkafolati
sifatida takrorlanmasin,faqat raqamli konseptual dars. Qaytmas amal/soxta
fakt kerak emas,oraliq tasdiq kutilmaydi. Biology406/6–7/old8/Web/Kimyo/
prod/AIExplain saqlandi;faqat lokal/test preview,umumiy nashr yo‘q.


## 8-sinf §36–40 — 2026-10-26 (Asia/Tashkent)

Isitgich tatbiqlari,xonadon sxemalari,elektr xavfsizligi,masalalar va
metallarda tok:5bo‘lim/20karta/5formula yozuvi/5namuna/32topshiriq
(22MCQ+5tartib+5FRQ). §36PDF102–104,§37PDF104–108,§38PDF108–111,
§39PDF111+112yuqori21-mashq,§40PDF115–117. Bosma raqamlar teng.
14asl sahifa tekshirildi:408pagechecks/395noyob.3yangi qoida,jami223.

Eski map§39PDFend111saqlandi;asl112yuqoridagi21-mashq tugashi chapterreview
sarlavhasidan oldin ko‘rildi. Faqat shu(book,topic,page112) uchun mavjud
SOURCE_CONTINUATIONS mexanizmi bilan extent_note talab qilinadi;qo‘shni
mavzuga sahifani noqonuniy biriktirish yoki note yo‘qligi testda rad etiladi.
Umumiy citation cheklovi bo‘shatilmadi. Q2parallel/seriesratio,bitta sim
bo‘lagining voltage-dropi va uch doimiy yuk hisoblari originalmodel.

**Muhim safety review:** PDF105neutral doim voltagefree,PDF106pastdagi
sim doimneutral,PDF107polarityirrelevant,PDF108neutral/faza switchinterchangeable,
PDF10942Vuniversalthreshold,PDF110livephaseinsulatedstance jumlalari
amaliy ko‘rsatma yoki kafolat sifatida berilmadi. Saqlagichortiqcha tokni
uzadi,barcha shockdan universalhimoya deyilmaydi. Faqat digital sxema,
xavfni tanish/tegmaslik/yordamchaqirish;wire-stripping/socket/indicator probe,
jonli montaj yoki tibbiy reanimatsiya protokoli topshirilmaydi. §37–38review
metadata electrical-safety expertni **generalpublicationdan oldin required**
deb belgilaydi. Bu talab bajarildi deyilmaydi. Ampacity jadvali universal
realdesign talabi sifatida qo‘llanmadi. Metallarda elektron drift va
shartli tok yo‘nalishi,termikharakat alohida;sun’iy FRQ37/38/40yo‘q.

Yangi test **11passed1.34s**. Physics/Biology **345passed,2PGopt-in skipped
75.58s**. Actual lokalPG16 **1passed34.58s**:147dars/import/reimport/1470XP,
replay,legacy137XP/3streak/2stars. FlutterPhysics **21passed**,100public8FRQ
320px/200%. Oldfull890backend/147Flutter/analyze natijalari alohida;yangidan
full923deb da’vo qilinmaydi. NativeAndroid/independentexpert bajarilmagan.

**147/316;169qolgan**.6:61/61,7:46/46,8:40/60,9:0/59,10:0/45,11:0/45.
Jami619karta/261formula yozuvi/160namuna/979topshiriq/321FRQ.
Keyingi **8-sinf§41«Suyuqliklarda elektr toki»,PDF/bosma117**. §41–45ning
PDF117–129OCR/aslrasmlari qayta o‘qildi,darslari hali yozilmagan. NaClaq
sodium deposition/atomic-vs-molar mass/source empiricalk tafovutlari
keyingireviewda ajratilsin;wetchemistry DIY qo‘shilmasin. Oraliq tasdiq
kutilmaydi. Biology406/6–7/old8/veb/Kimyo/prod/AIExplain saqlandi.


## 8-sinf §41–45 va aniq kasrli private rubrika — 2026-10-26 (Asia/Tashkent)

5bo‘lim:elektrolitlar,FaradeyI/II,originalmasalalar,elektroliztatbiqlari.
21karta/11formula yozuvi/7namuna/35topshiriq(19MCQ+5tartib+11FRQ).
§41PDF117–120,§42PDF120–123,§43PDF123–125(+M108manbasi§44PDF127),
§44PDF125–127,§45PDF127–129,bosma raqamlar bir xil.13aslrasm qayta o‘qildi;
421pagechecks/407noyob.11yangi qoida,jami234. kg/C,mg/C,kg/mol,g/mol,
C/mol,mol yopiqregistry;valentlik butun,F≈96500C/mol manbaberilgan.

**Orqaga mos private numeric kengaytma:** takrorlanuvchi ratsionalni
expected_si decimalga avval yaxlitlab noto‘g‘ri truth qilish muammosi bor edi.
Yangi optional expected_rational={numerator,denominator} faqat serverrubrikada;
128belgili butunson stringlari,musbat maxraj,noeval. Eski rubrikalar aynan
expected_si decimal qiymatini ishlatadi. Validator yangi exactratio ni mustaqil
Fractionoraclega solishtiradi;expected_si endi yangi rubrikada o‘quvchi
so‘ralgan qadamda yozadigan canonicaljavob bo‘lishi mumkin. Mavjud
abs_tol_si/rounding_increment_si grid bilan faqat oxirgi qadamda yaxlitlash.
Mijozga ratio/expected/gradingspec chiqmaydi,DTO yoki grade_answer orqali
javobkalitini kiritish rad etiladi. APIv2response/MCQ/publiccontract/DBschema
buzilmadi,migratsiya kerak emas. EskiJSONlar o‘zgarmadi.

FaradeyII da M molyar massa kg/mol,unitless atomicweight emas. PDF123aqNaCl
H2chiqishi bilan keyin Na massasidepositionni aralashtiradi;Naajralishi
ko‘r-ko‘rona o‘rgatilmadi. M108/F96500 nazariyAgk≈1.119mg/C bilan jadvalning
empirik1.118mg/C qiymati alohida berilgan. Lampoff≠exactzero,ikkita qoplangan
yuza uchun2koeffitsiyent,sourceCr90µm yaqinlashuvi reviewda. Faqat tanlangan
reaksiya100%current-efficiency nazariy modeli;wetchemistry DIY va haqiqiy
qaydlar yo‘q. Electrochemistryexpert generalpublication oldidan required.

Yangi grading/content testlari **29passed1.76s**. **To‘liqbackend952passed,
4PGopt-in skipped,13mavjud warning321.04s**. Actual lokalPG16 **1passed35.32s**:
152dars/import/reimport/1520XP/replay va legacy137XP3streak2stars. **To‘liq
Flutter147passed**,111public8FRQ320px/200%;analyze **No issues found1.6s**.
NativeAndroid/actualTCPHTTP152/webbuild qayta bajarilmadi,mustaqilekspert yo‘q.

**152/316;164qolgan**.6:61/61,7:46/46,8:45/60,9:0/59,10:0/45,11:0/45.
Jami640karta/272formula yozuvi/167namuna/1014topshiriq/332FRQ.
Keyingi **8-sinf§46«Vakuumda elektr toki»,PDF/bosma129**. §46–50PDF129–136/
139–145OCR/aslrasm o‘qildi,originalmatnprivateqoralamada,JSONhaliyo‘q.
Xaritada§49doimiy magnit,§50Bparametrlar;yarimo‘tkazgich darsi kiritilmaydi.
PDF132maydon≠ionizator,PDF140o‘rtadafieldzero universalclaim cheklansin.
Oraliq tasdiq kutilmaydi. Biology406/6–7/old8/Web/Kimyo/prod/AIExplain saqlandi.


## 8-sinf §46–50 — 2026-10-26 (Asia/Tashkent)

5dars: vakuumdagi tok, gazlardagi tok, nomustaqil/mustaqil razryad,
doimiy magnit, magnit induksiya va chiziqlar. 21karta/3formula yozuvi/
5namuna/31topshiriq (23MCQ+5tartib+3FRQ). §46PDF129–131,§47PDF131–133,
§48PDF133–136,§49PDF139–143,§50PDF143–145; bosma teng.
15asl sahifa qayta ko‘rildi:436pagechecks/421noyob.3yangi qoida,jami237.
Elektron sanoq faqat butun,N>=0,e=1.6e-19C,t/U>0; independent SI oracles.

Maydon ionizator emas,rekombinatsiya yagona yo‘qolish jarayoni deyilmaydi.
Mustaqil razryad tashqi ionizatorga ehtiyojsiz,elektr manbaiga ehtiyojsiz emas.
Magnit ranglari universal emas,markazdagi sust tortish B=0 kafolati emas.
B vektor,T birligi,berk chiziqlar/urinma,shkalasiz aniq tesla to‘qilmaydi.
§47–50sun’iy formula/FRQ yo‘q. Sahifa145§51boshlanishi:§50inclusive extentda
bor,lekin§50fakt/kartalarining manbasi sifatida ishlatilmadi.
Yuqori kuchlanish,ochiq alanga yoki vakuum qurilmasini yig‘ish berilmagan.

Yangi test13passed1.43s. Physics/Biology387passed/2PGopt-in skipped79.26s.
Actual localPG16 1passed36.64s:157dars/import/reimport/1570XP/replay,
legacy137XP/3streak/2stars saqlandi. FlutterPhysics21passed30s:114public8FRQ
320px/200%. Oldfull952backend/147Flutter alohida,bu partiyada full suite
qayta bajarilmadi. NativeAndroid/mustaqil ekspert/production sinovi yo‘q.

157/316,159qolgan.6:61/61,7:46/46,8:50/60,9:0/59,10:0/45,11:0/45.
Jami661karta/275formula yozuvi/172namuna/1045topshiriq/335FRQ.
Keyingi8§51«Yerning magnit maydoni»,PDF/bosma145. §51–55ning145–155asl
rasmlari va OCR o‘qildi;originaldars matni privateqoralamada,JSONhaliyo‘q.
Biology406/old6–8/Web/Kimyo/prod/AIExplain saqlandi. Oraliq tasdiq kutilmaydi.


## 8-sinf §51–55 — 2026-10-26 (Asia/Tashkent)

Yer magnit maydoni, tok maydoni, Amper kuchi, original masalalar va tokli ramka/asboblar: 5 dars/20 karta/10 formula yozuvi/6 namuna/36 topshiriq (21 MCQ+5 tartib+10 FRQ). §51 PDF145–146, §52 146–149, §53 149–151, §54 151–153, §55 153–155; bosma raqamlar teng. 11 asl sahifa ko‘rildi; 447 tekshiruv/431 noyob sahifa. 6 yangi formula oilasi; jami 243. T/mT/µT va μT/uT aliaslari yopiq registryda, massaning t birligi bilan chalkashmaydi.

Kompas mahalliy maydonga moslashadi, geografik va magnit qutblar bir nuqta emas. PDF145 yorug‘lik nuri/zaryadli oqim chalkashligi ajratildi; eski qutb koordinatalari bugungi navigatsiya kafolati emas. Erstedning 90° burilishi va g‘altak ichki parallel chiziqlari model shartlari bilan. Amper F=BIl faqat bir jinsli maydonga TIK to‘g‘ri faol qism uchun. Umumiy burchak formulasi yo‘q. PDF151 tarixiy amper jumlasining masofa/ideal uzunlik shartlari yo‘qligi sabab undan sonli kuch hisoblanmadi. PDF153 magnitni almashtirish tokni avtomatik almashtiradi degan gap takrorlanmadi; tashqi B va circuit current ajratildi. §51/52/55 sun’iy formula yoki FRQ yo‘q; qurilma yig‘ish topshirilmagan.

Yangi 16 test passed1.56s; dastlab ruff import/dict uslub xatolari to‘g‘rilandi, content test failure bo‘lmadi. Physics/Biology **403 passed, 2 PG opt-in skipped85.60s**. Actual isolated local PG16 **1 passed44.52s**:162 dars/import/reimport/1620XP/replay/legacy137XP3streak2stars. Flutter Physics **21 passed37s**, 124 public8FRQ 320px/200%; private javob/rubrika fixturega kiritilmadi. Old full952/147 alohida, full suite bu partiyada qayta bajarilmadi. Android/real lab/independent expert yo‘q.

**162/316;154 qolgan**. 6:61/61,7:46/46,8:55/60,9:0/59,10:0/45,11:0/45. Jami681 karta/285 formula yozuvi/178 namuna/1081 topshiriq/345FRQ. Keyingi **8§56 PDF/bosma155**. §56–60 original155–166 rasmlari/OCR ko‘rildi, matn private qoralama; PDF166 upper27-mashq davom etadi, arxiv165 chegarasi exact whitelist/note bilan kelgusi partiyada to‘g‘rilansin. Elektromagnit F scaling va universal motor/heat-engine FIK da’volari review talab qiladi; takrorlanmasin. Biology406/old grades/Web/Kimyo/prod/AI Explain saqlandi. Oraliq tasdiq kutilmaydi.


## 8-sinf §56–60 va 60/60 sinf regressiyasi — 2026-10-26 (Asia/Tashkent)

Lorens kuchi, elektromagnit/rele, raqamli elektromagnit laboratoriyasi, o‘zgarmas tok dvigateli va original masalalar:5 dars/22 karta/8 formula yozuvi/6 namuna/36 topsshiriq (21MCQ+5tartib+10FRQ). §56PDF155–157,§57PDF157–161,§58PDF161–162,§59PDF162–165,§60PDF165+166upper27-mashq. Bosma=PDF.12asl tasvir ko‘rildi;459review checks/442noyob sahifa.4yangi qoida,jami247 (238 reviewed+5 legacy b11,bu partiya+4). Oldingi reporting helper faqat REVIEWED_FORMULASni238deb sanagan edi; metric barcha FORMULAS union243deb tuzatildi,grading o‘zgarmadi. pN yopiq registry10^-12N,nN/mNdan farqli.

F=|q|vB faqat bir jinsli maydonga TIK tezlik va modul; manfiy zaryad kuch yo‘nalishini teskarilaydi,parallel holatda magnit kuch nol. Umumiy burchak/cyclotron-radius/LLM qo‘shilmadi. PDF157 F ning I yoki o‘ramga universal chiziqli bog‘lanishi shartsiz takrorlanmadi; controlled qualitative comparison. Rele kontakt turi ochiq,159oddiy relay va160photorelay farqli. Lab58 faqatdigital model,physical_experiment_completed=false,physical_assembly=not_assigned;elektrical-safety expert required_before_general_publication bajarildi deyilmaydi. PDF164 barcha motor>80%,barcha heatengine<=20%,nol pollution universal da’volari kontentga kiritilmadi;foiz/frq sun’iy yaratilmagan. Hech qanday appliance disassembly,winding/live circuit topshirilmagan.

Frozenstage1§60end165saqlandi;original166upper27-mashq2–5 exact(topic60,page166)whitelist va extent_note bilan. Chapterreview yangi numbered lesson deb hisoblanmadi. Review5ning tezliksiz massadan teng Lorentzforce xulosasi rad etilgan;originalsavolda tezlik/zaryad sharti aniq. Barcha sonli javoblar literal independent oracleda,formula alternatiflari/wrongunits/sign/domain bilan.

Yangi test:initial18passed/1failure faqat guard error-code regex expectednomi noto‘g‘ri bo‘lgani;citation_outside_topic bilan tuzatildi,grading/citation guard bo‘shatilmadi. Keyin19passed. **To‘liqbackend1000passed,4PGopt-in skipped,13mavjudwarnings340.46s**. Actual isolatedPG16 **1passed52.91s**:167lesson/import/reimport/1670XP/replay;legacy137XP3streak2stars saqlandi. **To‘liqFlutter147passed54s**,134public8FRQ320px/200%;analyzeNoissues1.7s. Sourceaudit all originalhashes/OCR/native/raster447→459checked. ActualTCPHTTP167/webbuild/nativeAndroid qayta bajarilmadi;independentexpert yo‘q.

**167/316;149qolgan**.6:61/61,7:46/46,8:60/60,9:0/59,10:0/45,11:0/45. 8-sinf253karta/129formula yozuvi/70namuna/419topshiriq/134FRQ/5digital lab/2practical. Jami703karta/293formula yozuvi/184namuna/1117topshiriq/355FRQ. Biologiya406/6–7/frozen8/Web/Kimyo/prod/AIExplain saqlandi.

Keyingi **9-sinf§1«Modda tuzilishining molekulyar-kinetik nazariyasi»,PDF/bosma4**. §1–5PDF4–21 cachedOCR/aslrasmlar tekshirildi;matn privateqoralamada,JSONhaliyo‘q. Brown particle threshold,relative-mass u label,coarsewatermass,NA approximations va RMS vs mean-square notation reviewda ajratilsin. Barcha316tayyor deb aytilmaydi;oraliq tasdiq kutilmaydi.


## 9-sinf §1–5 — 2026-10-26 (Asia/Tashkent)

MKN/Broun, molekula massasi/o‘lchami, modda miqdori, original masalalar, ideal gaz:5dars/24karta/24formula yozuvi/6namuna/46topshiriq(17MCQ+5tartib+24FRQ). Manbalar:§1PDF4–7,§2PDF7–12,§3PDF12–16,§4PDF16–18,§5PDF18–21;bosma=PDF,firstsegment local=original.18asl sahifa ko‘rildi;477pagechecks/460noyob.24yangi qoida,jami271. mm3/1/mol/1/m3,m^-3/m⁻³ aliaslari yopiq registry;nu ASCII kitobningnyu belgisi,nsonkonsentratsiya,Nbutun. Mkg/mol vaMrunitless ajratildi.

PDF6 Brown>1µm harakat yo‘q/<1nm universal threshold takrorlanmadi;Brounzarrasi va muhitmolekulalari ajratildi. PDF7 dust/convection directBrownproof deyilmaydi;sharchalar mexanik model,real molekula emas. PDF9 suvningpacking2.7e-26kg qo‘pol model,aniq massadek ishlatilmadi;masalalarda m0 ochiq. PDF10/11/12 noto‘g‘ri nisbiy massaga u yorlig‘i o‘rnigaMr/Ar o‘lchamsiz;u1.66e-27kg massayaqinlashuvi. Historical12g-carbon moledefinition currentexactSI deb aytilmagan;NA6.022e23/6.02e23/6e23 manbayaqinlashuvlari har hisobda beriladi. Zarra soni butun,nmanfiyemas,bo‘luvchilar>0.

PDF18 mean-square bilan19RMS farqlanadi;v_rmsarithmeticmean emas,E mean-translational-per-particle,totalgas emas. gas_rms_speedalone boundedexactroot optin:irrationalroot/floatapprox rad,eski parserdefaults saqlandi. 1/m3 Unicode m⁻³ oldpositiveexponentnormalizationdan keyinm⁻3ga aylanishi sababunknown_unitxatosi testda qayta hosil qilindi;normalized closedalias m⁻3 qo‘shildi,genericpermissiveparser yo‘q. Source16rod4.8e22/concentration6e26/coating1.75e20 va19sqrt600/20E3.6e-22mustaqil tekshirildi;authored masalalar original. Real coating/chemical operation yoki tajriba tasdig‘i berilmagan.

Yangi testinitial27pass/2fail normalizedUnicodeunitxatosi;rootcausefixed,keyin **29passed3.05s**. Physics/Biology **451passed,2PGopt-in skipped99.79s**. Actual isolatedlocalPG16 **1passed51.02s**:172lesson/import/reimport/1720XP/replay/eski137XP3streak2stars. FlutterPhysics **23passed44s**:134old8FRQ+24new9publicdrafts320px/200%,9sinfAPIquery/bibliografiya. Fixturesfaqatpublic savollar,privategradingkeys yo‘q. Old fullbackend1000/147Flutter/analyze1.7salohida;bu partiyada qaytafull/analyze/Android/TCPbuild bajarilmadi. GRADE8validationningnewtestseconds19passed2.12s bilan aniq tuzatildi;reporthelper original_page_checks459maydoni tiklandi.

**172/316;144qolgan**.6:61/61,7:46/46,8:60/60,9:5/59,10:0/45,11:0/45. Jami727karta/317formula yozuvi/190namuna/1163topshiriq/379FRQ. **Keyingi9§6«Temperatura»,PDF/bosma21**. §6–10original21–35/OCR ko‘rildi;Celsius/Kelvin273.15vs273approx,absolute/gaugepressure,SternflightvsRMS statistikasi,ideal equationconditions qayd etilsin. JSONhaliyo‘q. 8sinffinalbackendc224e7a/Fluttere7bf538 GitHubsaveconfirmed. Biology406/frozen6–8/Web/Kimyo/prod/AIExplain saqlandi;oraliq tasdiq kutilmaydi.


## 9-sinf §6–10 va exact-root grading — 2026-10-26 (Asia/Tashkent)

Temperatura, gaz molekulalari tezligi, original masalalar, holat tenglamasi, izotermik jarayon:5dars/25karta/24formula yozuvi/5namuna/44topshiriq(15MCQ+5tartib+24FRQ). §6PDF21–25,§7PDF25–28,§8PDF28–30,§9PDF30–33,§10PDF33–35;bosma=PDF.15asl sahifa ko‘rildi;492pagechecks/474noyob,24yangi qoida,jami295.

Private expected_root_rational answer-square,immutablePositiveSquareRoot va aniq squared-interval grading qo‘shildi:mandatory positive grid,abs_tol=grid/2,rel_tol0. Bounded128digitratio/4096bitradicand,no float/CAS/eval. Canonical decimal truth emas. Two-root source models414000→643.4m/s and249300→499.3m/s grid0.1. PerfectrootsFractionga qaytadi,eski exactrootparser/defaults saqlandi. Clientga privatekey/radicand/rules/tolerance chiqmaydi,answer injection rad. APIv2/publicDTO/DBschema saqlandi,migrationyo‘q. FRQ_NUMERIC_ROOTS.md texnik kontrakt;oldFRQplan tarixiy tasdiqkutish matni joriyishni bloklamasligi aniqlandi.

PDF22 exact273.15vsrounded273, signed Celsius givens va Kelvinoutput ajratildi;belowabsolutezero rad. PDF23/24meanperparticleE va totalTRANSLATIONAL3pV/2,absolute p vs gauge farqli. 0Kda barcha realharakatto‘xtaydi universalclaimko‘chirilmadi. PDF25kNAproduct8.3076vsroundedR8.31. Maxwellmostprobable vsRMS vsSternflightstat farqli;source28 flight592 andRMS~588.430yaqinligi ularni aynan bittaaverageqilmaydi. Isothermal/combined law bir xil amount/composition,positiveT,pabsolute;pressureincrease dp va finalp2alohida. No pressurevessel/hotfilament/rotatingapparatus/sho‘ng‘ish sinovi.

Root27+oldrational14+temperature/state36=**77passed3.73s**. Initialrootextremetest literal51digit legacyguardga urilgan;1e50+1boundedexpression bilan tekshirilibguard saqlandi. **Fullbackend1092passed,4PGopt-in skipped,13mavjudwarning351.78s**. Actual isolatedlocalPG16 **1passed62.56s**:177lesson/import/reimport/1770XP/replay/legacy137XP3streak2stars. **FullFlutter149passed63s**,48public9FRQ(roundedroots643.4/499.3drafts)+134old8FRQ320px/200%;analyzeNoissues1.6s. ActualTCP177/webbuild/nativeAndroid/mustaqilekspert bajarilmadi.

**177/316;139qolgan**.6:61/61,7:46/46,8:60/60,9:10/59,10:0/45,11:0/45. Jami752karta/341formula yozuvi/195namuna/1207topshiriq/403FRQ. **Keyingi9§11«Izobarik jarayon»,PDF/bosma35**. §11–15source35–43/50–53aslrasmlar/OCR ko‘rildi,privateoriginalmatnqoralama. PeamodelV/S effective thicknessnotexactdiameter;closedidishnotnecessarilyrigid;internalU3/2onlyMONATOMICclassicalideal;negativeDU conventions kelgusi reviewda saqlansin. Biology406/frozen6–8/old9/Web/Kimyo/prod/AIExplain saqlandi;oraliq tasdiq kutilmaydi.


## 9-sinf §11–15 — 2026-10-26 (Asia/Tashkent)

Izobarik/izoxorik,raqamli molekula/xonamodeli,originalmasalalar,ichki energiya:5dars/24karta/22formula yozuvi/5namuna/42topshiriq(15MCQ+5tartib+22FRQ),1digitalpractical. §11PDF35–37,§12PDF37–38,§13PDF38–40,§14PDF40–43,§15PDF50–53;bosma=PDF.13asl sahifa,505pagechecks/486noyob.21yangi qoida,jami316formulaoilasi;bu316darsdeganiemas!

Kelvinratios/absolute p,fixedamount/composition,pconstvsVconst aniq. Closedvesselnotalwaysrigid. Cooling/heatingpositive magnitude vs signedΔT ajratiladi. PeaV/S effective modelthickness,notexactdiameter;L/N separateaverage,packingerrorspossible. Classroom optionalmodel same§13ichida;conditioneddatasetsphysicalmeasurementemas. AirM29g/molsourceapprox. §14leakfremaining0..1,pressurefractionf=dp/p1boshqa meaning;hydrobubbleisothermal/no gasloss/surface tensionneglected,g10sourceapprox. Divesafety/realexperiment assignedemas.

§15U3nuRT/2 va3pV/2 ONLYCLASSICALMONATOMIC idealgas. General gas wording source50/51ko‘rko‘rona takrorlanmadi;source51eq8monatomicshartaniq. DU=U2-U1,sovishda−3739.5Jcorrect,positive3739.5signerror. ConstantpΔUvolumefaqatshu model,oldunsignedrulesunchanged. Source52argon−14958Jindependentoraclechecked. Source53fullnext16notusedas15facts. Authoringvalidator12uchunmissingformulacaught;3explicitformulateachingentry qo‘shildi,guardbo‘shatilmadi.

Yangi36testpassed3.10s. Physics/Biology **550passed,2PGopt-in skipped108.20s**. Actual isolatedlocalPG16 **1passed57.04s**:182lessons/import/reimport/1820XP/replay/eski137XP3streak2stars. FlutterPhysics **23passed49s**,70public9FRQ320px/200%,signedDUdraft−3739.5. Oldfull1092backend/149Flutter/analyze1.6s alohida;bu partiyadafull/TCP/webbuild/nativeAndroid qayta bajarilmadi. Independentphysics expert review bajarilmagan.

**182/316;134qolgan**.6:61/61,7:46/46,8:60/60,9:15/59,10:0/45,11:0/45. Jami776karta/363formula yozuvi/200namuna/1249topshiriq/425FRQ. Keyingi **9§16«Termodinamik ish»,PDF/bosma53**. §16–20source53–65original/OCRo‘qildi,darsJSONhaliyo‘q. PDF64unknownc numerator(m_s*c_s−m_k*c_k)minus publishedtypo:PDF58heatbalancecorrectpluswater+calorimeter;keyingidarsda source-supportederratum kerak. SpecificheatJ/(kg*K)unique;heatnotstoredstateproperty,isolated/no-worksumenergyindividualschange;20digitallabnotactualboilingprocedure. Oldgrades/Biology406/website/Kimyo/prod/AIExplain saqlandi;oraliq tasdiq kutilmaydi.


## 9-sinf §16–20 — 2026-10-26 (Asia/Tashkent)

Termodinamik ish,issiqlik/kalorimetriya,originalmasalalar,raqamli muvozanat amaliyoti va raqamli c laboratoriyasi:5dars/24karta/18formula yozuvi/5namuna/40topshiriq(15MCQ+5tartib+20FRQ),1digitalpractical+1digitallab. §16PDF53–55,§17PDF55–60,§18PDF60–63(+17PDF56),§19PDF63–64(+17PDF56/58),§20PDF64–65(+17PDF56/58). Bosma=PDF.13asl sahifa ko‘rildi;518pagechecks/498noyob.15yangi qoida,jami331. cJ/(kg*K),kJ/(kg*K)va yopiqcommon-notationaliases,oldkJ/Kdoimiylari o‘zgarmadi.

A gazBYwork,QheatTOBODY,signedDV(absolutevolumenotnegative) aniq. Isobaricworkpconst,no arbitrarycurvedpathrectangle. cconst/NOphasechange va heattransferNOTstoredstateproperty. IndividualUchange vs isolatedTOTALconservation;closedmatteralone notenough. Source59mghmodelFULLdissipationINTOsamewater,notfreeflightautomaticheating. Mixtureequalc/density/additivevolumeapprox explicit;impactfractionetaENVIRONMENTshare,body1-eta,no physicalimpactexperiment.

**Publishedsource64lab20minusERRATUM**:original58correctplusheatbalance coldwaterANDcalorimeterbothreceiveenergy. Correctch=(mw*cw+mc*cc)*(Tf-Tc)/(mh*(Th-Tf)),Tc<Tf<Th. Independentcase210+178=388J/K=>ch388,wrongminus32;testswrongformulavaluebothreject. Sourcepages58/64cited,samebatchreferences17/20allowed,no guardrelaxation. SOURCE_REVIEW.mderratumdocumented;independentcalorimetryexpertgeneralpublicationrequired,NOTperformed. 19/20conditionaldigitaldatasets notactualmeasurements,integer-Ktable notinfinitelyprecise timeprediction. No boiling/metaltransfer/glass/appliance operation assigned.

Newtestinitial35passed/1failure onlytest float−0.004 vs exactFraction(-1,250),fixedindependentexactoracle,**36passed3.15s**. Physics/Biology **586passed,2PGopt-in skipped109.98s**. Actual isolatedlocalPG16 **1passed54.34s**:187lesson/import/reimport/1870XP/replay/legacy137XP3streak2stars. Flutterinitial22passed/1failure stale70count compiledwhilefixture became90;orchestrationrace,codenotlayoutbug. Allmutationsawaited,then sequentialrerun **23passed40s**,90public9FRQ320px/200%,signedDV−0.004/Q−8400drafts. Oldfull1092backend/149Flutter/analyze1.6salohida;newfull/Android/TCP/webbuildnotrun.

**187/316;129qolgan**.6:61/61,7:46/46,8:60/60,9:20/59,10:0/45,11:0/45. Jami800karta/381formula yozuvi/205namuna/1289topshiriq/445FRQ. Keyingi **9§21«Yoqilg‘ining solishtirma yonish issiqligi»,PDF/bosma65**. §21–25original65–74andOCRread;lab25extends74upperbeforechapterreview. Frozenmap25end73preserve,exact(topic25,page74)whitelist/note needed. FirstlawA_BYvsworkON wording,sourceRrounding2500J→40.112Knotexact40,secondlawexternalchangesqualifier kelgusi reviewda. Biology406/frozen6–8/old9/Web/Kimyo/prod/AIExplain saqlandi;oraliq tasdiq kutilmaydi.


## 9-sinf §21–25 — 2026-10-26

Yoqilg‘i,termodinamika birinchi qonuni,originalmasalalar,qaytar/qaytmas jarayonlar,raqamli issiqlikbalansi laboratoriyasi:5dars/22karta/18formula/5namuna/40topshiriq(17MCQ+5tartib+18FRQ). §21PDF65–66,§22PDF67–70,§23PDF70–71,§24PDF72–73,§25PDF73–74;bosma=PDF. Lab25suv c4200 uchunoldingi tekshirilgan§17PDF56 ham citeqilindi va qaytaaslrasmdan tekshirildi. Faqat(topic25,page74)originalcontinuation va faqat(batch5,prior17,page56)oldingi tekshirilganfoundation whitelist. PriorbatchcontentSHA/previousrange/reviewSHA/originalreviewtrue talabqilinadi;unlistedpage/crossbatch/future/cycle/digesttamper rad. PDF va OCRprivate.529pagechecks/507unique.

Qfuelbatamomyonishajralganenergiyamusbatmoduli,Q_TO_SYSTEMsigneddanalohida;J/kg,kJ/kg,MJ/kg yopiqspecificenergybirliklari. Q=DU+A_BY,A_ON=-A_BY signed birinchiqonun;adiabaticQ0isothermalemas. 40/60ulush faqatclassicalmonatomicideal isobaricmodel;R8.31vaQ2493J→40Kauthoring,source2500J→40.1123Krounded40tafovut qayd. Cold-to-hot secondlawNOOTHERCHANGEsharti,sun’iyentropyformula yo‘q. Lab25conditionaldigitaldata,realheatmixing/measurementclaimyo‘q;Qhot/coldmagnitudesva signedhotQ ajratildi. Balansfarqiidish/atrof/modelshartlari bilanizohlanadi,energiyasaqlanishinibuzishdeyilmaydi.

Newcontent32passed3.42s;Physics/Biology618passed/2PGskipped122.18s. ActualisolatedlocalPG161passed61.61s:192lessons/import/reimport/1920XP/replay/legacy137XP3streak2stars. FlutterPhysics23passed54s,108publicgrade9FRQ320px/200%;oldfullbackend1092/Flutter149/analyzealohida. NativeAndroid,independentexpert,newTCP/webbuild/prodnotrun.

**192/316;124qolgan**:6:61/61,7:46/46,8:60/60,9:25/59,10:0/45,11:0/45. Jami822karta/399formula/210namuna/1329topshiriq/463FRQ,349executablefamilies. Keyingi **9§26«Ichki yonuv dvigatellari»,PDF/bosma81**;§26–30PDF81–90aslrasm/OCRreviewnavbatda,JSONhaliyo‘q. Biology406/frozen6–8/old9/Web/Kimyo/prod/AIExplain saqlandi;tasdiqkutmasdan davom.


## 9-sinf §26–30 — 2026-10-26

Ichki yonuv/dizel/reaktiv model,issiqlik dvigateli va Karno sikli,original masalalar,ekologik konseptlar,quvvat va yoqilg‘i masalalari:5dars/21karta/13formula/5namuna/37topshiriq(19MCQ+5tartib+13FRQ). §26PDF81–83,§27PDF83–86,§28PDF86–87,§29PDF87–89,§30PDF89–90;bosma=PDF. Barcha10aslrasm/OCR va88/89splitchegarasi tekshirildi.539pagechecks/517unique.

Qh/Qc musbat modullar,A_NET_BY=Qh-Qc,to‘liq sikldaDU0. Karno ikki izoterma/ikki adiabat,qaytar ikki rezervuar uchun eta_max=1-Tc/Th,Kelvin;real dvigatel aynan shu maksimumga teng deyilmaydi. Source85faqattemperaturafarqi jumlasi yetarli emas,maxrajTh ham bor:600/300Keta.5,1200/900Keta.25,farqbirxil.84siqilish A3ish egasi/is horasi ehtiyotkor ajratildi.86maktab273yaqinlashuvi vs273.15yashirin almashtirilmadi,yangiFRQKelvin.81qisqa ignition/intakebayoni to‘liq4takt jadvali emas,oktan gas claim takrorlanmadi;26/29sun’iyformula yo‘q.87–88historicalglobalstatistics currentfactdeyilmadi,allfreon/onlysolar umumlashtirishlari ommaviyilmiyfaktgaaylantirilmadi.89kerosin46MJ/kg vs66table42tafovut SOURCE_REVIEWda;authoredheatingnoma’lumfuelq40providedparameter,kerosinuniversalconstantaemas. Foydali heatingenergy mechanicalworkdebnomlanmaydi.

Newcontent36passed3.10s. Dastlabfullbackend1130pass/4skip/102setupERROR: /var/tmp/ilm-physics-g9b6-full read-only,muhit huquqi,kodtestfailureemas. Exacttempdirectorypermissionbilan fullrerun **1232passed/4PGopt-in skipped/13existingwarnings340.60s**. Guardlarpasaytirilmadi. ActualisolatedPG16 **1passed68.07s**,197lesson/import/reimport/1970XP/replay/legacy137XP3streak2stars. **FullFlutter150passed66s**,analyzeNoissues1.6s;121public9FRQ320px/200%,sourceKarno4stagelonglabelsentry/clear testi,formula va decimaldraftlar. No runtimeFlutterorwebsitechange. NativeAndroid/TCP197/newwebbuild/independentexpert/prodnotrun.

**197/316;119qolgan**:6:61/61,7:46/46,8:60/60,9:30/59,10:0/45,11:0/45. Jami843karta/412formula/215namuna/1366topshiriq/476FRQ,362families. Keyingi **9§31«Suyuqlikning xossalari»,PDF/bosma94**. §31–35PDF94–106aslrasmlar vaOCRko‘rildi;privateauthor/test/rulesqoralama,JSONhaliyo‘q. SigmaunitsN/m=J/m2,completewettingonlycapillary,needle/bubble2interfaces,labconditionaldata,source106windowglassflowmyth reviewda qayd etilsin. Biology406/frozen6–8/old9/Web/Kimyo/prod/AIExplain saqlandi.


## 9-sinf §31–35 — 2026-10-26

Suyuqlik/sirt tarangligi,ho‘llash/ideal kapillyar,originalmasalalar,raqamli dinamometr laboratoriyasi,kristall/amorf:5dars/22karta/13formula/6namuna/35topshiriq(17MCQ+5tartib+13FRQ). §31PDF94–97,§32PDF97–100,§33PDF100–103,§34PDF103–104,§35PDF104–106;bosma=PDF.13aslrasm/OCRtekshirildi;552pagechecks/530unique. SigmaN/m=J/m2,legacyforce-per-lengthstiffnessdimension nomi saqlandi,prujinaN/m/kN/mo‘zgarmadi. Yangi closedmN/m,J/m2,mJ/m2aliaslari. CompletewettingONLYidealcapillary,radius/diameterfactor2,exactrationalh73/4905m/r73/98100mfinalgrid. Needleikki kontakt,thinsoapbubbleikki interface,singledropbilan aralashmaydi;tomchiuzilishapprox,no fakeexact1040count. LabconditionalF2-F1baseline va2perimeter,realmeasurementnotclaimed. Crystal/allproperties anisotropy/amorphousisotropy universaldeyilmaydi;source106oldwindowglassflow claimreviewgaqoldirildi,verifiedfactemas.

New27passed2.32s,initialPhysics/Biology681passed/2skipped125.89s;PG1passed61.21s202lesson/import/reimport/2020XP/replay/legacy137XP3streak2stars;FlutterPhysics24passed50s134public9FRQ320px/200%. **InitialoriginalauditFAILED** original_page_text_or_pixels_mismatch95/104only2.0PNGafter2.2render. PDFSHA/OCR/native/2.2rasterallmatched;fresh2renderreviewmatched. Actualbugreproducedwithgenerated476x474indexedPNG110/115displaywidths,no textbookassetcommitted. `scripts/audit_physics_source_pages.py` isolatescatalog2.2andreview2.0documentcontexts;no hashcheckweakened,noreview/cataloghash rewritten. Two newregressionsactualdrift+tamperreject;15sourcetests0.54s. **RerunPhysics/Biology683passed/2PGskipped112.50s**,all552originalpagechecksPASS. Oldfull1232/150/analyze0issues1.6salohida;newfull/Android/TCP/webbuildnotrun.

**202/316;114qolgan**:6:61/61,7:46/46,8:60/60,9:35/59,10:0/45,11:0/45. Jami865karta/425formula/221namuna/1401topshiriq/489FRQ,375families. Keyingi **9§36«Qattiq jismlarning mexanik xossalari»,PDF/bosma106**. §36–40original106–119andOCRread,privateauthor/rulesqoralama,JSONhaliyo‘q. Source1094mmvs3mm,1106kgvs4kg/kamidalmax,114ice334vs115336,116windcause,119unsafeclosedvessel/meatneverclaims kelgusireviewda. Biology406/frozen6–8/old9/Web/Kimyo/prod/AIExplain saqlandi;tasdiqkutilmaydi.


## 9-sinf §36–40 — 2026-10-26

Mexanikxossalar/Young,originalmasalalar,erish/qotish,specificfusion/amorf,bug‘lanish/kondensatsiya:5dars/24karta/21formula/5namuna/40topshiriq(15MCQ+5tartib+20FRQ). §36PDF106–109,§37PDF109–111,§38PDF111–113,§39PDF113–116,§40PDF116–119;bosma=PDF.14aslrasm/OCR,566pagechecks/543unique.19yangi qoida oilasi;eski sensible_heat/thermal_pressure qaytaqo‘llandi. MPa/GPa closedaliases,Pa/kPa/prujinashartlari saqlandi.

DL/eps,Pa sig vsE vsN/mk alohida,kichik LINEARelasticmodel.1094mmvs3mm/1106kgvs4kg contradictorysamples copiednot;originalconsistentproblems. SelfweightlmaxMAXIMUMg10explicitthisfamily,notkamidaorrealworkingload.111–113idealcrystalplateaugivenpressure/temperatureapprox600K,preheatQ7800excludeslatent.114icelam334vs115sample336 documented,questionprovidedconstantconsistent. Signedfreeze/condenseQ_TO_BODYnegative,releasedmagnitude positive. Icebalanceinitial/finalTm/noexternal/calorimeter,exact84/167kgonlyfinal1ggrid=.503.116windcause/118allairbubbles/119meatneverorDIYsealedhotvesseluniversalclaimsnotassigned. p=nkTidealapproxnotexactvaporEOS.

AdditionalREALbug:oldnegativeworkQ spec sign_error generictextsaidnegativeimpossible. `assessment_runtime.submit` normalizesONLYthatliteraloldboilerplate to neutral sign/conventionfeedback. OldJSON/sourcehash/snapshot/gradedresultpayloadshape/XPunchanged. Alreadycommittedresponse replay returns before normalization,unchanged. APItestsissuedoldpositiveandnegativeworksnapshot,wrongoppositesign,repeatidenticalresponse,noxp,no storedspecmutation. Newcontentneutralfeedback. Initialnewtest32pass1failure expectedout_of_tolerancevsactualsign_error correctedtest;then33pass2FKfixturefail,oldquestionswere missingdisposableDB,fixtureimportsimmutableoldbatch4,FKnotdisabled. Final **35passed3.79s**.

**Fullbackend1296passed/4PGopt-in skipped/13existingwarnings360.41s**. ActualisolatedPG16 **1passed66.55s**,207lesson/import/reimport/2070XP/replay/legacy137XP3streak2stars. FlutterPhysics24passed57s,154public9FRQ320px/200% inclMPa/GPa,signedlatentQ. PreviousfullFlutter150/analyzeNoissues1.6salohida;newfullFlutter/Android/TCP207/newwebbuild/independentexpert/prodnotrun. All566originalsourcechecksPASSusingisolatedrendercontexts.

**207/316;109qolgan**:6:61/61,7:46/46,8:60/60,9:40/59,10:0/45,11:0/45. Jami889karta/446formula/226namuna/1441topshiriq/509FRQ,394families. Keyingi **9§41«Atmosferadagi hodisalar»,PDF/bosma119**. §41–45original119–126/131–138andOCRread;privateauthor/rulesdecisionsqoralama,JSONhaliyo‘q. 43exercise126upperneeds exactcontinuationwhitelist,frozen125endpreserve;psychrometry121row28diff10dubiousnotuse;12517C2kPa>sat1.93notstableunsaturatedcase. Fizeau4NlfFIRSTDARKandroundedhistoricalnums,mixedsourceerratareview;degreevsradindependentdimension,sinesgivenrationalFRQnoCAS. Biology406/frozen6–8/old9/Web/Kimyo/prod/AIExplain saqlandi;tasdiqkutilmaydi.


## 9-sinf §41–45 — 2026-10-26

Atmosfera/namlik,raqamli psixrometr laboratoriyasi,originalnamlikmasalalari,yorug‘lik tezligi,geometrikqaytish/sinish:5dars/24karta/21formula/5namuna/41topshiriq(15MCQ+5tartib+21FRQ). §41PDF119–124,§42PDF124–125+foundation41pages120/121,§43PDF125+126uppercontinuation,§44PDF131–134,§45PDF134–138;bosma=PDF.16aslrasm/OCR va132/133splitchecked;582pagechecks/558unique. 18yangi qoida,old densityfamilyreused. g/m3closedalias;angle_degreesdimension°/degexplicit,oldradunchanged,notinexactpi conversion.

RhoWATERVAPORmass/airvolume,relativehumiditySAMEtemperature/partialpNOTtotalatm,no Pa=densitysynonym,no100%molecularmotionstops. Selected121tablecells24/5→62%,20/4→66%,28/7→53%,dubious28/10=29notusedorrepairedwithoutsource.12215C12.5gvs12012.8approxnotexactdewpoint.12517Cp2kPa>sat1.93notcopiedasstableunsaturatedcase,newT300p1.662M18R8.31→.012kg/m3.126upper23mashqsource43beforechapterreview,frozenend125preserve,onlytopic43/page126+noteextraallowed.

Ryomerhistoricalrounding,FizoN720l8.6kmf12.67→313809408vsprinted313300000documented. c4NlfidealEQUALtooth/gapFIRSTDARK,frotationHz,Ninteger,lONEWAY;roundtrip2l. c299792458definitionvs3e8givenapprox distinct. ReflectionanglesFROMNORMAL,nabs=c/vvsrelative,sina/sinbGIVENSareSINnumbersNOTangledegrees,noCASarbitrarytrigclaim. Normalincidencenot0/0,evaluatedsinb>1rejectundertransmittedrayfamily. Ordinarybookmedia/wavelengthconditions,mixedroundedn/vtable/parallelplatescope explicit. Nophysicalthermometer/wheel/brightlightsystemassigned.

New38passed3.02s;Physics/Biology **756passed/2PGskipped132.13s**;actualisolatedlocalPG16 **1passed67.79s**,212lesson/import/reimport/2120XP/replay/legacy137XP3streak2stars. FlutterPhysics24passed56s175public9FRQ320px/200% incldensity/degree/SINdrafts. All582sourcechecksPASS. Previousfullbackend1296/Flutter150/analyze0issue1.6salohida;newfull/Android/TCP212/newwebbuild/independentexpert/prodnotrun.

**212/316;104qolgan**:6:61/61,7:46/46,8:60/60,9:45/59,10:0/45,11:0/45. Jami913karta/467formula/231namuna/1482topshiriq/530FRQ,412families. Keyingi **9§46«Masalalar yechish»,PDF/bosma138**. §46–50original138–146/OCRread,private rules/decisionsqoralama,JSONhaliyo‘q. Source140alpha30glassair saysbeta42 butsinbeta.75→~48.5904,source143M26TIRobservednotcriticalsoindicesonlybounds;criticalSINgivenratherthaninventangle;lab49normalentryfirstface;50signedD/Fnewfamiliesandbiconvexair-onlylensmaker planned. Biology406/frozen6–8/old9/Web/Kimyo/prod/AIExplain saqlandi;tasdiqkutilmaydi.


## 9-sinf §46–50 — 2026-10-26

Optik masalalar,to‘la ichki qaytish,critical/bound masalalari,raqamli prizma laboratoriyasi,linzalar:5dars/22karta/12formula/5namuna/34topshiriq(17MCQ+5tartib+12FRQ). §46PDF138–139,§47PDF139–142,§48PDF142–143+47page140foundation,§49PDF143–144,§50PDF144–146;bosma=PDF.9aslrasm/OCR,591pagechecks/566unique. Initialauthoringcitationguard rejectedmixed140/143single-topicref;fixedhelper splits exactowner47/page140 and48/page143,no guard weakened.

Equal-timepaths,ray-segmentINTERIORtheta2alpha(notvelocityvectors),planemirrorseparation2d. Source140glass1.5air1alpha30saysbeta42incorrect:independent sinbeta.75→48.59037789;alpha40→74.61856831,critical→41.81031490. NewquestionsdoNOTcopy42. TIRn1>n2,alphaSTRICTLYgreaterthancritical;criticalborderseparate. Source143M26observedTIRonlyimplies n2<n1*sina or n1>n2/sina,notuniqueactualindex. Tests two distinctn2=1.05/1.15bothTIRunder n1.5/sina.8,critical1.2grazing. ActualcriticalSINgivenfornumericfamily,5/3finalgrid1.667. Lab49FIRSTfaceNORMALentry,exitair,n=sinExit/sinAonlythisgeometry,digitalconditional2estimatesnotactualexperiment. SignedlensF/Dfamiliesseparateold6positive;negativeFstillrejectedbyoldlens_power. LensmakerrestrictedthinBIconvexair,n>1,R1/R2positivemagnitudes. No unsafeSunfocus/brightbeam/medicaloperationassigned.

New32passed2.86s;Physics/Biology **788passed/2PGskipped141.03s**. ActualisolatedlocalPG16 **1passed72.88s**,217lesson/import/reimport/2170XP/replay/legacy137XP3streak2stars. FlutterPhysics24passed59s,187public9FRQ320px/200% inclnegativeDdraft. All591originalsourcechecksPASS. Previousfull1296backend/150Flutter/analyze0issue1.6salohida;newfull/Android/TCP217/newwebbuild/independentexpert/prodnotrun.

**217/316;99qolgan**:6:61/61,7:46/46,8:60/60,9:50/59,10:0/45,11:0/45. Jami935karta/479formula/236namuna/1516topshiriq/542FRQ,424families. Keyingi **9§51«Yupqa linza yordamida tasvir yasash»,PDF/bosma146**. §51–55original146–156andOCRread,JSONhaliyo‘q. Source147signedF/fstatementvsmodulusminusformula conflict,149Kmagvsfsigned,150meanFtheninverseDvsmeanD,151D0/Fnearpointvsrelaxedeyeapprox,153objective/eyepiecelabelswap/microscope schoolapprox;55eyequantitative1.5/retinabiooversimplification/elderlyreadingvshyperopia needreview,keepconceptdiagramnotclinicalprescription. Biology406/frozen6–8/old9/Web/Kimyo/prod/AIExplain saqlandi;tasdiqkutilmaydi.


## 9-sinf §51–55 — 2026-10-26

Yupqa linzada tasvir,originaloptikmasalalar,raqamli fokus laboratoriyasi,optikasboblar,ko‘zkonseptlari:5dars/23karta/12formula/5namuna/36topshiriq(17MCQ+5tartib+14FRQ). §51PDF146–148,§52PDF148–150,§53PDF150–151,§54PDF151–154,§55PDF154–156;bosma=PDF.11aslrasm/OCR,602pagechecks/576unique.12yangi qoida,jami436.

Signed1/F=1/d+1/f izchil,F/fnegativeforvirtual/diverging;source147minusformulaonlymagnitudesbilanmos,signedkattaliklarnidoubleminusqilmaymiz. KpositivefMag/d,orientationseparate,d=Ffiniteimageno. Source149Konlyambiguousreal/virtual:explicitnewquestionsF.4K4real d.5/virtuald.3. Digital53labpositiveREALscreen d/f,source150meanFTHENinverseD,NOTmeanD:.15/.20/.25→Fmean.20,D5,meanD47/9. LupaD0/Frelaxedeye/schoolmodel,D0.25mconventionnotuniversalpersonalnearpoint;source151nearpointtextnotuniversalexactformula. Source153objective/ocularlabels correctedby152diagram84functionalroles. MicroscopelD0/(F1F2)explicitSCHOOLapproxlarge-separationmodel,notexactanydevice/resolution. Source152megapixelalwaysquality/microscope100000opticaluniversalclaimsnotcopied.55CONCEPTONLYnoartificialformula:n=1.5eyeconstant/retinayellowcoating/binocularidentical/universal15–20cm/agingequalsallhyperopiaclaimsnotclinicalfacts. Genericretinafocusfront/backminus/plusDIAGRAM,notdiagnosis/prescription.

New26passed2.48s;Physics/Biology **814passed/2PGskipped142.08s**. ActualisolatedlocalPG16 **1passed69.91s**,222lesson/import/reimport/2220XP/replay/legacy137XP3streak2stars. FlutterPhysics24passed57s201public9FRQ320px/200%,signedvirtualf/inversemeanF drafts. All602originalsourcechecksPASS. Previousfull1296backend/150Flutter/analyzeNoissues1.6salohida;newfull/Android/TCP222/newwebbuild/independentexpert/prodnotrun.

**222/316;94qolgan**:6:61/61,7:46/46,8:60/60,9:55/59,10:0/45,11:0/45. Jami958karta/491formula/241namuna/1552topshiriq/556FRQ,436families. Keyingi **9§56«Masalalar yechish»,PDF/bosma156**. §56–59original156–160/164–167andOCRread,JSONhaliyo‘q.56camera/microscope/abstracttwo-conjugateopticalmodelonly,source157nearreadingaloneNOTpersonalprescription;57W/m2powerdensitynotannualenergy,Parkentbookhistorynotcurrentcertificate,58mechanical/EM/quantumhistoricalmodelscopeNOTonly2fundamentalforces;59printingfirst19C/broken32/37refsnotcopied. No forcedformula57–59. Biology406/frozen6–8/old9/Web/Kimyo/prod/AIExplain saqlandi;tasdiqkutilmaydi.


## 9-sinf §56–59 va sinfning yakuniy tekshiruvi — 2026-10-26

4 dars: 16 karta, 4 formula yozuvi, 4 namuna, 26 topshiriq (18 MCQ, 4 tartiblash, 4 FRQ). §56 PDF/bosma156–157, §57 157–159, §58 159–160, §59 164–167. Kamera tasvirining balandlik modullari va berilgan optik model; shaxsiy ko‘z retsepti chiqarilmaydi. §57–59 konseptual: sun’iy formula qo‘shilmagan. W/m² quvvat/yuzadir; Parkent va muassasalar sanalari kitobdagi tarixiy ma’lumot sifatida, hozirgi holat sertifikati sifatida emas. Tarixiy dunyoqarashlar zamonaviy barcha kuchlar ro‘yxati deb berilmaydi. Asl manbadagi eskirgan yoki noaniq da’volar SOURCE_REVIEW.md va batch review’da qayd etilgan.

9-sinf jami59/59:271 karta,202 formula yozuvi,61 namuna,461 topshiriq,205 FRQ,6 raqamli laboratoriya va2 raqamli amaliyot. Raqamli mashg‘ulot real tajriba bajarilganini anglatmaydi. Barcha sinflar jami226/316,90 qolgan;974 karta/495 formula/245 namuna/1578 topshiriq/560 FRQ/438 qoida oilasi. Asl PDF/native/OCR/rasm auditi610 tekshiruv,583 noyob sahifa.

Yangi16 test passed9.89s. To‘liq backend1408passed/4opt-in PGskipped/13oldwarnings406.36s. Haqiqiy alohida lokalPG16 ikkala sinovi2passed85.08s: migratsiya,226dars import/reimport,2260XP,replay,parallel birinchi mukofot va eski137XP/3streak/2stars saqlandi. To‘liq Flutter150passed76s;analyzeNoissues2.1s;205 public grade9 FRQ draft320px/200% sinovidan o‘tdi. ActualTCP226/nativeAndroid/yangiwebbuild/mustaqilekspert/prod bajarilmadi.

Keyingi **10-sinf §1 «Fizikaning tadqiqot metodlari», PDF4/bosma3**. Birinchi besh mavzuning PDF4–17 asl tasvirlari va native matnlari o‘qilgan; grade10 kontenti hali yaratilmagan. PDF raqami bosma sahifadan1oldinda. Signed a/epsilon jadvalidagi double-minus va nazariy modellarning qo‘llanish chegaralari keyingi mualliflikda aniq saqlansin. Biology406, frozen6–8/old9 JSON, Flutter brendi/Ilmo, web, Kimyo va production saqlandi. Oraliq tasdiq talab qilinmaydi; 316/316 hali tugamagan.


## 10-sinf §1–5 — 2026-10-26

**2026-10-26 — Fizika 10-sinf §1–5:** **231/316, 85 qolgan**;6–9 to‘liq,10:5/45. Yangi24karta/20formula/6namuna/43topshiriq/20FRQ. Jami998karta/515formula/251namuna/1621topshiriq/580FRQ,451qoida oilasi.624asl sahifa tekshiruvi/597noyob. Physics/Biology1342passed/2opt-in PGskipped280.85s;actual localPG1passed76.68s231dars/2310XP/replay/legacy. FlutterPhysics26passed61s,20public10FRQ320px/200%,analyzeNoissues1.8s. Signed koordinata/omega/beta va yangi rad/s² birlik tekshiruvi;old6–9JSON/Biology406/Web/Kimyo/prod/AIExplain saqlandi. Keyingi **10§6PDF17/bosma16**,§6–10original17–25/29–36ko‘rildi,JSONhaliyo‘q. NativeAndroid/mustaqilekspert/ommaviyrelease bajarilmagan.

Har mavzu manbasi:§1PDF4–5/bosma3–4;§2PDF6–8/bosma5–7;§3PDF8–11/bosma7–10;§4PDF11–14/bosma10–13;§5PDF15–17/bosma14–16. WholePDF/native-text/formula/indeks/rasm14sahifa qayta tekshirildi; manba xeshi saqlandi. §1konseptual, sun’iyformula/FRQyo‘q. Yangi13qoida,7mavjud qoida qayta ishlatildi;eski qoida shartlari o‘zgarmadi. x koordinata/path farqi,signed v/a/omega/beta,cho‘qqida gnonzero,sameheightreturn,noair va sirpanmasmusbatmodul/butuntishlar shartlari aniq. No arbitrarytrig/CAS/LLM.

Dastlab yangi sinovlarda eski formula allowlistiga kirmagan `v0*t+g*t*t/2` test alternativi va `calculation_value` soniga tuple kutgan test topildi. Production allowlist susaytirilmadi: mustaqil literal oracle eski ruxsatli alternativga, test esa amaldagi sonli return kontraktiga tuzatildi.48yangi test qayta passed5.82s; Ruff va diffchecktoza. BarchaPhysics/Biology1342passed/2PGskip280.85s. Bu to‘liq backend emas; oldingi9yakuniyfull1408/Flutter150alohida. PG231lesson2310XP/immutableimport/replay/legacy va Flutter26/analyze amalda o‘tdi.

Keyingi10§6–10 asl manba ko‘rildi. PDF17originhnoaniqligi/signedvy,PDF21range dependsbothcomponents/45°scope,PDF25exercise8printed300rpmvs1000calculation,PDF31balanceonly2forces/thirdlawdifferentbodies,PDF35Fi sign inconsistency keyingiSOURCE_REVIEWga yozilsin. Local/testonly. Tasdiq kutilmaydi;316hali to‘liqemas.


## 10-sinf §6–10 — 2026-10-26

**2026-10-26 — Fizika 10-sinf §6–10:** **236/316, 80 qolgan**;6–9 to‘liq,10:10/45. Yangi23karta/19formula/5namuna/40topshiriq/19FRQ va1raqamli laboratoriya. Jami1021karta/534formula/256namuna/1661topshiriq/599FRQ,465qoida oilasi.641asl sahifa tekshiruvi/613noyob. To‘liq backend1505passed/4opt-in PGskipped/13mavjudwarning427.08s;actual localPG1passed90.43s236dars/2360XP/replay/legacy. To‘liqFlutter152passed83s,39public10FRQ320px/200%,analyzeNoissues2.2s. Ishorali noinersial kuch Fi=−mA,exact-root flighttime,sameheight/45°/sin-cosdata cheklovlari tekshirildi. Keyingi **10§11PDF36/bosma35**;§11–15original36–45/48–53o‘qildi,JSONhaliyo‘q,ilmiytafovutlar GRADE10_NEXT_REVIEW.md’da. Biology406/Web/Kimyo/prod/AIExplain saqlandi;nativeAndroid/mustaqilekspert/release bajarilmagan.

Manbalar:§6PDF17–19/bosma16–18;§7PDF19–22/bosma18–21;§8PDF23–25/bosma22–24;§9PDF29–32/bosma28–31;§10PDF33–36/bosma32–35.17asl sahifa tekshirildi.23karta/19formula/5namuna/40topshiriq(16MCQ+5ordering+19FRQ).14yangi formula oilasi;5mavjud qoida qayta ishlatildi. Eski darsJSON/reviewlar o‘zgarmagan.

Yer y0 va boshlang‘ich h, signedvy vsmodul,ikkita tarkibga bir xil vaqt,egri yo‘l vsmasofa;exact sqrt(3)1.73s/0.01sgrid;sinA/cosA tayyor dimensionlessdata va exactunitcirclepair;45° faqatnoair/sameheight/fixedv0. Digital lab faqatconditionaljadval/o‘rtacha,real tajriba emas. NewtonF net,thirdlawdifferentbodies,sharedsameforcecombinedmasses;nonrotatingtranslatingframeFi=-mA/ar=F/m-A,source35inconsistent2.4ni2.3vaNewtonbalansi bilan tekshirish. Qo‘llanish doirasi va source errata SOURCE_REVIEW.md/batchreviewda. AIExplain/trigCAS/rotatingframesolverqo‘shilmadi.

97testpassed7.99s =48oldbatch1+49newbatch2;Ruff va diffchecktoza. Fullbackend1505passed/4opt-inPGskipped/13mavjudwarnings427.08s;4skip natijasini actualPGsinovi bilan aralashtirmang. ActualisolatedPG16fullcourse1passed90.43s236lessonimmutableimport/reimport/2360XP/replay/legacy137XP3streak2stars. FullFlutter152passed83s,39public10FRQ/205old9FRQ320px200%,analyzeNoissues2.2s. All641originalsourcechecksPASS/613unique. YangiTCP236/nativeAndroid/independentexpert/prodpublication/webbuildqilinmadi.

Keyingi10§11«Gravitatsion maydonda harakat»PDF36/bosma35. §11–15 asl16sahifa o‘qildi va nativeSHA mos; hali dars emas. GRADE10_NEXT_REVIEW.md radius-vs-height/centripetalweight/contact/static-vs-kineticfriction/Atwood/mexanikenergiyascope/inclineworkuniterratahaqida. Mualliflik/test keyingi, tasdiqkutilmaydi. 316/316 vazifa hali tugamagan;80qoldi(10:35,11:45).


## 10-sinf §11–15 — 2026-10-26

**2026-10-26 — Fizika 10-sinf §11–15:** **241/316,75 qolgan**;6–9 to‘liq,10:15/45. Yangi22karta/20formula/5namuna/40topshiriq/20FRQ,1raqamli FIKlab. Jami1043karta/554formula/261namuna/1701topshiriq/619FRQ,474qoida oilasi.657asl sahifa tekshiruvi/628noyob. Physics/Biology1445passed/2opt-in PGskipped282.66s;actual localPG1passed80.50s241dars/2410XP/replay/legacy. FlutterPhysics26passed66s59public10FRQ320px/200%,analyzeNoissues1.7s. Localg/orbit radiusvsheight,contactweight/staticvskinetic/Atwood/signedwork/FIKexactfraction tekshirildi. Keyingi **10§16PDF54/bosma53**;§16–20original54–57/60–72o‘qildi,JSONhaliyo‘q. Biology406/Web/Kimyo/prod/AIExplain saqlandi;nativeAndroid/mustaqilekspert/release bajarilmagan.

Manbalar:§11PDF36–38/bosma35–37;§12PDF38–41/bosma37–40;§13PDF41–45/bosma40–44;§14PDF48–52/bosma47–51;§15PDF52–53/bosma51–52.16asl sahifa;22karta/20formula/5namuna/40topshiriq(15MCQ+5ordering+20FRQ).9yangi qoida oilasi va11mavjud qoidani qayta ishlatish. Ko‘rib chiqilgan h/r va3.9missingh tafovutlari SOURCE_REVIEW.md/batchreviewda; oldingi JSONvaoldruleunchanged.

Orbitalg LOCAL,rCENTER,h=r-R;T1radiusratioonlysamecentralfield. P tayanchmoduli gravitatsionmg/massadanfarqli,contacta<=g,up/downACCELnotvelocity. Staticfrictionnotalwaysmax,slidingexplicitmu_k,idealAtwoodbothNewtonbalances. Ish Fpr*s va gravityworkSIGNED,mexanikEvsfullenergy/konservativscope. Rampconstantvelocity/parallelpull/kineticmu,cotdata,exact8/11and2/3percentgrid;digitalFIKlabnotphysicalmeasurements. No independentexpertclaim.

54newpassed3.33s;allPhysics/Biology1445passed/2PGopt-inskipped282.66s. ActualisolatedlocalPG16course1passed80.50s:241lesson/reimport/2410XP/replay/legacy137XP3streak2stars. FlutterPhysics26passed66s59public10FRQ/320px200%,analyzeNoissues1.7s. All657originalchecksPASS/628unique. Previousfullbackend1505/Flutter152from§6–10alohida,samecurrentsafeappcode;newfull/TCP241/nativeAndroid/expert/prodnotrun. Gitdocsfirstattemptwrongcwd failedbeforewrites,rerunexplicitbackendpaths;Flutterwebsitecodewasnotmodified.

**241/316;75qolgan** (10:30,11:45). Keyingi10§16PDF54/bosma53. §16–20original17pages54–57/60–72/nativehashimagesread;contentnotauthored. GRADE10_NEXT_REVIEW.md sourceenergy/signedwork/ropeangle/leverarm/torquetypo/centrifugalcontactgeometry/Bernoulliscope/pistonanswererrata saqlandi. Keyingiagent xavfsiz mualliflikni shu yerdan davom ettirsin,oldcontentni qayta yaratmasin. Intermediateapprovalnotrequired;publication/localtestonly. Biology406/old6–9/Web/Kimyo/prod/AIExplainsaqlandi.


## 10-sinf §16–20 — 2026-10-26

**2026-10-26 — Fizika 10-sinf §16–20:** **246/316,70 qolgan**;6–9 to‘liq,10:20/45,11:0/45. Yangi21karta/19formula/5namuna/41topshiriq/19FRQ. Jami1064karta/573formula/266namuna/1742topshiriq/638FRQ,488qoida oilasi.674asl sahifa tekshiruvi/645noyob. Physics/Biology1497passed/2opt-in PGskipped281.33s;actual localPG1passed80.83s246dars/2460XP/replay/legacy. FlutterPhysics26passed67s78public10FRQ320px/200%,analyzeNoissues1.9s. Elasticmomentum/energy,verticalropeangle,signedmoment/zeroarm,inside-vs-convexcontact,Bernoulliscope/exactsqrt5tekshirildi. Keyingi **10§21PDF72/bosma71**;§21–25original72–75/79–91o‘qildi,JSONhaliyo‘q. Biology406/Web/Kimyo/prod/AIExplain saqlandi;nativeAndroid/mustaqilekspert/release bajarilmagan.

Source:§16PDF54–57/bosma53–56;§17PDF60–63/bosma59–62;§18PDF63–66/bosma62–65;§19PDF66–68/bosma65–67;§20PDF69–72/bosma68–71.17asl sahifa,21karta/19formula/5namuna/41topshiriq(17MCQ+5ordering+19FRQ).14yangi formula oilasi,5mavjud qoida qayta ishlatildi. Alloriginal674checks/645unique.

Izolyatsiyalangan1Delastic signedu1/u2/impuls+K balance,inelasticlossvsdeltaK;source7.8m/s/GJ va signerrsnotcopied. Static/rigidtorque/masscentre,ropephiFROMVERTICALvsmutualangle,ta’sirchizig‘igacha leverarm,clockwisepositivetorque/coupleF*d/supportingipsegmentsinteger. Zeroarmisvalidoldmoment0;initialbadtestexpectedrejectfixedtoNEGATIVEarm andexplicitzerotest,oldruntimeunchanged. Insideverticalhoopvsoutsideconvexnormalgeometry/contactdomains,N0boundaryRmaxnotuniversalexactequality. Continuity/idealsteadyincompressible/no-pump Bernoulli/samepressure-reference/height;pressure-differenceSIGNEDvsabsolutep2nonnegative. Pistonexactroot5/final.01m/sgrid. Manbada yo‘q M=I*beta/generaltrig/CAS/AIExplainyo‘q.

52newpassed3.36s;allPhysics/Biology1497passed/2opt-inPGskipped281.33s. IsolatedactualPG16course1passed80.83s246lesson/import/reimport/2460XP/replay/legacy137XP3streak2stars. FlutterPhysics26passed67s78public10FRQ/320px200%,analyzeNoissues1.9s. Previousfullbackend1505/Flutter152at§6–10alohida;newfull/TCP246/nativeAndroid/webbuild/independentexpert/prodnotrun. Ruff/diffchecktoza. Old6–9/BiologyJSON/reviewsbyteunchanged;websitecleanuntouched.

**246/316,70qolgan:**6:61/61,7:46/46,8:60/60,9:59/59,10:20/45,11:0/45. Jami1064cards/573formulaentries/266examples/1742assessments/638FRQ/488families. Keyingi **10§21 «Harakatlanayotgan gazlar va suyuqliklarda bosimning tezlikka bog‘liqligidan texnikada foydalanish»,PDF72/bosma71**. §21–25original17pages72–75/79–91/nativeSHA/imagesread,contentnotauthored. GRADE10_NEXT_REVIEW.md equal-transit-wingmyth/Torricelli/signedharmonicacceleration/staticx0vsincrement/1/2nativeOCRloss/smallanglependulum/digitalg/resonancescope qaydlarini saqlaydi. Piapprox/finitesin-cosdata/exactrootrubrics talab qilinadi,source25conceptualnoforcednumeric. Keyingi bosqich uchun yangi approvalso‘ralmasin;manba qayta solishtirilib originaldarslar yozilsin. 316/316 hali tugamagan,publicationlocaltestonly;Biology406/Kimyo/Web/prod/AIExplain saqlandi.


## 10-sinf §21–25 — 2026-10-26

**2026-10-26 — Fizika 10-sinf §21–25:** **251/316 bo‘lim, 65 qolgan**. 6–9-sinflar to‘liq; 10-sinf25/45, 11-sinf0/45. Yangi21karta/19formula/5namuna/41topshiriq/19FRQ; jami1085karta/592formula/271namuna/1783topshiriq/657FRQ,501qoida oilasi. Asl691sahifa tekshiruvi/661noyob. Physics/Biology1542passed/2opt-inPGskipped299.26s; haqiqiy lokalPG1passed88.58s (251dars/2510XP/replay/legacy). FlutterPhysics26passed74s (97public10FRQ,320px/200%),analyzeNoissues1.7s; yangi45test3.24s. Torrichelli,ishorali garmonik tezlanish,prujina/mayatnik va raqamli g tekshirildi. Keyingi **10§26PDF91/bosma90**. Biology406/veb/Kimyo/production saqlandi; nativeAndroid va mustaqil ekspert tekshiruvi bajarilmagan; local/testpreview only.

Manbalar: §21 PDF72–75/bosma71–74; §22 PDF79–82/78–81; §23 PDF82–86/81–85; §24 PDF86–87/85–86; §25 PDF87–91/86–90.17originalsahifa.13yangi finite formula oilasi,6mavjud qoida qayta ishlatildi. §25konseptual: sun’iy hisob/formula qo‘shilmadi. §24shartli raqamli laboratoriya, haqiqiy o‘lchov bajarildi deyilmaydi.

Manba tafovutlari: equal-transit-time qanot afsonasi takrorlanmadi; idealTorrichelli chuqurligi H−h, kattaidish/kichikteshik/samepressure shartlari aniq. x=A*sin(theta) bo‘lsa a=−omega²*x; PDF81cos xsin bilan mos emas. PDF82A.05/vmax.12/x.03 uchun a−.1728m/s², amax.288m/s²; bosilgan−.073vaamaxm/s noto‘g‘ri. Statik prujinada mg−k*x0=0, tebranishx muvozanatdan inkrement; manba5.11to‘liqbalans emas. PDF84aslenergiyada1/2bor, nativeOCRyo‘qotishi kitobxatosi emas. Kichikburchak/pivotCOM, p3.14 ochiq; amplitudalar/reversalfazalar izchil. Sin/cosPhase tayyor[-1,1] ma’lumot, umumiy trigsolver yo‘q. Rezonans barqaror/kichikso‘nish scope; avtotebranish manbali, perpetualmotion emas.

45yangi test3.24s; Physics/Biology1542passed/2opt-inPGskipped299.26s. PostgreSQL16izolyatsiyalangan1passed88.58s:251dars/import/reimport/2510XP/replay, eski137XP/3streak/2stars saqlandi. Flutter26passed74s/97public10FRQ320px200%, analyzeNoissues1.7s. 691aslPDFpagecheck/661unique. Ruff/diffcheck o‘tdi. Oldingi fullbackend1505/fullFlutter152 alohida tarixiy natija; bu partiyada yangi fullsuite/TCP251/webbuild/nativeAndroid/expert/prod bajarilmadi. EskiPhysics/BiologyJSON/review byteunchanged.

Keyingi: 10§26«Mexanik to‘lqinlarning muhitlarda tarqalishi…», PDF91/bosma90. §26–30 manba tayyorgarligi ketmoqda; interaktiv kontenti hali yozilmagan. Ruxsat qayta so‘ralmasin; tekshirilmagan kontentni tayyor demang.


## 10-sinf §26–30 — 2026-10-26

**2026-10-26 — Fizika 10-sinf §26–30:** **256/316 bo‘lim, 60 qolgan**. 6–9 to‘liq;10:30/45,11:0/45. Yangi25karta/20formula/5namuna/45topshiriq/20FRQ. Jami1110karta/612formula/276namuna/1828topshiriq/677FRQ,508qoida oilasi. Asl715sahifa tekshiruvi/684noyob. Physics/Biology1597passed/2opt-inPGskipped323.64s; actual localPG1passed89.53s256dars/2560XP/replay/legacy. FlutterPhysics26passed72s117public10FRQ320px200%,analyzeNoissues1.6s;55yangi test4.20s. Mexanik to‘lqin,tarang ip,signed termodinamika/Karno va signed elektr superpozitsiyasi tekshirildi. Keyingi **10§31PDF119/bosma118**. Biology406/veb/Kimyo/production saqlandi; Android/ekspert/release bajarilmagan,localpreview only.

Manbalar:§26PDF91–96/bosma90–95;§27PDF99–102/98–101;§28PDF103–106/102–105;§29PDF107–112/106–111;§30PDF115–118/114–117.24asl sahifa tasvirlari/nativehash solishtirildi.7yangi finite oilasi,13mavjud formula qayta ishlatildi;20mustaqil literal numeric oracle.

PDF91,92,93,94,95,96: Original text and page images checked. Mechanical waves require a medium; transverse/longitudinal directions distinguish particle oscillation from propagation. Wavelength nearest SAME-phase spacing, not amplitude; Lw is the explicit ASCII input alias for lambda (Python reserved word is not accepted by safe formula parser). Taut uniform string small-wave v=sqrt(F*l/m), mass/length same segment. Bulk shear-wave scope does not rule out water surface waves; E/rho rod approximation not universal solid speed or universal factor2. Hearing limits approximate; ultrasound use conceptual only, not clinical claims/instructions. Original questions, not textbook question copying.

PDF99,100,101,102: Original text/images checked. Reversible restoration includes surroundings, internal energy state function vs bulk energy. Signed Q_to/A_by/A_on explicitly retained using four existing first-law families. U zero reference is not a physical all-energy-zero claim. Kelvin-Planck statement requires CYCLIC single reservoir/no other change; source102 unconditional all-process wording not copied. No perpetual motion or new unsupported entropy formulas.

PDF103,104,105,106: Original diagrams/formulas checked. Adiabatic Q0 not isothermal nor any fast process exact; A_by=-DU. Source104 wording about Q decreasing along adiabatic not copied: no heat exchange. Cycle DU0, received/rejected heat positive magnitudes, net work vs expansion. Four reversible Carnot stages ordered. Kelvin ratios and reversible two-reservoir upper bound, not arbitrary real engine equality; existing finite thermodynamic families reused.

PDF107,108,109,110,111,112: Original images checked. Four-stroke ideal approximations vs actual engines; diesel compressed air then injected fuel. Historical book FIK/emissions/global-car totals not current universal facts. Chimney dispersal does not remove pollutant. Source111 compression work4.8J is MAGNITUDE (signed A_by negative). Original givens avoid copying worked question. Source112exercise7 Th117C/Tc21C with stated school273 conversion yields eta96/390~24.6%, Qc~45.23kJ, P~14.77kW, inconsistent printed23%/146kJ/14kW not used as answer key.

PDF115,116,117,118: Original formula/image checked. Closed total charge ALGEBRAIC signed sum; field vector positive-test convention; point E=k*|q|/r². Source118 printed worked answer750N/C loses fourth powers under root:4nC,distances.08/.06m,orthogonal E1=5625,E2=10000,result=sqrt(131640625)~11473.47N/C; source diagram incorrectly labels q2>0 despite opposite-charge givens. Error documented, original 3k/4k->5k component exercise independent. Same-point/same-axis signed sum and PERPENDICULAR-only norm families, no arbitrary-angle/trig/CAS. Old unsigned field_point contract preserved.

55yangi test4.20s; umumiyPhysics/Biology1597passed/2PGopt-inSkipped323.64s. Actual isolatedPG16:1passed89.53s256dars/reimport/2560XP/replay/old137XP3streak2stars. Flutter26passed72s117publicgrade10FRQ320px200%;analyzeNoissues1.6s. Ruff/diffchecktoza. Old6–9/Biology content/reviewsunchanged; webuntouched. Fullbackend1505/fullFlutter152 oldcheckpointonly; yangiTCP256/nativeAndroid/webbuild/expert/prodnotrun.

Keyingi10§31PDF119/bosma118;§31–35ning16asl sahifasi tasvir/nativehashlari o‘qildi,private tayyorgarlik bor,interactivebatch7/runtimehaliyo‘q. Manba125fieldworkindexsign va129answerkeys tafovutlari keyingi reviewda izchil yozilsin. Ordinaryapproval qayta so‘ralmasin.



## 10-sinf §31–35 — 2026-10-26

**2026-10-26 — Fizika 10-sinf §31–35: 261/316 bo‘lim, 55 qolgan.** 6–9-sinflar to‘liq; 10-sinf35/45, 11-sinf0/45. Jami1135karta/631formula/281namuna/1872topshiriq/696FRQ,524qoida oilasi. Asl731sahifa tekshiruvi/700noyob. Backend1774passed/4opt-inPGskipped/2sandboxdeselected/13warnings414.78s; actualPG1passed96.12s (261dars/2610XP/replay/legacy). FlutterFULL152passed85s,analyzeNoissues2.0s; yangi65test4.60s. Keyingi **10§36PDF137/bosma136**. Production/veb/Biology406/Kimyo saqlandi; nativeAndroid va ekspert tekshiruvi bajarilmagan, localpreview only.

Yangi 25 karta,19formula,5originalnamuna,44topshiriq (20MCQ+5ordering+19FRQ).16yangi finite formula oilasi,3mavjud qoida qayta ishlatildi. Manbalar:§31PDF119–121/bosma118–120;§32PDF121–123/120–122;§33PDF124–126/123–125;§34PDF126–129/125–128;§35PDF133–137/132–136.16asl sahifa nativehash/tasvir bilan tekshirildi.

PDF119,120,121: Native hashes and original images checked. Isolated conducting sphere in electrostatic equilibrium: interior E0, exterior radial point-charge magnitude at distance from CENTRE, just-outside surface r=R. Not uniformly volume-charged insulating sphere. Dielectric E0/eps for fixed free charges/homogeneous linear model, not fixed-voltage universal reduction. eps dimensionless>=1. Field strength vs dielectric polarization distinct.

PDF121,122,123: Original formulas/images checked. Signed potential zero at infinity, phi=k*q/(eps*r), potential energy qTest*phi signed, potential independent of test charge. Source121 statement that field always resists bringing a test charge is false for opposite sign: attraction/repulsion distinguished. Source122 W_-q/q notation not copied as sign convention; use explicit SIGNED test charge. Equipotentials are 3D surfaces, circles are section. Source123 E=(phi1-phi2)/d is uniform field/component along oriented displacement ONLY, not arbitrary point-field finite difference. Conducting sphere interior phi same as surface but E0, r measured from centre; source30nC/5cm worked values5400/2700V consistent.

PDF124,125,126: Original images checked. Electrostatic field work q*(phi_initial-phi_final)=W_initial-W_final=-DeltaW, path independent/static field and fixed endpoints. Source125 E*dx=phi2-phi1 and A=q(U2-U1) wording/sign convention conflicts source122; retain named INITIAL/FINAL and standard negative-gradient sign. Along-axis displacement SIGNED, q signed, cosPhi bounded[-1,1] only provided value, no general trig. Conservative field closed-loop work0 not nonconservative induction generalization.

PDF126,127,128,129: Original all1/2 coefficients and cap qoneplate/Ubetweenplates checked. Constant linearC/quasistaticcharging fromzero: W=qU/2=CU²/2=q²/(2C), isolatedconductor phi referencedinfinity. Fieldenergy w=eps0*eps*E²/2 in homogeneous LINEAR ideal parallelplate model, edgeeffects ignored. Generaldielectric/nonlinear/fixedCallconditionsnotassumed. Source129exercise5 midpoint +.4uC/-.6uC at.06m gives -30000V not -30V;exercise10 q2uC/W.5uJ gives4uF not16uF; keys not copied. Source128W/m³ vs J/m³ correctly energy density J/m³. Capacitorleakage not instantallidealmodels; no physical charging task.

PDF133,134,135,136,137: Original images/native checked. Conductance gamma=1/R in S vs material conductivity S/m. Ohm I=G*U only fixed-temperature ohmic element. Source134 copper8.4e23m^-3 is not accepted as verified general concentration (typical free-electron model order10^28), no claim copied. Classical ballistic t/2 drift derivation only textbook simplified model, not universal collision-time factor. Transport current I=n*e*S*vdrift with supplied conditional n/e, e positive modulus1.6e-19, conventional current opposite electron drift. Source136 graph verticalU horizontalI slope R, not conductance. Material conductivity depends conditions; no DIY mains or clinical-water-quality claims.

Runtime: services/assessment_grading.py da faqat explicit S/mS, J/m3/mJ/m3/µJ/m3 va N/Cga teng V/m/kV/m birliklari qo‘shildi. S siemens va s sekund farqi saqlandi; umumiy unit-expression parser/eval yo‘q. Signed potensial/energiya/ish, metall shar r/R domainlari, constant-linearC1/2, ideal dielectric energy density va conventional electron drift tekshirildi. Mavjud MCQ, unsigned eski fieldwork/field_point oilalari o‘zgarmadi. Javob/rubrikalar public fixturega chiqmaydi.

65yangi test4.60s. Backend suite (ikki o‘zgarmagan sandbox testi tashqari):1774passed,4opt-inPGskipped,2deselected,13mavjudwarning,414.78s. /var/tmp to‘liq suite boshlash avtomatik approval-review xizmatining usage limitida bajarilmadi; bu unsafe determination emas. Ruxsatli /tmpdagi muqobil run ikki sandbox/private-Gitguard testini ajratdi, kod/guard yumshatilmadi. Ushbu ikki test oxirgi batch6 Physics/Biology1597 runida o‘tgan; joriy7da qayta o‘tdi deyilmaydi. Boshqa barcha testlar (auth/security/Biology/Physics) bajarildi. Actual isolated localPG16:1passed96.12s,261lesson/import/reimport/2610XP/replay/legacy137XP3streak2stars. FullFlutter152passed85s,136public10FRQ320px200%;analyzeNoissues2.0s. Originalaudit731checks/700unique. Ruff o‘tdi; oldingi docsdagi trailing blank line shu checkpointda tuzatildi, gitdiffcheck toza. NativeAndroid/TCP261/webbuild/independentexpert/productionnotrun.

Keyingi **10§36PDF137/bosma136**. §36–40ning13asl sahifasi o‘qildi; shunt m vs n+1, parallel source limits va digital source lab review xulosalari tayyor. Keyingi darslar hozircha private draft, runtime7 checkpointdan keyin qo‘shiladi. 316/316 tugamagan; odatiy ish uchun approval qayta so‘ralmasin.


## 10-sinf §36–40 — 2026-10-26

**2026-10-26 — Fizika 10-sinf §36–40: 266/316 bo‘lim, 50 qolgan.** 6–9 to‘liq;10:40/45,11:0/45. Jami1160karta/649formula/286namuna/1915topshiriq/714FRQ,540qoida oilasi. Asl744sahifa tekshiruvi/712noyob. Physics/Biology1716passed/2PGopt-inskipped/2sandboxdeselected297.45s;actualPG1passed94.47s266dars/2660XP/replay/legacy. FlutterPhysics26passed76s154public10FRQ320px200%,analyzeNoissues1.9s;56yangi test4.22s. Keyingi **10§41PDF153/bosma152**. Biology406/veb/Kimyo/prod saqlandi, Android/ekspert/release bajarilmagan; localpreview only.

Yangi25karta/18formula/5namuna/43topshiriq(20MCQ+5ordering+18FRQ).16yangi qoida oilasi,2mavjud qoida qayta ishlatildi. Manbalar:§36PDF137–139/bosma136–138;§37PDF139–142/138–141;§38PDF142–145/141–144;§39PDF146–148/145–147;§40PDF148–149/147–148.13originalsahifa.

PDF137,138,139: Original images/native hashes checked. Current magnitude q/t, density I/S for area perpendicular to uniform current, vector direction conventional positive-charge flow; carrier density times drift speed distinct random speed. Circular S=pD²/4, Ddiameter,p3.14 explicitly approximate. No copying source138 household wire current ratings as wiring guidance/universal safe values. Thermal/magnetic/chemical effects conceptual by media, not all currents deposit ions.

PDF139,140,141,142: Original images checked. EMF non-electrostatic work per positive charge in VOLTS, not newton force. Constant ideal EMF+series internal ohmic resistance model DISCHARGING into passive R: I=Emf/(R+r),terminalU=IR,eta=R/(R+r). Open-circuitUapproximatelyEmf for negligible voltmeter load; no charging-mode universal U<=Emf claim. Short circuit explanation only; no physical test or optimization endorsement. R/r nonnegative with total>0; efficiency/current examples positive resistances.

PDF142,143,144,145: Original diagrams checked. Kirchhoff signed conservation conceptual. Identical cells same orientation/integern: series netEmf=nEmf,rnet=nr;parallelEmf unchanged,rnet=r/n. Exact formulas used. Approx parallel n-times current requires R<<r/n, not merely R<<r at arbitrary n. Unequal same-polarity source model high-impedance voltmeter, weightedU=(E1*r2+E2*r1)/(r1+r2); signed loopI=(E2-E1)/(r1+r2) under stated direction. Source145 worked table pairs E1=2/r1=.6 and E2=1.5/r2=.4 yield1.7V but printed1.8 uses swapped resistance pairing; new conditional pairs explicit. No instruction to parallel real batteries.

PDF146,147,148: Original images/formulas checked. Source146 uses n=I/Ig then Ir/Ig=n and n+1 inconsistency. Define m=fullrange/originalrange consistently: shuntRs=Rg/(m-1),parallel; voltageRadd=Rg*(m-1),series. Calibration multiplier m, not source147 contradictory m+1. m>1 need not integer. Source147 sample Ig5A,Rg.12/Rs.04 gives20A correctly; new independent values. Modifications only abstract digital model, no mains meter construction.

PDF148,149: Original digital EMF/internal-resistance lab and conditional table source checked. No physicalmeasurementclaim. Negligible voltmeter current, openUapproximatelyEmf, closedUload; r=(Emf-Uload)/I and Emf=Uload+I*r, Emf>Uload>0/currentpositive. Source149exercise10 .8mA/Rg1k gives additional resistances2.75/17.75/92.75/186.5k rather than printed9/49/249/499k; not copied. Exercise11 printed100kA not used as credible galvanometer current. Data made conditional, no live circuit or shorting task.

Runtime yangi explicitcurrent_density A/m2/A/mm2/mA/mm2; SI area6orders. Conditional current-source/internalR/batterycount/meter-rangetopologies finite. ncellcountmusbatbutun,mrangefactor>1butnotintegerconstraint; mismatchsource signedcirculatingI. Exact8/3V private rational/0.01V rounding verified. Initialtwo newtest assertions wrong feedbacknames and nongrid999999mV corrected to stable rounding_requirement/999990mV; runtime grader unchanged. Digital lab physicalfalse.

56newpassed4.22s; Physics/Biology1716passed/2PGskipped/2sandboxdeselected297.45s. Same two unchanged sandbox/private-Gitguard tests remain excluded because /var/tmp approvalservice quota unavailable; no bypass/guard change. Actual isolated localPG16 1passed94.47s266lesson/reimport/2660XP/replay/legacy137XP3streak2stars. FlutterPhysics26passed76s154publicFRQ320px200%,analyzeNoissues1.9s. Earlier fullbackend1774/fullFlutter152 at§31–35 separate; newfull/TCP266/webbuild/nativeAndroid/expert/prod notrun. Ruff/diffcheck passed. 744originalpagechecks/712unique; website/Biology/oldPhysicsJSON unchanged.

Keyingi10§41PDF153/bosma152;§41–45 original17pages153–169 native/text/images read. Private nextdraftready, not yet registered/runtime. Source vacuum pressure, phase-specific 3/2law, ordinary-metal temperature law, semiconductor carrier-count/current distinction and BJT base/emitter sign issues documented in nextreview. No formulas forced into conceptual§43–44. Ordinaryapprovalnotneeded; do notmark316done.


## 10-sinf §41–45 va sinf yakuni — 2026-10-26

**2026-10-26 — 10-sinf Fizika to‘liq: 45/45 bo‘lim. Jami 271/316, 45 qolgan.** 6–10-sinflar qamrab olingan; qolganlarning barchasi11-sinf. Jami1188karta/655formula/291namuna/1951topshiriq/721FRQ,545qoida oilasi. Asl761sahifa tekshiruvi/729noyob. Yakuniy Physics/Biology1749passed/2PGopt-inskipped/2sandboxdeselected295.81s;actualPG1passed94.56s271dars/2710XP/replay/legacy. FlutterPhysics26passed76s161public10FRQ320px200%,analyzeNoissues2.0s;33yangi test5.10s. Keyingi **11§1PDF5/bosma4**. Biology406/veb/Kimyo/production saqlandi. Localpreview only; Android/ekspert/release bajarilmagan.

Yangi28karta/6formula/5namuna/36topshiriq/7FRQ.5yangi finite oila,ohm_resistance bitta shartli nuqta uchun qayta ishlatildi. §43–44konseptual: sun’iy formula yoki sonli FRQ yo‘q. Manbalar:§41PDF153–155/bosma152–154;§42PDF155–158/154–157;§43PDF158–162/157–161;§44PDF162–166/161–165;§45PDF167–169/166–168.17asl sahifa.

PDF153,154,155: Original images/native hashes read. Vacuum conduction requires emitted electrons, not vacuum automatically/source153 p<<1e-13mmHg not universal necessary pressure copied. Cathode heating vs anode accelerating voltage distinguished. I=k*U^(3/2) only same-geometry/temp SPACE-CHARGE-LIMITED positive-bias regime, before saturation; current ratio sqrt((U2/U1)^3) cancels k, no fabricated k units. Saturation depends emission/temp, not universal I=U/R. No heating/vacuum DIY measurement claim.

PDF155,156,157,158: Original R/R0/rho formulas and coefficients checked. Linear approximate ordinary-metal law near specified reference with constant alpha; DT is temperature DIFFERENCE in K, not absolute Kelvin. Require positive modeled resistance/factor, signed cooling allowed, no extrapolation to superconducting/absolutezero regime. Source156 coefficient column labelled alpha degreesC is reciprocal unit1/K. Source157 zero/infinite resistance extrapolation is historical failed reasoning not asserted modern fact; mercury4.15K is historical reported approximate, no incomplete priority/BCStheory copied. Source158 sample early R0 rounding27 gives2518 while exact R0=30/1.1 gives~2488.89C schoolalpha.005, not publication answer key. Original modest-range givens avoid huge extrapolation. Source168Nickelin .0001 vs source156Nickel .0065 inconsistent, no guessed material value used.

PDF158,159,160,161,162: Original intrinsic/donor/acceptor diagrams read. Electron/hole transport distinguished; hole is missing valence electron effectivepositive carrier, not drifting actual positive ion. Intrinsic equal electron/hole concentrations does NOT imply equal currents without equal mobilities; source160 equal-conductivities and source169test4 electron1mA->total2mA not copied. n-type/p-type majority carriers do not imply whole doped crystal netnegative/positive. As5 donor inSi, In3 acceptor only supplied diagrams; no toxic doping task or edits to Chemistry branch. Semiconductor temperature/light trends bounded statedmodel, not allconditions/universal materials groupsIII–V only. No unsupported numeric formula forced.

PDF162,163,164,165,166: Original p-n depletion/forward/reverse/BJT/half-wave diagrams read. Depleted MOBILE carriers not absence of all fixed ion charge. Forward ppositive/nnegative, reverse opposite, smallreverse leakage allowed, not absolute all-bias zero. Bipolar transistor has emitter/base/collector,two junctions; emitterbase forward/collectorbase reverse in stated active mode. No invented beta/AC circuit formulas. Source165 emitter-base total current claimed much smaller than emitter-collector is misleading; small BASE branch controls larger collector circuit with external energy, not emitter current smaller than collector. Source165 allradioelement1nm/universal microchip historical claims not copied. Half-wave output pulsating unidirectional, not flatDC; no mains assembly task.

PDF167,168,169: Original diode lab curve axes and conditional data checked. DIGITAL only no physical experiment/36–42V instructions. Ivertical in mA,UhorizontalV,reverse quadrant and forward bias scales distinct. Rpoint=|U|/|I| for supplied nonzero conditional point, not constant Ohmic diode/global differential resistance. Forward/reverse data explicitly hypothetical, not measured dots claimed. Source168question2 says whyreverse current flows, source163nearlyzero clarified smallleakage not contradiction forcedzero. Unsupported intrinsic-current-equality key not used. NoShockley/newAI explain or added semiconductor equation.

1/K vaK^-1 explicit temperatura koeffitsiyenti birligi qo‘shildi; signedDTfarq0°Ctayanch,positiveabsoluteT/positivefactors; arbitraryCelsius parser yoki all-regime superconducting extrapolation yo‘q. Space-chargeI2/I1 exactroot/scope; diode Rpoint=|U|/|I| onlystatedconditionalpoint, not globalOhmlaw.

33yangi test5.10s. Course validator eski8-sinfdagi bir xil emissiya savolini tutdi: yangi41savol faqat nomi almashtirilmadi, sovuqkatod/anod voltage mavjud-vakuumda tok yo‘qligini tushuntirish vaziyatiga qayta tuzildi. Keyin original source/renderreviewyangilandi. Dastlabki umumiy run1748passed/1failed/2skipped/2deselected306.91s: eski grade10batch1test tugallangan sinfda next46ni kutgan. To‘g‘ri terminalNone mezoniga yangilandi, all-courseAPItest grade10catalog45completed/grade_content_completetrue ni ham tekshiradi. Yakuniytakroriyrun **1749passed/2PGskipped/2sandboxdeselected295.81s**. Ikki unchanged sandbox testi approvalservice quota/syntheticGitmount sabab qayta bajarilmadi; eng oxirgi oldverifiedbatch6da o‘tgan. Guardkod/testyumshatish yo‘q. Actual localPG16 **1passed94.56s**271dars/reimport/2710XP/replay/legacy137XP3streak2stars. FlutterPhysics **26passed76s**,161public10FRQ320px/200%;analyzeNoissues2.0s. 761originalchecks/729unique. Ruff/diffchecko‘tdi. NativeAndroid, liveTCP271,newwebbuild, independentexpert,productionbajarilmagan.

10-sinf yakuni45/45; source mapping records tartibi takrorlanmaydi va har bir xususiy javob literaloracle/servergrading orqali o‘tadi. 6:61/61,7:46/46,8:60/60,9:59/59,10:45/45,11:0/45. Keyingi **11§1«Magnit maydon. Magnit maydonni tavsiflovchi kattaliklar»,PDF5/bosma4**.11§1–5original13pages5–17 nativehash/imagesread; privateauthoringdraft bor, hali runtimega qo‘shilmagan. Normalvsplaneangle/thincoilvslongsolenoid/mu0schoolapprox/source14answerfactor10/historicalamperedefinitionreview qaydlari tayyor. 316/316 hali tugamagan, odatiy ishga approval qayta so‘ralmasin.


## 11-sinf §1–5 — 2026-10-26

**2026-10-26 — Fizika 11-sinf §1–5: 276/316 bo‘lim, 40 qolgan.** 6–10-sinflar to‘liq;11-sinf5/45. Jami1213karta/667formula/296namuna/1983topshiriq/733FRQ,556qoida oilasi. Asl774sahifa tekshiruvi/742noyob. Backend1913passed/4PGopt-inskipped/2sandboxdeselected/13warnings456.07s;actualPG1passed109.55s276dars/2760XP/replay/legacy. FullFlutter154passed98s,analyzeNoissues1.8s;50yangi test3.64s. Keyingi **11§6PDF18/bosma17**. Physics localpreview only; Biology406/veb/Kimyo/prod saqlandi. Android/ekspert/release bajarilmagan.

Yangi25karta/12formula/5originalnamuna/32topshiriq(15MCQ+5ordering+12FRQ).11yangi finite oila,oldampere_force qayta ishlatildi. §1PDF5–8/bosma4–7;§2PDF8–10/7–9;§3PDF11–14/10–13;§4PDF14–15/13–14;§5PDF16–17/15–16.13originalnativehash/tasvir qayta tekshirildi.

PDF5,6,7,8: Original whole PDF SHA/pagecount and native/image pages checked. Magnetic induction vector T vs signed scalar flux Wb. Uniform B and flat oriented area Phi=B*S*cosAlpha, alpha angle with NORMAL not surface plane. Source7 worked wording angle to frame ambiguous, calculation uses normal60deg; new prompts explicitly normal/provided cosine. Closed field lines no monopole claim within school model; outside NtoS/inside return, not all lines start N endS. No false physical iron-filings experiment.

PDF8,9,10: Original couple/leverarm/currentloop diagram and M formulas checked. SINGLEloop M=BISsinAlpha, Nidenticalcoplanarturns multiplyN evidenced source10 worked example. alpha B vs loopNORMAL, maximum at90deg minimum0, opposite sideforces cancelnetF but nonzerocouple. Moment N*m vs energy J semantic distinction preserved. Source10 B1.25mT correct independent. No electric-motor physical experiment, no general inertia/trig solver.

PDF11,12,13,14: Original right-hand/BiotSavart/longwire/circularloop/coil formulas checked. Infinite straight thinwire B=mu0I/(2pid) dperpendicular fromaxis; circularcenter B=mu0I/(2R). Nturn formula mu0NI/(2R) only thin/coincident circular turns nearcommonplane, NOT longsolenoid universal despite source13longcoil picture. Same-point vectorcomponent sum, not all magnitudes sum. mu0=4p*1e-7 with p3.14 explicitly approximate input (modern SI mu0 not exactdefinedconstant). Source14 working1.25e-6T correct but final12.5e-6T inconsistent; no bad answerkey copied.

PDF14,15: Original Ampere work geometry checked. Straight current perpendicularB and motionparallelforce gives A=IBld; general provided sin between current/B when motion alongforce A=IBldsinAlpha. Iconstant,currentlooporientedflux relation A=I*DPhi with sign/orientation explicit. Energy from maintaining source, not free static magnetic field/contradiction to individual-charge Lorentz no work. No homemade electron gun or high-current experiment.

PDF16,17: Original two long parallel wires force and worked sample checked. Codirectional attraction/opposite repulsion under vacuum longthinwire model; force magnitude mu0I1I2l/(2pid), same per-selectedlength not arbitrary finiteendgeometry. Source17 2018 ampere two-wire definition is HISTORICAL, modern SI fixes elementary charge since2019; do not present olddefinition or exactmu0 as current release standard. Numeric givenmu0/p approximation explicitly stated, no real wire experiment.

Wb/mWb/µWb,N/A2 va mN*m/µN*m explicit birliklari qo‘shildi. J energiya va N*m moment eski semantik farqi saqlandi. Orientatsiyalangan oqim/DPhi/Bx signed,loopnormalangle/wholeturncount/shorthincoilvslongwire geometry va mu0/p schoolapprox checker bor. PublicDTO privateanswer/rulesiz. FlutterAPP kodi o‘zgarmadi: genericpreview yangi11catalog bilan ishlaydi; testmock/book/publicFRQfixture va yangi11selector/320px200%drafttest qo‘shildi. Legacy/mobileAPI Physics flagi/prod o‘zgarmadi.

50yangi test3.64s. Fullbackend (ikki unchanged sandbox testi tashqari):1913passed/4PGopt-inskipped/2deselected/13existingwarnings456.07s. Sandbox tempoutsideGitmount runapprovalservice quota unavailableoldblock saqlandi, chetlab o‘tilmadi; bu ikki guard oldbatch6da o‘tgan, joriyda qayta o‘tdi deyilmaydi. Actual isolatedPG16:1passed109.55s276lesson/import/reimport/2760XP/replay/legacy137XP3streak2stars. APIallcourse checks11book2018/id/available6–11, current5completed, sourcegradepartialhonesty, old9/10completion. FullFlutter154passed98s; analyzeNoissues1.8s,12public11FRQ signedflux/moment/draftunit320px200%. 774originalchecks/742unique. Ruff/diffcheckpassed. NewnativeAndroid/TCP276/webbuild/expert/prodnotrun. Biology406/otherPhysicsimmutableJSON/website/Chemistry unchanged.

6:61/61,7:46/46,8:60/60,9:59/59,10:45/45,11:5/45. Next **11§6Lorens kuchi,PDF18/bosma17**. §6–10original18pages18–22/27–39read; privateauthoringdraftready, notregistered/runtimeyet. Nonrelativisticradius/period, averageFaraday/Lenz, perturnfluxvslinkage,linearL/solenoid, relativepermeability<1allowed, unsaturatedmaterialscope, historicalmedicalclaimexcluded and sourceenergyanswererrors detailed in GRADE11_NEXT_REVIEW.md. Ordinaryapprovalnotneeded. 316/316 hali tugamagan.


## 11-sinf §6–10 — 2026-10-26

**2026-10-26 — Fizika 11-sinf §6–10: 281/316 bo‘lim, 35 qolgan.** 6–10 to‘liq;11:10/45. Jami1238karta/683formula/301namuna/2024topshiriq/749FRQ,572qoida oilasi. Asl792sahifa tekshiruvi/760noyob. Physics/Biology1855passed/2PGopt-inskipped/2sandboxdeselected340.28s;actualPG1passed109.81s281dars/2810XP/replay/legacy. FlutterPhysics28passed85s28public11FRQ320px200%,analyzeNoissues2.0s;56yangi test4.14s. Keyingi **11§11PDF43/bosma42**. Localtestpreviewonly; Biology406/veb/Kimyo/production saqlandi, Android/ekspert/release bajarilmagan.

Yangi25karta/16formula/5namuna/41topshiriq(20MCQ+5ordering+16FRQ).16yangi finite family. Manbalar:§6PDF18–22/bosma17–21;§7PDF27–30/26–29;§8PDF30–33/29–32;§9PDF33–35/32–34;§10PDF36–39/35–38.18asl sahifa/nativesha/imageschecked.

PDF18,19,20,21,22: Original images/native hashes checked. Lorentz magnetic force perpendicularv does no work; signedcharge reversesdirection while scalar formulas use MODULUS. Circular R=mv/(|q|B),T=2p*m/(|q|B) only uniform magneticfield/vperpendicularB/nonrelativistic; generalangle force |q|vBsinAlpha. New speeds low vs c, source8.4e7m/s example not asserted relativistically exact. Source21exercise1 radius4cm/B.5 gives2.512mWb not25.12; source22exercise15 v.12m/s*3s=.36m vs given.08m, answer.4A corresponds first, not copied. Source22exercise20 electronperiod8s gives~4.47e-12T not4.5mT (8ns would fit but not guessed/restored). New classical radius/speed graders apply a conservative authored-preview policy v<3e6m/s to avoid near-relativistic problems; this is not claimed as a textbook universal cutoff or new learner formula.

PDF27,28,29,30: Original Faraday/Lenz diagrams/formulas read. Average Emf=-N*DPhi/Dt over interval; equals instantaneous only constant rate. Flux is per turn, Npositivewhole, normal/looporientation consistent. Lenz opposes CHANGE not alwaysB; open cutring can have inducedvoltage but no closedconductioncurrent, sourceabsolute nointeraction treated approximation. Source30.1A worked value is magnitude; signed DPhi+.005/.2 yieldsEmf-.025,I-.1 in defined orientation. No physical magnet/ring experiments.

PDF30,31,32,33: Original self-induction/henry/solenoid pages checked. For Nturn coil distinguish perturnPhi from LINKAGE Psi=N*Phi=L*I; source31Phi=LI must be interpreted linkage or one-turn, not missingN. ConstantlinearL,Emf=-L*DI/Dt average, signopposescurrentCHANGE not alwayscurrent. L=Emag*dt/DImag only positive magnitudes. LongsolenoidL=mu0*muR*n²*S/l, homogeneous linear core/fixed geometry/endignored, not saturating ferromagnet universal. Same explicit mu01.256e-6 approximate convention. No coil interruption/spark/battery live tests.

PDF33,34,35: Original magneticmaterials ratio B=muR*B0 checked with SAMEcurrent/geometry, not fixedvoltage alone universal comparison. muRpositive dimensionless may <1diamagnet or slightly>1paramagnet; no eps>=1 dielectric guard reused. Ferromagnet response/state/temp/nonlinear saturation matter, not constantmuR onlynature/allfields. Source35example B0.5T/muR60->30T conditional linear algebra not realistic universally unsaturated iron, not used as actual material measurement. Source35 magneticbracelet blood-pressure claim not independently substantiated and not copied into course.

PDF36,37,38,39: Original magneticenergy1/2 and inverse root read. W=LI²/2 for constantLINEARL, work to build field not allsourceenergy(Rloss). Iroot sqrt(2W/L) magnitude; linkageenergy I*Psi/2 sourcePhi clarified. No unsupported B²/(2mu) energy density formula added because not taught here. Source39exercise10 I2.5A/Phi.8mWb gives1mJ not2.5;exercise11L5mH/I.4A gives.4mJ not4;exercise12W60mJ/I3A gives13.333mH not90. Source38.08H*.6A=48mWb not mWatt. New independent numbers and exact root/rounding rules, no homemade electromagnet/fire/razor experiment.

Runtime explicit H/mH/µH birliklari, signedaverageFaraday/Lenz andselfinduction, linkagePsiinsteadperturnPhi, npositivewhole, muR>0allowsdiamag<1, constantlinearLstoredenergy/evenI andexactinverse root. Previewclassicalradius/speed v<3e6m/s authoringqualitypolicy rejectsnearrelativisticexamples; nottextbooknewlaw. NegativeDI/DPhi/Emf/I signfeedbacksupports. Old MCQ/8Lorentz/electrolysisFaraday unchanged.

56newpassed4.14s; Physics/Biology1855passed/2PGskipped/2unchangedsandboxdeselected340.28s. Two sandbox tests remain blockedbyoutsideGittemp escalation serviceusagequota, no guard bypass or claim rerun. Actual isolatedPG16:1passed109.81s281lesson/import/reimport/2810XP/replay/legacy137XP3streak2stars. FlutterPhysics28passed85s28public11FRQ320px200%,analyzeNoissues2.0s. Previousfullbackend1913/fullFlutter154 from§1–5 separate, newfull/TCP281/webbuild/nativeAndroid/expert/prodnotrun. Ruff/diffcheckpassed. 792originalchecks/760unique; website/Biology/oldPhysicsimmutabledata unchanged.

Next **11§11 «Erkin elektromagnit tebranishlar…»,PDF43/bosma42**. §11–15 original15pages43–57 read/nativehashes/images verified; source/phase/RMS/idealcap review notes ready, no runtimebatch3/JSONauthoredyet. Rounding exactroot and rational required; qcosphase I=dq/dt convention and source wrong +sin sign must be handled. Ordinaryapprovalnotneeded; 316/316 notcomplete.


## 11-sinf §11–15 — 2026-10-26

**2026-10-26 — Fizika 11-sinf §11–15: 286/316 bo‘lim, 30 qolgan.** 6–10 to‘liq;11:15/45. Jami1263karta/699formula/306namuna/2066topshiriq/765FRQ,586qoida oilasi. Asl807sahifa tekshiruvi/775noyob. Physics/Biology1903passed/2PGopt-inskipped/2sandboxdeselected336.77s;actualPG1passed106.95s286dars/2860XP/replay/legacy. FlutterPhysics28passed84s44public11FRQ320px200%,analyzeNoissues1.6s;48yangi test4.46s. Keyingi **11§16PDF58/bosma57**. Localtestpreviewonly; Biology406/veb/Kimyo/production saqlandi, Android/ekspert/release bajarilmagan.

25karta/16formula/5namuna/42topshiriq(21MCQ+5ordering+16FRQ),14yangi finitefamily/2reuse. §13generatorconceptual, sun’iy formula/FRQyo‘q. §11PDF43–46/bosma42–45;§12PDF46–49/45–48;§13PDF49–52/48–51;§14PDF52–55/51–54;§15PDF56–57/55–56.15originalnativehash/tasvirchecked.

PDF43,44,45,46: Original idealLC energy exchange/Thomsonroot and sample checked. Uniform constantLINEARL/C,Rignored, T=2p sqrt(LC),nu=1/T, conservedW=q²/(2C)+LI²/2. Signedinstantq/I vs peakqm/Im distinct, capacitorplatecharge convention. Quarter-cycleenergyrotation conceptual, no real LC switching task. p3.14 explicitly approximate; exact root/rational round rules. Source46sample T.01256s/20uJ consistent.

PDF46,47,48,49: Original qcos/Ucos/i phasegraphs read. Fix convention I=dq/dt INTO chosenpositiveplate; q=qmcos(theta) then I=-Imsin(theta)=Imcos(theta+pi/2). Source46 prints cos(theta+pi/2)=+sin(theta), wrong sign, while source47 Igraph negative afterqmaximum supports minus. Source48 text says I grows toward negativepeak: |I|/magneticenergy grows, signedI decreases. q/U samephase; current quartershift. Damping energy turnsheat, not disappearance; R-increasesperiod only underdampedmodel beforecritical, not allRstilloscillates. No invented exponential damping formula.

PDF49,50,51,52: Original transistorfeedback/energysource diagram checked. Sustained selfoscillator uses externalDCenergy and phasedfeedback; no perpetualmotion. Source51 180deg is specific inverting-stage/coil convention, not universal totalfeedbackphase; suitable loopfeedback returnsenergy inphase. Transistor not only imaginable possible oscillator switch; no all-mechanical-MHz impossibility assertion. Unsupported universal eachorganresonance/psychologicalhealth claims not included. Conceptual no forced beta/medical/radiation/LLM/newgeneratorruntime.

PDF52,53,54,55: Original pureactiveR sinusoid/phasor/RMS/power1/2 checked. FixedR,pureR,u/i samephase. Pinst=Um*Im*cosPhase² nonnegative and doubledfreq, Pavg=Um*Im/2; RMS=peak/sqrt2 only SINUSOID, not any waveform/universal lightbulb eyes16–20fps myth. Typed providedcos data not generaltrig. Peak/rms mixednotallowed in suppliedgivens. Source55average30W example interprets2A as amplitude, newprompts explicit. ExactirrationalRMS rubrics retain square and SI roundinggrid, not float expectedtruth.

PDF56,57: Original idealcap derivative i=-UmC*omega*sin(theta)=Imcos(theta+pi/2) agrees fixed I=dq/dt convention. Current LEADS voltage90deg in steady sinusoidalidealcap; steadyDC current0aftercharging, not nevertransient. Xc=1/(omegaC)=1/(2pnuC),Im=Um*omegaC. omega rad/s vs nuHz,p3.14 explicit, Xcohms reactive not heatresistor; no claim passivecap dissipatesrmsUI. Source57sample50Hz50uF63.69ohm consistent approximate. No live mains construction.

IdealLCconservedenergy signedq/I,sqrtperiod/exactrepeatingfrequency; chosenI=dq/dt INTO selectedplate unifies qcos/-Imsin andidealCcurrentlead90. Rfixed/sinusoidalRMS keeps privateexactroot50 or1/50 withSIgrid0.01V/0.001A, nofloat gradingtruth. Average pureRpower andsinusoidalcapacitivereactancefrequency vsangular separate, allamplitudesexplicit. Genericparsernotexpanded/noLLM; oldMCQ/XP/Biologyunchanged.

48newpassed4.46s; Physics/Biology1903passed/2PGopt-inskipped/2unchangedsandboxdeselected336.77s. SameoutsideGittempapprovalservicequotablock for2sandboxguards; no bypass orfalse rerunclaim. ActualisolatedPG16:1passed106.95s286lesson/reimport/2860XP/replay/legacy137XP3streak2stars. FlutterPhysics28passed84s44public11FRQ320px/200%;analyzeNoissues1.6s. Previousfullbackend1913/fullFlutter154 at§1–5 separate; newfull/TCP286/webbuild/nativeAndroid/expert/prodnotrun. Ruff/diffcheckpassed,807originalchecks/775unique.

Next **11§16 «O‘zgaruvchan tok zanjiridagi induktiv g‘altak»,PDF58/bosma57**. §16–20original15pages58–72 nativehash/imagesread; source/phase/phasor/resonance/digitallabRMS review notesready, noJSON/runtimebatch4yet. Source66upsweepUC<ULinstruction contradictedmathematicaldirection, correctedconditionalUL/UCtable derivedindependently, not realmeasurement. Ordinaryapprovalnotneeded;30sectionsstillremain.


## 11-sinf §16–20 — 2026-10-26

**2026-10-26 — Fizika 11-sinf §16–20: 291/316 bo‘lim, 25 qolgan.** 6-sinf 61/61; 7-sinf 46/46; 8-sinf 60/60; 9-sinf 59/59; 10-sinf 45/45; 11-sinf 20/45. Jami 1288 karta, 715 formula yozuvi, 311 namuna, 2108 topshiriq, 781 FRQ. 822 asl sahifa tekshiruvi/790 noyob. Physics/Biology 1954 passed/2 PG opt-in skipped/2 sandbox deselected (361.25s); actual PG 1 passed (110.32s). Flutter Physics 28 passed (94s), analyze No issues found (2.0s); yangi 51 test (4.58s). Keyingi **11§21, PDF77/bosma76**. Local test preview; Biology406/veb/Kimyo/production saqlandi, native Android/ekspert/release bajarilmagan.

Yangi: 25 karta/16 formula/5 namuna/42 topshiriq/16 FRQ. §16 PDF58–60; §17 PDF60–63; §18 PDF63–65; §19 PDF66–67; §20 PDF67–72. Butun manba kitobida PDF=bosma+1; original tasvirlar/native hashlar qayta tekshirildi.

PDF58,59,60: Original idealinductor phasor/reactance checked. Choose passive terminalvoltage uL=L*di/dt and i=Imcos(theta): uL=-omegaLImsin(theta)=Umcos(theta+pi/2); source58 derivative+sin/cosidentity sign inconsistent, source59 voltageLEADScurrent90 conclusion correct. SelfEmf=-Ldi/dt vs terminaluL opposite. XL=omegaL=2pnuL,Im=Um/XL onlyidealL/steadySINUSOID, noRloss; fieldenergyexchange not allheat.

PDF60,61,62,63: Original SERIES RLC phasor/norm checked. Choose currentreference i=Imcos(theta), then totalu=Umcos(theta+phi); source60 gives bothcos withnooffset despitegenerallynonzerophase. Z=sqrt(R²+(XL-XC)²),Imax=Um/Z,voltagephasornorm NOTsumofmagnitudes. Source62tanphi denominator printedUm but correctUR (reactdiff/R nextcorrect); finite grader tanPhi=(XL-XC)/R signed/unbounded not sine/cosrange. No generalcomplexsolver/trigatan.

PDF63,64,65: Original fixedseriesRLC resonance criteria/voltagemagnification checked. XL=XC,omegarez=1/sqrtLC, Zmin=R>0 and Ipeak=Um/R forfixedUm/R/L/C frequency-independentidealcomponents. Rlarge stillreactivecancellationexists but broadlessvisiblepeak, not mathematicallynoresonance. Voltageindividualcanexceedsupply whenQ=sqrt(L/C)/R>1, notforALLcircuits. Source65C50Hz.1H~101.4uF approximated100uF acceptable statedrounding; new rationalrounding explicit. Alllowvoltageconditionalno physicalovervoltagetask.

PDF66,67: Original digitalresonance lab uses UL/UC vs frequency. Source66initialUC<UL thenincreasefrequencyuntilUC=UL is wrong fixedLC sweepdirection: above resonanceXL>XC, increasingf movesaway. Correct digitaltable beginsbelowresonanceUC>UL,passesUL=UCthenUL>UC. Original conditional data mathematically checked forR100ohm,L1H,C=1/(4*3.14²*100²)F,UsourceRMS1V:50HzUC1.33/UL.33;100Hz6.28/6.28;150Hz.79/1.77, rounded. No real instrument readings/20Vmeter or mainsinstruction claim. Sampledequalitywithinmodel, threepointsnotallcontinuouscurveproof.

PDF67,68,69,70,71,72: Original sinusoidalRMSaveragepower/factor equations checked. Pavg=UeffIeffcosPhi, A=Pavg*t forsteadyintegercycles/wholeperiodaverage, passivefixedseriesRLCfactor0..1, R/Z notarbitraryactivegeneratorcosbound. Source67 usesu*i*t asworkonlysmallintervalapprox, notexactarbitrarytimephase; source68halfperiodpositive/halfnegative notuniversally foranyphi, onlyspecialreactivecase. Source70=.85cos policy not asserted universalcurrentlegalrequirement; noDIYcompensation. Source70sample cos~.5427 and P~132.5W correct reference but printedcos²/fractionderivation inconsistent notcopied. Source71q4LC1H/2.5uFomega~632rad/s not630e6;source71q6firstequalenergyt~3.925e-5s not39e-5; badkeysnotused. Average/reactiveenergyexchange and gridloss distinct.

15yangi finite formula oilasi, eski ohm_current ekvivalent rezonansR uchun qayta ishlatildi. IdealLpassiv terminalcosderivative, signedtanPhi unbounded vs boundedcosPhi, phasornorm/current/exactroot, resonantcapacitance5/49298F/1µFgrid, passiveRMSwork/wholecyclepolicy tekshirildi. §19 beshta MCQ/tartiblashli shartli laboratoriya, sun’iy formula/FRQyo‘q. Qatorlar R100Ω/L1H/C=1/(4*3.14²*100²)F/Urms1Vdan mustaqil Decimalreference orqali tekshirildi. Haqiqiy tajriba bajarildi deyilmaydi.

Actual local PostgreSQL16: 291 dars import/reimport, 2910XP/replay, legacy137XP/3streak/2stars saqlandi. 11-sinfning60publicFRQdrafti320px/200%widgetrun bilan tekshirildi. Ruff va gitdiffcheck passed. Ikki o‘zgarmagan sandbox testi outside-Git tempdir escalation approval-review usage limit sabab ajratilgan; guard chetlab o‘tilmadi yoki yumshatilmadi, joriyda o‘tdi deyilmaydi. Oxirgi to‘liq backend1913 va fullFlutter154 §1–5checkpoint natijalari alohida; bu partiya Physics/Biology + FlutterPhysics tanlovini bajardi. NativeAndroid/liveTCP/newwebbuild/independentexpert/productionnotrun. EskiPhysics/BiologyimmutableJSON/website/Chemistry saqlandi.

Keyingi11§21PDF77/bosma76. §21–25 original20sahifa77–96 nativehash/tasvirlari qayta o‘qildi, scientificnotes tayyor, JSON/runtimebatch5haliyo‘q. Emwave/relativeindex/intensity/radar/history/coherentinterference/Newtonrings/grating source tafovutlari GRADE11_NEXT_REVIEW.md da yozilgan. Oddiy bosqichda approval qayta so‘ralmasin. 25bo‘lim qolgan;316tugallangan emas.


## 11-sinf §21–25 — 2026-10-26

**2026-10-26 — Fizika 11-sinf §21–25: 296/316 bo‘lim, 20 qolgan.** 6-sinf 61/61; 7-sinf 46/46; 8-sinf 60/60; 9-sinf 59/59; 10-sinf 45/45; 11-sinf 25/45. Jami 1316 karta, 731 formula yozuvi, 316 namuna, 2151 topshiriq, 797 FRQ. 842 asl sahifa tekshiruvi/810 noyob. Physics/Biology 1996 passed/2 PG opt-in skipped/2 sandbox deselected (366.73s); actual PG 1 passed (120.98s). Flutter Physics 28 passed (96s), analyze No issues found (2.1s); yangi 42 test (3.44s). Keyingi **11§26, PDF97/bosma96**. Local test preview; Biology406/veb/Kimyo/production saqlandi, native Android/ekspert/release bajarilmagan.

Yangi: 28 karta/16 formula/5 namuna/43 topshiriq/16 FRQ. §21 PDF77–79; §22 PDF80–84; §23 PDF84–88; §24 PDF88–91; §25 PDF92–96. Butun manba kitobida PDF=bosma+1; original tasvirlar/native hashlar qayta tekshirildi.

PDF77,78,79: Original images/native checked. EMsignal propagation distinct electron drift; c3e8 school VACUUM/airapprox, not every wire exactspeed. Hertz historical demonstration/Maxwell theory no sole-priority oversimplification. Wavev=lambda*nu andinverse, lambda inputASCII Lw (safe parserreservedlambda). Openoscillator radiation not allenergyperfectescape nor no closedcircuit everradiates. No spark/highvoltage radio experiment.

PDF80,81,82,83,84: Original reflection/refraction/transversewave/intensity formulas read. Stationaryinterfacefrequencyunchanged, speed/wavelengthmaychange; source81lambda=c/nu limitedvacuum, use actualv inmedium as source83example. n21=v1/v2, epsratio assumes mu~1/nondispersiveordinarymedia. B/Etransverse for idealplanewave/farfield not arbitrarynearfield. Metalplate/dielectricreflection experiment particularfrequency, not metalscannottransmitanyfrequency/dielectricsneverreflect. Intensity W/(Sdt)=Pavg/S in W/m², averageenergydensityw J/m³ andI=w*c forvacuumunidirectionalplane wave. Inversesquare isotropicpointsourcefarfield/noabsorption only. Source83 I proportionalomega^4 requiresfixeddipoleamplitude/sourceconditions, not anyEMsignal/universalenergyvsfrequency, not used unqualified.

PDF84,85,86,87,88: Original radio/modulation/detection/radar pages read. Information signal versus carrier; LCtuning,demodulation distinct roles, no receiverbuilding. Broadcastcanbeintercepted, source84 claimmessagescannotcaptured not copied. HistoricalPopov/Marconi reportedinsource not one-inventor universalpriorityclaim. RadarR=c*echoTime/2 specific monostaticroundtrip/boundedobjectmotion/vacuumapprox. Source88asksminimumrange but solves Lmax~37.5km; tau2us minrange~300m forTx/Rxblockedpulse model, maxunambig c/(2PRF)~37.5km(ignorepulsewidth;subtract gives37.2). Not copied conflated answer. Nperpulse=c*tPulse/lambda vs pulse repetitionrate separate. No operationalradar/targettracking hardware.

PDF88,89,90,91: Original television blocks/history read. Analog camera electricalsignal/transmission/receiverseparation/screen/speaker preserved, diagramnotallmoderndigitalTVuniversalarchitecture. Source90TV50–230MHz and lineofsight givenhistoricalanalogband/model, not currentallTVfreq/globalrange. Source90–91 Tashkent1928Telefot/Grabovsky/Belyansky/1956centre/375mtower are SOURCE-reported historicalcase, not independentlyverifiedsoleglobalinvention or currentrank/channelcount; no unsupportednewhistory. Conceptualcourse,no artificialformula.

PDF92,93,94,95,96: Original coherence/pathconditions/Newtonrings/grating images checked. Source92rainbow not same general thin-film interference mechanism (rainbow primarilyrefraction/reflection/dispersion), not copied. Equalfrequency/constantphase,LINEARsameuniformmedium/samepolarization/inphase sources for Delta=mLw constructive/(m+.5)Lw destructive; unknownstartingphase/unequalmedia notuniversal. Thinfilmreflectionphase matters. Newtonairfilm reflectednormal/smallgap Rcurvature: darksqrt(mLwR),brightsqrt((m+.5)LwR),mwhole>=0,nottransmission/liquidgeneral. Diffractionnoticeable a~lambda notstrictonlya<lambda. GratingNORMALincidence/monochromatic PRINCIPALmax d*sinPhi=nLw,nwhole>=0; source96half-integer universalgratingminima wrongformultislit not copied. Inverselambda/d requiresn>0/sin>0; no generaltrig/asin. Twoindependentthermalbulbs notstablecoherent, not blanketallseparatesourcesimpossible. No directlasereye/DIYbeam experiment.

16 closed formula families independently recompute EM wavelength/frequency/speed, relative index, intensity, monostatic radar, pulse cycles, coherent path difference, reflected Newton radii and normal grating. Added explicit MHz/GHz/ms/µs/ns and W/m² prefix units. 42 semantic/domain/oracle tests passed, no eval or client keys; old MCQ/XP/idempotency preserved.

Actual local PostgreSQL16: 296 dars import/reimport, 2960XP/replay, legacy137XP/3streak/2stars saqlandi. 11-sinfning76publicFRQdrafti320px/200%widgetrun bilan tekshirildi. Ruff va gitdiffcheck passed. Ikki o‘zgarmagan sandbox testi outside-Git tempdir escalation approval-review usage limit sabab ajratilgan; guard chetlab o‘tilmadi yoki yumshatilmadi, joriyda o‘tdi deyilmaydi. Oxirgi to‘liq backend1913 va fullFlutter154 §1–5checkpoint natijalari alohida; bu partiya Physics/Biology + FlutterPhysics tanlovini bajardi. NativeAndroid/liveTCP/newwebbuild/independentexpert/productionnotrun. EskiPhysics/BiologyimmutableJSON/website/Chemistry saqlandi.

11§26–30 PDF97–116 original native hashes and all20 images re-read. Private original draft prepared; batch6 JSON/runtime not yet added at this checkpoint. Next §26PDF97/bosma96.


## 11-sinf §26–30 — 2026-10-26

**2026-10-26 — Fizika 11-sinf §26–30: 301/316 bo‘lim, 15 qolgan.** 6-sinf 61/61; 7-sinf 46/46; 8-sinf 60/60; 9-sinf 59/59; 10-sinf 45/45; 11-sinf 30/45. Jami 1340 karta, 741 formula yozuvi, 321 namuna, 2188 topshiriq, 808 FRQ. 862 asl sahifa tekshiruvi/830 noyob. Physics/Biology 2030 passed/2 PG opt-in skipped/2 sandbox deselected (373.43s); actual PG 1 passed (120.56s). Flutter Physics 28 passed (96s), analyze No issues found (2.2s); yangi 34 test (2.94s). Keyingi **11§31, PDF116/bosma115**. Local test preview; Biology406/veb/Kimyo/production saqlandi, native Android/ekspert/release bajarilmagan.

Yangi: 24 karta/10 formula/5 namuna/37 topshiriq/11 FRQ. §26 PDF97–98; §27 PDF99–104; §28 PDF104–107; §29 PDF108–111; §30 PDF111–116. Butun manba kitobida PDF=bosma+1; original tasvirlar/native hashlar qayta tekshirildi.

PDF97,98: Original diagram x axial/y transverse and approximate sin≈tan were visually checked. Smallangle Lw≈d*y/(n*x), explicit authored y/x<=0.1 limit, not exact/general. Original digital rows600/620nm ->mean610nm, deviations10nm. Source table delta recursive typo corrected to |Lw_i-mean|; mean deviation not complete instrument uncertainty. Physical measurement false; no eye/laser experiment.

PDF99,100,101,102,103,104: Dispersion n depends on frequency/vacuum wavelength, interface frequency same; ordinary normal dispersion not allmedia redalwaysfaster. White spectrum not exactly7discretefrequencies; reversed prism not universally converging lens. Atomic line spectra can have multiplelines despite source singularline phrase. RGB finite gamut, no allcolors universal claim. Symmetric thin biconvex air F=R/[2(n-1)] and original0.6/0.5m values independently checked; no copied long text.

PDF104,105,106,107: Original Malus I=I0cos²alpha checked in image: I0 is LINEAR incident at analyzer, not natural light beforefirstpolarizer. cos input[-1,1], intensity>=0, no negativeintensity. Ideal parallel/crossed limit, no artificial unpolarized factor1/2 assignment beyondthissource.

PDF108,109,110,111: IR/UV/Xrays conceptual activity only. Avoid dubious mosquito IR-seeing, IR sterilization and absolute historicalpriority claims. UV category gaps and overlapping Xray frequency numbers not tested as exactsingleuniversalbound. Thermal/nuclear/ionizing safety no real device/therapy. Book medical/sterilization examples not DIYinstructions.

PDF112,113,114,115,116: Radiometric W/m² distinct photometric lm/cd/lx. Omega sphericalPATCHarea/R², not planararea. Iv=Phi/Omega uniform withinangularpatch, Phi=4piIv onlyisotropic; Phi/S RECEIVEDuniformflux; Ev=IvcosNormal/r² point/noabsorb. Source55nm visually confirmed typo, avoid copying asSI:555nm near photopicpeak, oldplatinumcandela definition historical notcurrent. Luminance directional projectedarea, sourceI/S onlynormalcase, notunqualified universal. No generatedfalsemeasurement.

10 closed source-scoped formula families: small-angle grating, phase index, symmetric biconvex focus, Malus, spherical patch and uniform photometry. New sr/lm/cd/lx units distinct from radiometric units. Photometry small angular-patch preview family restricts Omega<=4sr explicitly; full-sphere4pi relation explained, no general equivalence claim. 34 independent source/domain/answer tests passed.

Actual local PostgreSQL16: 301 dars import/reimport, 3010XP/replay, legacy137XP/3streak/2stars saqlandi. 11-sinfning87publicFRQdrafti320px/200%widgetrun bilan tekshirildi. Ruff va gitdiffcheck passed. Ikki o‘zgarmagan sandbox testi outside-Git tempdir escalation approval-review usage limit sabab ajratilgan; guard chetlab o‘tilmadi yoki yumshatilmadi, joriyda o‘tdi deyilmaydi. Oxirgi to‘liq backend1913 va fullFlutter154 §1–5checkpoint natijalari alohida; bu partiya Physics/Biology + FlutterPhysics tanlovini bajardi. NativeAndroid/liveTCP/newwebbuild/independentexpert/productionnotrun. EskiPhysics/BiologyimmutableJSON/website/Chemistry saqlandi.

11§31–35 all20 original mapped pages (116–119,125–133,136–142) visually read and native hashes matched. No runtime batch7 content at this checkpoint. Next11§31PDF116/bosma115.


## 11-sinf §31–35 — 2026-10-26

**2026-10-26 — Fizika 11-sinf §31–35: 306/316 bo‘lim, 10 qolgan.** 6-sinf 61/61; 7-sinf 46/46; 8-sinf 60/60; 9-sinf 59/59; 10-sinf 45/45; 11-sinf 35/45. Jami 1363 karta, 756 formula yozuvi, 326 namuna, 2229 topshiriq, 824 FRQ. 882 asl sahifa tekshiruvi/849 noyob. Physics/Biology 2074 passed/2 PG opt-in skipped/2 sandbox deselected (375.32s); actual PG 1 passed (119.41s). Flutter Physics 28 passed (96s), analyze No issues found (2.1s); yangi 44 test (4.96s). Keyingi **11§36, PDF143/bosma142**. Local test preview; Biology406/veb/Kimyo/production saqlandi, native Android/ekspert/release bajarilmagan.

Yangi: 23 karta/15 formula/5 namuna/41 topshiriq/16 FRQ. §31 PDF116–119; §32 PDF125–129; §33 PDF129–133; §34 PDF136–137; §35 PDF138–142. Butun manba kitobida PDF=bosma+1; original tasvirlar/native hashlar qayta tekshirildi.

PDF116,117,118,119: Equal NORMAL illuminance balance Iv1/r1²=Iv2/r2² gives Iv1=Iv2*r1²/r2². Source117 visually has invertedratio; corrected notcopied. Source E=1/r² omits sourceintensity, use Ev=Iv/r². Digitalcomparison only, no mains/voltageexperiment. Exercisepages includedmappedrange butnotallendofchapterquestions separatecoverageclaims.

PDF125,126,127,128,129: Inertialvacuum c same, Lorentz tables/signs viewed. Proper intervalsameclock, lengthparallelmotion simultaneous endpoints; not allobserverdimension contraction. Velocity collinear SIGNED (u+v)/(1+uv/c²),frame |v|<c, object|u|<=c, noresultsuperluminal; use explicitc3e8 approximation. Rational-root original examples use.6c/.8c, notfloatingtruth.

PDF129,130,131,132,133: Historical velocity-dependent mass m=gamma*m0 is energy/c² convention, invariant restmassm0 unchanged. Prefer E=gamma*m0*c²,K=E-m0c²,p=gamma*m0v. Source kinetic classical1/2mv² mustnotbeusedallrelativisticspeeds. Source.89c lifetime5x answer inconsistent (gamma~2.19), no copiedkey; water/coal/petrol equalrestenergiesatideal1kg not equalchemicalusableenergy.

PDF136,137: Wien lambda_peak*T=b for wavelength spectraldensity/thermalblackbodymodel, notuniversal allsources orfrequencydensity peak converted. Source b2.898e-3mK,h6.626e-34Js givenapprox not modernexactSI. PlanckE=hnu, classicalfailure doesnotmeanallclassicalphysicsinvalid. Source claimSunnotthermal atall misleading; steady energyinput permitsradiationnotisolatedequilibrium; avoidclaim.

PDF138,139,140,141,142: Single-photon photoelectric Kmax=hnu-A>=0,thresholdnu0=A/h,stopUpositiveMODULUS=K/e; belowthresholdnoemissionnotnegativeK. Frequencycontrolsmaxenergy; intensitychangesnumberabove thresholdundermodel. Internalvs external effectdistinct; photonrestmass0, historicalE/c²notinvariantmass. h6.626e-34/e1.6e-19 explicitbookapproximations. No actualvacuum/highvoltageexperiment.

15 closed families plus J*s and m*K unit dimensions. Signed collinear relativistic addition, exact rational/square-root proper-time and parallel-length checking, invariant rest mass/total/kinetic/momentum, Wien wavelength-density peak, quantum and threshold-safe photoelectric grading. Corrected equal-Ev source-distance ratio. 44 independent tests passed. Explicit rounded ratio tolerance fixed in new authored data without weakening grader or old content.

Actual local PostgreSQL16: 306 dars import/reimport, 3060XP/replay, legacy137XP/3streak/2stars saqlandi. 11-sinfning103publicFRQdrafti320px/200%widgetrun bilan tekshirildi. Ruff va gitdiffcheck passed. Ikki o‘zgarmagan sandbox testi outside-Git tempdir escalation approval-review usage limit sabab ajratilgan; guard chetlab o‘tilmadi yoki yumshatilmadi, joriyda o‘tdi deyilmaydi. Oxirgi to‘liq backend1913 va fullFlutter154 §1–5checkpoint natijalari alohida; bu partiya Physics/Biology + FlutterPhysics tanlovini bajardi. NativeAndroid/liveTCP/newwebbuild/independentexpert/productionnotrun. EskiPhysics/BiologyimmutableJSON/website/Chemistry saqlandi.

11§36–40 all23 original mapped pages143–148/152–168 re-read as images and native hashes matched. Private original draft prepared, no batch8 runtime at checkpoint. Next11§36PDF143/bosma142.


## 11-sinf §36–40 — 2026-10-26

**2026-10-26 — Fizika 11-sinf §36–40: 311/316 bo‘lim, 5 qolgan.** 6-sinf 61/61; 7-sinf 46/46; 8-sinf 60/60; 9-sinf 59/59; 10-sinf 45/45; 11-sinf 40/45. Jami 1388 karta, 769 formula yozuvi, 331 namuna, 2268 topshiriq, 837 FRQ. 905 asl sahifa tekshiruvi/872 noyob. Physics/Biology 2115 passed/2 PG opt-in skipped/2 sandbox deselected (372.05s); actual PG 1 passed (122.07s). Flutter Physics 28 passed (97s), analyze No issues found (2.1s); yangi 41 test (3.37s). Keyingi **11§41, PDF168/bosma167**. Local test preview; Biology406/veb/Kimyo/production saqlandi, native Android/ekspert/release bajarilmagan.

Yangi: 25 karta/13 formula/5 namuna/39 topshiriq/13 FRQ. §36 PDF143–148; §37 PDF152–157; §38 PDF157–161; §39 PDF161–164; §40 PDF165–168. Butun manba kitobida PDF=bosma+1; original tasvirlar/native hashlar qayta tekshirildi.

PDF143,144,145,146,147,148: Vacuum photonE=hc/lambda,p=h/lambda,normalperfectabsorptionp=I/c/reflection2I/c checked. Source sunlight pressure/force number0.48µN wrongmagnitude/unitforgeneric sunlight notcopied. Source147workedtable lambda=nu/c typo corrected c/nu; h6.6e-63 exercise typo notcopied. No assumptionuniversalmediumphotonmomentum (Abraham/Minkowskiambiguity). LEDisnot automaticallysemiconductorlaser, emissionnotinternalphotoeffect inreversewording. PVefficiency/historyfiguresnotcurrentupperbounds. Original source faithful explanations/problems, noactualdevices.

PDF152,153,154,155,156,157: Bohr stationary/transition postulates originalimageschecked. Source155radiuswritten n*h²eps/(pi*m*e²) missingn²; scientificcorrectionr_n=a0*n² recorded/used. Varyingclassicalorbitv=constant notgenerallycorrect, avoidclassicalcollapseargumentwiththatextraassumption. En=-Eion/n² hydrogenapprox,zeroionizationreference; npositivewhole. EmissionEi>Ef,negativeboundsallowed,photonpositive. Original unnamedgivenlevelmodel notclaimedactualelementlevels. hbar1.05e-34/h6.626e-34explicitbookapprox,not hidden exactconstants.

PDF157,158,159,160,161: Laser conceptualonly/noartificialFRQ. Stimulatedvs spontaneous, pumping/metastable and rubyCr3+ chain reviewed. Notalllasers fixedpower/linewidth/polarization orallLEDlaser. Bookexactorders1e16–1e20W/m²not universalrequiredfacts. NoDIYlasers/isotopeseparation/surgicaloperationalinstructions; safeclassificationonly.

PDF161,162,163,164: A,Z,Ncounts distinct masses; isotopes sameZvsisobars sameA. Dm=Zmp+(A-Z)mn-mNUCLEUS; atomicmassnot mixed. BoundenergyDm*c²,pernucleonE/A average. Source95%mass claim inaccurateapprox(usually>99.9%)excludednumericaltest. Source164 binding-per-nucleon chart not copied as universal stability criterion. Original givenA4Z2mp1.6726e-27mn1.6749e-27mNuc6.644e-27 ->Dm5.1e-29/E4.59e-12J independentexactdecimalbalance; masses declaredapproximatemodelnotnewmeasuredisotopeclaim.

PDF165,166,167,168: Detector pulsecountvs spatialtrack,Geiger gasionization,cloud droplets,bubble superheatedliquid,scintillation light/photoemulsion reviewed. No perfectefficiency/zerodeadtime assumptions. Source168electronv~6e7 classical calculation needsrelativistic correction (~2%); neworiginal low-speedcase~8.79e5 chosen within existingexplicitpreview<3e6 guard,nottextbookfundamentalcutoff. qpositivechargeMODULUS/Bperpendicularuniform/Rcurvature. Rounded exact80000000/91 ->879000m/s at1000grid. Noactualradioactivesource/highvoltageexperiment.

12 new closed families plus existing classical magnetic-speed family; vacuum photon momentum/energy/normal radiation pressure, Bohr moment/negative bound energy/radius n², nuclear counts/mass defect/binding. Added µPa and canonical action J*s. 41 independent tests passed. Initial new-test assumptions kg always dimension-mismatch and non-grid wrong answer out-of-tolerance were corrected to test actual unit and rounding contract; grading code not weakened.

Actual local PostgreSQL16: 311 dars import/reimport, 3110XP/replay, legacy137XP/3streak/2stars saqlandi. 11-sinfning116publicFRQdrafti320px/200%widgetrun bilan tekshirildi. Ruff va gitdiffcheck passed. Ikki o‘zgarmagan sandbox testi outside-Git tempdir escalation approval-review usage limit sabab ajratilgan; guard chetlab o‘tilmadi yoki yumshatilmadi, joriyda o‘tdi deyilmaydi. Oxirgi to‘liq backend1913 va fullFlutter154 §1–5checkpoint natijalari alohida; bu partiya Physics/Biology + FlutterPhysics tanlovini bajardi. NativeAndroid/liveTCP/newwebbuild/independentexpert/productionnotrun. EskiPhysics/BiologyimmutableJSON/website/Chemistry saqlandi.

11§41–45 all19 original mapped pages168–186 visually reviewed, native hashes matched;privateoriginaldraft prepared. No batch9 runtime at this checkpoint. Next11§41PDF168/bosma167.

## 11-sinf §41–45 va316/316 yakuniy checkpoint —2026-10-26

**2026-10-26 — Fizika 6–11-sinflar: 316/316 bo‘lim yozildi va lokal/test tekshiruvlaridan o‘tdi; qolgan bo‘lim 0.** 1413 karta, 780 formula yozuvi, 336 namuna, 2305 topshiriq/848 FRQ. Backend 2272 passed/4 PG opt-in skipped/2 sandbox deselected (568.38s); alohida PostgreSQL16 1 passed (130.25s),316dars/3160XP/replay. Flutter full 154 passed (117s), analyze No issues found (1.9s), local Physics preview web build passed (59.9s). 924 asl sahifa tekshiruvi/890 noyob; Biology406 saqlandi. **Mustaqil ekspert va haqiqiy Android sinovi bajarilmagan; ommaviy release emas.** [Yakuniy dalillar](docs/physics/COURSE_COMPLETION.md).

Yangi25karta/11formula/5namuna/37topshiriq/11FRQ. sourcePDF168–186/bosma167–185. Muhimfayllar:grade11_batch9.json/review,physics_rules.py,assessment_grading.py,assessment_runtime.py,physics_curriculum.py,yangi decay va complete-coverage testlari,Flutterpublicfixtures/tests. EskiJSONlar o‘zgartirilmadi.

PDF 168,169,170,171: Decay originalpages viewed/nativehash matched. N=N0*2^(-t/T) expectedensembleparentcount,notdeterministicindividualtime. Newexactcalculatorrestricted WHOLE halfperiods0<=t/T<=4096,notphysicalclaimfractionalperiodsforbidden. ClosedAST symbolicpoweroptin ONLY formula-shapecomparison,neverexecuteslearnerinput; exactFraction fixedbase2 calculationguard. Activitypositive=-dN/dt=decayRate*N,source derivative missingminus corrected. Bqnotfrequency/dose,explicitln2=.693approx. Source allradioactivityabsolutelyunaffectedbytemperature/chemistry notgeneralextremeconditions;Bi209stableclaimobsolete,notcopied.

PDF 171,172,173,174: A/Z conservation vsrestmassenergy distinct. AlphaAd=A-4/Zd=Z-2 andbetaMinusZd=Z+1,Aunchanged. Sourcebeta-minus schematic omitsantineutrino; note missingparticle forenergy/momentum/leptonbalance,notclaimfullreaction. Gamma A/Zunchanged,energylevelchanges; XrayvsGamma origin notuniversalfrequencythreshold. Qsigned=(summin-summout)c² consistentnuclearinventory,positiveQnotguaranteedreactionrate/barrierabsence. Originalsmallabstract Qbalance notexperimentalreactionclaim.

PDF 174,175,176,177,178: Source historicalelementary300count/7fundamentaltypes/gravitonconfirmed excluded. Protonuud/neutronudd,valencequarkcharges+2/3and-1/3 imageverified. Antineutronnotselfidentical merelyneutral; sameantiQuantumNumbersconcept. ParentATREST two-photonONLY decay impliesoppositeequalenergyEq=mc²/2,noallmovingdecayclaim. Source two-photon parentworkedformula checked, originaldeclared2.4e-28kgmodelmass notnewmeasuredpionvalue.

PDF 178,179,180,181,182,183: Fissionbindingenergycomparison, generalchainconcept andheat→steam→turbine→generator reviewed. DoNOTcopyallk>1instantnuclearexplosionstatement orallglobalpowermostlyAESclaim. Industrialsafetyisnonoperationalgeneralconcept; nofuelsourcing/enrichment/criticalmassgeometry/procedure/shielddesign instructions. Etotal=Nevents*Qsingle abstractenergybookkeeping withfictionaldeclaredsmallcount,notreactorprediction. ExistingDB/XP/Biologyunchanged.

PDF 183,184,185,186: Uzbekistan1949/1956institutehistory explicitlybookhistoricalcontext,notliveverifiedinstitutionstate. Radiationmaterialscience/detectors/agricultural/treatmentexamples conceptualnotmedicalDIY. 1995productcountnotcurrentstatistic. Mappedendexercise186 reviewedwithoutclaimingeveryendchapterexercise individually authored. Nativeexpert/physicalmeasurementsnotclaimed.

Finaltest/cheklovlar COURSE_COMPLETION.md va COURSE_VALIDATION_316.json da. Keyingi authoringsectionyo‘q; keyingi bosqich ekspertiza va realAndroidQA.
