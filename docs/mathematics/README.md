# ILM AI Matematika — joriy tekshirilgan davom

## 2026-11-04 — III qism 6–10: jami 83 lokal dars

Yangi 5 dars: 30 karta, 5 misol/15 qadam, 40 topshiriq, 11 sonli tenglik.
**I qism41/41, II qism32/33, III qism10/37 matnli mavzu**.
Jami **83 dars, 482 karta, 624 topshiriq, 83 misol/249 qadam,
127 sonli tenglik, 75 boshlang‘ich model turi**. Eski78 dars JSONlari o‘zgarmagan.
Faqat lokal preview; butun1–11kurs tugamagan, umumiy qolganlar soni noma’lum.

PDF16–25/bosma14–23ning to‘liq asl tasvirlari tekshirildi. Butun va uning
qismlari, bir xil birliklar, barcha tanlov mezonlarini tekshirish, joriy
natijadan ketma-ket hisob, noma’lum qism/qo‘shiluvchi va nol uchun original
masalalar yaratildi. Manbadagi birliksiz chang tortish/ovoz sonlariga watt
yoki dB to‘qilmadi; yil ko‘rsatilmagan taqvim va bayram sanasi tarixiy fakt
sifatida kiritilmadi. Tibbiy/dori konteksti matematik ko‘nikma uchun original
ko‘rgazma/qatnashchilar hisobi bilan almashtirildi. Har karta, savol, izoh,
sonli tenglik va misol qadami ikki aniq manba sahifasiga bog‘langan.

Flutterga butunni yig‘ish, talablar bo‘yicha bir/nechta/hech bir moslik,
strelkali yo‘l,53lik noma’lum qism va ustunli teskari jadval modellar qo‘shildi.
Nol va to‘liq qism, model almashganda eski76dan yangi53diapazonga tiklanish,
barcha talablar, ikkala mos model uchun soxta yagona g‘olib bo‘lmasligi tekshirildi.
II74 yo‘q; oldingi strict prerequisite va faqat explicit local QA bridge
saqlanadi. Missing74ga hech qanday progress yoki XP yaratilmaydi.

Math **113 passed,1 skipped (120.06 s)**. OwnloopbackPG16 qayta tiklangach
**1 passed (23.99 s)**:83dars/967XP (seed137), replay0, immutable import,
parallel reward va UID/streak himoyasi. Dastlab konteyner exit255 sabab
connectionrefused bo‘ldi; bu muvaffaqiyat deb yozilmadi. PrivateQAparoli xato
traceback ko‘rishda chiqib qolgani uchun aynan o‘zimizning lokal baza paroli
almashtirildi va private loglar redakt qilindi. Production credential ishlatilmadi.
Flutter yangi va oldingi IIIqism target **21 passed (11 s)**;5yangi to‘liq
320px/200%matn/ReduceMotion oqimi. Full Flutter **512 passed (2:47)**; analyze **0 muammo (3.8 s)**.
Debug JS web build34.4s (invalid compile-only token, localURL/UID;
Wasm dry-run o‘chirildi, brauzer/API/Android testi degani emas). Source audit23PDF/2958sahifa/83dars/166tanasahifasi.
Biology/Physics/OAuth11test oldingi5darscheckpointda o‘tdi; bu partiyada ularning
kodi o‘zgarmadi, yangi protected/fullbackend natijasi da’vo qilinmaydi.

**Keyingi:11-dars «Masalalar yechish»,PDF26–27/bosma24–25**, keyin manba14–17
(path12–15). 12–13 nazorat alohida tanasiz; tayyor darsga aylantirilmagan.
Keyingi10sahifa tasvirda o‘qildi, lekin hozirgi checkpointda dars sifatida import
qilinmagan. [Qamrov](PART3_PROGRESS.md), [dalil](checkpoints/grade1_part3_batch2.json).
Android/o‘qituvchi/pilot/rasmiy2026–27moslik not_verified. Frontend/normalapp/
auth/Gradle/boshqa fanlar/production/main o‘zgarmagan. PDF/OCR/kalit Gitga qo‘shilmadi.


## 2026-11-04 — III qism 1–5: jami 78 lokal dars

