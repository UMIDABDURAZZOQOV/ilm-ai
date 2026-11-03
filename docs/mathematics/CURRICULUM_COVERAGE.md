# Qamrov — boshlangan, to‘liq kurs emas

| Sinf/manba | Haqiqatan yozilgan dars | To‘liq curriculum xaritasi | Manba cheklovi |
|---|---:|---|---|
| 1-sinf I qism | 10 | partial: dastlabki10 tana tasviri; mundarijada41 mavzu | qolgan31 mavzu uchun kontent kerak |
| 1-sinf II–IV | 0 | pending | PDF mavjud |
| 2-sinf I–IV | 0 | pending | PDF mavjud |
| 3-sinf I–IV | 0 | pending | PDF mavjud |
| 4-sinf I–IV | 0 | pending | PDF mavjud |
| 5-sinf I–II | 0 | pending | PDF mavjud |
| 6-sinf I | 0 | pending | II qism source_missing |
| 7-sinf Algebra | 0 | pending | alohida Geometriya source_missing |
| 8-sinf Algebra | 0 | pending: skan | alohida Geometriya source_missing |
| 9-sinf Algebra | 0 | blocked | 32MiB transfer; Geometriya source_missing |
| 10-sinf Algebra | 0 | pending | alohida Geometriya source_missing |
| 11-sinf II | 0 | pending | I qism transferda bloklangan, prerequisite tekshirilsin |

**Umumiy haqiqiy mavzular soni hali aniqlanmagan.** To‘liq qolgan dars soni ham noma’lum; PDF sahifasini darsga tenglashtirmaymiz. TOCdan ajratilgan `toc_candidates.json` faqat locator: actual_heading_pdf_page null, `toc_text_candidate_not_body_verified`. Bular tayyor xarita/dars emas.

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

## Birinchi5 dars

| Tartib | Mavzu | PDF | Bosma | Karta | Guided | MCQ | FRQ | Transfer |
|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | Narsalarning xossalari | 5–6 | 4–5 | 6 | 3 | 1 | 1 | 1 |
| 2 | O‘xshashlik va farq | 7–8 | 6–7 | 6 | 3 | 1 | 1 | 1 |
| 3 | Narsalarning joylashishi | 9–10 | 8–9 | 5 | 3 | 1 | 1 | 1 |
| 4 | Narsalar sanog‘i | 11–12 | 10–11 | 6 | 3 | 1 | 1 | 1 |
| 5 | Yassi va hajmli shakllar | 13–14 | 12–13 | 6 | 3 | 1 | 1 | 1 |

Jami29 karta,5 original ishlangan misol/15 qadam,15 guided,5 MCQ,5 FRQ va5 yangi-vaziyat topshirig‘i. Response turlari: 19 choice, 8 short_text, 3 exact_number. Phase bilan response_kind bir xil sanoq emas. Erta konseptual mavzularga sun’iy formula qo‘shilmadi. 5 original interaktiv model bor; grafik/statistika/integral/haqiqiy3D engine hali yo‘q.

Keyingi aniq nuqta: **1-sinf I qism6 «Vaqt bo‘yicha ketma-ketlik», PDF15–16, bosma14–15**. PDF15–16 oldindan chiqarilgan, ammo ularning tanasi hali dars sifatida tasdiqlanmagan. Keyin7 «Narsalar guruhi», PDF17dan sarlavha chegarasini mustaqil tekshiring. Darslik xaritasi keyingi kontent bilan birga manba asosida yakunlansin.

2026–2027 rasmiy dastur bilan moslik `not_verified`: ushbu eski nashrlarni amaldagi dastur deb tasdiqlamaymiz; rasmiy manba qiyosi hali kerak.

## PDF sahifa mappingi: topilgan takror

1-sinfIpart PDF53–54 va55–56 asl tasvirlari ko‘rildi: ikkalasi ham25 «0 soni va raqami», bosma52–53ning takror skanlari. Pixel va nativeSHA boshqa, lekin topshiriq va qo‘lyozma javoblari bir xil.55–56 alohida mavzu yoki yangi bilim sifatida sanalmaydi. Bosma86mundarija PDF89da. Shuning uchun barcha sahifaga bir xil offset qo‘llash xato. Qo‘lyozma o‘quvchi javoblari darslikning tasdiqlangan javob kaliti emas.

`grade1_part1_map.json`:41TOCbirligi asl mundarija tasviri bilan nomlangan va native tana sarlavhalari lokatoriga bog‘langan. Faqat1–5tana sahifalari authored lesson reviewdan o‘tgan; qolgan36hali body review/content pending. Duplicate investigation25mavzuni tayyor dars qilmaydi.
