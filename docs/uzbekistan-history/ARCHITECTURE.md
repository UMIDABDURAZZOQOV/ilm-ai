# Izolyatsiya va integratsiya chegaralari

Backend worktree:`/workspace/ilm-ai-uzbekistan-history`,basePhysics`e2aab00`. Flutter worktree:`/workspace/ilm-ai-flutter-uzbekistan-history`,base`ba2e0e2`. Ikkalasida`feat/uzbekistan-history-curriculum`. AslPhysics/vebworktreelari o‘zgartirilmaydi.

Kimyo backend`9b37213`/Flutter`0312ff3`,Jahon tarixi backend`720c279`/Flutter`8c3f1d1`read-onlyremote ref orqali o‘rganildi. Kimyo268tayyorligi uning o‘z hisobotida qayd etilgan;bu branchlar izolyatsiya qilinganPhysicsbasega merge qilinmagan. Hamma fanlar bitta integratedbranchda regressiondan o‘tdi deb aytilmaydi. Protectedbaseline552existingfileSHAni va parallelcheckpointlarni saqlaydi.

Yangi kod faqat`uzbekistan_history`fayl/namespace’ida bo‘lsin. Sharedmodels/router/Ilmo/Googlelogin/XP/progressmodullarini parallel branch bilan konfliktli tahrirlashdan oldin explicitintegrationpatch/handoff talab qilinadi. Alohida additive lokal/testadapter oldin manba va tushuntirilgan fakt kalitlarini tekshiradi. Production startupga seed/import/router avtoulanmaydi.

Dars kontrakti:nazariya→originalmisol→guidedmashq→MCQ/obyektivshortFRQ/xronologiya→manbali feedback→result→once-onlyXP/progress. Qisqa javoblar explicit tekshirilgan aliaslar bilan normalize qilinadi,fuzzy/LLMgrade yo‘q. Sabab-oqibat tahlili vaesse uchunteacher/selfreview rubrikasi,bitta satrkaliti bilan haqiqat/o‘qituvchi bahosi da’vosi yo‘q.

Har fakt/karta/savol/yechimda book_id,grade,chapter_id,topic_id,fact_id,PDF/bosma sahifa,verification,review_note bo‘lsin. OCRlocator xolos. Intra-pageboundary aniq saqlansin. Kelajakdagi checkpointhaqqoniy bobdagi barcha darslar o‘tilmaguncha ochilmasin. Independentteacher/Androidqa bo‘lmasa,nashr-ready false qoladi. AIExplain/Tutor/production/mainmerge ruxsat etilmagan.


2026-10-27 qayta read-only `ls-remote`: Jahon tarixi backend `e557c822de76ced5b66f303c4e690053dc643dcd`, Flutter `18647eec0efc2cb2ae3ffda0ceeead02a2876613`gacha davom etgan. Ularning remote branchiga push/merge/checkout qilinmadi; oldingi protected baseline ularni muzlatishga urinish emas, ushbu history worktree uchun boshlang‘ich himoya qaydi. Kimyo refs `9b37213`/`0312ff3` bo‘lib qoldi. Joriy integration qarorlarini bu mustaqil branchdan majburan almashtirmang.


## 2026-10-27 — to‘liq kontent qamrovi va nashr tasdig‘i

Catalog javobiga orqaga mos `course_content_complete` boolean qo‘shildi. U faqat
DBga haqiqatan import qilingan barcha5sinf ketma-ketligi manba katalogi bilan
bir xil bo‘lsa va bloklangan manba bo‘lmasa `true`. Bitta dars import qilinmagan
bo‘lsa, boshqa sinf to‘liq bo‘lsa ham umumiy flag `false` qoladi.
`grade_content_complete` faqat tanlangan sinfning import qamrovini ko‘rsatadi.
Bu belgilar o‘quvchining shaxsiy progressi yoki mustaqil pedagogik tasdiq emas.

`course_complete=false`, `course_ready=false`, `independent_review_pending=true`
va `publication=local_test_preview_only` saqlanadi. Normal API, Google login,
production router, boshqa fan va DB sxemasi o‘zgarmadi. Eski v2 mijozlar uchun
maydon qo‘shilishi ixtiyoriy; hech bir oldingi maydon yoki baholash qoidasi
almashtirilmagan. Manba katalogi bitta so‘rov ichida qayta o‘qilmaydi.

`tests/test_uzbekistan_history_completion.py` barcha172darsni bitta lokal
akkauntda asl sahifadan tuzilgan5sinf literal javoblari bilan tugatadi:
1027topshiriq,1720yangiXP,eski137XP saqlanishi,shu kuni3streak saqlanishi,
34bob yakun belgisi,qayta ochish va qayta urinishda0XP tekshiriladi.
Yo‘q import/manba umumiy qamrovni yolg‘on `true` qilmasligi ham tekshiriladi.
Bu ASGI/API va SQLite sinovi; haqiqiy telefon yoki production ma’lumotlari emas.
