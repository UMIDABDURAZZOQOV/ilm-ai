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
