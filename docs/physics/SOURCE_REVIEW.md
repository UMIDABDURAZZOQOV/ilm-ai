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

## 9-sinf §31–35 — sirt va qattiq jismlar (2026-10-26)

PDF/bosma94–106 ning barcha13 asl tasviri va OCR tekshirildi. F=sigma*l da l
samarali jami kontakt chizig‘i; igna modelidagi2*l ikki tomon ekanligi alohida.
W=sigma*S da S jami sirt yuzi. N/m va J/m2 bir xil fizik o‘lcham; serverdagi
oldingi `stiffness` dimension nomi force/length sifatida saqlandi, prujina
kontrakti o‘zgarmadi. Yangi yopiq aliaslar mN/m,J/m2,mJ/m2. sigma ni fizik
ma’noda prujina bikrligi deb o‘rgatmaymiz.

99-sahifadagi h=2*sigma/(rho*g*r) formula miqdoriy mashqlarda **ideal to‘liq
ho‘llash**,vertikal doiraviy kapillyar uchun cheklangan; noma’lum kontakt burchagi
va barcha ho‘llamaydigan chuqurliklarga universal tatbiq qilinmadi. Radius va
diametrning2omili tekshirildi. g=9.81N/kg va pi=3.14 aniq berilgan model
parametrlari. Balandlik73/4905m va radius73/98100m exact-rational rubrika
bilan faqat oxirida so‘ralgan gridga yaxlitlanadi.

101-sahifadagi tomchi soni1040 yaxlitlangan, aniq butun sonli o‘lchov emas.
Tomchi uzilishi m0=sigma*pi*d/g sodda kuch balansi yaqinlashuvi sifatida berildi.
Yupqa sovun pufagida ikki sirt bor; DW=8*pi*sigma*(R2^2-R1^2), bitta tomchiga
asossiz2omili qo‘yilmaydi. Original masalada R1=.01m,R2=.03m,sigma=.04N/m,
pi3.14 bilan DW=.00080384J mustaqil hisoblandi.103-sahifadagi laboratoriya
faqat shartli digital natijalar: F2-F1 baseline ayirmasi va2*l. Real tajriba
bajarildi degan belgi yoki uyda igna/sim/tomizg‘ich yasash topshirig‘i yo‘q.

104–106-sahifalarda kristall panjara,mono/poli,amorf va yo‘nalishga bog‘liqlik
tekshirildi. Har bir kristallning har bir xossasi doimo anizotrop,har qanday
polimer doimo izotrop kabi universal hukmlar talab qilinmaydi.106-sahifadagi
eski deraza pastki qismi qalinligini shishaning xona sharoitida sezilarli oqishiga
dalil qilish tekshirilgan fakt sifatida ishlatilmadi; mustaqil materialshunoslik
review’iga qayd qoldirildi. Kristall erishi sharoitga bog‘liq; amorfning yumshashi
bu bosqichda sun’iy hisoblash formulasiga aylantirilmadi. Biology,oldingi
curriculum,PDF va xarita o‘zgarmadi. Mustaqil ekspert/native Android/general
publication hali tasdiqlanmagan.

### Asl sahifa render auditi barqarorligi

9-sinf95/104-sahifalarda original PDF/OCR/native-text/2.2x raster to‘liq mos,
ammo2.2x dan keyingi2.0x PNG oldingi review PNG’sidan farq qildi. MuPDF
masshtablangan indeksli rasmlarni keshda saqlashi sababli render tarixi ta’siri
sun’iy476x474 palitrali test rasmining110/115punktli ko‘rinishlarida qayta
hosil qilindi. Audit endi katalog2.2x va review2.0x uchun alohida hujjat
kontekstlaridan foydalanadi; ikkala kutilgan xesh,PDF SHA/OCR/native/binding
tekshiruvlari saqlangan. Eski review yoki katalog xeshlari qayta yozilmadi.
2yangi regression ham haqiqiy cache farqini,ham buzilgan review xeshi rad
etilishini tekshiradi. Barcha552asl sahifa tekshiruvi tuzatishdan keyin o‘tdi.

## 9-sinf §36–40 — elastiklik va faza o‘zgarishi (2026-10-26)

