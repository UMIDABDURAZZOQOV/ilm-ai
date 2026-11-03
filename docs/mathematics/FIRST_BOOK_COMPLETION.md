# Matematika — birinchi kitob va aniq davom handoffi

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

## Manbali darslar

| № | Mavzu | PDF | Bosma | Karta | Topshiriq |
|---|---|---|---|---:|---:|
| 1 | Narsalarning xossalari | 5–6 | 4–5 | 6 | 6 |
| 2 | O‘xshashlik va farq | 7–8 | 6–7 | 6 | 6 |
| 3 | Narsalarning joylashishi | 9–10 | 8–9 | 5 | 6 |
| 4 | Narsalar sanog‘i | 11–12 | 10–11 | 6 | 6 |
| 5 | Yassi va hajmli shakllar | 13–14 | 12–13 | 6 | 6 |
| 6 | Vaqt bo‘yicha ketma-ketlik | 15–16 | 14–15 | 5 | 6 |
| 7 | Narsalar guruhi | 17–18 | 16–17 | 5 | 6 |
| 8 | Guruhlarni taqqoslash | 19–20 | 18–19 | 5 | 6 |
| 9 | 1 dan 10 gacha bo‘lgan sonlar | 21–22 | 20–21 | 5 | 6 |
| 10 | Narsalar sanog‘i | 23–24 | 22–23 | 5 | 6 |
| 11 | Qo‘shish | 25–26 | 24–25 | 5 | 6 |
| 12 | Ayirish | 27–28 | 26–27 | 5 | 6 |
| 13 | Sonlarni taqqoslash | 29–30 | 28–29 | 5 | 6 |
| 14 | 1 soni va raqami | 31–32 | 30–31 | 5 | 6 |
| 15 | 2 soni va raqami | 33–34 | 32–33 | 5 | 6 |
| 16 | 3 soni va raqami | 35–36 | 34–35 | 5 | 6 |
| 17 | 4 soni va raqami | 37–38 | 36–37 | 5 | 6 |
| 18 | 5 soni va raqami | 39–40 | 38–39 | 5 | 6 |
| 19 | 1 dan 5 gacha bo‘lgan sonlar | 41–42 | 40–41 | 5 | 6 |
| 20 | 1 dan 5 gacha bo‘lgan sonlar bilan amallar bajarish | 43–44 | 42–43 | 5 | 6 |
| 21 | 6 soni va raqami | 45–46 | 44–45 | 6 | 8 |
| 22 | 7 soni va raqami | 47–48 | 46–47 | 6 | 8 |
| 23 | 8 soni va raqami | 49–50 | 48–49 | 6 | 8 |
| 24 | 9 soni va raqami | 51–52 | 50–51 | 6 | 8 |
| 25 | 0 soni va raqami | 53–54 | 52–53 | 6 | 8 |
| 26 | 10 soni | 57–58 | 54–55 | 6 | 8 |
| 27 | 1 dan 10 gacha bo‘lgan sonlar. Sonlarni taqqoslash | 59–60 | 56–57 | 6 | 8 |
| 28 | Natural sonlar | 61–62 | 58–59 | 6 | 8 |
| 29 | Juft va toq sonlar | 63–64 | 60–61 | 6 | 8 |
| 30 | Nuqta. To‘g‘ri va egri chiziq | 65–66 | 62–63 | 6 | 8 |
| 31 | To‘g‘ri chiziq kesmasi. Siniq chiziq | 67–68 | 64–65 | 6 | 8 |
| 32 | Qo‘shish hadlari | 69–70 | 66–67 | 6 | 8 |
| 33 | Ayirish hadlari | 71–72 | 68–69 | 6 | 8 |
| 34 | Noma’lum qo‘shiluvchini topish | 73–74 | 70–71 | 6 | 8 |
| 35 | Noma’lum kamayuvchini topish | 75–76 | 72–73 | 6 | 8 |
| 36 | Noma’lum ayriluvchini topish | 77–78 | 74–75 | 6 | 8 |
| 37 | Qo‘shish va ayirish orasidagi o‘zaro bog‘liqlik | 79–80 | 76–77 | 6 | 8 |
| 38 | Qo‘shishning o‘rin almashtirish xossasi | 81–82 | 78–79 | 6 | 8 |
| 39 | Qo‘shish jadvali | 83–84 | 80–81 | 6 | 8 |
| 40 | Taqqoslash xossasi | 85–86 | 82–83 | 6 | 8 |
| 41 | Ifodalar | 87–88 | 84–85 | 6 | 8 |

