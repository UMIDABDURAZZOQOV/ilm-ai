# Fizika 2-bosqich — 6-sinf §1–7 lokal sinov partiyasi

Sana: **2026-10-22 (Asia/Tashkent)**. Boshlang‘ich backend: `cb46a02`,
`feat/physics-curriculum-map`. Flutter bazasi: `79608c2`, yangi
`feat/physics-first-batch`. Veb-saytga tegilmagan.

**7 ta haqiqiy, manbaga bog‘langan dars lokal sinov uchun yozildi.** Bu 316 bo‘limli
kursning to‘liq tayyorligi, mustaqil pedagog/fan ekspertizasi yoki umumiy nashri emas.
Qolgan 309 bo‘lim generatsiya qilinmadi. §8–17 foydalanuvchining keyingi tasdig‘ini kutadi.

## Kontent va manba

N. Sh. Turdiyev, *Fizika. 6-sinf*, Niso Poligraf, 2017, qayta ishlangan uchinchi nashr.
Asl PDF SHA-256:
`ccfe285c53072e33966df6ee22ec50c730ca66b5e16e2202a9ad732c77ea2534`.

Har keltirilgan sahifaning **to‘liq asl tasviri va matni** qayta ko‘rildi. PDF hash,
14 sahifa matn hash’i va qayta render qilingan 14 tasvir hash’i ham amalda solishtirildi.
PDF/rasm/to‘liq matn repozitoriyaga kiritilmadi. Original qisqa tushuntirish va yangi
sonli masalalar yozildi; darslikdagi uzun matn yoki masalalar qayta nashr qilinmadi.
Manba tekshiruvi metadata sanasi UTC 2026-10-21; hisobot foydalanuvchi vaqt zonasida.

| § | Mavzu | Asl PDF sahifasi | Bosma sahifa | Karta | Formula qoidasi | Yechilgan/hayotiy misol | Topshiriq | FRQ |
|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | Fizika nimani o‘rganadi? Fizik hodisalar | 3–5 | 3–5 | 5 | 0 | 1 | 6 | 0 |
| 2 | Fizika taraqqiyoti tarixidan ma’lumotlar | 6–8 | 6–8 | 4 | 0 | 1 | 5 | 0 |
| 3 | Jamiyat rivojlanishida fizikaning ahamiyati. O‘zbekistonda fizika taraqqiyoti | 8–9 | 8–9 | 4 | 0 | 1 | 5 | 0 |
| 4 | Fizikada ishlatiladigan ayrim atamalar | 9–10 | 9–10 | 4 | 0 | 1 | 6 | 0 |
| 5 | Kuzatishlar va tajribalar | 10–12 | 10–12 | 4 | 0 | 1 | 6 | 0 |
| 6 | Fizik kattaliklar va ularni o‘lchash | 12–14 | 12–14 | 5 | 2 | 1 | 7 | 2 |
| 7 | O‘lchashlar va o‘lchash aniqligi | 14–16 | 14–16 | 5 | 3 | 2 | 8 | 3 |
| Jami | | **14 noyob sahifa** | | **31** | **5** | **8** | **43** | **5** |

43 topshiriq: **36 konseptual tanlov, 2 tartiblash, 5 son+formula+birlik FRQ**.
Yo‘naltirilgan va mustaqil bosqichlar alohida belgilangan. §1–5 ga sun’iy formula
qo‘shilmagan. §7 dagi `A = a ± delta_a` natija yozuvi kartada tushuntiriladi;
jadvaldagi 5 — bajariladigan FRQ hisoblash qoidalari soni.
Birinchi yetti mavzuda alohida raqamlangan laboratoriya yo‘q. Varaq qalinligi va
asbob tanlash kabi faoliyatlar rejalash/mulohaza sifatida beriladi: raqamli javob
haqiqiy tajriba bajarilganini bildirmaydi.

Kontent: `scripts/curriculum/physics/grade6_batch1.json`. Har karta, fakt, formula,
misol, yechim bosqichi va savolda book/chapter/topic ID, PDF/bosma sahifa, kitob va
sahifa matn hash’lari bor. `grade6_batch1_review.json` asl tasvir tekshiruvi,
ilmiy chegaralar va frozen kontent hash’ini saqlaydi. Validator source/catalog
mosligi, o‘rgatilgan fakt, mustaqil hisoblangan sonli javob, formula domeni va
publikatsiya cheklovini tekshiradi. Testlarda sonli javoblar alohida hisoblash
orakullari bilan ham tekshirilgan. Avtomatik test fan ekspertining o‘rnini bosmaydi.

## Ilmiy aniqlik bo‘yicha qarorlar