PDF/bosma106–119 asl tasvirlari va OCR tekshirildi. DL=l-l0,eps=DL/l0,
sig=F/S=E*eps va k=E*S/l0 kichik chiziqli elastik o‘q bo‘ylab model bilan
beriladi. Mexanik sig va E Pa; elektr V yoki sirt sigma N/m bilan bir xil
kattalik deb o‘rgatilmaydi. Yopiq MPa/GPa aliaslari eski Pa/kPa fizik
kontraktini saqlaydi. E modda xossasi,k geometriyaga ham bog‘liq.

109-sahifadagi37namuna1 matnida4mm,berilgan/calculationda3mm.110-sahifadagi
namuna2 matnida6kg,berilganda4kg va g≈10 bilan hisob. Yangi masalalar boshqa,
izchil sonlarda;zid javob ko‘r-ko‘rona ko‘chirilmadi. O‘z og‘irligidagi simning
lmax=sigLimit/(rho*g) chegarasi **eng katta**,manbadagi «kamida» emas. g10 bu
qoida shartida aniq,eski9.81qoidalar o‘zgarmadi. Model real arqon/qurilish
yuk ruxsati,xavfsizlik zaxirasi yoki fizik uzish tajribasi emas.

111–113-grafikda qo‘rg‘oshin300→600K qiymatlari27/327°Cuchun kitobning273
yaqinlashuvi. Qattiq fazadagi0.1*130*300=3900J va erish platosi2500J
ajratildi. Temperatura platosi sof kristall,berilgan bosim,muvozanat modeli;
barcha qotishmalar yoki real qizish/sovish tarixlari aynan bir xil deyilmaydi.
114-muz lam334kJ/kg jadvali bilan115namunadagi336kJ/kg shart farqi qayd
etildi;yangi savolda berilgan qiymat izchil qo‘llanadi. Qotish signedQ=-lam*m,
berilgan modul musbat. Maksimal muz balansida muz boshlanishidaTmda,finalTm,
idish/tashqi almashinuv yo‘q;84/167kg faqat oxirida1ggridga yaxlitlanadi.

116–119-bug‘lanish va kondensatsiya bir temperaturadagi latent energiya bilan
ishlaydi. Suv r≈2.3MJ/kg normal qaynash uchun maktab qiymati. Qcond_TO_BODY
manfiy,chiqargan modul musbat. To‘yingan bug‘da oqimlar teng,jarayonlar to‘xtab
qolmagan. p=nkT faqat ideal yaqinlashuv,saturatsiya uchun yangi aniq holat
tenglamasi emas. Shamolni faqat energiya qo‘shish bilan izohlash,har doim havo
pufakchasi mavjudligi,tog‘da go‘sht hech qachon pishmasligi va germetik idishni
qizdirish ko‘rsatmasi tekshirilgan universal fakt/topshiriq sifatida olinmadi.

Yangi testda oldingi signed ish savollaridagi umumiy feedback xatosi ham
tasdiqlandi: sign_error uchun «manfiy bo‘lishi mumkin emas» shabloni manfiy
kutiladigan ish/Qga mos emas. Runtime faqat aynan shu eski shablonni neytral
ishora-konvensiyasi izohiga almashtiradi;grading,qoidalar,immutable snapshot,
oldin saqlangan replay response va XP o‘zgarmaydi. Ijobiy/manfiy eski issued
snapshotning API replay testi bor;yangi kontentning sign_error matni ham to‘g‘ri.
Eski dars JSONlari qayta yozilmadi. Birinchi yangi sinovda testning sign_error
kutishi noto‘g‘ri edi;API fixtureda eski savol FK importi ham yetishmasdi.
Ular testlarda tuzatildi,guard yoki FK pasaytirilmadi. Yakuniy natija progress
hujjatida qayd etiladi. Biology406/website/Chemistry/production/AIExplain saqlandi.

## 9-sinf §41–45 — namlik va yorug‘lik (2026-10-26)

