# Matematika QA — birinchi partiya

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

2026-10-27. Tekshirilgan qamrov — **1-sinf, I qismning dastlabki 5 darsi**. 1–11-sinf kursi hali tugallanmagan.

- **backend_regression**: `2567 passed, 10 skipped, 2 deselected, 13 warnings in 1028.07s (0:17:08)`.
- **math_latest**: `47 passed, 1 skipped in 2.80s`.
- **postgres**: `1 passed in 3.03s`.
- **flutter_full**: `01:51 +382: All tests passed!`.
- **flutter_math**: `00:14 +13: All tests passed!`.
- **analyze**: `No issues found! (ran in 1.2s)`.

23 ta PDF, 2958 sahifaning mavjudligi, tartibi va SHA identifikatorlari tekshirildi. Dastlabki 5 darsning 10 ta tana sahifasi asl tasvirda o‘qildi. 29 karta, 5 ishlangan misolning 15 qadami va 30 topshiriq yaratildi. Birinchi qismdagi 41 ta mundarija birligi lokatorga bog‘langan; qolgan 36 mavzu uchun tana review va kontent kerak. PDF 55–56 bosma 52–53 ning takror skani bo‘lib, qo‘shimcha mavzu sifatida sanalmadi.

Bitta QA akkauntida 5 dars va 30 javob yakunlandi: eski 137 XP saqlanib, jami 187 XP bo‘ldi; shu kundagi 3 kunlik streak saqlandi. Progressni qayta ochish va replay 0 XP tekshirildi. Ikki parallel birinchi completion faqat bir marta 10 XP berdi. Soat bir xil bo‘lsa ham, javoblar tartibi tasodifiy UUID bilan almashmasligi tekshirildi.

Web debug JavaScript build 41.0 sekundda o‘tdi. Haqiqiy token o‘rniga yaroqsiz compile-only placeholder ishlatildi. Bu natija haqiqiy brauzer HTTP end-to-end sinovi emas.

## Test doirasi

Umumiy backend regressiyasi yangi source/setup guard testlari qo‘shilishidan avval kolleksiya qilingan. Keyingi 47 ta Matematika testi shu 4 ta yangi himoya sinovi va yangilangan misollarni ham alohida tekshiradi. Umumiy tekshiruvda 10 ta opt-in test skip qilindi; PostgreSQL sinovi alohida amalda o‘tdi. Ikki standalone positive sandbox testi chiqarildi. Git katalogi himoyasi chetlab o‘tilmadi; yangi CLI yaratish/resume oqimining ijobiy sinovi bu muhitda bajarilmagan. Matematikaning manfiy sandbox/production testlari esa 47 ta test ichida o‘tdi.

SQLite ASGI/TestClient va haqiqiy loopback PostgreSQL ishlatildi. PostgreSQL uchun o‘zimiz yaratgan tasodifiy staging sxemasi sinovdan keyin yopildi. Production bazaga ulanilmadi.

Flutter’ning 382 ta testi mavjud Auth/Biology/Physics/History regressionlari va 13 ta Matematika testini qamraydi. Dastlabki 5 darsning tushuntirish → misol → guided → MCQ/FRQ → natija oqimi 320×568 ekran va 200% matnda tekshirildi. Landscape va klaviatura inseti, ikki marta bosish, timeoutdan keyingi UUID replay, 422 xatosidan keyingi tahrir, origin/UID bo‘yicha qoralama ajralishi, har shaklni bir marta sanash va tasmalar masshtabi ham tekshirildi. Test transporti haqiqiy ASGI public DTO’laridan tuzilgan; bu telefon yoki Google login sinovi emas.

## Ochiq tekshiruvlar

- Android SDK/adb yo‘q. APK, TalkBack, signing, native lifecycle va past quvvatli haqiqiy telefon sinovi bajarilmagan.
- `.mathqa` Gradle patch Flutter branchida `git apply --check`dan o‘tdi, lekin qo‘llanmagan va compile qilinmagan. Hozirgi umumiy Gradle normal ilova bilan bir xil package berishi mumkin; integratsiya reviewdan oldin Math APK’ni oddiy ilova ustiga o‘rnatmang.
- Mustaqil matematika o‘qituvchisi ko‘rigi va rozilikli bola piloti yo‘q. Hali o‘qimagan bolalar uchun matn/klaviatura/audio mosligi, mustaqil transfer va bilimning saqlanishi tasdiqlanmagan.
- Normal mobil katalog, production router, ilg‘or symbolic/graph/interval/integral engine hamda qolgan mavzular bajarilmagan.
- Ikki katta PDF transferda bloklangan; yana beshta manba berilmagan. Ularsiz to‘liq 1–11-sinf qamrovi tasdiqlanmaydi.

Backend: [e60cdee](https://github.com/UMIDABDURAZZOQOV/ilm-ai/commit/e60cdee90b1ec3538e08bf6b8c76806d66e2e16b). Flutter: [86e7d30](https://github.com/UMIDABDURAZZOQOV/ilm-ai-flutter/commit/86e7d303c4f28b4239e5234c0a386b5004dc1ea1). [Mashina o‘qiydigan dalil](checkpoints/grade1_part1_batch1.json).
