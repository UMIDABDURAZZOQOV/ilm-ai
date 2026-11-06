# ILM AI Beta — lokal telefon sinovi

2026-11-06: Beta registration now has one main action. Unconfigured Google is
explicitly identified; local device identity, secure tokens and saved progress
are reused. Google provider lookup uses verified `sub` first and requests an
account chooser once staging OAuth is configured. All subject cards remain
visible for every selected grade; readiness grades come from the existing full
catalogue. See Flutter `docs/BETA_GRADE_AVAILABILITY.md` and central CLAUDE.md.

**2026-10-31 yangilanish:** joriy alohida branch `feat/beta-subject-switch-ai-help`.
Learn ichida Fanlar orqali tez fan/sinf almashtirish va savolga bog‘langan
manbali izoh/chat ulandi. Haqiqiy AI token hozir yo‘q; tokensiz rejim aniq
belgilanadi. [To‘liq kontrakt va keyingi private konfiguratsiya](STUDY_HELP.md).
Quyidagi `--resume` va `install -r` buyruqlari yangi build uchun ham amal qiladi.

2026-10-29. Faqat ichki debug beta; production reliz emas.
Foydalanuvchi HTTPS staging va Google OAuth hozir yo‘qligini tasdiqladi va
lokal beta hamda sozlash talablarini tayyorlashni so‘radi.

## Muhit va ajratish

- Backend: `C:\Users\Page\Desktop\Projects\ilm-ai-beta`.
- Flutter: `C:\Users\Page\Desktop\Projects\ilm-ai-flutter-beta`.
- Ikkalasining joriy branchi: `feat/beta-subject-switch-ai-help`.
- Android package: `com.ilmai.app.beta`, nomi **ILM AI Beta**.
- Asosiy entrypoint: `lib/main.dart`; odatiy ILM AI splash/onboarding/navigatsiya.
- API: `http://127.0.0.1:8930`; faqat loopback. LAN/tashqi proxy bloklangan.
- Baza va server kaliti: `Projects\ilm-ai-beta-local`, Git tashqarisida.
- Alohida beta app storage; rasmiy ilova va oldingi QA app almashtirilmaydi.
- Manba PDF, OCR, foydalanuvchi bazasi, credential yoki token Gitga kirmaydi.

## Backendni boshlash

Quyidagi katalog allaqachon yaratilib, 1 381 birlik qat’iy import qilingan.
Bir PowerShell oynasida:

```powershell
Set-Location 'C:\Users\Page\Desktop\Projects\ilm-ai-beta'
python -u -X utf8 scripts/serve_mobile_beta.py `
  --directory 'C:\Users\Page\Desktop\Projects\ilm-ai-beta-local' `
  --resume --port 8930
```

Server darslik importlarini tekshiradi; muvaffaqiyatli ishga tushganda
`Integrated beta ready` va besh fan sonini chiqaradi. Ushbu oynani ochiq qoldiring.
To‘xtatish: Ctrl+C. Qayta ishga tushirish ham shu buyruq, `--resume` bilan.

Yangi mustaqil sinov bazasi kerak bo‘lsa, **mavjud bo‘lmagan boshqa katalog**
bilan `--resume`siz boshlanadi. Bu tayyor baza va progressni o‘chirmaydi.
Mavjud katalogni `--resume`siz ishlatish ataylab rad etiladi.

## Telefonga o‘rnatish

Telefonda USB debugging yoqilib, kompyuterning RSA ruxsati tasdiqlangan bo‘lsin.
Ikkinchi PowerShell oynasi:

```powershell
$adb = 'C:\Android\platform-tools\adb.exe'
& $adb devices -l
& $adb reverse tcp:8930 tcp:8930
& $adb install -r 'C:\Users\Page\Desktop\Projects\ilm-ai-flutter-beta\build\app\outputs\flutter-apk\app-debug.apk'
& $adb shell am start -n com.ilmai.app.beta/com.ilmai.ilm_ai_flutter.MainActivity
```

Bir nechta telefon bo‘lsa, har bir ADB buyrug‘iga `-s <devices ro‘yxatidagi serial>`
qo‘shing. `install -r` beta ilovani yangilaydi, uning progressini saqlaydi.
USB uzilib qayta ulanganda `adb reverse`ni qaytadan bajaring. Bu APK kompyuterdagi
lokal server ishlagan va reverse ulanishi mavjud paytda onlayn mashqlarni ishlatadi.

## Kirish va odatiy foydalanish

Til → Ilmo welcome → bitta **RO‘YXATDAN O‘TISH** tugmasi.
Google sozlangan bo‘lsa mavjud provayder oqimi ochiladi. Hozir sozlanmaganligi
va shu qurilmadagi ichki Beta akkaunti ishlatilishi ekranda aniq yoziladi.
Yangi akkaunt autentifikatsiyadan keyin onboardingni tugatadi; avval tugatgan
akkaunt Learn ekraniga kiradi. Haqiqiy saqlangan sessiya kirish ekranini chetlab
o‘tadi. Alohida “Menda akkaunt bor” yoki ikkinchi Google/local auth tugmasi yo‘q.
QA pairing kodi yoki alohida QA bosh menyusi yo‘q.

