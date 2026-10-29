# Fizika: formula, FRQ va bosqichma-bosqich implementatsiya loyihasi

> **Amaldagi holat — 2026-10-26:** 6–9-sinf to‘liq: 226/316 lokal/test dars. 90 bo‘lim qolgan (10/11-sinflar). Assessment v2, server grading, replay-safe XP va Flutter preview amalda. To‘liq backend1408/PG2/Flutter150/analyze toza. Keyingi10§1PDF4/bosma3. Eng yangi holat [STAGE2_PROGRESS.md](STAGE2_PROGRESS.md)da. Quyidagi 1-bosqich tasdiq kutish matni tarixiy; joriy ruxsatni cheklamaydi. Production/nashr/ekspert/nativeAndroid alohida qoladi.

**Eng yangi ruxsat — 2026-10-22:** foydalanuvchi barcha 316 bo‘lim bo‘yicha
oraliq tasdiqsiz davom etishni buyurdi. Runtime va mualliflikning joriy, haqiqiy
qamrovi [STAGE2_PROGRESS.md](STAGE2_PROGRESS.md)da. Quyidagi birinchi partiya
ruxsati hamda implementatsiyadan oldingi takliflar tarixiy qaydlardir.

**2026-10-22 amaldagi holat:** foydalanuvchi 2-bosqichning faqat **6-sinf §1–7**
partiyasiga ruxsat berdi. Bajarilgan tor v2 subset — concept/ordering va
formula+son+birlik FRQ; local/test-only endpointlar, opt-in migration, replay-safe XP
va Flutter inputlar. Tafsilotlar: [birinchi partiya](STAGE2_GRADE6_BATCH1.md).
Quyidagi umumiy formula/compound unit/partial-credit/graph rejalari to‘liq
implementatsiya qilingan deb talqin qilinmasin. AI Explain hali yaratilmagan.

## Saqlangan 1-bosqich taklifi

**Loyiha taklifi, implementatsiya emas.** Sana: 2026-10-21. Barcha yangi nomlar,
endpointlar, jadvallar va flaglar quyida taklif sifatida yozilgan; hozir mavjud deb
talqin qilinmasin. AI Explain bu ishga kiritilmaydi. 8/9-sinfning bo‘lak manbalari
o‘qildi; olti sinfning mavjud bo‘lim xaritalari tayyor. 7-sinfning bosma1–7 kirish
sahifalari foydalanuvchi qaroriga ko‘ra blok emas; mavjud §1–46 dan foydalaniladi.
Xarita tayyorligi barcha formula, fan faktlari yoki interaktiv kurs tayyorligi emas.

## Mavjud koddan kelib chiqadigan cheklovlar

| Mavjud modul | Haqiqiy holat | Keyingi bosqich uchun qaror |
|---|---|---|
| `services/models.py:SkillQuestion` | `question_type IN ('mcq')` DB constraint; variantlar va matn javob | Fizika FRQ’sini MCQ maydonlariga yashirin joylashtirmaslik |
| `services/study.py:grade` | Javob faqat snapshot variantlaridan olinadi; server baholaydi | Eski MCQ v1 o‘zgarmaydi; typed v2 grader alohida kiritiladi |
| `services/curriculum_validation.py` | Biologiya, 5–11-sinf, original karta/fakt/4 variant validatorlari | Biologiya validatorini susaytirmasdan alohida Physics schema/validator |
| `services/curriculum.py` | Importer Biologiya subjectini va immutable content key/SHA’ni ishlatadi | Subjectga umumlashtirish faqat regression bilan; Physics uchun explicit importer |
| `services/mobile_publication.py:reviewed_content` | Faqat reviewed Biologiya manifest key/SHA’lari | Faqat environment flagini o‘zgartirish Fizikani publish qilmaydi va yetarli emas |
| Flutter `SkillQuestion`, lesson UI | To‘rtta variant, matn javob, mavjud Ilmo/feedback/result | Capability bilan boshqariladigan typed input; MCQ ekranlari saqlanadi |
| Flutter `mobile_release.dart` va route guardlar | Biologiya-only, eski SAT/IELTS yashirin | Fizika nashri alohida tasdiqlanadi; eski modullar avtomatik ochilmaydi |

