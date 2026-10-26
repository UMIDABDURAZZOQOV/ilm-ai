# ILM AI — JAHON TARIXI 6–11-SINFLARNI TO‘LIQ YARATISH

Sen ILM AI loyihasidagi Jahon tarixi fanini yaratadigan Codex agentsan.

**Mening qat'iy topshirig‘im: 6-sinfdan 11-sinfning oxirgi mavzusigacha, men taqdim etgan 6 ta tarix darsligi asosida, birorta mavzuni qoldirmasdan to‘liq interaktiv kurs yarat.**

Oldingi Biologiya, Fizika va Kimyo fanlarini ishlab chiqishda qo‘llangan manbaga bog‘langan kontent, qat'iy validatsiya, MCQ/FRQ va GitHub checkpoint qoidalariga amal qil.

## 1. Darsliklar

Men quyidagi oltita asl PDF faylni taqdim etdim:

- `qadimgi_dunyo_tarixi_6_uzb.pdf` — 6-sinf, 2017, 192 PDF sahifasi.
- `jahon_tarixi_7_uzb.pdf` — 7-sinf, 2017, 161 PDF sahifasi.
- `jahon_tarixi_8_uzb.pdf` — 8-sinf, 2019, 160 PDF sahifasi.
- `jahon_tarixi_9_uzb.pdf` — 9-sinf, 2019, 160 PDF sahifasi.
- `jahon_tarixi_10_uzb.pdf` — 10-sinf, 2017, 144 PDF sahifasi.
- `jahon_tarixi_11_uzb.pdf` — 11-sinf, 2018, 144 PDF sahifasi.

**Jami: 961 PDF sahifasi.**

Avval mahalliy kompyuterda shu fayllar mavjudligini tekshir. Ularni avtomatik ravishda VS Code muhitiga kelgan deb taxmin qilma.

PDF fayllar repozitoriyadan tashqaridagi alohida manbalar papkasida saqlansin. GitHub'ga asl PDF, katta OCR matni yoki darslik rasmlari push qilinmasin.

9-sinf PDF'i asosan skanerlangan. Unda oddiy text extraction yetarli emas. Sahifa rasmlarini o‘qib, zarur OCR natijalarini asl tasvir bilan solishtirib tekshir. OCR chiqishini ko‘r-ko‘rona bilim sifatida qabul qilma.

## 2. Fanlar chegarasi

Tarix ILM AI'da ikki mustaqil fan bo‘ladi:

- `jahon_tarixi` — hozir to‘liq ishlab chiqiladigan fan.
- `ozbekiston_tarixi` — keyinchalik alohida ishlab chiqiladigan fan.

Hozir faqat Jahon tarixini yarat.

6-sinfdagi «Tarix. Qadimgi dunyo» kitobi Jahon tarixining boshlang‘ich kursi hisoblanadi. Unda O‘rta Osiyo va O‘zbekiston hududiga tegishli mavzular borligi sababli ularni tashlab ketma — ular aynan ushbu kitobning bir qismidir.

Ammo mustaqil O‘zbekiston tarixi kursining boshqa darslarini hozir yaratma.

## 3. Arxitektura va branch xavfsizligi

Loyihadagi:

- `ilm-ai` backend;
- `ilm-ai-flutter` mobil ilova;
- markaziy `CLAUDE.md`;
- mavjud curriculum validatorlar;
- MCQ/FRQ grading;
- XP, progress, prerequisite va lesson engine

tizimlarini o‘rgan.

Jahon tarixi uchun alohida `feat/world-history-curriculum` feature branchlarini va mustaqil worktreelarni yarat.

Boshqa agent Fizika ustida ishlayotgan bo‘lishi mumkin. Uning worktree, fayllari va commitlariga tegma.

Kimyoning 268 ta, Biologiyaning 406 ta tayyor darslarini saqla.

Boshqa fanlarga regressiya keltirmaydigan, additive arxitekturadan foydalan.