PDF/bosma119–126 va131–138 asl tasvirlari/OCR ko‘rildi. Absolyut namlik
rho=m/V aynan suv bug‘ining massasi/havo hajmi,kg/m3 yoki g/m3. Pa bilan
bosim boshqa fizik kattalik. phi=rho/rhoSat yoki p/pSat **bir xil Tda**,p bug‘ning
parsial bosimi,umumiy atmosfera bosimi emas.100%namlikda molekulyar almashinuv
to‘xtamaydi.122-sahifadagi12.5g/m3/15°Cchizma120jadval12.8g/m3qiymatiga
yaqinlashtirilgan,aniq shudring nuqtasi oracle’i sifatida olinmadi.

Raqamli42-laboratoriyada121-jadvalning asl kataklari24°C/DT5→62%,20°C/DT4→66%,
28°C/DT7→53% tekshirildi.28°C/DT10katagidagi29shubhali,ishlatilmadi va taxminan
«tuzatilmadi».124-lab120/121ni aniq havola qiladi;shu batch ichidagi foundation
refs.43ning23-mashqlari126yuqorisida IVbob review’idan oldin davom etadi:
frozenend125saqlandi,faqat(topic43,page126)+extent_note whitelist qo‘shildi.
125dagi17°C/p2kPa misoli120jadvaldagi to‘yingan1.93kPa dan katta;barqaror
to‘yinmagan havo deb ko‘chirilmadi. Yangi ideal bug‘ misoliT300K/p1.662kPa/
M18g/mol/R8.31→rho.012kg/m3.125dagi8°CpSat1.06va120dagi1.07farqi yashirilmaydi;
berilgan qiymat bir hisobda izchil ishlatiladi. Real termometr yig‘ish/o‘lchov yo‘q.

Ryomerning284millionkm/22min natijasi~215151515m/s,215million esa yaxlitlangan.
132FizoN720,l8.6km,f12.67→313809408m/s,manbadagi313300000bilan aynan teng emas.
Yangi sonlar original va mustaqil hisoblangan. c=4*N*l*f faqat teng tish/tirqishli
ideal birinchi qorong‘ilanish sharti;Nbutun,faylanishHz,lbir tomon masofa.
Qaytish yo‘li2*l. Aniq c299792458m/s va maktab3e8yaqinlashuvi ajratildi.
Tez aylanuvchi g‘ildirak/kuchli nur qurilmasi topshirig‘i yo‘q.

Qaytish burchaklari normaldan,alpha=gamma; sirt bilan burchakb bo‘lsa90-b.
Yangi°/deg yopiq birligi radian bilan inexact pi orqali yashirin aylantirilmaydi;
eski rad ma’nosi saqlandi. Bu yerda mustaqil `angle_degrees` dimension bor.
n=c/v absolyut,n21=n2/n1=v1/v2=sin(alpha)/sin(beta)nisbiy. Sines FRQlarida
sina/sinb **berilgan sinus sonlari**,gradus burchagi emas;arbitrary trig/CAS
parser qo‘shilmadi. Normal tushishda0/0bilan n topilmaydi. Olingan sinus>1bo‘lsa
shu berilganlar uchun singan nur sifatida rad qilinadi. Muhitlar oddiy shaffof
maktab modeli bilan chegaralangan;manba n/vjadvali yaxlitlangan. Bir jinsli
geometrik nur modeli va parallel plastinka sharti boshqa holatlarga shartsiz
umumlashtirilmadi. Mustaqil ekspert/Android/ommaviy release tasdiqlanmagan.

## 9-sinf §46–50 — TIR, prizma va signed linza (2026-10-26)

PDF/bosma138–146 ning barcha9asl tasviri/OCR tekshirildi.46da bir xil vaqtdagi
s1/s2yo‘llar va n1*v1=n2*v2ishlatiladi. Normal ikki yonidagi nur kesmalari
orasidagi ichki geometrik theta=2*alpha,tezlik vektorlari orasidagi boshqa
burchak bilan almashtirilmaydi. Yassi ko‘zguda buyum/tasvir masofalari teng.