Mavjud server baholashi, bir martalik study event, replay fingerprinti, user locki,
XP/streak hisoblari va prerequisite tekshiruvlari qayta ishlatiladi. Yangi fizika
kontenti Biologiya course/unit/lesson ID’larini yoki tarixiy progressni qayta ishlatmaydi.

## Darsning manbaga bog‘langan modeli

Har dars: `book_id + source SHA + chapter_id + source_section_id + revision`.
Har karta, formula, namunaviy masala bosqichi, savol, javob izohi va rubric **o‘zining**
`source_refs` ro‘yxatiga ega: fayl/segment, PDF sahifa, bosma sahifa, paragraf,
kerak bo‘lsa boshqa paragrafdagi supporting source. Bitta lesson citationini hamma
savolga avtomatik nusxalash javobning tasdig‘i sifatida qabul qilinmaydi.

8/9-sinf uchun asl birlashtirilgan PDF hash’i to‘qilmaydi: tartiblangan segment
manifestining `source_set_sha256`si, har qismning haqiqiy SHA-256si, asl PDF va
qism ichidagi sahifa alohida saqlanadi. 9-sinf mundarijasi asl PDF172→173→171
tartibida o‘qiladi; original sahifalar qayta raqamlanmaydi.

Hisoblash darsi olti qismdan iborat:

1. Original qisqa nazariya kartalari; darslikning uzun matni yoki tayyor masalasi ko‘chirilmaydi.
2. Formula: belgi ma’nosi, shartlari, o‘lchov birligi, qo‘llanish chegarasi.
3. Original yechilgan namuna: berilgan → SI → formula → o‘rniga qo‘yish → hisob → birlik → tekshiruv.
4. Bosqichli mashq: har bosqichda aniq typed javob, xato turiga mos qisqa feedback.
5. Mustaqil FRQ: o‘quvchi formula, hisob va birlikni o‘zi kiritadi; A/B/C/D bilan cheklanmaydi.
6. Serverda deterministik baholash, izoh va mavjud XP/progress natijasi.

Konseptual mavzu: hodisani tartiblash, rasm/grafikdagi belgi, tajriba natijasini
taqqoslash, sabab-oqibat yoki cheklangan javobli tushuncha topshirig‘i. Ochiq erkin
esse’ni AI’siz avtomatik «to‘g‘ri» deb baholash va’da qilinmaydi; formal rubricga
sig‘magan matn o‘zini tekshirish/teacher review sifatida aniq belgilanadi.

Laboratoriya: manbadagi maqsad, o‘lchash jadvali, ma’lumot tahlili va xulosa bilan
raqamli faoliyat rejalashtiriladi. Simulyatsiya yoki berilgan jadvalni yechish real
tajriba bajarilganiga teng emas. Uy amaliyoti, amaliy topshiriq va laboratoriya
alohida turlardir. Elektr/optika/yadro mavzularida mos faoliyat va nazorat darajasi
manbadan tekshiriladi; ilova jismoniy bajarilganlikni o‘zi tasdiqlamaydi.

## Yangi assessment kontrakti taklifi

`CurriculumAssessment` nomli alohida v2 jadval/manifest qatlami tavsiya qilinadi:
`lesson_id`, `key`, `revision`, `schema_version`, `response_kind`, public prompt,
private `grading_spec`, `source_refs`. Bu eski `chk_skill_qtype`ni o‘zgartirishni
talab qilmaydi. Additive migration, PostgreSQL rehearsal va server/client capability
kelishuvi keyingi tasdiqlangan bosqichga tegishli.

Response turlari:

- `numeric_quantity`: son/sonli ifoda + birlik; istalsa alohida formula maydoni.
- `formula_expression`: ruxsat berilgan o‘zgaruvchilar bilan tenglama/ifoda.
- `calculation_steps`: formula, SIga o‘tkazish, qiymat, birlik uchun bosqichli rubric.
- `concept_selection`, `ordering`, `graph_interpretation`: manba bo‘yicha obyektiv tekshiriladigan faoliyat.
- Mavjud `mcq` v1 saqlanadi; eski API payloadlari FRQ deb talqin qilinmaydi.

