# 2-sinf I qism — manba bo‘shlig‘idan keyingi lokal sinov

2026-11-05. Bu production yoki ommaviy kursni yoqish yo‘riqnomasi emas.

## Tekshirilgan doira

§26–30, path27–31, PDF55–64 / bosma56–65 uchun beshta original dars yaratildi.
Har birida6karta,1misol/3izohli qadam,8savol va2sonli tekshiruv bor.
Jami30karta,5misol/15qadam,40savol (5MCQ va35sonli javob),10sonli tenglik.
Savollarning shartga mos bosqichli hintlari va to‘liq yechimlari serverda saqlanadi.

| Manba | Path | PDF | Bosma | Original model |
|---|---|---|---|---|
|26|27|55–56|56–57|46+28: yangi o‘nlik va qolgan birlik|
|27|28|57–58|58–59|Ustunda xona qiymatlarini moslash; 47+21,68−41,53+4|
|28|29|59–60|60–61|52−27: eski birliklarni saqlab,ikkala xonani ayirish|
|29|30|61–62|62–63|54−28:20ni,keyin4va4ni olish|
|30|31|63–64|64–65|47+28: carry va birlik qoldig‘i|

Ko‘rgazmali modellar o‘quv misollari. Mustaqil savollar kalitlari Flutterga yuborilmaydi.
To‘rtta yangi explorer turi, orqaga qadam/presetni almashtirganda reset, semantika
va katta matn uchun Wrap/scroll ishlaydi; yangi animatsiya Reduce Motionni chetlab o‘tmaydi.
Grafikdagi tillar qaydi alohida bolalar sanog‘i deb shartsiz qo‘shilmaydi.
Ketma-ketlikning o‘suvchi farqlar qoidasi topshiriqda ochiq berilgan.

## Yetishmayotgan §25

Kitob SHA-256: `31124258de8a1432c1ce15006ff6465f818cf9c10fa86cbaf5dc6566c4c64f54`.
PDF54/bosma53dan keyin PDF55/bosma56 keladi. Source25/path26/bosma54–55 yo‘q.
§26ning sarlavhasi §25bilan bir xil bo‘lsa ham,boshqa haqiqiy paragraf. Raqamlash siljitilmagan.
Yo‘q mavzuga lesson,attempt,progress yoki XP yaratilmaydi.

Serverning yangi `MATHEMATICS_QA_GRADE2_PART1_SOURCE_GAP=true` flagi odatda o‘chiq.
Faqat development/test + alohida loopback/stagingDB + preview ruxsati bilan ishlaydi.
Aniq kitobSHA,44map/43body,yo‘q source25/path26,oldingi/keyingi PDF-bosma chegarasi,
body yo‘qligi va oldingi25haqiqiy darsning yakunlangani tekshiriladi.
Keyingi import qilingan darslar mapdagi tekshirilgan tana/ID bilan ketma-ket mos kelishi shart.
Oddiy prerequisite keyingi mavjud darslar orasida saqlanadi.

APIversion1ga alohida ixtiyoriy `source_sequence_gap_bridge` metadata qo‘shilgan.
Eski `source_gap_bridge` oldingi kitob bo‘shlig‘i ma’nosini saqlaydi.
2-sinf I qismga kirish oldingi sinfni tugatishni talab qilmaydigan mavjud sinf tanlash qarorini o‘zgartirmaydi.
Mijoz so‘rovi bu ruxsatni berolmaydi; qo‘shimcha startfield422.
Flag o‘chsa tugallanmagan urinish start/resume/answer/complete va yangi replay bloklanadi.
Tugallangan aynan o‘sha urinish natijasi oldingi requestUUID bilan o‘qiladi;avvalgiXP saqlanadi.
`course_ready=false`,missing-topic-completedfalse va Flutterda ochiq manba qaydi saqlanadi.

## Windowsda alohida sinov

Backendvenv/faqat lokal dependencylar tayyorlangandan keyin,Git papkasidan tashqarida yangi private katalog tanlang:

```powershell
python -m scripts.serve_mathematics_preview --directory C:\ILM-QA-PRIVATE\math --allow-known-grade2-part1-source-gap
```

Oldingi o‘zingiz yaratgan sandboxni davom ettirish uchun `--resume`ni qo‘shing.
Oldingi darslar/progress qayta yaratilmaydi; yangi immutable darslar import qilinadi.
Flagni har ishga tushirganda aniq bering; keyingi ishga tushirishda avtomatik yoqilgan deb hisoblamang.

Flutter alohida debug entrypoint:

```powershell
flutter run -d chrome --web-port 7358 -t lib/mathematics_preview_main.dart --dart-define-from-file=C:\ILM-QA-PRIVATE\math\flutter-defines.json
```

Android emulatorda private defines faylining `API_URL`ini `http://10.0.2.2:8892`ga moslang.
USB telefon uchun `adb reverse tcp:8892 tcp:8892`dan so‘ng loopbackURL ishlatilishi mumkin.
AndroidSDK/adb,debugHTTP siyosati va haqiqiy qurilmada moslik alohida tekshirilishi shart.
TestJWT faqat o‘sha sandboxga tegishli va60minutli;private defines/server.jsonni Gitga/logga yubormang.
Avval2-sinf Iqismning25haqiqiy darsini bajaring;serverflag bu prerequisite o‘rnini bosmaydi.
Productionlogin yoki mavjud haqiqiy akkauntdan foydalanmang.

Cloud muhitida `/workspace/.git` va `/tmp/.git` sintetik ajdodlari sababli standaloneCLI
positive sandbox yaratilishi hali tekshirilmagan. Guard chetlab o‘tilmadi.
Haqiqiy API sinovlari izolyatsiyalangan TestClient/SQLite va o‘z loopbackPostgreSQL schemasida bajariladi.
AndroidSDK,realAndroid/TalkBack,o‘qituvchi ko‘rigi,o‘quvchi piloti va2026–27dastur mosligi tasdiqsiz.

Keyingi mavjud manba: **§31,path32,PDF65–66/bosma66–67**.
2-sinf Iqismda14birlik qolgan:13mavjud tana va1yo‘q§25. Butun1–11kurs tugallanmagan.
