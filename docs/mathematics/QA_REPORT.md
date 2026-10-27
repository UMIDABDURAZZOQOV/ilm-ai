# Matematika QA — birinchi partiya

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