140-sahifada n1=1.5dan n2=1ga,alpha30°uchun beta42°berilishi xato:
sin(beta)=.75 → beta≈48.59037789°. alpha40°uchun≈74.61856831°(~75°),kritik
burchak≈41.81031490°(~42°). Bu agentning mustaqil hisob tekshiruvi;pedagogik
mutaxassis review’i bajarildi deyilmaydi. Yangi topshiriq bu xato42ni ko‘chirmaydi.
TIRn1>n2va alpha>alphaCrit;chegarada tenglik beta90°holatini ajratadi.
Tolada o‘zak nkatta va tushish burchagi sharti kerak;hamma nur yo‘qotishsiz
kafolat bilan uzatiladi deyilmaydi.

143-sahifadagi26-mashq4/5faqat «TIR kuzatildi»deydi,kritik burchakligi berilmagan.
Noma’lum nyagona son emas:n2<n1*sina yoki n1>n2/sina. Yangi savollar aniq
sinuslarda shu qat’iy chegarani tekshiradi;n1.5/sina.8→n2<1.2; n2=1.2/sina.75
→n1>1.6. Sonli criticalFRQda esa aynan sinCritberilgan:5/3faqat oxirida.001gridga
yaxlitlanadi. Sin37≈.6maktab yaqinlashuvi aniq trigonometrik tenglik emas.

49-labning73-rasmida birinchi yuzaga normal kirish bor. Faqat shu geometriyada
beta=A+gamma,n=sin(A+gamma)/sinA. FRQdagi sinExit/sinAochiq berilgan sinus
sonlari;istalgan prizma burchagiga umumiy formula emas. Raqamli qayd/ikkita
baho o‘rtachasi haqiqiy tajriba bajarilganini tasdiqlamaydi.

50da yangi signedF/Dqoidalari mavjud6-sinfdagi faqatF>0/D>0qoidalarni saqlagan
holda qo‘shildi. Sochuvchi F=-.2m→D=-5dptr. Eski lens_powerga manfiyFberish
hanuz rad qilinadi. Havodagi yupqa bikonveks radius formulasi n>1va R1/R2musbat
modullari uchun;arbitrarysignedradius/shaklga qo‘llanmaydi. Konveksning yig‘uvchi
bo‘lishi tashqi muhit shartiga bog‘liq. Quyosh kuydirish,kuchli nur,shisha/igna
qurilmasi yoki tibbiy amal topshirig‘i yo‘q. Noexpert/nativeAndroid/generalrelease
claim;Biology,website,Chemistry,productionvaAIExplain o‘zgarmadi.

## 9-sinf §51–55 — signed tasvir, asboblar va ko‘z (2026-10-26)

PDF/bosma146–156 asl tasvirlari/OCR to‘liq ko‘rildi. Bir xil signed konvensiya:
haqiqiy buyumd>0,yig‘uvchiF>0,sochuvchiF<0,haqiqiyf>0,mavhumf<0;
1/F=1/d+1/f.147-sahifadagi signedF/fmanfiy degan matndan so‘ng -1/F=1/d-1/f
formulasi berilishi modullar bilan ishlaganda mos,allaqachon signed sonlarga
esa ikki marta minus qiladi. Yangi dars izchil signed tenglamadan foydalanadi.
O‘lcham nisbati K=|f|/d,musbat fMagberilgan;tasvir orientatsiyasi alohida.
d=Fuchun chekli fyo‘q. Ideal uzoq obyekt nuqtasimon tasviri barcha keng
obyekt tasviri nuqta bo‘ladi degan universal da’vo qilinmaydi.

149-dagi kattalashtirish masalasida haqiqiy/mavhum turi berilmasa,ikkita shox
bo‘lishi mumkin:haqiqiy d=F*(1+1/K),mavhum d=F*(1-1/K). Yangi savollar
shoxni aniq aytadi. F=.4/K4uchun .5mva.3m alohida mustaqil testlar bilan.
53-lab shartli haqiqiy ekran:positive d/f.150dagi tartib Fbaholari→meanF→1/meanF;
mean(1/F)bilan almashtirilmaydi. .15/.20/.25m→meanF.20/D5,individual Dlar
mean47/9;bu farq regressionda tekshiriladi. Real lampa/linza/ekran amali yo‘q.