## Qabul mezonlari

| Mezon | I qism | Barcha1–11sinf |
|---|---|---|
| Haqiqiy mavzular qamrovi | complete41/41 | partial; jami noma’lum |
| Original tushuntirish/mashq | barcha41da bor;yetarlilik ekspertizasi not_verified | partial |
| Visual completeness | boshlang‘ich modellar bor;pedagogik yetarlilik not_verified | partial;ilg‘or grafika/haqiqiy3D yo‘q |
| Matematik javob/manba | literaloracle,exactparser,manba/imageaudit o‘tdi | partial |
| Product quality | widget/API/PG o‘tdi;nativeAndroid not_verified | partial |
| Educational effectiveness | teacher/pilot/durablemastery not_verified | not_verified |

## Keyingi sessiya — aynan shu yerdan

1. Ikki Math worktreening HEAD/statusini va remote branchni tekshir. Reset/forcepush yo‘q.
   Birinchi8batchJSON/reviewlar muzlatilgan; avvalgi41darsni qayta yozma.
2. IIqism xaritasi source_number42–74;partlocal sequence1–33 bilan source_numberni
   ajrat. `math-1-2-1-r1` kabi yangi key va haqiqiybook_id/part2citation kerak.
3. `load_course` registryga yangi source-reviewed batch qo‘shishdan oldin auditni
   book_id bo‘yicha guruhla: hozir authored reviewlar birinchi kitobga tegishli.
   Birinchi10mavzuning formulasiz cheklovini faqatgrade1/part1ga scoped qil;
   part2sequence1dagi10+1kabi manbali tenglikni noto‘g‘ri rad etma.
4. Flutter repositorycatalogga grade/partquery va sinf/qism tanlovini qo‘sh;
   `_sources` hozir1-sinf/Iqismbibliografiyasi bilan yozilgan, haqiqiyrefga moslashsin.
   Umumiy normalapp/catalog/Gradlega tegma. Qoralama namespaceUID/origin/lessonkey
   himoyasi saqlansin. Partlar orasidagi prerequisite qoidasini ochiq testla.
5. IIqism42PDF5–6asl tasvirlarini qayta o‘qi: o‘nlik/birlik,11–20,10+birlik,
   qadamlar. Originalhouse-number problem bo‘lsa, raqamlash1dan boshlanishini
   aniq ayt. Qo‘lyozma javoblarni kalit sifatida olma. Pin evidence map2da.
6. Native32headinglocator — faqatlocator. Keyingi43dan73gacha barcha tanalarni
   haqiqiytasvirda o‘qi.74uchunbosma68–69manbasi yo‘q: shu mavzuni blocked qoldir.
   Keyin mavjudIII/IVmanbalarga o‘tish mumkin; yo‘q74ni taxmin qilma.
7. Har5–10yangi darsda explicitliteraloracle/API/XP/replay,Math/Flutter testlari,
   sourceaudit,CLAUDEva checkpoint,commit/push. Userdan takroriy davom ruxsati kerak emas.

Xususiy manbalar/rasmlar/log/helperlar `/workspace/.setup/mathematics` va
`/workspace/attachments`da; ulardan hech biri Gitga qo‘shilmasin. TestPG URL
`/workspace/.setup/mathematics/pg.url`da, mazmunini logga chiqarmang. O‘zimizning
Math container nomi `pg-container-name`faylida; tekshiruvdan so‘ng to‘xtatilgan,
keyingi sessiyada kerak bo‘lsa faqat shu own localcontainer qayta ishga tushsin.
Boshqa agent/Kimyo/JahonTarixi worktree va productionga tegmang.

Windowslocaldebug uchun oldingi `RESUME_CHECKPOINT.md`dagi standalonebuyruqlar
amal qiladi. Cloudgit-directoryguard chetlab o‘tilmagan; positiveCLIsetup/resume
hali sinovdan o‘tmagan. Android `.mathqa` patch qo‘llanmagan. SDK/realphone,
TalkBack/signing va ota-ona/o‘qituvchi rozilikli pilot alohida tekshiruvda.
