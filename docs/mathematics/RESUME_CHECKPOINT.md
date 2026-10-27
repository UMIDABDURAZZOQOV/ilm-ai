# Matematika — davom checkpointi

2026-10-27. Branch: `feat/mathematics-curriculum`. Backend code `e60cdee90b1ec3538e08bf6b8c76806d66e2e16b`, Flutter code `86e7d303c4f28b4239e5234c0a386b5004dc1ea1`. Worktreelar: `/workspace/ilm-ai-mathematics` va `/workspace/ilm-ai-flutter-mathematics`. Yangi sessiya avval status, log va remote SHA’ni tekshirsin; reset yoki overwrite qilmasin.

Dastlabki 5 dars tayyor: «Narsalarning xossalari», «O‘xshashlik va farq», «Narsalarning joylashishi», «Narsalar sanog‘i», «Yassi va hajmli shakllar». Jami 29 karta, 5 original misolning 15 qadami, 30 topshiriq va 5 interaktiv boshlang‘ich model. Math v1 alohida autentifikatsiyalangan API va 4 ta opt-in jadvalda ishlaydi. Aniq arifmetika parseri umumiy CAS emas. [QA doirasi](QA_REPORT.md), [dalil](checkpoints/grade1_part1_batch1.json).

- **backend_regression**: `2567 passed, 10 skipped, 2 deselected, 13 warnings in 1028.07s (0:17:08)`.
- **math_latest**: `47 passed, 1 skipped in 2.80s`.
- **postgres**: `1 passed in 3.03s`.
- **flutter_full**: `01:51 +382: All tests passed!`.
- **flutter_math**: `00:14 +13: All tests passed!`.
- **analyze**: `No issues found! (ran in 1.2s)`.

## Aniq davom nuqtasi

**1-sinf, I qism, 6-mavzu — «Vaqt bo‘yicha ketma-ketlik», PDF 15–16, mundarijada bosma 14–15.** Asl tasvirlarni qayta o‘qing: bu mavzu hali dars sifatida yaratilmagan. Keyin 7–10-mavzular keladi; native sarlavha lokatorlari PDF 17–24 da.

`load_course` hozir birinchi partiyani yuklaydi. Keyingi partiya uchun registry, source review va manbadan mustaqil tuzilgan literal javob testlarini kengaytiring. Birinchi 5 darsning JSON/review fayllarini va mavjud progressni qayta yozmang. Test javoblarini rubricdan olib yasamang. Vaqt/tartib yoki yangi visual/response turi kerak bo‘lsa, client/server kontrakti va versiya mosligi testlansin.

Barcha 23 mavjud PDF bo‘yicha to‘liq curriculum va tana review davom etishi kerak. Mundarija lokatori tayyor dars emas. Birinchi qismdagi 25-mavzuning kanonik sahifalari PDF 53–54; PDF 55–56 takror skan. Bosma 52–53 ikki marta sanalmaydi. Barcha kitob uchun bitta doimiy sahifa offsetini taxmin qilmang. Qo‘lyozma javoblar darslik javob kaliti emas.

9-sinf Algebra va 11-sinf I qism uchun 32 MiB’dan kichik segmentlar kerak. 6-sinf II qism va 7–10-sinf Geometriya manbalari yo‘q. Bu holat boshqa mavjud manbalardagi ishni to‘xtatmasin; yo‘q qism taxmin bilan to‘ldirilmasin. [Engine rejasi](INTERACTIVE_MATH_ENGINE.md)dagi grafik, geometriya, statistika, integral, ildiz, interval va domain tekshiruvlari hali implementatsiya qilinmagan.

## Muhit va ishga tushirish

23 asl PDF `/workspace/attachments`da; nom va SHA `source_manifest.json`da. Xususiy yo‘llar, loglar, tasvirlar va yordamchi scriptlar `/workspace/.setup/mathematics`da. Yangi muhitda fayllarni mavjud deb taxmin qilmang. Image pinlar PyMuPDF 1.26.6, RGB, 1.3 scale bilan olingan. Renderer farqini yashirmang: asl tasvirlarni qayta tekshiring. PDF, OCR, transkript, rasm va token Gitga qo‘shilmaydi.

Windowsda Gitdan tashqaridagi yangi xususiy papkadan foydalaning:

```powershell
python -m scripts.serve_mathematics_preview --directory C:\ILM-QA-PRIVATE\math
# Keyingi ishga tushirishda progressni saqlaydi:
python -m scripts.serve_mathematics_preview --directory C:\ILM-QA-PRIVATE\math --resume
```

Flutter worktree ichida:

```powershell
flutter run -d chrome --web-port 7358 -t lib/mathematics_preview_main.dart --dart-define-from-file=C:\ILM-QA-PRIVATE\math\flutter-defines.json
```

Defines faylida faqat lokal sandbox uchun maxfiy test JWT bo‘ladi; Gitga qo‘shmang. Ushbu cloudning yoziladigan ildizlarida Git markerlari bor, shuning uchun CLI’ning positive setup himoyasi chetlab o‘tilmadi. SQLite/ASGI va private PostgreSQL sxemasi alohida tekshirildi. Android identity patch hali qo‘llanmagan; Flutter’dagi Android handoffga qarang.

Normal main router, app katalogi, Google login, umumiy Gradle, frontend va boshqa fanlarga tegmang. Production DB/import/deploy, main merge, nashr va AI Tutor/Explain uchun ruxsat yo‘q. O‘qituvchi, pilot, real Android va rasmiy 2026–2027 dastur mosligi `not_verified`. Oddiy 5–10 darslik partiyalar uchun qayta tasdiq kutish shart emas: manba → matematik/API testlari → Flutter → hujjatlar → commit/push.