I qism 41/41 va II qismning 32/33 darsi o‘zgarmagan. III qismning 2024-yilgi
kitobidan dastlabki **5 dars** qo‘shildi: 30 karta, 5 original misol/15 qadam,
40 topshiriq va 8 sonli tenglik. Jami **78 dars, 452 karta, 584 topshiriq,
78 misol/234 qadam, 116 sonli tenglik, 70 boshlang‘ich model turi**.
Butun 1–11-sinf kursi tugamagan; umumiy qolgan mavzular soni noma’lum.
Faqat `local_test_preview_only`; pedagog, pilot va real Android tasdig‘i yo‘q.

III qismda 37 ta haqiqiy ikki sahifali mavzu chegarasi tasvirda tekshirildi
(PDF 6–79 / bosma 4–77). Birinchi 5 darsning to‘liq tanasi o‘qildi; qolgan
32 mavzuning sarlavha/sahifa chegarasi tekshirilishi ularning to‘liq mazmuni
tasdiqlandi degani emas. Mundarijadagi nazorat/o‘yin uchun 5 qo‘shimcha qatorning
alohida tanasi yo‘q; ular tayyor deb sanalmaydi. Raqamlash 1 dan qaytadi:
1–11, 14–26, 30–42. Takror 28 yoki yo‘q 29 qayta to‘qilmagan.
[37 chegara va hozirgi darslar](PART3_PROGRESS.md).

II qism 74-mavzusining bosma 68–69-sahifalari hali yo‘q. Oddiy prerequisite
saqlangan. III qismni lokal sinashga **alohida server flag** qo‘shildi:
`MATHEMATICS_QA_SOURCE_GAP_BRIDGE=true`, yoki standalone serverda
`--allow-known-part2-source-gap`. U faqat staging/dev/test, aniq II/III PDF
SHA jufti va mavjud 73 darsning barchasi bajarilganda ishlaydi. Default o‘chiq;
client parametri uni yoqolmaydi. `previous_book_complete=false` saqlanadi;
UIda yetishmagan 74 va sinov rejimi ochiq ko‘rsatiladi. Yetishmagan mavzuga
progress/XP yaratilmaydi. Flag o‘chsa tugallanmagan urinishning davom etishi
403 bilan to‘xtaydi, qoralama va progress o‘chmaydi; yana yoqilsa UUID bilan
aynan o‘sha urinish davom etadi. Boshqa kitob/sinf uchun umumiy bypass emas.
Normal ilova, auth, fan katalogi yoki production API o‘zgarmadi.

To‘liq manbali karta → misol → mustaqil masala; shart/savol/yechim/javob,
bitta tarmoqli algoritm, butun/qism, bir shartning turli ko‘rinishi va jadval
ustuni uchun original interaktiv modellar yaratildi. Yangi savollar kaliti
literal mustaqil testda; noto‘g‘ri qo‘lyozma manba kaliti deb olinmagan.
Server javob kalitlari mijozga chiqmaydi; assessment v1 orqaga mos.

Math **107 passed, 1 skipped (112.80 s)**; alohida own-loopback PG16
**1 passed (22.58 s)**; 78 dars/917 XP (boshlang‘ich 137), replay 0 XP,
parallel first reward, immutable reimport, boshqa UID himoyasi o‘tdi.
Flutter yangi to‘liq oqim/model/policy **10 passed (11 s)**, barcha 5 oqim
320px/200% matn/Reduce Motion bilan; analyze 0 muammo (1.8 s).
Biology/Physics/mobile OAuth **11 passed (30.18 s)**. 23 PDF/2958 sahifa,
78 to‘liq dars/156 tana sahifasi va III qismning 74 chegara pinlari auditi o‘tdi.
To‘liq Flutter **501 passed (2:41)**. Debug JS web build **35.1 s** (lokal URL/UID, invalid compile-only token);
Wasm dry-run dependency ogohlantirishlari bor, Wasm/brauzer/API/Android
sinovi o‘tdi degan da’vo yo‘q;
yangi to‘liq backend to‘plami natijasi da’vo qilinmaydi.

**Keyingi: III qism 6-dars «Butunni topishga doir masalalar»,
PDF 16–17 / bosma 14–15.** 6–10 tana sahifalari keyingi original partiya uchun
ko‘rildi, ammo ushbu checkpointda import qilinmagan. Android SDK/adb yo‘q;
o‘qituvchi/pilot/rasmiy 2026–27 moslik tekshirilmagan. Standalone positive CLI
Git-directory guard sabab bu cloud muhitida hali sinovdan o‘tmagan; himoya
chetlab o‘tilmadi. Ikkala repo PR GraphQL ruxsati Forbidden; PR da’vosi yo‘q.
Boshqa fanlar, frontend, production va main o‘zgarmagan. PDF/rasm/OCR/kalitlar Gitga kiritilmagan.