V2 start response faqat input capability, ruxsatli belgilar, berilgan qiymatlar,
o‘lchov tizimi, vazifa va source’larni beradi. **Private expected answer/rubric**
serverdagi `StudySession` snapshotida qoladi. Variant bo‘lmagan javobni mavjud
`correct_answer` public maydoniga uzatish mumkin emas. Yangi endpoint nomi kelishilgach,
explicit `assessment_version: 2` bo‘ladi; eski clientga bunday dars yuborilmaydi.

Submit: `attempt_id`, `question_id/assessment_key`, `schema_version`, matn formula,
matn sonli ifoda, matn birlik va zarur bosqichlar. `is_correct`, `score`, `XP`
mijozdan ishonchli qiymat sifatida olinmaydi. Begona/takror ID, boshqa akkaunt,
snapshotga mos kelmagan revision va eskirgan urinish mavjud xavfsizlik qoidalariga
ko‘ra rad etiladi. Private grader/DB qiymatlari logga yozilmaydi.

## Deterministik formula va son parseri

1. Unicode bo‘shliq, minus, `×/·`, kasr, ustki daraja va lotin/grek aliaslari faqat
   assessment manifestida ruxsat etilgan kontekst bo‘yicha normallashtiriladi.
2. Sonlar `Decimal`/aniq rational orqali o‘qiladi. `1,25` va `1.25` decimal shakllari
   qabul qilinishi mumkin; vergulli ro‘yxat va minglik ajratgich noaniq bo‘lsa rad etiladi.
3. `NaN`, `Infinity`, boolean, noma’lum belgi, bo‘sh ifoda, nolga bo‘lish, massiv,
   assignment/import/function call, HTML/LaTeX command va juda uzun ifoda rad etiladi.
4. `eval`, `exec`, xom `sympify/parse_expr` ishlatilmaydi. Tokenizer + yopiq AST:
   raqam, ruxsatli symbol, qavs, `+ − * / ^`; zarur bo‘lsa explicit whitelistdagi
   `sqrt/sin/cos` tugunlari. Daraja, son uzunligi, token/chuqurlik/vaqt chegaralari bor.
5. Formula ekvivalentligi: muallif belgilagan domain ichida aniq algebraik normal
   shakl yoki oldindan tekshirilgan ekvivalent ASTlar. Masalan, bir manbadagi
   `ρ=m/V` uchun `m=ρV`ni qabul qilish tanlangan rubricga bog‘liq; formula boshqa
   noma’lumni talab qilsa, tenglikning o‘zi to‘liq javob emas.
6. Tasodifiy nuqtalarda son qo‘yish ekvivalentlikning isboti emas. Ratsional ifodalarda
   maxrajning noldan farqliligi, ildiz osti, musbat massa/vaqt va boshqa domain
   cheklovlari tekshiriladi. Whitelistdan tashqari ifoda taxminan qabul qilinmaydi.

Sonli tekshiruv:

```text
abs(actual_SI − expected_SI) <= max(abs_tol, rel_tol * abs(expected_SI))
```

`abs_tol`, `rel_tol`, yaxlitlash va significant-digit talabi **har masalada** yoziladi.
Nol kutilgan javobda ham `abs_tol` aniq bo‘lishi shart. Avval birlik va qiymat SIga
o‘tkaziladi, keyin taqqoslanadi; ekranga yaxlitlangan matn baholash bazasi emas.
Oraliq bosqichlarda yaxlitlashni kechiktirish va yakunda so‘ralgan aniqlikni saqlash kerak.

## Birlik, fizik kattalik va doimiylar

- Versionlangan birlik registri: 7 SI asosiy o‘lcham, hosilaviy birliklar, prefixlar
  va kursda haqiqatan ishlatilgan aliaslar. Har registr yozuvi source evidence bilan
  kiritiladi; tashqi bilimni kursga yashirin qo‘shish uchun ishlatilmaydi.
- `m/s`, `m·s⁻¹`, `km/soat` kabi ko‘rinishlar mos o‘lchamga tekshiriladi. `m` uzunlik,
  `m` milli-prefix, `M` mega-prefix va `N` birlik/katta harf farqlari kontekstga bog‘liq.
