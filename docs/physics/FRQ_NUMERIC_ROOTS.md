# Sonli ildizlar va oxirgi yaxlitlash — 2026-10-26

Bu hujjat 9-sinf PDF25–29 dagi RMS topshiriqlari uchun amalda qo‘shilgan
assessment v2 kengaytmasini tasvirlaydi. Fizika lokal/test preview holatida.
Eski MCQ, decimal, exact-rational va exact-root qoidalari saqlangan.

## Serverdagi aniq qiymat

Yangi private `expected_root_rational={numerator,denominator}` javobning SI
o‘lchovidagi **kvadrati**ni saqlaydi. Masalan, kislorod modeli uchun
`3*8.31*320/0.032=249300`; haqiqiy tekshiruv qiymati `sqrt(249300)`.
`expected_si=499.3` o‘quvchi so‘ralgan qadamda yozadigan canonical javob,
tekshiruvning matematik haqiqatini almashtirmaydi.

Butun sonlar string, har biri ko‘pi bilan128belgi; maxraj musbat, radikand
manfiy emas. Aniq ratsional ildiz `Fraction`ga, irratsional ildiz immutable
`PositiveSquareRoot`ga normallanadi. Radikand uchun4096bit chegarasi bor.
`expected_rational` bilan birga kiritish rad etiladi. Bu private rubrika;
public DTO yoki javob yuborish orqali kiritib bo‘lmaydi.

Yangi ildiz rubrikasi musbat `rounding_increment_si=g`, `abs_tol_si=g/2`,
`rel_tol=0` talab qiladi. O‘quvchining javobi SI ga yopiq birlik jadvali orqali
aylantiriladi va gridga mosligi tekshiriladi. `a>=0`, `h=g/2` bo‘lsa:

`max(0,a-h)^2 <= radicand <= (a+h)^2`

shu aniq ratsional tengsizlik to‘g‘ri javobni belgilaydi. Float, yashirin
Decimal aniqligi yoki oldindan yaxlitlangan ildiz tekshiruv haqiqatiga
aylantirilmaydi. Boshlang‘ich tekshiruvda noto‘g‘ri birlik/formula alohida
feedback beradi; manfiy modul, noto‘g‘ri qadam va noto‘g‘ri son ham ajratiladi.

## Kiritish va chegaralar

Formula maydonida faqat ko‘rib chiqilgan oilalardagi `sqrt(...)` va ruxsatli
muqobil shakllar ishlaydi. Sonli maydonda so‘ralgan yaxlit decimal yoziladi.
Umumiy CAS, irratsional ifodalar ustida erkin arifmetika, trigonometrik solver
qo‘shilmadi. Eski numeric parser irratsional ildizni taxminan hisoblamaydi.

Celsius qiymati alohida `celsius_reading` sifatida signed kirishdir; shu
konversiya topshirig‘i javobni Kelvin talab qiladi. Bu ikkita shkalani
oddiy ko‘paytiruvchi bilan o‘zaro almashtirish emas. PDF22 dagi273.15 aniq
bog‘lanish va273 maktab yaqinlashuvi ochiq ajratiladi. Boshqa gaz tenglamalari
Kelvin va **absolyut** bosim bilan; manometr ortiqcha bosimi yashirincha
absolyut deb olinmaydi.

## Tekshiruvlar

`tests/test_assessment_exact_root.py`: 27test; exact-square interval,
90digit independent Decimal reference faqat testda, birlik konversiyasi,
oldingi kalitga qaytmaslik, manfiy/yaroqsiz/cheksiz nisbat, grid siyosati,
private-key injection va katta radikand. Dastlab uzun literal mavjud parser
chegarasiga urilgan test `1e50+1` bounded ifodasiga tuzatildi; himoya saqlandi.
Old exact-rational14test bilan41passed0.05s.

Yangi temperature/state36test bilan77passed3.73s. To‘liq backend1092passed,
4opt-in PGskipped,13mavjudwarning351.78s. Haqiqiy lokalPG16da177dars,
1770XP/import/reimport/replay/eski progress:1passed62.56s. Flutter149passed,
48public9FRQ/134old8FRQ320px/200%,analyzeNoissues1.6s.

API version2, public javob formati, DBschema va production konfiguratsiyasi
almashtirilmadi; migratsiya kerak emas. Hech qanday production import yoki
nashr bajarilmadi. Mustaqil fan eksperti va native Android sinovi bajarilmagan.