[Machine checkpoint](checkpoints/grade1_part3_batch1.json).


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


## 2026-11-04 — II qism62–68: jami68 dars

I qism41/41 o‘zgarmagan; II qism42–68dan27dars. Yangi7dars42karta/7originalmisolning21qadami/56topshiriq/12sonli tenglik. Jami68dars,392karta,504topshiriq,68misol/204qadam va96sonli tenglik. Butun1–11kurs hali tugallanmagan, umumiy mavzu soni noma’lum. Faqat lokal test.

| № | Mavzu | PDF | Bosma |
|---|---|---|---|
|62|Ikki xonali sonlarni taqqoslash|45–46|44–45|
|63|Ikki xonali sonlarni qo‘shish — xona usuli|47–48|46–47|
|64|Ikki xonali sonlarni qo‘shish — guruh/zanjir|49–50|48–49|
|65|Ikki xonali sonlarni qo‘shish — shart/noma’lum|51–52|50–51|
|66|Ikki xonali sonlarni ayirish — xona usuli|53–54|52–53|
|67|Ikki xonali sonlarni ayirish — qolgan miqdor|55–56|54–55|
|68|Ikki xonali sonlarni ayirish — teskari oila|57–58|56–57|

Hamma asl tasvirlar va native-text pinlari tekshirildi. Bir xil nomli mavzular qayta nomlangan soxta darslar emas: har biri o‘zining haqiqiy raqami/sahifasi hamda xona usuli, guruh sharti, noma’lum qo‘shiluvchi, qo‘shish/ayirish zanjiri yoki teskari bog‘lanish maqsadiga ega. Ikki xonali qo‘shish misollari birliklar yig‘indisi10dan kichik; ayirishda birliklar yetarli. Umumiy qoida yangi o‘nlik/borrowholatiga asossiz yoyilmadi. Normal parser umumiyCAS deb ko‘rsatilmaydi.

Mantiqiy shartlar aniq: qo‘shni ichki oraliqlar, ikki to‘liq rangli guruh, o‘yin navbati va faqat berilgan og‘irlik munosabati. Dori/termometr/kimyoviy idishlar haqidagi puzzle bolaga tibbiy yoki kimyoviy ko‘rsatma bo‘lib berilmadi. Dinozavrlar ratsionini o‘txo‘r/yirtqich bilan sun’iy to‘liq ikkiga bo‘lish o‘rniga aniq ikki rangli belgilar ishlatildi. Amaldagi do‘kon narxlari yoki yangi mahsulot valyutasi yaratilmagan; original belgi zaxirasi masalasi ishlatilgan.

Flutter:10–99taqqoslash, xonalar bo‘yicha bosqichli qo‘shish/ayirish, oldinga qo‘shish bilan noma’lumni topish va teskari4tenglik modeli.99li modeldan11–20ga qaytganda qiymatlar16/13ga tiklanadi; slider diapazoni buzilmaydi. Mashq/Ilmo/brend, serverbaholashi va progress saqlangan.

Math **94passed,1skipped86.00s**; ownloopbackPG16 **1passed19.84s**; Flutter Math **113passed1:19**; analyze **0issue1.9s**.7yangi oqim320px/200%matn/ReduceMotionda, literalto‘g‘ri/noto‘g‘ri javoblar/ordering/UUIDreplay tekshirildi. UID1old137XP→817/68progress, UID2XP0; replay0/parallel firstreward/immutableimport.23PDF/2958sahifa,68mavzu/136tanasahifasi sourceauditi. To‘liq Flutter472/web33.5s oldingi57–61checkpointniki, himoya46undan avvalgi natija; bu partiyada takrorlanmagan. Yangi to‘liq backend natijasi da’vo qilinmaydi.