- `N` 6-sinfda quvvat belgisi ham (PDF74); `I` 7-sinfda kuch impulsi (PDF124),
  11-sinf PDF112da intensivlik. Symbol nomi global bitta ma’noga bog‘lanmaydi.
- `°C` absolyut temperatura va `Δ°C` farqi ajratiladi; gradus/radian burchak rejimi
  oldindan e’lon qilinadi. Vektor yo‘nalishi va skalyar modul alohida javob turidir.
- `g` manba/masala bo‘yicha tanlanadi: 6-sinf PDF68da **9,81 N/kg** yozilgan.
  Hamma masalaga o‘zboshimchalik bilan `g=10` yoki `g=9,8` qo‘yilmaydi. `π`, `c`, `h`
  va boshqa konstantalar ham source va talab qilingan aniqlik bilan manifestda saqlanadi.
- Birlik talab qilingan vazifada faqat sonni to‘g‘ri kiritish to‘liq javob emas.
  Muqobil mos birliklar konversiya orqali qabul qilinadi; noto‘g‘ri o‘lcham alohida
  `dimension_mismatch` feedbackini beradi.

### 8/9-sinf rasmlaridan aniqlangan kontrakt cheklovlari

- 8-sinf PDF82–83: C₃/U₃ oldidagi manba minuslari matndagi yig‘indi bilan zid;
  ularni avtomatik graderga kiritish mumkin emas. PDF124 A atom/molyar massa
  va Faradey doimiysi birliklari talqini ham alohida fan review talab qiladi.
- 9-sinf PDF109: §37 1-masalaning sharti va yechim jadvalidagi sonlar turlicha;
  bu misol tekshirilgan javob sifatida ishlatilmaydi.
- 9-sinf PDF145–147: linza radiusi va sochuvchi linza uchun masofalar/modullar
  ishora konvensiyasi kelishilmaguncha FRQ qoidasi yozilmaydi. PDF153 mikroskop
  modelidagi l talqini ham aniq belgilanadi.
- 9-sinf PDF22: T=t+273 kitobda yaxlitlangan; PDF133 c ning aniq va yaxlitlangan
  qiymati alohida berilgan. Har masala manbadagi aniqlikni e’lon qiladi.
- σ — sirt taranglik [N/m] yoki mexanik kuchlanish [Pa]; q — elektr zaryadi [C]
  yoki yonish issiqligi [J/kg]; C — sig‘im belgisi yoki kulon birligi; F — kuch,
  Faradey doimiysi yoki fokus belgisi. Global symbol almashinuvi ishlatilmaydi.

Bu yozuvlar manba review natijasi; runtime parser yoki yangi savol implementatsiyasi emas.

## Feedback, xavfsizlik va progress

Feedback toifalari: `invalid_expression`, `unknown_symbol`, `wrong_formula`,
`domain_error`, `wrong_unit`, `dimension_mismatch`, `conversion_error`, `sign_error`,
`out_of_tolerance`, `rounding_requirement`, `correct`. Har izoh oldindan yozilgan,
manbali va vazifaga mos; AI Explain endpointiga so‘rov qilinmaydi.

Bosqichli mashqda bo‘lak rubric o‘quv feedbacki beradi; bir darsni qayta yuborish
yangi XP bermaydi. Final complete mavjud tranzaksiya, user lock, immutable snapshot
va `StudyEvent` ledger bilan atomik bajariladi. Replay fingerprinti serverdagi
normallashtirilgan qiymat va rubric revisionga bog‘lanadi; mutlaqo boshqa javob bilan
yakunlangan urinishni almashtirish 409 bo‘ladi. Parallel retry, rollbackdan keyingi
retry, 24 soat expiry va account almashishi alohida testlanadi.

Flutter formula/son/birlik uchun alohida inputlar, oddiy keyboard va math toolbar,
TalkBack nomlari, 200% matn, scroll va IME insetlarini qo‘llaydi. Maxsus klaviaturani
ishlatolmagan o‘quvchi oddiy matn orqali ham javob kiritishi mumkin. Hisoblash/submit
paytida double-tap himoyasi, offline retry va draft tiklash bo‘ladi. Ilmo, mavjud
brend ranglari, Reduce Motion, Skill Path va natija ekranlari saqlanadi.

## 6-sinfdan ketma-ket implementatsiya partiyalari

