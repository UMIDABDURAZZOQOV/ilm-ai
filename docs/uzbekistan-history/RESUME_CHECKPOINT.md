# Davom checkpointi — kontent 172/172

2026-10-27. Barcha 7–11-sinfning 172 o‘quv birligi yozilgan, manbaga bog‘langan, testdan o‘tgan va feature branchlarga saqlangan. **Mualliflik uchun qolgan mavzu: 0.** Eski darslarni qayta yaratmang; frozen r1/review fayllarini qayta yozmang.

| Sinf | Bob | Manba birligi | Tayyor lokal/test dars | Qolgan | Karta | MCQ | Qisqa FRQ | Xronologiya | Jami topshiriq |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 6 | 42 | 42 | 0 | 325 | 168 | 83 | 29 | 280 |
| 8 | 4 | 41 | 41 | 0 | 319 | 140 | 82 | 23 | 245 |
| 9 | 9 | 39 | 39 | 0 | 293 | 139 | 77 | 14 | 230 |
| 10 | 6 | 28 | 28 | 0 | 184 | 84 | 56 | 15 | 155 |
| 11 | 9 | 22 | 22 | 0 | 159 | 66 | 44 | 7 | 117 |
| **Jami** | **34** | **172** | **172** | **0** | **1280** | **597** | **342** | **88** | **1027** |

- **backend_full**: `2524 passed, 9 skipped, 2 deselected, 13 warnings in 829.05s (0:13:49)`.
- **postgres**: `5 passed, 223 deselected in 100.80s (0:01:40)`.
- **whole_course**: `3 passed in 35.72s`.
- **flutter_history**: `00:23 +215: All tests passed!`.
- **flutter_analyze**: `No issues found! (ran in 1.6s)`.
- **flutter_full**: `01:27 +369: All tests passed!`.

Tekshirilgan backend `1409236526e5e5e2609125bfe72f668a99caa643`, Flutter `fa6c305c4a56b16f397aa5d73f40b8040f016ed3`. Ikkala branch: `feat/uzbekistan-history-curriculum`. Yangi sessiya git status/log/remote SHA’ni tekshirsin; reset yoki overwrite qilmasin. [Yakuniy hisobot](COURSE_COMPLETION.md), [dalillar](checkpoints/final_validation.json).

## Qolgan review va release ishlari

1. Mustaqil tarix o‘qituvchisining faktologik va pedagogik ko‘rigi bajarilmagan. [Umumiy manba tafovutlari](SOURCE_REVIEW.md) va [11-sinf auditi](GRADE11_SOURCE_REVIEW.md)dagi bahsli da’volar avtomatik kalitga kiritilmadi. Ular uchun taxminiy tuzatish yozilmadi.
2. Rasmiy 2026–2027 dastur bilan to‘liq qiyos tasdiqlanmagan. 27-oktabrda gov.uz va uzbmb.uz qayta so‘raldi; proxy 403 qaytardi. Eski nashrlarni amaldagi dasturga avtomatik tenglashtirmaymiz. [Dastur auditi](CURRICULUM_ALIGNMENT_2026_2027.md).
3. Haqiqiy Android, TalkBack, native lifecycle va APK sinovi yo‘q: Android SDK/adb mavjud emas. History uchun alohida Android QA identity patchi Flutter branchidagi handoffda saqlangan, shared Gradle fayliga qo‘llanmagan. Telefon va real Google login sinovi bajarildi deyilmaydi.
4. Kurs alohida lokal/test preview rejimida. Normal mobil/production router va ommaviy fan katalogiga ulanmagan. Reviewer/teacher workflow, kontent revisionlarini ko‘tarish va umumiy integratsiya alohida bosqichlar.
5. 34 bob belgisi progress asosida ishlaydi; ular alohida checkpoint quiz emas. 172 ochiq refleksiya self/teacher rubrikasida, avtomatik esse baholash yoki teacher submission workflow yaratilmagan. Matnli xarita tahlili manba sahifalariga tayanadi; yangi interaktiv kartografik renderer yaratilgani da’vo qilinmaydi.
6. Standalone yangi sandbox CLI bu muhitdagi Git markerlari sabab to‘liq tekshirilmagan. Ikki positive sandbox testi full suite’dan chiqarildi; guard chetlab o‘tilmadi. SQLite ASGI/API va real loopback PostgreSQL sinovlari o‘tdi. Production migratsiya yoki deploy bajarilmadi.

PDFlar `/workspace/attachments`da, xususiy tasvirlar `/workspace/.setup/uzbekistan-history`da. Yangi muhitda ularni mavjud deb taxmin qilmang: source catalog SHA bilan tekshiring. PDF/rasm/OCRni Gitga qo‘shmang. Keyingi bosqich — teacher/rasmiy dastur/Android/normal mobil integratsiya. Production deploy, main merge yoki nashr ruxsati yo‘q.