Oldingi checkpoint GitHubda backend`049d777`/Flutter`42b333e`. Keyingi69«Qo‘shish bilan ayirish orasidagi bog‘lanish»PDF59–60/bosma58–59.69–73PDF59–68tasvirlari ko‘rildi; bu checkpointda import qilinmagan. IIqismda faqat5mavjudbodyqolgan,74bosma68–69manbasizblocked. Android/pedagog/pilot/rasmiydastur tekshiruvi yo‘q. Frontend/auth/Gradle/boshqa fanlar/production o‘zgarmadi. [Dalil](checkpoints/grade1_part2_batch5.json).


## 2026-11-04 — II qism57–61: jami61 dars

I qism41/41 saqlangan; II qism42–61dan20dars. Yangi5dars30karta/5originalmisolning15qadami/40topshiriq/10sonli tenglik. Jami61dars,350karta,448topshiriq,61misol/183qadam,84sonli tenglik. To‘liq1–11kurs hali tugamagan, umumiy mavzu soni noma’lum; faqat lokal test.

| № | Mavzu | PDF | Bosma |
|---|---|---|---|
|57|O‘nlikdan ayirish usuli|35–36|34–35|
|58|Yaxlit sonlar|37–38|36–37|
|59|21 dan100 gacha sonlar|39–40|38–39|
|60|21 dan100 gacha o‘qish/yozish|41–42|40–41|
|61|21 dan100 gacha o‘qish/yozish — cho‘t|43–44|42–43|

Asl tasvir va native-text pinlari tekshirildi. O‘nlikdan ayirishda alohida birliklar saqlanishi,10ta o‘nlik100birlik/1yuzlik ekanligi, qo‘shni sonlar,2/3/5/10qadam, xona qo‘shiluvchilari, cho‘t yo‘llari hamda shartdan son tuzish yoritildi. Raqamlari yig‘indisi5sharti bir nechta sonlarga mosligi ochiq aytildi; MCQda faqat bitta taklif etilgan javob mos. Darslikdagi «matematikaga oid ilk kitob» ustuvorligi haqidagi umumiy tarixiy da’vo kiritilmadi. Ruchka ixtirosining nisbiy yillari hozirgi tarixiy sana sifatida olinmadi. Qadimiy belgili puzzle faqat aniq berilgan original cheklangan kalit bilan ishlaydi.

Flutter: o‘nlikdan ayirish yo‘li,10–100o‘ntalab slider, 0–99jadval va alohida100, xavfsiz100chegarali qadam, o‘nlik/birlik modeli, faol toshi✓bilan ajralgan original cho‘t.100modelidan ikki xonali modelga o‘tganda holat42ga tiklanib noto‘g‘ri slider diapazoni kelib chiqmaydi. Cho‘tning6faol toshi42miqdorni bildirishi tekshirildi. 100dan keyingi qadam o‘chiq. Ilmo/brend va normalappsaqlangan.

Math **86passed,1skipped82.66s**; ownloopbackPG16 **1passed20.51s**; to‘liq Flutter **472passed2:15**; analyze **0issue1.5s**. DebugJS preview webbuild **33.5s**, lokalURL/testUID/invalidcompile-onlyplaceholder bilan; haqiqiyJWT buildga kiritilmadi. Bu brauzer/API yoki Android testi emas. UID1old137XP→747/61progress, UID2XP0; replay0/parallel firstreward/immutableimport o‘tdi.23PDF/2958sahifa va61mavzu/122tanasahifasi sourceauditi. Biology/Physics/OAuth46sinovi47–51checkpointda o‘tdi; bu safar takror bajarilmadi. Yangi to‘liq backend da’vosi yo‘q.

Oldingi checkpoint GitHubda backend`904aac0`/Flutter`f940d9a`. Keyingi62«Ikki xonali sonlarni taqqoslash»PDF45–46/bosma44–45.62–68PDF45–58tasvirlari ko‘rildi, bu checkpointda import qilinmagan. IIqism12mavjudbodyqolgan,74bosma68–69manbasizblocked. Android, pedagog/pilot va rasmiy2026–27tekshiruvi yo‘q. Frontend, auth, Gradle, boshqa fanlar, production o‘zgarmadi. [Dalil](checkpoints/grade1_part2_batch4.json).


## 2026-11-04 — II qism52–56: jami56 dars

I qism41/41 saqlangan; II qism42–56dan15dars. Yangi5dars30karta/5originalmisolning15qadami/40topshiriq/10sonli tenglik. Jami56dars,320karta,408topshiriq,56misol/168qadam,74sonli tenglik. To‘liq1–11kurs hali tugamagan, umumiy mavzu soni noma’lum; faqat lokal test.