151-dagi K=D0/Fko‘z bo‘shashgan/uzoq yakuniy tasvir yoki maktab yaqinlashuv
modeli sifatida cheklangan;rasm/textyaqin nuqta holati uchun universal aniq
formula deb olinmadi. D0=.25mshartli tayanch,har bir odamning o‘lchangan yaqin
nuqtasi emas.153matnida obyektiv/okulyar nomlari152dagi84-rasm vazifalariga
nisbatan almashgan. Yangi dars buyum yaqinidagi obyektiv oraliq haqiqiy tasvir
hosil qilishi,ko‘z yaqinidagi okulyar lupa vazifasini ajratadi. K=lD0/(F1F2)
katta ajralishdagi maktab yaqinlashuvi,har qanday haqiqiy mikroskopning aniq
kattalashtirishi yoki resolution kafolati emas. Megapiksel katta bo‘lsa sifat
har doim yaxshi va optik mikroskop100000marta universal degan jumlalar
ko‘chirilmadi. Qo‘shimcha kitobdan tashqari formula talab qilinmadi.

55faqat konseptual sxema:to‘r pardadagi haqiqiy/inverted/kichik tasvir,
akkomodatsiya,ko‘z qismlari,binokulyar chuqurlik va oldin/ortda fokusning
kitobdagi minus/plus tuzatish chizmasi. n=1.5inson gavhari universal constanta,
to‘r parda oddiy sariq qoplama yoki ikki ko‘z tasvirlari aynan bir xil degan
soddalashtirishlar tekshirilgan miqdoriy fakt qilinmadi.15–20cmbarcha odamga
diagnostik chegara emas. Katta yoshdagi barcha o‘qish qiyinchiligini bir holatga
tenglash yo‘q;tasvirlangan sxema shaxsga tashxis/ko‘zoynak retsepti emas.
Mustaqil oftalmologik/pedagogik review bajarildi deyilmaydi. Biology406,oldingi
curriculum/progress,Flutterbrand,website,Chemistry,production,AIExplain saqlandi.

## 9-sinf §56–59 — yakuniy manba ko‘rigi (2026-10-26)

156–159va164–167 asl8sahifa/OCR ko‘rildi.160yuqoridagi57savollari ham kuzatildi,
lekin ulardan yangi manba da’vosi olinmadi;160–163bob review’i yangi raqamlangan
bo‘lim emas.59/59raqamlangan bo‘limlar tartibi,6laboratoriya va2amaliy faoliyat
saqlanadi.57–59ga sun’iy formula yoki nominal FRQqo‘shilmadi.

56kameraH=h*(d-F)/Fva d=F*(1+H/h)haqiqiy tasvir,positive balandlik modullari
doirasida. Source1561.76mhisob tekshirildi;yangi masalalar boshqa izchil sonlar.
Mikroskop hali kitobning soddalashtirilgan modeli.157yaqindan o‘qish masofasining
o‘zi insonning klinik ko‘zoynak retseptini aniqlamaydi. Yangi sonli misol shaxsga
bog‘lanmagan ikki conjugatli abstrakt yupqa linza: d=.25m,f=-.2m→D=-1dptr.

158«yillik energiya300–1340W/m2»yozuvi birlik jihatidan quvvat/yuzadir,
yillik energiya emas. Bu raqamlar universal doimiy yoki yangi yillik energiya
ma’lumotiga aylantirilmadi.159Parkent1987/1MWtavsifi kitob tarixi,bugungi
unumdorlik yoki dunyoda faqat ikki qurilma bor degan joriy tasdiq emas.
Geliotexnika energiya aylanishi/quritish/isitish/materiallar bilan o‘rganiladi;
nol barcha ekologik ta’sir,universal barcha telefon quyoshli yoki shifo
ko‘rsatmasi berilmaydi. Quyosh fokusida kuydirish topshirig‘i yo‘q.

