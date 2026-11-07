# Google OAuth — yangi bepul staging uchun operator qadamlari

Staging: https://ilm-ai-103-stage-8b0727.onrender.com

Google kirishi hozir **o‘chirilgan**. Katalog/HTTPS sinovi muvaffaqiyatli o‘tgani
haqiqiy akkaunt orqali kirish ishlaganini anglatmaydi. Production client/serverga
o‘zgartirish kiritmang.

## Google Cloud’da

1. Production’dan alohida staging loyiha yoki tasdiqlangan test resursida Google
   Auth Platform consent/audience sozlamalarini tayyorlang. Testing holatida
   faqat o‘zingiz boshqaradigan test akkauntlarini qo‘shing.
2. OAuth client turini **Web application** deb tanlang. Bu ilovadagi brauzer orqali
   OAuth + backend callback oqimi uchun; API kaliti emas.
3. Authorized redirect URI aynan quyidagicha bo‘lsin:

   `https://ilm-ai-103-stage-8b0727.onrender.com/auth/google-callback-mobile`

   Scope: `openid email profile`. Production callback’ni almashtirmang.
4. Client JSON faylini yuklab, Git checkout’laridan tashqarida saqlang, masalan:

   `C:\Users\Page\.config\ilm-ai\staging-google.private.json`

5. Agentga **faqat fayl yo‘lini** yuboring. Client secret, token yoki JSON
   mazmunini chatga/Git’ga yubormang.

[Google rasmiy Web OAuth ko‘rsatmasi](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred).

## Agent keyin bajaradigan amallar

- Fayldagi client ID/redirect va uning production clientdan alohidaligini
  qiymatlarni oshkor qilmasdan tekshirish.
- Faqat yangi staging servisga `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` qo‘yish;
  `STAGING_AUTH_SETUP_PENDING=false`. Test-login/preview himoyalarini ochmaslik.
- Qat’iy staging validatorini qayta ishlatish va faqat stagingni deploy qilish.
  Render env-var PUT barcha qiymatlarni almashtiradi: tasodifan boshqa sozlamalar
  o‘chib ketmasin; production servis ID’sini qat’iy rad etish.
- Public PKCE/config preflightdan so‘ng haqiqiy test akkaunt bilan yangi/qaytgan
  akkaunt, boshqa akkaunt, cancellation, session/refresh/logout, progress va
  tarmoq uzilishi holatlarini tekshirish. Unit testni haqiqiy Google sinovi deb
  belgilamaslik.
- Zarur bo‘lganda `com.ilmai.app.staging`/`ilmai-staging` va aynan HTTPS API_URL
  bilan alohida Android build tayyorlash. Secret APK ichiga kiritilmaydi.
- ADB telefonni ko‘rsa o‘rnatish; ko‘rmasa o‘rnatilgan deb yozmaslik. Lokal Beta
  `com.ilmai.app.beta` va production `com.ilmai.app` ma’lumotlarini tozalamaslik.

Account deletion uchun alohida test mailbox/policy/storage va HTTPS tekshiruv
hali kerak. Hozir uni yoqish yoki production deploy/Play upload qilishga ruxsat
berilmagan. Chatda oshkor bo‘lgan Render kalitini chiqarishdan oldin almashtirish
talabi ham saqlanadi.