| № | Mavzu | PDF | Bosma |
|---|---|---|---|
|52|O‘nlikdan o‘tib qo‘shish — to‘ldirish|25–26|24–25|
|53|O‘nlikdan o‘tib qo‘shish — qo‘llash|27–28|26–27|
|54|O‘nlikdan o‘tib qo‘shish — qadam/guruhlar|29–30|28–29|
|55|Sonlarni ayirish|31–32|30–31|
|56|Sonlarni bo‘laklab ayirish|33–34|32–33|

Asl tasvir va native-text pinlari tekshirildi; har kontent birligida manba bor. Original masalalarda sig‘im va massalar bir xilkgda, yo‘l davomiyligi kelishdagi soatdan farqlanadi, sug‘orish puzzle aniq12joyli ro‘yxatga aylantirildi, kesishgan ro‘yxatdagi bir joy qayta sanalmaydi. Sana masalasi ayni vaqtdagi aniq kun oralig‘i bilan yozildi. Ko‘lmak qurishidan ob-havo taxmin qilinmadi; kun/tun uzunligi universal fakt emas, berilgan jadval sifatida ishlatildi. Transportning tabiatga umuman zararsizligi kabi umumlashma kiritilmadi.

Flutterda o‘nlikka to‘ldirish, yo‘l qadamlari, o‘nlikni saqlab birliklardan ayirish va10orqali bo‘laklab ayirishning5modeli. Ikkinchi sonning ikkala qismi bir martadan ishlatiladi, model misoli o‘zgarsa qadam qayta boshlanadi. Original nuqtali guruhlar to‘liq o‘nlikka birlashadi; boshlanish joyi0qadam semantikasi bilan farqlanadi. Brend/Ilmo va servergrading/progress saqlangan.

Math **80passed,1skipped76.28s**; alohida ownPG16 **1passed16.94s**; Flutter Math **95passed1:08**; analyze **0issue1.7s**. Yangi5to‘liq oqim320px/200%matn/ReduceMotionda.137oldXP→697/56progress; boshqaUIDXP0; replay0/parallel firstreward/immutableimport o‘tdi. Oldingi Iqism tengliktesti partlocal11raqamini IIqism11bilan adashtirishi aniqlandi: test haqiqiygrade1/part1koordinatasiga scoped qilindi; javob yoki kontent o‘zgartirilmadi. Barcha yangi sonli literal javob va noto‘g‘ri alternativalar testlandi.23PDF/2958sahifa,56mavzu/112tana sahifasi hash auditi. To‘liq Flutter457 va himoya46natijalari oldingi47–51checkpointniki; bu partiyada takror bajarilmadi.

Oldingi checkpointlar GitHubda backend`704a9cd`/Flutter`cf5c581`. Keyingi57«O‘nlikdan ayirish usuli»PDF35–36/bosma34–35;57–61PDF35–44tasvirlari o‘qildi, bu checkpointda import qilinmagan. IIqism17mavjudbodyqolgan,74ning bosma68–69sahifalari manbasizblocked. Android/pedagog/pilot/rasmiydastur hali not_verified. Frontend, normalapp/auth, Gradle, boshqafanlar va production o‘zgarmadi. [Dalil](checkpoints/grade1_part2_batch3.json).


## 2026-11-04 — II qism47–51: jami51 dars

I qism41/41 muzlatilgan, II qism42–51dan10 dars tayyor. Yangi partiya30 karta,5original misol/15qadam,40topshiriq va9sonli tenglik; jami51dars,290karta,368topshiriq. Hali butun1–11kurs tugallanmagan, jami mavzular soni noma’lum. Faqat lokal test.

| № | Mavzu | PDF | Bosma |
|---|---|---|---|
|47|17 va18 sonlari|15–16|14–15|
|48|19 va20 sonlari|17–18|16–17|
|49|Sonlarni taqqoslash|19–20|18–19|
|50|Qavslar|21–22|20–21|
|51|Qavslar — ikkita guruh|23–24|22–23|

