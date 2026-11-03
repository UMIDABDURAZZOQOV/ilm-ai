# Pedagogika va o‘zlashtirish

## 2026-11-03 — joriy checkpoint

1-sinf I qism: 41/41 dars, 230 karta, 288 topshiriq. Butun 1–11-sinf kursi hali tugallanmagan.
Math: 65 passed. Alohida PG: 1 passed. Flutter: 440 passed. Analyze: 0 muammo.
II qism: 33 mundarija bo‘limi, 32 native lokator, 0 tayyor dars. 74-mavzuning bosma 68–69-sahifalari yo‘q.
Bu status oldingi checkpointlardan yangiroq. [To‘liq dalil va texnik davom](FIRST_BOOK_COMPLETION.md),
[machine checkpoint](checkpoints/grade1_part1_batch8.json).

Hozirgi namuna: intuitiv vaziyat → yoshga mos kartalar → original ishlangan misolning action/why qadamlari → boshqariladigan model → guided → MCQ → FRQ → yangi vaziyat → natija. Dastlabki mavzularda formula kerak emas. 3D buyum bilan uning ekrandagi chizmasi aniq farqlanadi; chiroyli chizma isbot o‘rnini bosmaydi.

V1 mastery mezoni aniq: darsning barcha authored guided/MCQ/FRQ/transfer savollariga oxir-oqibat to‘g‘ri javob. Xato javobdan keyin keyingi savolga sakralmaydi; ayni savolda kichik ishora → qoida → sodda o‘xshash misol → xato tekshiruvi → oxirgi yordam bosqichida izohli yechim. Har bir yangi retry uchun yangi UUID, transport retry uchun aynan avvalgi UUID/payload. Xato uchun XP olib tashlanmaydi. Birinchi completion10XP, replay0XP; bu real mahsulot statistikasi emas, QA reward qoidasi.

`first_try_correct` va `support_uses` saqlanadi. Completion chuqur yoki uzoq muddatli o‘zlashtirish isboti emas. Yordam bilan javobni topish va mustaqil yangi masalani yechish alohida pilotda o‘lchansin. Yangi-vaziyat savoli ham hozir qayta urinishni qabul qiladi; mustaqillik/retention kafolati yo‘q. 256 answer/attempt chegarasi storage/abuse uchun; yangi urinish boshqa penalti yoki XP dublikatini bermaydi.

Ochiq yoshga moslik: 1-sinf hali to‘liq o‘qimaydigan bolalar uchun matnli FRQ va ko‘p o‘qish mustaqilligi pilot bilan tasdiqlanmagan. Deterministik audio/illustrated input keyingi accessibility bosqichi; mavjud namunani o‘quvchi 100% mustaqil ishlata oladi demang. Oldindan tayyorlangan matn/visual ishlatildi, AI Tutor/Explain/LLM yo‘q.

## Rozilikli pilot rejasi — hali o‘tkazilmagan

O‘qituvchi ko‘rigi va ota-ona/tegishli vakil roziligidan keyin kichik pilot: pretest, original o‘rganish, ko‘rilmagan transfer,3–7kun retention, qaysi yordam foydali bo‘lganini ixtiyoriy fikr. Yoshi/to‘liq ismi/ovoz/ekran yozuvlarini hozir yig‘maymiz. Psevdonim QA ID, minimal consentli metrika, eksport/retention/deletion siyosati alohida tasdiqlansin. Boshqa manbaga majburiy murojaat va tushunilmagan qadam alohida qayd etilsin. Pilot natijasi hozir mavjud emas.