## 4. Avval barcha kitoblarni katalogla

6–11-sinflarning har bir darsligini sahifama-sahifa inventarizatsiya qil.

Quyidagilarni aniqlagin:

- kitob nomi, mualliflari, yili va nashri;
- SHA-256 identifikatori;
- bob, bo‘lim va mavzular;
- paragraf raqamlari;
- PDF va bosma sahifalar;
- xaritalar, jadvallar va xronologiyalar;
- manbada berilgan savol va mashqlar;
- takrorlash va amaliy faoliyatlar.

Katalogdan haqiqiy umumiy mavzu sonini hisobla. Mavzular sonini oldindan taxmin qilma.

2026–2027 o‘quv dasturi bilan moslikni alohida audit qil. Farqlarni qayd et, ammo men yuborgan kitoblardan tashqaridagi mavzularni avtomatik kiritma.

## 5. Har bir dars faqat tekshirilgan kitob bilimiga tayansin

Bu mening eng muhim talabim.

Har bir nazariya kartasi, tarixiy sana, shaxs, davlat, voqea, xarita mazmuni, sabab-oqibat izohi va savol aniq kitob manbasiga bog‘lansin.

Har bir fakt uchun imkon qadar quyidagi evidence saqlansin:

- `book_id`;
- `grade`;
- `chapter_id`;
- `topic_id`;
- `pdf_pages`;
- `printed_pages`;
- `fact_id`;
- `verification`;
- `review_note`.

AI o‘zidan tarixiy fakt yoki sana uydirmasin.

Tarixiy talqin va dalilni farqlagin. Darslikning bahsli yoki eskirgan xulosalarini tekshirilgan mutlaq fakt sifatida bermagin. Ziddiyatlarni review hujjatiga yoz.

Aniq xato topilganida uning manbasini va tekshirilgan tuzatish asosini qayd et. Noaniq faktlardan avtomatik baholanadigan savol tuzma.

Darslikni uzun parchalar bilan ko‘chirib nashr qilma. Undagi bilimlarga asoslangan original nazariya va mashqlar yarat.

## 6. Duolingo uslubidagi tarix darslari

Har bir mavzuda kitobga mos ravishda:

1. Tushunarli nazariya kartalari.
2. Muhim tarixiy sanalar va davrlar.
3. Tarixiy shaxslar va ularning faoliyati.
4. Davlatlar va hududlar.
5. Voqea sabablari va oqibatlari.
6. Xronologik ketma-ketlik mashqlari.
7. Tarixiy tushunchalar va atamalar.
8. Original MCQ savollari.
9. Qisqa yozma FRQ savollari.
10. Javob izohi va manba.
11. XP, progress va darsni yakunlash.

Har bir turdagi topshiriqni faqat mavzuga mos bo‘lsa qo‘sh.

Sanalar, asrlar va miloddan avvalgi/milodiy davrlarni hisoblashda xatoga yo‘l qo‘yma.

FRQ uchun oldindan belgilangan to‘g‘ri javoblar va asosli muqobil variantlarni qo‘llab-quvvatla.

Murakkab ochiq tarixiy fikrni deterministik tekshiruvchi bilan ishonchli baholash imkonsiz bo‘lsa, uni avtomatik to‘g‘ri/noto‘g‘ri deb baholama.

## 7. Ilova tajribasi

Ilmo maskoti, Duolingo uslubidagi o‘quv yo‘li, mavzu kartalari, feedback, natija va XP tizimini saqla.

Jahon tarixi uchun 6 ta sinf tanlash imkoniyati bo‘lsin.

Har bir sinfning boblari, darslari va bibliografiyasi alohida ko‘rsatilsin.

Ilovaning o‘zbek, rus va ingliz interfeyslarini buzma. Manbadan tekshirilmagan avtomatik tarjimalarni tasdiqlangan dars kontenti sifatida nashr qilma.

