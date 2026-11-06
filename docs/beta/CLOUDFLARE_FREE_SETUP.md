# ILM AI: bepul Workers AI ulash — 2026-11-06

**So‘nggi aniqlik:** foydalanuvchida Cloudflare akkaunti yo‘q. Keyin kalitlar
Hugging Face’dan ekanligini aytdi; issuer hali mustaqil tasdiqlanmagan. Ushbu
hujjat optional alternativani tayyorlaydi, Cloudflare tanlangani yoki ulanganini
anglatmaydi. Hozir hech qanday tashqi AI provider faollashtirilmagan.

## Hozirgi holat

Foydalanuvchi **faqat bepul xizmat** va API ulashga ruxsat berdi. Backend adapteri
tayyor; haqiqiy Cloudflare akkaunti yoki tokeni hali olinmadi. Brauzer boshqaruvi
`failed to write kernel assets` xatosi bilan, resetdan keyin ham ochilmadi.
Wrangler o‘rnatilmagan; tekshirilgan standart CLI konfiguratsiya yo‘llari va
Cloudflare environment credentiallari mavjud emas. Akkaunt ochildi, Free plan
tasdiqlandi yoki real inference ishladi deb hisoblamang.

Local port8930 serveri qayta ishga tushirilmagan, AI konfiguratsiyasiz ishlayapti.
APKni qayta yig‘ish bu server adapteri uchun zarur emas. Telefon progressi,
login, OAuth, baholash, XP va darslik validatorlari o‘zgarmadi.

## Bepul rejimning chegarasi

[Cloudflare pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/):
Workers **Free** hisobida umumiy kunlik 10 000 Neuron ajratiladi; limit 00:00 UTC
(Toshkent 05:00)da yangilanadi. Neuron token bilan bir xil birlik emas. Free limit
tugasa so‘rovlar rad etiladi. Workers **Paid** hisobida esa ortiqcha ishlatish
pullik bo‘lishi mumkin. Shuning uchun aynan ishlatiladigan hisobning Workers Free
ekanligini dashboardda tekshirish kerak; `free_only: true` billingni o‘zgartirmaydi
va hisobning haqiqiy tarifini mustaqil tekshirmaydi.

Karta, Paid, prepaid AI Gateway credits, billing o‘zgartirish yoki avtomatik
upgrade bu vazifaga kirmaydi. Dashboard shularni talab qilsa to‘xtang va mavjud
tekshirilgan dars izohlarini ishlating. Akkauntlar orasida bepul kvota aylanmasi
yo‘q. Ilova 24/7 cheksiz bepul generativ AI xizmatiga aylandi deb e’lon qilmang.

## Backend qanday ishlaydi

- Faqat `@cf/meta/llama-3.3-70b-instruct-fp8-fast`, bitta account va bitta token.
  So‘rov belgilangan `api.cloudflare.com` REST endpointiga yuboriladi; redirect,
  arbitrary URL, environment proxy, billing/upgrade API yoki boshqa model yo‘q.
- Tashqariga server tekshirgan mavzu/savol va o‘quv parchalarining ID/tur/matni
  yuboriladi. O‘quvchining erkin xabari, tanlagan javobi, akkaunt/token/attempt ID,
  grader feedbacki va private yechimi yuborilmaydi.
- Model faqat mavjud evidence IDlarini tanlaydi. Ilmiy izohlar original reviewed
  materialdan olinadi; model yozgan yangi ilmiy matn ko‘rsatilmaydi. Graderning
  tekshirilgan natija/yechimlari har doim saqlanadi.
- Ikki parallel so‘rov, process uchun 20/min va 1000/UTC-kun. Input 24 000 belgi,
  model output 256 token, javob transporti 32KB bilan cheklangan. Bu lokal request
  limitlari provayderdagi real neuron hisoblagichini almashtirmaydi.
- Bitta network urinish, connect/read timeout 3/6s. Bu qat’iy o‘lchangan umumiy
  UI latency kafolati emas. Xato/timeout/schema/unknown ID → reviewed fallback.
- 401/403 credential qayta sozlanguncha o‘chiriladi; 429/5xx kamida 60s yoki
  Retry-After bo‘yicha pauza qiladi. **429/code3036** kunlik bepul limit uchun
  keyingi UTC kungacha pauza qiladi. Boshqa account/modelga avtomatik o‘tmaydi.

