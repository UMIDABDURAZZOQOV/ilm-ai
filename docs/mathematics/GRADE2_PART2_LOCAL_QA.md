# 2-sinf II qism — manbali darslar va lokal sinov

Faqat alohida development/test preview. Normal mobil katalog yoki productionni yoqmaydi.

## Tayyorlangan partiya

§42–46,path1–5,PDF5–14/bosma4–13ning10to‘liq sahifasi qayta ko‘rildi.
5original dars:30karta,40savol,5misol/15izohli qadam,10sonli tenglik.
Yuzlik/ming,uch xonali yozuv,nol xonalari,xona raqami va to‘liq guruhlar farqi o‘rgatiladi.
1000ning4raqami borligi,to‘liq yuzlik10ta bo‘lsa ham ming xonasining alohidaligi ochiq ko‘rsatiladi.
Yangi5model turi bitta barqaror widget/painterdan foydalanadi:hundreds_thousand,
three_digit_place,zero_tens_place,zero_units_place,full_place_groups.
Yuzlik100,o‘nlik10,birlik1deb berilgan;ekran maydoni fizik miqdor masshtabi emas.
Mustaqil savol kaliti yokiXPmijozda baholanmaydi. Ilmo,brend,oldingi186dars saqlandi.
Kasblar,harbiy guruhlar,yo‘l hodisalari,haqiqiy shahar masofalari,avia-tariflar va yuqumlilik
normasi kabi tashqi ma’lumotlar matematika kaliti sifatida taxmin qilinmadi;original neytral shartlar ishlatildi.

## Xaritadagi muhim farq

73body sahifasining header/footerlari asli tasvirda tekshirildi.
34haqiqiy chegara birligi:31raqamlangan§42–72,2raqamsiz yakuniy dars va1mantiqiy to‘plam.
Mundarija§73degan bosma68sahifada(PDF69–70)aslida raqamsiz yakuniy dars bor.
Uni§73qilib soxtalashtirmaymiz;kim/nima uchun farq paydo qilgani hali tasdiqsiz.
5dars tayyor,29birlik to‘liq kontent ko‘rigi/authoringni kutadi.
Mantiqiy to‘plamdagi ichki mashqlar soni hali aniqlanmagan.34raqami hamma mazmun to‘liq o‘qilganini anglatmaydi.

## Oldingi I qismdagi manba kamchiligi

I qism43mavjud darsdan iborat;yo‘q§25/path26/bosma54–55uchun dars yoki progressyo‘q.
Standart previous-book-complete shu sabab falseqoladi.
Yangi odatda o‘chiq serverflag:`MATHEMATICS_QA_GRADE2_PART2_PREVIEW`.
U bilan birga oldingi`MATHEMATICS_QA_GRADE2_PART1_SOURCE_GAP`hamtruebo‘lishi kerak.

Ruxsat faqat2-sinf IIqismga tegishli. Exactikki kitobSHA,prev44map/43actualbody,
source25gapning aniq chegarasi,barcha43haqiqiy oldingi darsning yakuni va
import qilingan IIqism darslarining map/ID/ketma-ketligi tekshiriladi.
IIqism ichidagi oddiy prerequisite o‘zgarmaydi.
Mijoz so‘rovi flagberolmaydi;qo‘shimcha maydon422. UIDbegona urinishni o‘qiy/bajara olmaydi.
Flaglardan biri o‘chsa unfinished start/resume/answer/complete va yangi replay bloklanadi.
Tugallangan aynan shu urinish natijasi eski requestUUIDbilan o‘qilishi mumkin;oldingiXPsaqlanadi.
Bajarilgan badge o‘zi yangi urinish uchun ruxsat emas.
APIversion1dagi eski`source_gap_bridge`kontrakti ishlatiladi,previous_book_completefalse,
previous_book_navigation_readyfaqatlokalruxsatda true. course_readyfalseqoladi.
Productionprerequisite,eskiGooglelogin yoki boshqa fan APIlari o‘zgarmadi.

## Windows lokal sandbox

O‘zingiz yaratgan mavjud sandbox uchun:

```powershell
python -m scripts.serve_mathematics_preview --directory C:\ILM-QA-PRIVATE\math --resume --allow-known-grade2-part1-source-gap --allow-known-grade2-part2-preview
```

Yangi katalog bo‘lsa`--resume`berilmaydi. Katalog Gitdan tashqarida va privatebo‘lsin.
Dastlab Iqismning43haqiqiy darsi o‘sha testakkauntda bajarilishi kerak;flags buning o‘rnini bosmaydi.
Private Flutterdefines bilan alohida debugentrypoint:

```powershell
flutter run -d chrome --web-port 7358 -t lib/mathematics_preview_main.dart --dart-define-from-file=C:\ILM-QA-PRIVATE\math\flutter-defines.json
```

JWTfaqatshu sandbox uchun1soatli;config/tokenni Gitga yoki logga yubormang.
Androidemulatorda APIURL10.0.2.2:8892,yokiUSBtelefondaadb reverse bilan alohida moslash talab qilinadi.
Bu muhitda AndroidSDK/realAndroid/TalkBack hamda standaloneCLIpositive sandbox tasdiqlanmagan.
SintetikGitajdod guardi chetlab o‘tilmagan;APItestlar TestClient/SQLite va o‘zloopbackPostgreSQLschema orqali bajariladi.
Teacherreview,o‘quvchi piloti,2026–27dastur va framebench ham hali tasdiqsiz.

Keyingi§47,path6,PDF15–16/bosma14–15. Uning asl ikki sahifasi ko‘rildi,darsi hali yozilmagan.
Dastur jadvalidagi21→2yuzlik,1o‘nlik,0birlik satri kitobda tekshirish uchun ataylab berilgan noto‘g‘ri yozuv;
uni21ning haqiqiy tarkibi deb ko‘chirmang. To‘g‘risi0yuzlik,2o‘nlik,1birlik.
Taqqoslashda avval yuzlik,so‘ng teng bo‘lsa o‘nlik,undan keyin birlik ishlatiladi.
Robotning oldinga43+28,orqaga37+35yo‘li misolida jami yo‘l143m,
yo‘nalishlar farqi1m;ikkisini almashtirmang. Bu keyingi mazmun uchun revieweslatma,hozir tayyor dars emas.

## Minglik yozuvining muqobil shakli

Yangi1000topshirig‘ida`1 000`kabi odatiy guruhlangan literal ilgari rad etilgani qayta hosil qilindi.
Mathclosedparser endi faqat butun literal uchun bo‘shliq/NBSP/narrow-NBSPbilan uch raqamli guruhlarni tan oladi.
`1 000`,`1 000`,`1 000`qiymati1000;`1 00`,`12 34`,`2 1/2`,`1 000+2`rad qilinadi.
Guruhlangan ifoda o‘rnida`1000+2`yoziladi;tokenlar o‘zboshimchalik bilan birlashtirilmaydi.
Vergul kasr ajratuvchisi bo‘lib qoladi:`1,000`qiymati1,ming emas.
Mavjud160belgi/80token/12depth/256bitcheklovlari,powers/functions/variables/injectionrad etilishi saqlanadi.
Bu Matematika-onlyparser;Physics/Chemistry yoki publicbaholashAPIlariga tegmagan.
Yangi literal/wrong/unsafeva haqiqiyAPIhamdaPostgreSQL oqimlari alohida tekshirildi.
