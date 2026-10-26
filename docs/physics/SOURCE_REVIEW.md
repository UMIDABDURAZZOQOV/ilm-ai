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