164–165mexanik/elektromagnit/kvant manzara tarixiy doira va model chegaralari
bilan bayon qilinadi. Absolyut vaqt/bir onda ta’sir hozirgi universal fizik qonun
emas. Galiley birinchi inson tajribasi egasi yoki tabiatda faqat ikki fundamental
ta’sir bor degan da’vo yo‘q. Kitobdan tashqari kvant formulasi talab qilinmadi.
166printingXIXasrda ilk paydo bo‘lgan degan umumlashtirish ko‘chirilmadi.
167dagi32/37eski cross-refshu nashrdagi mavzularga mos kelmaydi,yadro mazmuni
taxminan yaratilmaydi. Institutlar kitobning tarixiy qaydi sifatida,asboblar
vazifasi esa optika/yarimo‘tkazgich tadqiqotlari bilan bog‘lanadi. Distraktorlar
shu fizik fan/asbob tushunchalaridan tuzildi,mahsulotning ichki texnik so‘zlari
kontentga kiritilmadi. Expert/nativeAndroid/prodrelease bajarildi deyilmaydi.

## 2026-10-26 — 10-sinf §1–5, PDF4–17 / bosma3–16

Asl butun PDFning matn xeshlari va barcha14 sahifa tasvirlari qayta tekshirildi.
Native matnda kasr/formula belgilarining bir qismi ajralib ketgan; formulalar
matndan taxmin qilinmadi, tasvirdagi kasr va indekslar o‘qildi. Bibliografiya
va manba SHA saqlandi. Bu sinfda PDF sahifasi bosma raqamdan1oldinda.

- §1: gipotezaning bir tajribada tasdiqlanishi cheksiz xatosiz qonun degani
  emas. Model, dalil, nazariya doirasi va moslik prinsipi farqlanadi.
  Konseptual mavzuga sun’iy sonli FRQ yoki formula qo‘shilmadi.
- PDF6 va14 jadvalida a/epsilon manfiy deb yozilgach yana minus qo‘llash
  mumkin bo‘lgan noaniqlik bor. Yangi koordinata va aylanish proyeksiyalari
  doim `+a*t²/2`, `omega0+beta*t` ko‘rinishida ishorali a/beta bilan ishlaydi.
  Eski dars/qoida bytes va baholash chegaralari almashtirilmadi.
- Vertikal model: qarshilik va ko‘taruvchi kuch tashlangan, doimiy g ochiq
  berilgan; otilgan balandlikka qaytish sharti alohida. Cho‘qqida v nol,
  g esa nol emas. v proyeksiyasi bilan uning musbat moduli boshqa kattalik.
- PDF14 urinma tezlanish har doim tezlik bilan bir yo‘nalishda degan jumla
  sekinlashishda o‘rinli emas. at ishorali, normal tarkib unga tik;
  umumiy modul Pifagor orqali tekshiriladi. `rad/s²` alohida yopiq birlik.
- Friksion/tasma/tishli nisbatlar sirpanmaslik va musbat modullar uchun.
  Ochiq/kesishgan tasma va tashqi tishlashish yo‘nalishi alohida savollar.
  Butun tishlar soni, nol radius/vaqt va noto‘g‘ri birliklar rad etiladi.

Asl manba tekshiruvi muallifning tekshiruvidir; mustaqil pedagog/fan eksperti
imzosi hamda native Android tajribasi deb ko‘rsatilmaydi. Fizika lokal/test
preview holatida, ommaviy nashr yoqilmadi.

## 2026-10-26 — 10-sinf §6–10, PDF17–25/29–36

Asl17 sahifa matni, formulalari, indekslari va tasvirlari qayta o‘qildi;
PDF=bosma+1. Har kontent birligi tegishli paragraf sahifalariga bog‘landi.

- PDF17 matnida o‘q boshi otilish nuqtasi deyiladi, ammo y=h−gt²/2 yerga
  bog‘langan koordinatadir. Yangi dars yer y=0, boshlang‘ich y=h, x=0 ni aniq
  belgilaydi. PDF18 vy=gt musbat moduli bilan yuqoriga o‘qdagi vy=−gt
  proyeksiyasi ajratiladi. Egri yo‘l va gorizontal uzoqlik boshqa kattalik.
- PDF21 uzoqlik «faqat gorizontal tarkib»ga bog‘liq degan jumla to‘liq emas:
  uchish vaqti vertikal tarkibga ham bog‘liq.45° maksimum faqat bir xil v0,
  bir xil boshlang‘ich/yakuniy balandlik va qarshiliksiz model uchun.
  PDF22 havodagi30–40° universal optimum sifatida ko‘chirilmadi.