- PDF6–7: qadimgi atom tasavvuri zamonaviy «bo‘linmas atom» faktiga aylantirilmagan.
  Kopernik millati va teleskop ustuvorligiga oid ishonchsiz tarixiy iboralar
  dars/savollarga kiritilmagan.
- PDF10–11: Piza rivoyati isbotlangan tarixiy tajriba yoki havo qarshiligisiz
  hamma sharoitga tatbiq qilinadigan qonun sifatida o‘rgatilmaydi.
- PDF13: eski metall metr etaloni hozirgi SI ta’rifi sifatida berilmagan.
- PDF14: manba matnidagi «10 ichki chiziqcha» bilan `/10` hisobidagi tafovut
  ko‘r-ko‘rona ko‘chirilmagan. **Oraliqlar** sanaladi; 11 jami belgi → 10 oraliq.
- PDF15–16: yarim bo‘linma xatoligi faqat shu oddiy shkala modeli uchun.
  O‘rtacha natija barcha, jumladan sistematik xatolarni yo‘qotadi degan va’da yo‘q.

## Amaldagi FRQ v2

Yangi namespace: **`/preview/physics/v2`**, faqat Bearer token bilan.
`PHYSICS_PREVIEW_ENABLED=true` + `ENVIRONMENT=development|test` va SQLite yoki
loopbackdagi **staging nomli PostgreSQL DB** kerak. Default o‘chiq;
production/staging environment yoki public DB host bilan flag yoqilganida ham 404.

- `GET /catalog`: 7 tugun; avvalgi darsdan kamida 60% olinsa keyingisi ochiladi.
- `POST /lessons/{key}/start`: `assessment_version:2`, UUID `request_id`.
  Bir request ID bitta akkaunt/darsning o‘sha urinishini qayta ochadi. 24 soatlik
  tugallanmagan urinishdan keyin yangi urinish kerak; yakunlangan natija saqlanadi.
- `POST /attempts/{id}/answers`: question key + typed answer. Konseptual javob
  `choice_id`, tartiblash `order`, FRQ `formula`, `value`, `unit` yuboradi.
  Mijoz `is_correct`, score yoki XP yubormaydi; ortiqcha maydonlar rad etiladi.
- `POST /attempts/{id}/complete`: hamma savolga javob berilgach server yakunlaydi.

Sonlar exact rational/Decimal orqali hisoblanadi. Vergul/nuqta, ilmiy son yozuvi,
cheklangan arifmetik ifoda qabul qilinadi. Birlik SI qiymatiga keltiriladi; faqat
shu darsda tekshirilgan uzunlik birliklari va aniq aliaslar qabul qilinadi.
`kg`/`s` uzunlik javobiga mos kelmaydi; katta/kichik harf farqi saqlanadi.

Formula parseri `eval`, Python chaqiruvlari, atributlar, CAS yoki AI ishlatmaydi.
128 belgi/64 token/cheklangan AST chuqurligi, daraja va son hajmi bor.
Besh reviewed qoida: `100*x`, `x/1000`, `(b-a)/n`, `(x1+x2)/2`, `d/2`.
Ruxsat etilgan ekvivalentlar, kommutativ yig‘indi/ko‘paytma, `×`, `·`, `−` va
LHSsiz ifoda taniladi. Istalgan algebraik tenglikni umumiy isbotlash da’vosi yo‘q;
implicit ko‘paytirish, noma’lum belgi va o‘zboshimcha funksiya qabul qilinmaydi.
Absolute/relative tolerance va yaxlitlash grid’i testlangan. Birinchi partiyadagi
besh yangi masalaning javobi chekli va aniq; sun’iy yaxlitlash talabi qo‘shilmagan.
Murakkab birliklar, barcha SI o‘lchamlari, grafik javoblar, symbolic umumiy CAS va
bosqichli partial-credit rubric hali keyingi ishdir.

Javob kaliti/tolerance/equivalence/rubric faqat serverda. `/start` javobida ular
bo‘lmaydi. **Javob qabul qilingandan keyin** faqat shu savolning original feedbacki,
yechim bosqichlari va manbasi ochiladi. Format xatosi 422 bo‘lib, yechimni ochmaydi;
uni tahrirlash mumkin. Baholangan javob o‘zgartirilmaydi; xatodan so‘ng yangi
urinishda mashq qilish mumkin. Bir xil payload replay’i ayni natijani qaytaradi,
o‘zgartirilgan replay 409 oladi.

Birinchi muvaffaqiyatli yakun uchun **10 XP**, takroriy muvaffaqiyat uchun **0 XP**.
User/session lock, immutable answer fingerprint, progress va bitta StudyEvent
bir tranzaksiyada ishlaydi. Parallel ikki urinish ham birinchi XP’ni ikki marta
bermaydi. Streak/daily/league uchun mavjud account activity ledger ishlatiladi;
Biologiya progress/SRS/ID va tarixiy XP qayta yozilmaydi.