Mavjud fanlar va foydalanuvchi progressini o‘zgartirma.

## 8. 6-sinfdan 11-sinfgacha uzluksiz ish

Ish tartibi:

6-sinfning birinchi paragrafi → 6-sinf oxiri → 7-sinf → 8-sinf → 9-sinf → 10-sinf → 11-sinf oxiri.

Har 5–10 darslik partiyada:

1. Asl kitob sahifalarini o‘qi.
2. Har bir muhim faktni tekshir.
3. Original nazariya kartalarini yoz.
4. MCQ/FRQ savollarini yarat.
5. Barcha savol kalitlari va izohlarni validatsiya qil.
6. Backend va tegishli Flutter testlarini bajar.
7. Zarur lokal API va PostgreSQL staging tekshiruvlarini bajar.
8. Source review va progress hujjatlarini yangila.
9. Git commit va xavfsiz push qil.
10. Keyingi partiyaga o‘t.

**Har bir partiyadan so‘ng mendan «Davom ettiraymi?» deb so‘rama.**

6-sinf tugasa, 7-sinfga o‘t. Har bir sinfda shunday davom et.

Ammo manba yo‘qligi, hal qilib bo‘lmaydigan ilmiy ziddiyat yoki xavfli amal mavjud bo‘lsa, taxmin qilmasdan muammoni qayd et.

## 9. GitHub checkpoint va limitlar

Codex sessiyasi yoki foydalanish limiti tugashi mumkin.

Har bir partiyadan keyin quyidagilar saqlansin:

- umumiy mavzular soni;
- haqiqatan tayyor darslar soni;
- qolgan darslar soni;
- oxirgi tayyor sinf va paragraf;
- manbasi tasdiqlanmagan bo‘limlar;
- test natijalari;
- oxirgi commit SHA;
- push holati;
- keyingi aniq davom nuqtasi.

Sessiya uzilganda keyingi agent barcha tayyor ishni qaytadan yozmasdan davom eta olsin.

## 10. Qat'iy cheklovlar

- Fizika, Biologiya, Kimyo kurslarini buzma.
- O‘zbekiston tarixining alohida kursini hozir yaratma.
- Boshqa agentning worktree va branchlariga tegma.
- Production bazasi yoki real foydalanuvchilar ma'lumotlarini o‘zgartirma.
- `main` branchga merge qilma.
- Production deploy qilma.
- AI Tutor yoki AI Explain'ni hozir qo‘shma.
- Validator yoki xavfsizlik tekshiruvlarini o‘chirib qo‘yma.
- Mualliflik huquqi bilan himoyalangan darsliklarning katta matnlari va rasmlarini repoga joylama.

## 11. Yakuniy qabul mezonlari

Barcha oltita darslik kataloglangan bo‘lsin.

6–11-sinflarning har bir haqiqiy mavzusi interaktiv dars bilan qamrab olinsin.

Har bir nazariya va savol source-validator orqali tekshirilsin.

MCQ, FRQ, xronologiya, XP, progress, replay va grade transition ishlasin.

Backend, Flutter, lokal API va tegishli PostgreSQL testlari muvaffaqiyatli yakunlansin.

Alohida `WORLD_HISTORY_FINAL_AUDIT.md` tayyorla.

Mustaqil tarix o‘qituvchisi ko‘rigi va haqiqiy Android tekshiruvi bajarilmagan bo‘lsa, bajarildi deb ko‘rsatma.

**Jahon tarixi 6–11-sinflarning barcha kataloglangan bo‘limlari tayyor bo‘lmaguncha vazifa yakunlandi deb e'lon qilma.**

Endi mavjud loyihani va oltita darslikni tekshirishdan boshla. Manbalar mavjud bo‘lsa, 6-sinf §1 dan darslarni ishlab chiqishni boshlagin.

Xudo xohlasa, barcha sinflarni to‘liq va sifatli yakunlaymiz!