- SinA/cosA savolda berilgan birliksiz ma’lumot; burchak gradusi emas.
  Umumiy trig/CAS solver qo‘shilmadi. To‘liq uzoqlikda exact unit-circle
  jufti tekshiriladi. sqrt(3)s savoli aniq kvadrat haqiqati va0,01s yakuniy
  grid bilan; oldingi exact-root himoyalar o‘zgarmadi.
- Laboratoriya8 faqat shartli jadval tahlili va uch qaydning o‘rtachasi.
  Ballistik moslama/metal sharcha bilan operational yo‘riqnoma berilmaydi,
  real o‘lchash bajarilgani aytilmaydi. PDF25 mashq8da omega2=100*pi,
  R1=30cm,R2=10cm dan omega1=100*pi/3rad/s va1000rpm chiqadi;
  bosilgan300rpm javob ko‘chirilmadi. Raqamlanmagan mashqlar alohida yangi
  curriculum bo‘limlari sifatida sun’iy ko‘paytirilmadi.
- PDF31 kuchlar muvozanatida teng/qarama-qarshilik aynan ikki kuchga xos;
  umumiy holatda vektor yig‘indi nol. Uchinchi qonun jufti turli jismlarda.
  F/a orqali massa aniqlashda0/0 ishlatilmaydi. Bir xil F bilan ikkita massa
  birlashtirilgandagi a=a1*a2/(a1+a2) sharti aniq.
- PDF34 nisbiy ko‘chish har doim kichik deyilishi teskari yo‘nalishda umumiy
  qoida emas. Galiley nisbiyligi klassik inersial to‘g‘ri siljishga tegishli.
  Yer aylanishining e’tiborsizligi barcha tajriba uchun mutlaq da’vo emas.
- PDF35 yuqoridagi2.4 `Fi=m*(aAbs−aRelative)` belgisi2.3
  `m*aRelative=F+Fi` hamda `F=m*aAbs` bilan mos emas. Shu tenglamalardan
  `Fi=m*(aRelative−aAbs)=−m*A` keladi; sahifa pastidagi manfiy ishora va
  sxema ham bunga mos. Yangi qoida faqat aylanmaydigan, tezlanib siljiydigan
  sistemada `Fi=−m*A`, `aRelative=F/m−A` ni ishlatadi. Mustaqil sonli
  tenglik testida m=2,F=10,A=3 uchun Fi=−6,ar=2 va m*ar=F+Fi=4.
  Aylanuvchi sistemalar uchun umumiy solver yaratilmagan.

Bu manbaga tayangan muallif tekshiruvi; mustaqil ekspert tasdig‘i emas.
Biologiya va oldingi Fizika darslarining immutable JSON/reviewlari saqlandi.

## 2026-10-26 — 10-sinf §11–15, PDF36–45/48–53

16 asl sahifaning native matni/formulalari/indekslari/tasvirlari qayta o‘qildi.
Inersial tavsifda gravitatsiya markazga intilma tezlanishni beradi; ikkinchi
haqiqiy centrifugal kuch bilan bekor bo‘lmaydi. v²=g*r da g orbitada, r
markazdan. PDF38 h=6,6R≈42000km radius va balandlikni aralashtiradi:
yangi dars r va h=r−R ni ajratadi, xato geostatsionar sonli kalit yo‘q.
T=T1*sqrt((r/R)^3) bir xil markaziy maydondagi aylana orbitalar uchun.

Tayanch P, gravitatsion mg va massa farqli; lift natijasi tezlik emas,
tezlanishga bog‘liq. Erkin tushishda P0, massa/gravitatsiya0emas.
Kontaktli modelda pastga a<=g. P/mg va mg/P teskari nisbatlari farqlandi.
Tinch ishqalanish maksimalgacha moslashadi, doim mu*N emas; tenglik
chegarasi o‘zi albatta tezlanib sirpanish emas. Yangi ramp savoli allaqachon
sirpanish/kinetik mu uchun, manfiy a sekinlashish sifatida mumkin.
Ideal Atwood shartlari va m2>m1 aniq. a,T har ikkala yukning Nyuton
balansiga qo‘yib tekshirildi; T=m1g=m2g deb olinmadi.

