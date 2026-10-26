# Fizika 316 bo‘lim: Android QA — 2026-10-26

**Holat:** bu cloud muhitida Android SDK va `adb` yo‘q. Quyidagi buyruqlar Windows uchun tayyorlangan, lekin Windows/Android’da bajarildi deb ko‘rsatilmaydi. Web build va Flutter widget testlari native Gradle, qurilma yoki pedagogik ekspertiza o‘rnini bosmaydi.

Fizika faqat lokal/test konfiguratsiyasida. Production API, mavjud bazalar va haqiqiy foydalanuvchi akkauntlari bilan import qilmang. Alohida debug kirish nuqtasi faqat maxsus sandbox JWT qabul qiladi; bu oddiy Google loginni chetlab o‘tish emas.

## Windows PowerShell: lokal backend

Python, Flutter, Android SDK va USB debugging tayyor bo‘lgach `flutter doctor -v` orqali muhitni tekshiring. Repository yo‘llarini o‘z kompyuteringizdagi yo‘llarga almashtiring.

Birinchi terminal, backend checkout:

```powershell
cd C:\Projects\ilm-ai
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$qaDir = Join-Path $env:LOCALAPPDATA 'ILMAI\physics-qa316'
python -m scripts.serve_physics_preview --directory $qaDir
```

Bu yangi, Gitdan tashqaridagi SQLite sandbox yaratadi, alohida test akkaunti va 316 darsni import qiladi. `main`/production startup va umumiy seed ishlatilmaydi. `flutter-defines.json` test tokenini saqlaydi: uni Gitga, chatga yoki ommaviy joyga yubormang. Token 60 daqiqalik.

Serverni keyingi safar avvalgi progress bilan ochish:

```powershell
python -m scripts.serve_physics_preview --directory $qaDir --resume
```

Bu tokenni yangilaydi va eski javob/XPni saqlaydi. Ochiq ilovani yangi konfiguratsiya bilan qayta yig‘ish yoki `flutter run` qilish kerak. Begona mavjud katalogni sandbox sifatida ishlatmang; skript uni rad etadi. Cloud muhitidagi sintetik `.git` mount cheklovi oddiy Windows katalogiga avtomatik tatbiq qilinmaydi, ammo skriptning Gitdan tashqari katalog talabi saqlanadi.

## USB orqali debug APK

Ikkinchi terminal, Flutter checkout. USB bilan ulangan telefonda developer options/USB debugging yoqilgan bo‘lsin:

```powershell
cd C:\Projects\ilm-ai-flutter
$qaDir = Join-Path $env:LOCALAPPDATA 'ILMAI\physics-qa316'
flutter doctor -v
flutter pub get
flutter analyze
flutter test
adb devices
adb reverse tcp:8887 tcp:8887
flutter build apk --debug -t lib/physics_preview_main.dart --dart-define-from-file="$qaDir\flutter-defines.json"
adb install -r .\build\app\outputs\flutter-apk\app-debug.apk
```

`adb reverse` telefonning `127.0.0.1:8887` manzilini kompyuterdagi lokal serverga bog‘laydi; LAN IP/tokenni qo‘lda ko‘chirish talab qilinmaydi. USB uzilib qayta ulansa reverse’ni takrorlash kerak bo‘lishi mumkin. Bir nechta qurilma bo‘lsa `adb -s DEVICE_ID ...` ishlating.

Mavjud Gradle konfiguratsiyasi bu debug target va `PHYSICS_PREVIEW=true` uchun alohida **`com.ilmai.app.physicsqa` / ILM AI Fizika QA** identifikatorini ko‘zda tutadi. Uning native manifest merge/APK qurilishi hali ushbu muhitda tekshirilmagan. Preview bilan release task bloklanadi; bu QA APK Play Market nashri uchun emas. Oddiy `com.ilmai.app` ilovasi o‘z identifikatorini saqlaydi.

## Telefonda aniq tekshirish

- 6–11-sinflar katalogi mos ravishda **61, 46, 60, 59, 45, 45** bo‘lim ko‘rsatsin. Fizika oddiy production katalogida ochilmasin.
- Har sinfning birinchi mavjud darsini oching; keyingi tugun oldingi dars tugamasdan ochilmasin. Oraliq tugallangan progress bilan navbatdagi bo‘lim mavjud bo‘lsin.
- Nazariya → namuna → guided mashq → mustaqil MCQ/FRQ → feedback → natija oqimini tekshiring. Uzun matn scroll bo‘lsin, pastdagi tugma klaviatura ostida qolmasin.
- Sonli qiymat, manfiy sath energiyasi, `3.313e-19`, vergulli decimal, `sqrt(...)`, `2^(-t/T)` va birlik maydonlarini sinang. Noto‘g‘ri formula, birlik, ishora va yaxlitlash uchun tushunarli feedback chiqsin.
- Bir javob/Continue tugmasini tez ikki marta bosing, tarmoqni uzib qayta yuboring. Shu dars yakuni uchun XP bir marta qo‘shilsin; xato javob/failed attempt yangi XP yaratmasin.
- Dars o‘rtasida ilovani yopib oching. Javoblar va dars davom nuqtasi tiklansin. Yakundan keyin Profil/progress yangilansin. Sandboxni `--resume` bilan qayta ishga tushirganda XP va javoblar qolishi kerak.
- Offline start, savol yuborish paytidagi uzilish, timeout, server to‘xtashi va retry holatini tekshiring. Mazmunsiz loading yoki soxta muvaffaqiyat bo‘lmasin.
- 320–360 px ekran, landscape, 200% matn va TalkBack’da savol, birlik hamda feedback o‘qilsin. Fokus, tugmalar kattaligi, klaviatura va Reduce Motion’ni tekshiring.
- Laboratoriya natijasi **raqamli hisob/tahlil** deb ko‘rsatilsin. Haqiqiy lazer, elektr yoki radioaktiv tajriba bajarilgani belgilanmasin.
- Ilmo, ILM AI logotipi va indigo `#2A1F6B`, sariq `#F9A825`, firuza `#2DD4BF` brendi saqlansin.

Bu alohida sandbox Google OAuth, production hisob, push notification yoki imzolangan release sinovini tasdiqlamaydi. Ular alohida qurilma/integratsiya QA bosqichidir. Ommaviy nashrdan oldin mustaqil fan/pedagogik ekspertiza va foydalanuvchining alohida release tasdig‘i talab qilinadi.
