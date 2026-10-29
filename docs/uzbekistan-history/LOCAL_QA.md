# Faqat lokal/test O‘zbekiston tarixi adapteri

Normal `main`, mobil fanlar katalogi, Google login va boshqa fanlarning endpointlari o‘zgartirilmagan. Alohida `/preview/uzbekistan-history/v2` routeri production ilovaga ulanmagan. Preview ikki shartda ishlaydi: `UZBEKISTAN_HISTORY_PREVIEW_ENABLED=true`, `ENVIRONMENT=test|development`; DB ham nomi `uzbekistan_history_staging` bo‘lgan lokal SQLite yoki loopback staging PostgreSQL bo‘lishi kerak.

To‘rtta qo‘shimcha `uzbekistan_history_preview_*` jadvali bor. Mavjud foydalanuvchi, sessiya va XP/activity ledger bilan FK/transaction orqali ishlaydi. Sessiya turi `uz_history_assessment_v2` mavjud `varchar(24)` chegarasiga sig‘adi. Asl uzun nomning PostgreSQL xatosi testda qayta hosil qilindi va umumiy sxemani o‘zgartirmay tuzatildi.

`assessment_version=2`, autentifikatsiya va server baholashi majburiy. MCQ variant ID, qisqa ism/atama va xronologiya tartibi tekshiriladi. FRQ explicit manbadan tasdiqlangan aliaslar, katta-kichik harf, nuqta va o‘zbek apostrofi ko‘rinishlarini qabul qiladi. Fuzzy, LLM yoki erkin esse uchun avtomatik baho yo‘q. Noto‘g‘ri javob uchun oldindan yozilgan izoh bor. Takroriy jo‘natish ayni natijani qaytaradi; o‘zgargan javob/session identifikatori konflikt beradi. 24 soatlik urinish, oldingi darsning muvaffaqiyatli tugashi va akkount egaligi tekshiriladi.

Har bir bobning barcha manba mavzulari tugamaguncha yakun belgisi ochilmaydi. Hozir bu **bob tugallanish belgisi**, alohida checkpoint testi emas. Alohida bob testi hali yaratilmagan. O‘quvchi refleksiyalari self/teacher review uchun; ularga avtomatik to‘g‘ri/noto‘g‘ri ball qo‘yilmaydi.

## Xavfsiz lokal ishga tushirish

Python virtualenv va Flutter bog‘liqliklari o‘rnatilgan kompyuterda, barcha Git repozitoriyalaridan tashqaridagi yangi maxsus papkadan foydalaning:

```bash
python -m scripts.serve_uzbekistan_history_preview --directory /ABSOLUTE/PRIVATE/history-qa
# Keyingi ishga tushirishda progressni saqlash va bir soatlik test JWTni yangilash:
python -m scripts.serve_uzbekistan_history_preview --directory /ABSOLUTE/PRIVATE/history-qa --resume
```

Script production rejimni, symlinkni va Git ichidagi katalogni rad etadi. Yangi sandbox faqat maxsus test foydalanuvchisi va alohida SQLite bazasini yaratadi. `--resume` avvalgi progressni o‘chirmaydi; import xeshi mos kelmagan eski revisionni qayta yozmaydi. Maxfiy `flutter-defines.json`, DB va setup loglarini Gitga qo‘shmang. Scriptning yangi sandbox yaratishi joriy cloud muhitida to‘liq bajarilmadi: ikkala yoziladigan ildizda `/workspace/.git` va `/tmp/.git` markerlari bor. Guard chetlab o‘tilmagan. DB/API ishlashi alohida vaqtinchalik test bazalari va real PostgreSQL fresh schema orqali tekshirildi.

Flutter worktree ichida faqat debug preview:

```bash
flutter run -d chrome --web-port 7357 -t lib/uzbekistan_history_preview_main.dart --dart-define-from-file=/ABSOLUTE/PRIVATE/history-qa/flutter-defines.json
```

Normal app tokenlari ishlatilmaydi. Flutter ham flag, debug rejim, lokal/private API hosti va alohida test identity talab qiladi. UI saqlangan qoralamani API origin + foydalanuvchi + dars bo‘yicha ajratadi. Tarmoqqa uzilish, loading/retry, bekor qilish va javobni ikki marta bosish holatlari mavjud preview oqimi bilan saqlangan.

## Android integratsiyasi hali bajarilmagan

Hozirgi Gradle QA package suffixi Physics uchun yozilgan. Uni History uchun tekshirmasdan APK o‘rnatmang: oddiy paket bilan bir xil ID chiqishi mumkin. Shared Gradle faylini parallel agent bilan konflikt qiladigan tarzda tahrirlamadik. Android SDK/adb bu muhitda yo‘q. Alohida `uzhistoryqa` application ID va label uchun integratsiya patchi/handoff, Android build va real telefonda QA talab qilinadi. Google login, TalkBack, native lifecycle yoki jismoniy telefon sinovlari shu preview natijalaridan kelib chiqib tasdiqlanmaydi.


2026-10-27: konkret `docs/uzbekistan-history/ANDROID_QA_IDENTITY.patch` va `ANDROID_QA_HANDOFF.md` Flutter feature branchida saqlandi. Patch `git apply --check`dan o‘tdi, ammo shared Gradlega qo‘llanmadi va Android SDKda compile qilinmadi. U `.uzhistoryqa` ID/label/callback scheme hamda preview-release radini integratsiya review uchun tayyorlaydi. Shu review va haqiqiy SDK tekshiruvi tugamaguncha History APK normal app bilan to‘qnashmaydi deb da’vo qilinmaydi.

42-darsning haqiqiy serverdan olingan public DTO/feedbacklari bilan Flutter widget oqimi MCQ→ikkita matnli FRQ→xronologiya→natija va tez ikki marta bosishda bitta jo‘natishni tekshiradi.320×568/200%matn ishlatilgan. Bu TestClientdan olingan kontraktning mock-transportdagi UI sinovi; haqiqiy telefon, brauzer HTTP end-to-end yoki Google OAuth sinovi emas. Web build compile-only yaroqsiz placeholder token bilan bajarildi, haqiqiy maxfiy token buildga kiritilmadi.


## 172 darsli yakuniy lokal QA

2026-10-27: 7/8/9/10/11-sinflarning42/41/39/28/22birligi import qilinadi.
Bitta test akkauntida barcha1027javob va172dars yakuni,34bob belgisi,
137→1857XP,shu kuni3streak,qayta ochish va0XP replay tekshirildi:
`tests/test_uzbekistan_history_completion.py` — **3 passed in35.72s**.
`course_content_complete=true` barcha importlar mavjudligini bildiradi;
`course_ready=false` mustaqil review va umumiy nashr tasdig‘i yo‘qligini saqlaydi.

Oxirgi FlutterdebugJavaScriptbuild41.7sekundda o‘tdi. Buildga faqat yaroqsiz
compile-onlyplaceholder kiritildi,haqiqiytestJWT emas. SDKdoctor AndroidSDK
yo‘qligini yana tasdiqladi;APK/TalkBack/realtelefon natijasi da’vo qilinmaydi.