Asl tasvirlar ko‘rildi; hash/native-text bog‘lanishlari auditi o‘tdi. Qatorning faqat ichki qo‘shni oraliqlari,20dagi ikki o‘nlik, oxirgi raqam bo‘yicha juftlik, sig‘imga aynan tenglik va qavsli hisoblar original mashqlarda yoritildi. Kitobdagi terak/archa kislorod nisbati ilmiy umumlashma sifatida ishlatilmadi. Rasm yonidagi tartib yorliqlari miqdor deb olinmadi. Chapdan o‘ngga qoida faqat shu darsdagi+va−ga tegishli; ikki mustaqil qavsning boshqa to‘g‘ri hisoblash navbati ham mavjudligi tushuntirildi.

Flutter:17/18va19/20tarkib modeli; o‘nliklarni birliklardan oldin taqqoslash; qavsli/qavssiz15−(3+4)=8va15−3+4=16yo‘llarini qadam bilan ko‘rish; ikki qavs natijasidan keyingi tashqi amal. Manba bibliografiyasi/parttanlovi, Ilmo/brend saqlandi. Privategrading/answerkey mijozga yuborilmaydi. Backendda yangi5mavzuning literal javoblari/noto‘g‘ri alternativalari va qavsli muqobil sonli input/decimalcomma tekshirildi.

Haqiqiy natija: Math **74passed,1skipped51.23s**; ownloopbackPostgreSQL16 **1passed13.55s**; to‘liq Flutter **457passed2:00**; analyze **0issue1.8s**; Biology/Physics/mobileOAuth **46passed95.30s**.5yangi oqim320px/200%matn/ReduceMotion bilan o‘tdi. UID1old137XP→647/51progress, UID2XP0; replay0; parallel firstreward va immutable reimport. Sourceauditi23PDF/2958sahifa va51mavzu/102tanasahifasi. To‘liq backend yana ishga tushirilmadi; yangi webbuild hali bajarilmadi.

42–46 checkpointlari GitHubda: backend`0b579f2`, Flutter`b298590`. Hozirgi keyingi52PDF25–26/bosma24–25.52–56PDF25–34tasvirlari ko‘rildi, bu checkpointda import qilinmagan. IIqismda22mavjudbodyqolgan va74bosma68–69manbasizblocked. Beshta himoyalangan worktree HEAD/statuslari avvalgi checkpoint bilan bir xil va toza. Frontend/auth/Gradle/production/boshqafanlar o‘zgarmadi. Android, mustaqil pedagog/pilot/rasmiydastur tekshiruvi hali yo‘q. [Dalil](checkpoints/grade1_part2_batch2.json).


## 2026-11-04 — II qism42–46: jami46 tekshirilgan dars

I qismning41 darsi va barcha JSON/reviewlari byte-for-byte saqlandi. II qismning birinchi5 mavzusi qo‘shildi:30 karta,5 original misol/15 qadam,40 topshiriq va9 sonli tenglik. Jami46 dars,260 karta,328 topshiriq; butun1–11kurs tugallanmagan, jami/qolgan mavzu soni noma’lum. Nashr faqat lokal test, `course_ready=false`.

| № | Mavzu | PDF | Bosma |
|---|---|---|---|
|42|11 dan20 gacha bo‘lgan sonlar|5–6|4–5|
|43|11 dan20 gacha sonlarning o‘nlikda yozilishi|7–8|6–7|
|44|11 va12 sonlari|9–10|8–9|
|45|13 va14 sonlari|11–12|10–11|
|46|15 va16 sonlari|13–14|12–13|

Manbalar asl tasvir/native-text SHA bilan tekshirildi; qo‘lyozma javoblar kalit emas. Kitobdagi hayvonlarning yo‘qolish tezligi va terak/archa kislorod nisbati mustaqil tasdiqlanmagan; ilmiy fakt sifatida darsga kiritilmadi. Yomg‘irli kunlarda quyosh paneli umuman ishlamaydi degan xulosa qo‘llanilmadi. Uch bolaning1/2/3 miqdori kimga tegishliligini qo‘shimcha shartsiz aniqlab bo‘lmasligi ko‘rsatildi. Daraxtning ekilganidan beri vaqt uning to‘liq biologik yoshi deb olinmadi.

API: katalog faqat import qilingan kitoblarni `available_books` bilan qaytaradi. `source_number`42–46 part-local`sequence`1–5dan alohida. IIqism Iqismning barcha41mavzusi tugamaguncha serverda ham403`finish_previous_book` bilan yopiq. Kitob va mavzu ichki prerequisite birgalikda tekshiriladi; takror bajarish0XP. Source auditor reviewlarni haqiqiy `book_id` bo‘yicha ajratadi; birinchi kitobga tegishli ilk10formulasiz qoida endi faqat Iqismga scoped. Takror grade/part/sequence importda rad etiladi. DBschema yoki public normalappAPI o‘zgarmadi.

