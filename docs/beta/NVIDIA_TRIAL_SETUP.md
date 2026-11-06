# NVIDIA Muse Glimmer — lokal Beta adapteri, 2026-11-06

## Model va API tasdiqlandi

Foydalanuvchi provider nomini NVIDIA deb tuzatdi va model havolasini berdi:
[meta/muse-glimmer-30b](https://build.nvidia.com/meta/muse-glimmer-30b).
[Rasmiy API](https://docs.api.nvidia.com/nim/reference/meta-muse-glimmer-30b-infer):
`POST https://integrate.api.nvidia.com/v1/chat/completions`.
Cloudflare/Hugging Face bu vazifaning faol provideri emas.

**Haqiqiy ulanish hali bajarilmadi.** Oldin chatda berilgan sakkiz kalit
saqlanmadi va hech qaysi providerga yuborilmadi. NVIDIA hujjatida Build API
kalitlari odatda `nvapi-` bilan boshlanishi aytilgan; oldingi qiymatlar bu
qo‘llab-quvvatlanadigan formatda emas. Bu live authentication natijasi yoki
boshqa issuer haqidagi tasdiq emas. [Kalit turi va olish yo‘li](https://docs.nvidia.com/nemo/retriever/latest/extraction/api-keys/).
Eski oshkor qilingan qiymatlarni qayta ishlatish o‘rniga yangi NVIDIA Build
kalitini quyidagi maxfiy usulda bering. Kalitni chatga yubormang.

## Bepul endpointning doirasi

[Model card](https://build.nvidia.com/meta/muse-glimmer-30b/modelcard) ushbu hosted
endpoint uchun [NVIDIA API Trial Terms](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)ni
ko‘rsatadi. §§1.2–1.4 ichki sinov/baholashni productiondan ajratadi; bepul trial
production uchun ruxsat emas. §§3.3/4.3 kontent qayta ishlanishi va shaxsiy
ma’lumot cheklovlarini bildiradi. Operator rozilik berishga qonuniy vakolatli
bo‘lishi kerak. Modelni yuklab ishlatish litsenziyasi hosted trial shartlaridan
alohida. Play release trafikini bu free endpointga ulamang.

Aniq bepul kvota/amal qilish muddati hisobda tekshirilmagan. Katalogdagi model
statistikasini foydalanuvchining token krediti deb ko‘rsatmang. Adapter obuna,
karta, pullik hamkor endpoint yoki avtomatik kredit xaridini yoqmaydi.

## Amalga oshirilgan chegaralar

- Config: `provider=nvidia_trial`, aynan Muse Glimmer modeli, `free_only=true`,
  `usage=internal_evaluation`, audience va trial review reference. Referencelar
  operatorning review qaydi; avtomatik yuridik tekshiruv emas.
- Load va runtime guard: faqat `ENVIRONMENT=test` va `ILM_BETA_ENABLED=true`.
  Production/development/oddiy app rejimi rad etiladi. Asl local Beta own-DB,
  source/auth/preview va ownership guardlari saqlanadi.
- 1–8 ta unique `nvapi-` kalit Git tashqarisidagi private JSONda. Kalitlar
  APKga, Flutter definega yoki environmentdan avtomatik olib kirilmaydi.
- Faqat tekshirilgan savol/mavzu va teaching evidence ID/tur/matni yuboriladi.
  Erkin learner xabari, javobi, UID, token, attempt ID, source metadata,
  private feedback/yechimlar modelga yuborilmaydi.
- Modeldan faqat JSON IDlar olinadi. Ilmiy proza, markdown, tool call,
  truncation/refusal yoki noto‘g‘ri ID → asl reviewed fallback. Grader feedbacki
  va yechimlar doimo tekshirilgan server materialidan ko‘rsatiladi.
- Aynan NVIDIA endpointi; redirect/arbitrary URL/proxy/paid model yo‘q.
  Har urinishda 3/6s connect/read timeout, envelope 32KB, input 24k belgi,
  output 256 token. Reasoning va tools o‘chirilgan; qaytgan reasoning tashlanadi.
  Prompt JSON so‘raydi; endpointda schema kafolati tekshirilgan deb aytilmaydi.
- Process uchun 2 parallel, 20/min, 1000/UTC-kun request limiti.
  401 yoki transport/headersiz 5xx uchun ko‘pi bilan bitta authorized standby
  urinish. **429 butun poolni pauza qiladi; 402/403 operator qayta sozlaguncha
  poolni to‘xtatadi. Kvota tugaganda boshqa akkauntga o‘tish yo‘q.**
  Retry-After uyqu bilan threadni band qilmaydi. Bu durable/distributed billing
  accounting yoki qat’iy umumiy latency kafolati emas.

## Maxfiy kiritish — qolgan zarur qadam

1. Model sahifasidagi **Generate API Key** orqali yangi NVIDIA Build kaliti
   oling. NVIDIA hisobidagi login/email/2FAni akkaunt egasi bajaradi. Karta yoki
   paid subscriptionni yoqmang. Oddiy evaluation uchun bitta kalit kifoya;
   sakkiz kalit sakkizta mustaqil bepul kvota deb hisoblanmaydi.
2. Haqiqiy operator/model/audience va internal-trial review qaydlarini saqlang.
   Bu texnik hujjat operatorning yoshi/vakolati yoki hisob shartlari qabulini
   o‘z-o‘zidan tasdiqlamaydi.
3. O‘z PowerShell oynangizda (token command historyga yozilmaydi):

```powershell
Set-Location 'C:\Users\Page\Desktop\Projects\ilm-ai-beta'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\configure_nvidia_trial.ps1 `
  -PrivateDirectory 'C:\Users\Page\Desktop\Projects\ilm-ai-nvidia-private' `
  -AudienceReviewReference '<haqiqiy audience/model review qaydi>' `
  -TrialReviewReference '<haqiqiy internal trial review qaydi>' `
  -KeyCount 1
```

Agar haqiqatan sakkiz mos va ruxsatli NVIDIA kaliti bo‘lsa `-KeyCount 8`.
Skript har birini yashirin so‘raydi; duplicate/foreign-format qiymatni rad etadi.
Yangi papkaga joriy Windows userining protected ACLini o‘rnatib,
`nvidia-trial.json` yaratadi. Eski papka/fayl almashtirilmaydi. Bu owner-ACL bilan
himoyalangan plain JSON; shifrlangan vault emas. `ExecutionPolicy Bypass` faqat
shu processga tegishli; tizimning doimiy policy sozlamasi o‘zgarmaydi.

Skript network chaqirmaydi, backendni restart qilmaydi va shartlarni qabul
qilmaydi. Chatga **faqat tayyor JSONning lokal yo‘lini** yuboring. Keyin
controlled `--resume` restart, provider smoke va phone feedback sinovi kerak.

Hozirgi8930 server source fallback bilan qoladi; yangi kod hot-reload bo‘lmaydi.
APK qayta buildi server adapteri uchun kerak emas. Main/subject branchlari,
production backend/DB, Play upload, foydalanuvchi progressi o‘zgartirilmaydi.
Oldingi production NO-GO bloklovchilari saqlanadi.

## Yakuniy tekshiruv

**152 passed, 6 PostgreSQL cases deselected, 1 existing Starlette warning,
74.99s.** NVIDIA/OpenAI/Cloudflare transport va private-config regressiyasi,
Windowsda 1/8 fake-key provisioning/ACL, reviewed SQLite Beta API, whitelisted
evidence, grader feedback, wrong IDs va quota fallback o‘tdi. Real token/tarmoq
inference yo‘q. Full backend/Flutter/PG qayta ishga tushirilmadi. Ruff va
whitespace tekshiruvi o‘tdi. Secretlar Git/APKga kiritilmadi.