Ish Fpr*s signed, musbat proyeksiya aynan parallellik emas. Gravitywork
mg(h1−h2),E=K+U; ishqalanishda mexanik E saqlanishini umumiy energiya
saqlanishi bilan tenglashtirmaymiz. Ramp formulalari faqat tekis/parallel
pull/kinetikmu. PDF52(3.9) oxirida h tushgan;3.10 mgh bilan izchil,
yangi At shu3.10,eta3.11/finalscalarF3.12ga tayanadi. CotA tayyor
birliksiz qiymat, gradus emas. Digital lab15 shartli P,F,h,l jadvali;
real o‘lchov tasdig‘i yo‘q.0,01foiz punkti ulushda0,0001grid;8/11 va2/3
aniq private truth,72,73%/66,67% yakuniy yaxlitlangan javoblar.
Idealmu0 da eta1 mumkin,>1 rad etiladi. Eski JSON/review/qoida chegaralari
saqlandi. Mustaqil fan eksperti, real laboratoriya/nativeAndroid bajarilmagan.

## 2026-10-26 — 10-sinf §16–20, PDF54–57/60–72

17asl sahifa native xeshlari, formulalari va rasmlari solishtirildi.
Izolyatsiyalangan1D elastik modelda signed u1/u2, ikki impuls/energiya
balansi tekshiriladi; elastiklik vaqtinchalik deformatsiya umuman yo‘qligi
deb olinmaydi. Noelastik loss=Ki−Kf musbat, deltaK teskari ishorali.
PDF56mashq3ning7,8m/s/200GJ birligi va PDF57mashq7 gravitywork+4J,
mashq8 changeK+3J xatolari yangi kalitga ko‘chirilmadi.

Static netF0 bilan umumiy rigidbody moment sharti ajratildi. Massa markazi
hisobiy nuqta. Simmetrik arqonlarda phi HAR ARQONDAN VERTIKALGA:
PDF62 o‘zaro60° matni bilan PDF63har biri60° sxemasi aralashmadi.
Kuch yelkasi ta’sir CHIZIG‘IGACHA tik masofa. Clockwise musbat moment
F1*l1−F2*l2; PDF64 oxirgiF2l2−F2l2 typo ko‘chirilmadi. Juft momentF*d,
d ikkala chiziq orasida. F=P/n da n yukni ushlovchi butun ip segmentlari.
Eski moment qoidasi o‘qdan o‘tgan kuchning nol yelka/momentini to‘g‘ri
qabul qiladi: dastlabki testning nol yelkani rad etish talabi tuzatildi,
production qoida o‘zgarmadi, alohida nol moment assertionsaqlanadi.

Aylana radial kuch haqiqiy kuchlar yig‘indisi, bir jismdagi yangi NewtonIII
centrifugal juft emas. PDF67normal formulasi geometrik shart bilan:
ICHKI halqa topida N=m(v²/R−g),TASHQI qavariq topida N=m(g−v²/R).
Har ikkisida N>=0 kontakt tekshiruvi. PDF68R=v²/g faqat N0chegarasi,
contactR<=Rmax, tenglik barcha holatga majburlanmaydi. Operatsion chelak/
moto/halqa qurish sinovi berilmagan; manbada yo‘q M=I*beta qo‘shilmadi.

Statsionar/branchsiz oqimda mass conservation, siqilmas bir xilrho da
S1v1=S2v2. Bernoulli bir oqim chizig‘i/ideal/siqilmas/statsionar/nasos va
ishqalanish yo‘qotishisiz; balandlik ham ta’sir qiladi. PDF71bosim ishining
plus typosi emas, izchil final4.8 ishlatiladi. Signed dp=p1−p2, absolyutp2
manfiy bo‘lsa rad. Porshen modelida rho/g/yuza shartlari aniq;
source4.9m/s soni noto‘g‘ri, yangi original m/h/S bilan exactsqrt5 va
0,01m/sgrid. Umumiy trig/CAS/LLM yo‘q. Manba review muallif tekshiruvi,
mustaqil ekspert/nativeAndroid/realphysicalexperiment/prodclaim emas.


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