Flutter: alohida Math previewda kitob tanlash, haqiqiy IIqism ISBN/yil/sahifalar, o‘nlik/birlik va sonni qismlarga ajratish modellari.20 ikkita to‘liq o‘nlik va0 ortiqcha birlik bilan ko‘rsatiladi. Kitob almashish timeoutida eski katalog/tanlov saqlanadi va xato ko‘rinadi.422dan keyin tahrirlash qayta ochiladi, ekran javobdan uzoqqa sakramaydi. Ilmo/brend, UID/origin/draft va idempotency himoyalari saqlangan.

Haqiqiy testlar: Math **67passed,1skipped42.08s**; alohida loopbackPG16 **1passed11.93s**; to‘liq Flutter **449passed1:47**, analyze **0issue1.7s**;22targetedwidgettest o‘tdi.320px/200%matn/ReduceMotion bilan5yangi to‘liq oqim. Lokal UID1 eski137XP→597,46progress; UID2XP0/IIqismyopiq; parallel firstreward/replay/immutable import o‘tdi.23PDF/2958sahifa,46mavzu/92tana sahifasi hash auditi o‘tdi. Bu partiyada yangi web build yoki to‘liq backend to‘plami bajarilmadi; oldingi keng natijalar alohida tarixda.

IIqism74ning bosma68–69sahifalari hali yo‘q:33TOCmavzudan32bodymavjud,5tayyor,27mavjudbodyqolgan,1blocked. Keyingi47«17 va18sonlari»PDF15–16/bosma14–15;47–51PDF15–24tasvirlari ko‘rildi, hali bu checkpointda import qilinmagan.9-sinfAlgebra/11-sinfIqism32MiB transfer va6-sinfII/7–10Geometriya manba cheklovlari saqlangan.

Frontend, boshqa fanlar, Googlelogin, umumiyGradle va production o‘zgarmadi. AndroidSDK/realtelefon, mustaqil o‘qituvchi/pilot/rasmiy2026–27moslik not_verified. PostgreSQL konteyneri restartida dinamik port o‘zgargani sabab dastlab connectionrefused bo‘ldi; privateURL faqat owncontainerning yangi loopbackportiga yangilanib test qayta o‘tdi. Credential logga chiqarilmadi. Cloud Git-directoryguard chetlab o‘tilmadi; standaloneCLIpositive-run sinovi hali ochiq. [Machine checkpoint](checkpoints/grade1_part2_batch1.json).


## 2026-11-03 — joriy checkpoint

1-sinf I qism: 41/41 dars, 230 karta, 288 topshiriq. Butun 1–11-sinf kursi hali tugallanmagan.
Math: 65 passed. Alohida PG: 1 passed. Flutter: 440 passed. Analyze: 0 muammo.
II qism: 33 mundarija bo‘limi, 32 native lokator, 0 tayyor dars. 74-mavzuning bosma 68–69-sahifalari yo‘q.
Bu status oldingi checkpointlardan yangiroq. [To‘liq dalil va texnik davom](FIRST_BOOK_COMPLETION.md),
[machine checkpoint](checkpoints/grade1_part1_batch8.json).

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

23 PDF va 2958 sahifa inventari, 1-sinf I qismdagi 41 ta mundarija lokatori va 5 ta interaktiv dars yaratildi. 1–11-sinf to‘liq kursi hali tayyor emas.

- [Foydalanuvchi talablari](REQUIREMENTS.md)
- [Manba inventari](SOURCE_CATALOG.md)
- [Curriculum qamrovi](CURRICULUM_COVERAGE.md)
- [Pedagogika va mastery](PEDAGOGY_AND_MASTERY.md)
- [Interaktiv matematika engine](INTERACTIVE_MATH_ENGINE.md)
- [Manba review](SOURCE_REVIEW.md)
- [Haqiqiy QA](QA_REPORT.md)
- [Qayta boshlamasdan davom](RESUME_CHECKPOINT.md)
- [Tugallanish mezonlari](COURSE_COMPLETION.md)