Ilova birinchi kirishda qurilmaning xavfsiz xotirasiga tasodifiy credential
yaratadi; server faqat uning SHA-256 hashini saqlaydi. Access/refresh tokenlar
oddiy auth oqimida runtime’da beriladi. Shu beta o‘rnatilishida qayta kirish
o‘sha akkauntni tiklaydi. Ilovani o‘chirib tashlash yoki uning storage’ini tozalash
ushbu lokal test identifikatorini yo‘qotadi; sinovlar uchun buni qilmang.

Sinf va fan → odatiy dars yo‘li → nazariya/formula/misol → MCQ/mavjud FRQ →
server feedback → natija/XP → keyingi dars. Boshqa fanlar fan tanlash orqali
ochiladi. Profil besh fan progressini birlashtiradi. Dars qoralamasi qurilmada,
tasdiqlangan javoblar va XP server bazasida saqlanadi.

| Fan | Sinflar | Birlik |
| --- | --- | ---: |
| Biologiya | 5–11 | 406 |
| Fizika | 6–11 | 316 |
| Kimyo | 7–11 | 268 |
| O‘zbekiston tarixi | 7–11 | 172 |
| Jahon tarixi | 6–11 | 219 |

Matematika/Ona tili ham ko‘rinadi — **Hozircha mavjud emas**, qulf bilan. Biologiyada FRQ yo‘q;
uning mavjud v1 nazariya/MCQ tizimi saqlangan. Qolgan fanlarda faqat avvalgi
tekshirilgan, mavzuga tegishli FRQ va editorlar ishlatiladi. Yangi AI kontent yo‘q.
Tarixdagi ochiq mulohaza vazifalari avtomatik baholanadi deb ko‘rsatilmaydi.
Beta boshqa fanlarning practice tabida bajarilgan darslarni qayta ishlashni
taklif qiladi; Biologiyaning mavjud daily/mistake/lightning mexanizmlari saqlanadi.

## HTTPS staging uchun hali zarur ishlar

Hozir staging server **yo‘q**. Lokal servisni internetga port-forward qilish yoki
uning loopback/source cheklovlarini o‘chirib tashlash tayyor staging yaratmaydi.

1. Productiondan ajratilgan, foydalanuvchiga tegishli domen va server tanlash.
2. TLS sertifikatli bitta HTTPS origin; backend porti va PostgreSQL tashqariga
   ochilmasin. Alohida staging DB/user/JWT kaliti; production bazasini ulash yo‘q.
3. Mavjud qat’iy subject preview/source/DB guardlarini saqlagan staging launcher
   va host allowlist/proxy ishonch chegaralarini alohida implementatsiya/test qilish.
   Hozirgi `serve_mobile_beta.py` ataylab loopback-only.
4. HTTPS stagingda `BETA_TEST_AUTH_ENABLED=false`; lokal test-login ochilmasin.
5. Flutter debug betani `INTEGRATED_BETA=true`, `API_URL` va `BETA_API_ORIGIN`
   bir xil **tasdiqlangan staging origin** bilan qayta yig‘ish. Hozirgi APK lokal.
6. Google login, qayta kirish, token refresh/logout va akkaunt ownership’ini
   haqiqiy telefon orqali yana boshidan oxirigacha tekshirish.

## Google OAuth uchun aniq talablar

Hozirgi ilova Google’ning server orqali web OAuth oqimini ishlatadi:
`/auth/google-login` → Google → backend `/auth/google-callback-mobile` →
`ilmai-beta://auth/callback?code=...&state=...` → PKCE bir martalik code exchange.
Asl `routers/auth.py` saqlangan; beta wrapper faqat oxirgi app scheme’ini o‘zgartiradi.

- Productiondan alohida Google Cloud OAuth loyiha/client va consent screen;
  test rejimida tasdiqlangan test foydalanuvchilari ro‘yxati.
- Hozirgi oqimga mos **Web application** OAuth client. Google Console authorized
  redirect URI backendning aniq `https://<staging-domain>/auth/google-callback-mobile`
  manziliga teng bo‘lishi kerak. `ilmai-beta://...` Google redirect URI sifatida
  ro‘yxatdan o‘tkazilmaydi; u backenddan ilovaga qaytish manzili.
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `MOBILE_OAUTH_REDIRECT_URI` faqat
  serverning secret store’ida. APK/dart-define/Git/chatga secret qo‘yilmaydi.
- Beta package/scheme production va QA bilan to‘qnashmasin. Hozir native Google
  Android SDK ishlatilmayapti; Android client + package/SHA fingerprint talablari
  shu SDK’ga alohida migratsiya qilinsa qo‘llanadi. Buni bajarildi deb hisoblamang.
- HTTPS callback, state/PKCE, bir martalik code, cancel/error, refresh/revoke,
  qayta ishlatilgan code va boshqa akkauntga kirishni rad etish tekshirilsin.
- Lokal OAuth uchun `--oauth-config-file` faqat tashqaridagi xususiy JSON faylni
  qabul qiladi (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`); hozir bunday fayl yo‘q,
  Google orqali real login tasdiqlanmagan.

Talablar [Google web-server OAuth hujjati](https://developers.google.com/identity/protocols/oauth2/web-server)
asosida tekshirildi: redirect aniq mosligi, serverda secret saqlash, HTTPS qoidalari.
Native mobil OAuth cheklovlari [Google native-app hujjatida](https://developers.google.com/identity/protocols/oauth2/native-app)
alohida ko‘rsatilgan. USB debugging/RSA va o‘rnatish uchun
[Android ADB hujjati](https://developer.android.com/tools/adb).