[REST](https://developers.cloudflare.com/workers-ai/get-started/rest-api/),
[JSON mode](https://developers.cloudflare.com/workers-ai/features/json-mode/),
[model](https://developers.cloudflare.com/workers-ai/models/llama-3.3-70b-instruct-fp8-fast/),
[error codes](https://developers.cloudflare.com/workers-ai/platform/errors/).

## Maxfiy konfiguratsiya: qolgan amaliy qadam

1. O‘zingizga tegishli [Cloudflare dashboard](https://dash.cloudflare.com/)ga
   kiring. Email/2FA tekshiruvini akkaunt egasi bajaradi. Workers tarifining Free
   ekanligini tekshirib, sanali lokal review qaydini yarating. Hech qanday to‘lov
   ma’lumotini kiritmang va Paid hisobni bu konfiguratsiya bilan ishlatmang.
2. Workers AI → Use REST API → Create a Workers AI API Token. Ruxsatlarni aynan
   shu accountdagi Workers AI Read/Edit bilan cheklang; account IDni oling.
   Boshqa xizmatlar yoki billing uchun ruxsat bermang. Tokenni chatga yubormang.
3. Quyidagi skriptni **o‘zingizning interaktiv PowerShell oynangizda** bajaring.
   `AudienceReviewReference` va `FreePlanReviewReference` haqiqiy review
   hujjatlariga ishora bo‘lsin; avtomatik tasdiq yoki o‘ylab topilgan sana emas.

```powershell
Set-Location 'C:\Users\Page\Desktop\Projects\ilm-ai-beta'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\configure_cloudflare_free.ps1 `
  -PrivateDirectory 'C:\Users\Page\ilm-ai-private-cloudflare' `
  -AudienceReviewReference '<haqiqiy audience/model review hujjati>' `
  -FreePlanReviewReference '<dashboard Workers Free tekshiruv qaydi>'
```

Bu faqat shu PowerShell processidagi script execution parametridir; Windowsning
doimiy execution policy sozlamasi o‘zgarmaydi. Skript yangi, Git tashqarisidagi
papkaga faqat joriy Windows foydalanuvchisi ACLini o‘rnatadi, tokenni yashirin
so‘raydi va `cloudflare-free.json`ni saqlaydi. Eski papka/faylni almashtirmaydi.
Secret command argumenti yoki logga chiqmaydi. Bu diskda shifrlangan vault emas;
Windows ACL bilan himoyalangan server secret fayli. Testlar faqat sun’iy tokenlar
bilan bajarilgan. Ushbu buyruq network chaqirmaydi va backendni restart qilmaydi.

Faylni tekshirish (faqat yo‘l command argumentida; secret chiqarilmaydi):

```powershell
python -X utf8 -c "from services.study_help_provider import load_provider; load_provider(r'C:\Users\Page\ilm-ai-private-cloudflare\cloudflare-free.json'); print('Private config valid; not a live provider test')"
```

Keyin operatorga **faqat fayl yo‘lini** bering. Google AI Studio kalitlarini
ishlatmang. Xususiy JSONning to‘liq tarkibini terminalga yoki chatga chiqarmang.

## Model/audience tekshiruvining aniq doirasi

Built with Llama (faqat optional adapter faollashtirilganda).

[Llama 3.3 license](https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/LICENSE)
va [acceptable use policy](https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/USE_POLICY.md)
ko‘rildi: operatorning qonuniy vakolati, model attributioni va zararli/noqonuniy
ishlatishni cheklash talablari bor. Bu matnlardan barcha 7+ yoshdagi foydalanuvchi
uchun umumiy huquqiy tasdiq chiqarilmadi. Runtime faqat original tekshirilgan
maktab kontentini yuboradi; erkin shaxsiy suhbat va yangi ilmiy javob yaratmaydi.
Ommaviy yoqishdan oldin haqiqiy operator/audience/privacy review, tegishli
disclosure/attribution va accountdagi model shartlari yakunlansin.

[Workers AI data policy](https://developers.cloudflare.com/workers-ai/platform/data-usage/)
stateless inference mazmuni saqlanishi va training bo‘yicha cheklovlarni beradi,
ammo operatsion metadata va qonuniy istisnolar mavjud. Adapter Gateway
logging/caching/stateful xizmatlarni yoqmaydi. Bu butun ILM AI ilovasi umuman
ma’lumot yig‘maydi degani emas; Play Data safety qaydi alohida moslashtiriladi.

## Keyingi boshqariladigan ulash

Private config va Free plan tasdiqlangach: lokal backendni aynan mavjud
`--directory ...ilm-ai-beta-local --resume --port 8930` bilan, yangi
`--ai-config-file` yo‘li qo‘shib restart qilish; health, synthetic source-only
provider smoke va MCQ/FRQ fallbackni tekshirish. `--resume`ni tushirmang, yangi
test akkauntni foydalanuvchi o‘rniga yaratmang, progressni tozalamang.

Hozir bunday restart yoki real API so‘rovi bajarilmadi. Production deploy,
production DB yozuvi, Play upload va release signoff yo‘q. Mavjud production
bloklovchilari `AI_PROVIDER_READINESS.md`da saqlanadi.

## Yakuniy lokal tekshiruv

**102 passed, 5 PostgreSQL case deselected, 1 oldingi Starlette warning, 48.83s.**
Transport/config, Windows ACL/provisioning va reviewed SQLite Beta API testlari:
asosiy to‘rt fan/Biology study help, ownership/grade/source guardlar, MCQ/FRQ
natijalari, no-progress-write, fake Cloudflare orqali source whitelist,
grader feedback saqlanishi, code3036 kvota/fallback. Haqiqiy token yoki tashqi
inference ishlatilmadi. Ruff va `git diff --check` o‘tdi. Full backend/Flutter/PG
suite yoki yangi APK bu adapter o‘zgarishi uchun qayta bajarilmadi.