**Hozir boshlanmaydi.** Mavjud olti sinfning bo‘lim xaritalari yakunlangan.
6-sinfni boshlash uchun foydalanuvchi tasdig‘i kutiladi. Har partiyaning to‘liq
matn/fakt/formula/birlik review’si dars yozilishidan oldin bajariladi; 145 tanlangan
transkripsiya butun olti kitobdagi formulalar tugaganini anglatmaydi.

| Partiya | Manbadagi tartib | Qamrov va tekshiruv |
|---|---|---|
| 0 | Assessment poydevori | Additive schema/API capability, parser/birlik/sonli grader; eski MCQ regression |
| 1 | 1–7 | Kirish, kuzatish, o‘lchash; konsept va manbada o‘tilgan birlik/aniqlik mashqlari |
| 2 | 8–17 | Modda tuzilishi, diffuziya, massa, zichlik; §13 uy amaliyoti, §15/17 laboratoriya |
| 3 | 18–29 | Harakat, tezlik, kuch, bosim, Arximed, ish/quvvat; §22 laboratoriya |
| 4 | 30–35 | Muvozanat, moment, oddiy mexanizm, FIK; §32 laboratoriya |
| 5 | 36–46 | Issiqlik va elektrga dastlabki kirish; §42 laboratoriya; sun’iy Q=cmΔT/Om mavzusi qo‘shilmaydi |
| 6 | 47–56 | Yorug‘lik, ko‘zgu, linza, spektr; §55/56 laboratoriya |
| 7 | 57–61 | Tovush, aks sado, shovqin; manbali hisoblash va konsept mashqlari |
| 8 | 6-sinf yakuni | Yetti haqiqiy bob va manbadagi nazoratlar, qamrov/prerequisite/XP regression |
| Keyin | 7 → 8 → 9 → 10 → 11 | Faqat tegishli manba xaritasi, formula inventari va oldingi sinf partiyalari tekshirilgach |

Har partiyada nazariya/formula/namuna/mashq/FRQ/rubric uchun source refs va original
mualliflik tekshiriladi; fan ekspertining belgi/ishora/aniqlik review’si qayd etiladi.
Import faqat explicit reviewed manifestdan; glob orqali draft publish qilinmaydi.
Partiya tugashi qolgan boblar yoki butun sinf tayyorligini bildirmaydi.

## Qabul testlari va nashr to‘siqlari

| Qatlam | Talab qilinadigan tekshiruv |
|---|---|
| Manba | 6 kitobning har sahifasi, segment uzilish/kesishish, SHA va ikkala raqam; barcha bob/paragraf/activity; noaniq OCR rasmdan |
| Formula | Algebraik muqobil shakl, domain, manfiy/vektor, ildiz/trigonometrik whitelist, yaroqsiz AST va resurs chegarasi |
| Son/birlik | Decimal vergul, ilmiy yozuv, SI prefix/konversiya, katta-kichik harf, nol javob, chegara tolerance, missing/wrong unit |
| Pedagogika | Faqat o‘tilgan faktni so‘rash, original misol, manbali javob/izoh; konseptga sun’iy formula yo‘q |
| API | V1 o‘zgarmaydi, V2 capability va maxfiy expected spec, forged score/ID, snapshot/replay/parallel retry |
| DB | SQLite + haqiqiy PostgreSQL additive migration/reimport; eski Biologiya ID/XP/streak/progress o‘zgarmaydi |
| Flutter | Formula/son/birlik inputi, Ilmo/feedback/result, barcha qo‘llab-quvvatlangan activity turi, offline/background/restore |
| Accessibility | 320px, landscape, 200% matn, TalkBack/focus, klaviatura overlay, Reduce Motion va real Android |
| Nashr | To‘liq evidence, ekspert review, foydalanuvchi tasdig‘i; Biology-only flag faqat alohida ruxsat bilan kengayadi |

Bugungi audit testlari faqat source-only katalogning izchilligini tekshiradi.
Yuqoridagi kelajak FRQ, UI, DB migration va telefon testlari **hali bajarilmagan**.
Production deploy/import/migratsiya, main merge yoki Play Market nashri reja
tasdig‘ining o‘zi bilan ruxsat etilgan hisoblanmaydi.