## Baza va moslik

`AssessmentBase` eski `Base.metadata`dan alohida: oddiy backend startup bu yangi
jadvallarni avtomatik yaratmaydi va Fizikani seed/import qilmaydi.
`0013_add_assessment_v2` explicit additive migration to‘rtta v2 jadval yaratadi.
Shared study tables eski installationda yo‘q bo‘lsa, ularni ham qo‘shadi;
ular bor bo‘lsa o‘zgartirmaydi. Downgrade shared Biology ledgerini o‘chirmaydi.
Alembic autogenerate ikkala metadata’ni biladi; v2 jadvallarini begona deb
`drop` taklif qilmasligi testlangan. Bu butun tarixiy Alembic chain’i har qanday
eski bazaga tekshirilgan degani emas: aynan 0013 upgrade legacy/staging schema’da sinovdan o‘tdi.

Explicit importer immutable key/SHA bilan ishlaydi, startupda ishlamaydi. U faqat
ikkita content jadvalini Core orqali reflect qiladi; legacy ORM/`services.db`ning
auto-migration import hooklarini yuklamaydi. Minimal eski user jadvali va tripwire
DB testida schema/data o‘zgarmasligi amalda tekshirildi. Oddiy PostgreSQL URL
installed psycopg2 driveriga moslanadi; CLI import ham haqiqiy stagingda tekshirildi:

```bash
python -m scripts.import_physics_preview --dry-run
# Faqat reviewed 0013 o‘tkazilgan lokal/test DB uchun:
# ENVIRONMENT=test DATABASE_URL=sqlite:////absolute/local-preview.db
python -m scripts.import_physics_preview --import-content
```

`DATABASE_URL`ni productiondan olmang. Importer explicit SQLite yoki loopback
PostgreSQL staging URLdan boshqasini rad etadi. Quyidagi sandbox usuli mavjud
lokal bazaga ham tegmaydi va birinchi sinov uchun afzal.

`/skills`, `/mobile/skills`, eski MCQ constraint/importer o‘zgarmagan.
`MOBILE_PUBLISHED_SUBJECTS=biologiya`, `BIOLOGY_ONLY=true`, `SUBJECTS_ONLY=true`
saqlangan. 406 Biology manifest + 47 checkpoint / 2 527 karta / 2 609 savolga
tegilmadi. Oddiy Physics xaritalari va 145 stage-one formula transkripsiyasi
saqlangan; yangi lokal darslar alohida artefaktdir.

## Flutter va lokal sinov

`PHYSICS_PREVIEW=true` va local/private `API_URL` bo‘lgandagina oddiy ilovada
Settings → «Fizika sinovi • 6-sinf» ochiladi. Default/production hostda deep link
ham Learn’ga qaytaradi. Ilmo original assetlari, indigo/sariq/firuza brendi,
3D tugmalar va mavjud motion widgetlari ishlatiladi. Bu preview faqat o‘zbekcha.

Kartalar → formula → namuna → mashqlar → server feedback → natija oqimi bor.
Son/formula/birlik maydonlari, belgi helperlari, tartiblash, source sheet, busy/error
va retry, account/origin/lesson bo‘yicha draft va urinishni qayta ochish ishlaydi.
Yuborilayotgan javob network timeout/restart orqali aynan saqlanib retry qilinadi;
server qabul qilgan javob resume’da yarashtiriladi. Dispose/account change’da
request cancel/mounted/generation guard bor. Server natijasi bo‘lganda umumiy
study revision yangilanadi. Javobdan keyin klaviatura yopilib feedbackga scroll
qilinadi; o‘quvchining kiritgan javobi alohida o‘qiladigan summaryda saqlanadi. Kichik/landscape ekran va 200% matn tekshirildi;
Reduce Motion’da cheksiz loading animatsiyasi matnga almashadi.

Standalone QA Android debug build uchun `PHYSICS_PREVIEW=true` va
`physics_preview_main.dart` targeti birga bo‘lsa `com.ilmai.app.physicsqa`,
`ILM AI Fizika QA`, `ilmai-physics-qa` callback ishlatiladigan Gradle konfiguratsiyasi
qo‘shildi. Oddiy `com.ilmai.app` / `ILM AI` / `ilmai` defaults saqlandi; preview
release task rad etiladi. XML va static default-contract test tekshirildi;
Android SDK bo‘lmagani uchun haqiqiy Gradle build/manifest merge tasdiqlanmagan.

Normal app loginini o‘zgartirmasdan, alohida **debug-only**
`lib/physics_preview_main.dart` lokal sandboxga ulanadi. Qoidalar: debug mode,
explicit flag, local/private URL, faqat sandbox test JWT. Oddiy main/OAuth bunga
bog‘lanmagan. Bu Google login tekshiruvi yoki production login bypass’i emas.

