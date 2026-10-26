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
