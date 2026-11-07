# Staging akkaunt o‘chirish — bepul email yuboruvchini tayyorlash

2026-11-08: ikki haqiqiy Google akkaunti, MCQ/FRQ va progress alohidaligi tekshirildi.
Keyingi to‘siq: haqiqiy email-kod yetkazilishi va akkaunt o‘chirish siyosati/storage
tekshiruvi. Staging `/account-deletion`200, `/account/deletion/config`200 va
`available=false`. Hech qanday OTP yoki deletion so‘rovi yuborilmadi.

## Mavjud imkoniyat

Backend `services/email.py` Brevo/Resend HTTPS API va Gmail SMTP adapterlariga ega.
Google login uchun berilgan `openid email profile` ruxsati xat yuborish huquqi emas.
OAuth client secretni mailer paroli sifatida ishlatmang.

Render Free tashqi25/465/587 portlarini bloklaydi. Shu sabab bu stagingda mavjud
Gmail SMTP adapteri yechim bo‘lmaydi. Brevo HTTPS adapteri443 orqali ishlaydi;
haqiqiy yetkazilish alohida tasdiqlanishi kerak.

- [Render Free cheklovlari](https://render.com/docs/free)
- [Brevo Free tarif cheklovlari](https://help.brevo.com/hc/en-us/articles/208580669-FAQs-What-are-the-limits-of-the-Free-plan)
- [Brevo yuboruvchi/domain tasdig‘i](https://developers.brevo.com/docs/getting-started-with-senders-and-domains)

Brevo rasmiy hujjatiga ko‘ra Free tarifda kuniga300 email limiti mavjud. Bu
production hajmi/deliverability yoki cheksiz bepul xizmat va’dasi emas. Pulli
tarif, qo‘shimcha xizmat yoki yangi xarajat alohida roziliksiz yoqilmaydi.

## Egasi bajaradigan tashqi sozlama

1. Alohida staging/test uchun o‘zingiz boshqaradigan Brevo Free akkauntini tanlang.
   Pulli tarif/add-on yoqmang. Akkaunt/email/2FA tasdig‘ini o‘zingiz bajaring.
2. O‘zingiz boshqaradigan sender emailini tasdiqlang; platforma talab qilgan
   domain autentifikatsiyasini bajaring. Production yuboruvchi kalitini ko‘chirmang.
3. [API keys bo‘limida](https://help.brevo.com/hc/en-us/articles/209467485-Create-and-manage-your-API-keys)
   staging uchun alohida **API key** yarating (SMTP key emas). Git checkoutlaridan tashqarida, masalan
   `C:\Users\Page\ILM-AI-secrets\staging-mailer.private.json` faylida saqlang:

   ```json
   {
     "BREVO_API_KEY": "<faqat lokal maxfiy fayldagi haqiqiy kalit>",
     "BREVO_FROM_EMAIL": "<tasdiqlangan staging yuboruvchi emaili>",
     "BREVO_FROM_NAME": "ILM AI Staging"
   }
   ```

4. Agentga faqat fayl yo‘lini yuboring. Kalitni chat, Git, APK yoki logga yozmang.
   Test uchun o‘zingiz boshqaradigan mailboxlarni ishlating.

## Agent uchun keyingi ish tartibi

- Maxfiy faylni qiymatlarini chiqarmasdan tekshirish; staging va production
  konfiguratsiyasi ajratilganini tekshirish. Faqat tasdiqlangan HTTPS APIga yuborish.
- Sender konfiguratsiyasi borligi `ACCOUNT_DELETION_ENABLED=true` qilish uchun
  yetarli emas. Avval `ACCOUNT_DELETION_POLICY_REFERENCE` uchun haqiqiy egasi
  ko‘rib chiqqan siyosat, storage-root/cleanup-worker va retention holatini tekshirish.
  Soxta "approved" yozuvi bilan guardni aylanib o‘tmaslik.
- Faqat stagingda alohida deletion secret; JWT/Google/production secretlarini
  qayta ishlatmaslik. Mavjud sessiya sirlarini almashtirmaslik.
- Runtime/storage/worker tayyor bo‘lsa strict validator va tegishli testlar;
  kerakli staging deployni aniq kod/env bilan qayd qilish. Productionga tegmaslik.
- Haqiqiy OTP yetkazilishini, noto‘g‘ri/eskirgan kodni, retry/provider failure va
  web/app oqimini tekshirish. Mailbox kodini egasi ilovaga o‘zi kiritadi.
- Faqat aniq tanlangan owned staging akkauntni doimiy o‘chirishga rozilikdan
  keyin deletion acceptance: sessiya bekor bo‘lishi, boshqa akkaunt progressi
  saqlanishi, qayta ro‘yxatdan o‘tishning yangi/bo‘sh profil yaratishi.
- Public sahifa/config200 natijasi OTP yetkazilishi yoki deletion muvaffaqiyati
  degani emas. Xato bo‘lsa "deleted" deb yozmaslik.

To‘liq talablar: [ACCOUNT_DELETION.md](ACCOUNT_DELETION.md).
Joriy release qarori: [PRODUCTION_READINESS_20261108.md](PRODUCTION_READINESS_20261108.md).
Bu yo‘riqnoma tashqi akkaunt yaratgani, sender sozlangani yoki deletion sinovi
bajarilgani haqida da’vo qilmaydi. Google Play/production uchun alohida tasdiq kerak.