Backendda yangi, Gitdan tashqaridagi direktoriyani tanlang:

```bash
python -m scripts.serve_physics_preview --directory /tmp/ilm-physics-qa
# Keyin serverni o‘sha private sandbox/progress bilan qayta ochish:
python -m scripts.serve_physics_preview --directory /tmp/ilm-physics-qa --resume
```

Bu faqat yangi SQLite DBga schema/import va bitta aniq belgilangan QA account
qo‘shadi; `main`, eski DB, seedlar, public league yoki production bilan ishlamaydi.
Git ichidagi directory, mavjud begona fayl/directory yoki production environment
rad etiladi. Private `flutter-defines.json` 60 daqiqalik sandbox JWT saqlaydi:
uni Gitga yoki ommaviy joyga chiqarmang. Token eskirganda `--resume` va Flutter
qayta ishga tushirish/build kerak; progress o‘sha DBda qoladi.

Flutter checkoutda:

```bash
flutter run -d chrome --web-port 7357 -t lib/physics_preview_main.dart \
  --dart-define-from-file=/tmp/ilm-physics-qa/flutter-defines.json
```

CORS faqat lokal 7357 port uchun. API default 127.0.0.1:8887. Hech qanday haqiqiy
Google credential yoki production token talab qilinmaydi. Bular test ma’lumotlari.

Windows/USB Android amaliy buyruqlari va telefon QA:
Flutter repo **`PHYSICS_PREVIEW_QA.md`**.

## Haqiqiy tekshiruv natijalari

Yakuniy kod holatida amalda bajarilgan tekshiruvlar:

- Backend full suite: **681 passed, 3 skipped**, 13 old deprecation/SQLAlchemy warnings.
- Physics source + v2 targeted: **99 passed**.
- Lokal PostgreSQL16.15: old Biology/OAuth + yangi Physics testlari **3 passed**;
  final Physics-only qayta yugurish **1 passed**. 0013 migratsiya, immutable import,
  7 dars, parallel distinct attempts va legacy 137 XP/3 streak/2 stars saqlanishi.
  Biology testi 406 dars/faoliyat + 47 checkpointni shu isolated PG’da o‘qib/yakunlab tekshirgan.
- Flutter full suite: **141 passed**; yangi Physics: **15 passed**;
  explicit FRQ accessibility labels/Android minimum tap targets ham tekshirildi.
- `flutter analyze`: **No issues found**.
- Standart Flutter web **release JS** va alohida preview **debug web** build o‘tdi.
  Eski `flutter_tts`/secure-storage JS interop paketlari WASM dry-run ogohlantirishlarini
  chiqaradi; WASM build muvaffaqiyati da’vo qilinmaydi.
- Asl PDF + 14 page text/render hash: **pass**.
- Haqiqiy loopback HTTP: **7 dars, 43 javob, 5 FRQ, 70 XP**, completion replay o‘zgarmas.
- Chromium portrait/landscape: **§6, 2 konseptual javob va formula/170/cm FRQ haqiqiy API orqali o‘tdi; 390×844 va 640×320 tasvirlar ko‘rildi, JS page error yo‘q**. Bu Android testi emas.
- Android SDK topilmadi; native APK/iOS build, real telefon, TalkBack va native
  keyboard sinovi bajarilmadi. Linux desktop uchun ham toolchain yetishmaydi.

Hech qanday production deploy/migratsiya/main merge, AI Explain, PDF upload yoki
boshqa sinflar kontent generatsiyasi bajarilmagan. Umumiy nashrdan oldin mustaqil
fan/pedagog ekspertizasi va real Android QA kerak. **Keyingi aniq nuqta: 6-sinf
§8–17, faqat ushbu birinchi partiya hisobotidan keyingi foydalanuvchi tasdig‘i bilan.**


## Git va davom nuqtasi

- Backend: `feat/physics-curriculum-map`, `cb46a02` ustidan ushbu birinchi partiya.
- Flutter: `feat/physics-first-batch`, **`9f152f0`** (`79608c2` ustidan).
- Website: `054f0ce`, `feat/mobile-release-hardening`, ish daraxti o‘zgarishsiz.
- Source map/frozen Biology va eski user progress qayta yaratilmagan.
- §8–17 boshlanmagan. Keyingi bosqich tasdiqlansa, avval uning asl PDF sahifalari
  va tasvirlari ko‘riladi; formulalar va laboratoriya/uy amaliyoti talablari shundan
  keyin alohida ko‘rib chiqiladi. Bu batch validatorining qabul doirasi ataylab §1–7.
