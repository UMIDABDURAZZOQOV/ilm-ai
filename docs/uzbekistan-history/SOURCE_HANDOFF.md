# 8-sinf manbasini davom ettirish — 2026-10-27

**2026-10-27: bu manba to‘sig‘i yopildi.** To‘rtta segment haqiqatan olindi va tekshirildi. Quyidagi eski matn tarixiy checkpoint sifatida saqlandi; joriy davom nuqtasi [STAGE2_PROGRESS.md](STAGE2_PROGRESS.md), yangi manba auditi [GRADE8_SOURCE_REVIEW.md](GRADE8_SOURCE_REVIEW.md).

Joriy haqiqiy manba to‘sig‘i: `ozbekiston_tarixi_8_uzb.pdf`, attachment `file_000000009ed0824399cda20ac00057a3`, foydalanuvchi bildirgan45.4 MB/160sahifa. Executor `download_file`32MiBdan katta faylni ko‘chirmaydi. Windowsdagi `C:\Users\Page\Desktop\O'zbekiston Tarixi` bu cloud muhitida mavjud emas. Fayl baytlari olinmagan: SHA, muallif/ISBN, bob/mavzu soni, OCR yoki fakt tasdig‘i yo‘q. Jami besh kitob mavzu soni ham noma’lum.

Kerakli uzluksiz segmentlar: **PDF1–40,41–80,81–120,121–160**; har biri32MiBdan kichik. Bular bosma emas, asl PDF indekslari. Agar bir segment katta chiqsa uni yanada kichik, chegaralari aniq bo‘lgan qismlarga ajratish mumkin. Asl PDF, qismlar va OCR hech qachon Gitga qo‘shilmaydi.

Foydalanuvchi kompyuterida PyMuPDF o‘rnatilgach, quyidagi Python kodini manba papkasida ishga tushirish mumkin. Bu kod bu cloud muhitida 8-sinf baytlari yo‘qligi sabab bajarilmagan; natijalar tasdiqlangan deb ko‘rsatilmaydi. Original PDFni o‘zgartirmaydi, mavjud output papkasini qayta yozmaydi. Output ham barcha Git repozitoriyalaridan tashqarida bo‘lsin.

```python
from pathlib import Path
import hashlib, json, fitz

original = Path("ozbekiston_tarixi_8_uzb.pdf")
output = Path("ozbekiston_tarixi_8_private_parts")
assert not any((p / ".git").exists() for p in [output.resolve(), *output.resolve().parents])
book = fitz.open(original)
assert len(book) == 160, "Sahifalar soni o‘zgargan: taxmin qilmang"
output.mkdir()  # Existing output is never overwritten.
manifest = {"original_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
            "original_pdf_pages": len(book), "segments": []}
for first, last in [(1,40), (41,80), (81,120), (121,160)]:
    segment = fitz.open()
    segment.insert_pdf(book, from_page=first-1, to_page=last-1)
    target = output / f"ozbekiston_tarixi_8_pdf_{first:03}-{last:03}.pdf"
    segment.save(target, garbage=4, deflate=True)
    segment.close()
    assert target.stat().st_size < 32*1024*1024, "Segmentni yanada kichraytiring"
    with fitz.open(target) as check:
        assert len(check) == last-first+1
    manifest["segments"].append({"file": target.name, "first_pdf_page": first,
        "last_pdf_page": last, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
(output / "source_manifest.private.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
book.close()
```

## Keyingi sessiya uchun aniq tartib

1. Ikkala history feature branchidagi eng yangi remote commit va lokal o‘zgarishlarni tekshiring;7-sinf42r1 darsini qayta yozmang. `CLAUDE.md`, `COURSE_COMPLETION.md`, `STAGE2_PROGRESS.md` va himoyalangan baseline’ni o‘qing.
2. Barcha segmentlarni haqiqatda oling, bayt SHA va sahifa sonini tekshiring. Ketma-ketlik1dan160gacha aynan bir marta bo‘lsin; bir xil sahifa indeksini ikki marta sanamang. Manifest va asl SHA olingan bo‘lsa ham segmentlardan qayta tuzilgan PDF baytlari original SHAga teng bo‘lishi shart emas: qayta yozish PDF metadata/strukturani o‘zgartiradi. Original identifikatori va har segment SHA alohida saqlanadi.
3. 8-sinf skanerlangan: OCR locator xolos. Bibliografiya, mundarija va har mavzu sarlavhasini asl tasvirdan o‘qing. PDF va bosma sahifa offsetini taxmin qilmang; yetishgan sahifani alohida tekshiring. Har kartaga/savolga kiradigan fakt, sana va javob uchun asl tasvirni qayta ko‘ring. OCR/transkript/tasvirni Gitga qo‘shmang.
4. Haqiqiy bob/paragraf sonini katalogdan hisoblang; existing schema va auditdagi `blocked_books` holatini faqat haqiqiy dalil bilan yangilang. Kombinatsiyalangan mavzu, qaytarilgan sarlavha, kirish/xulosa alohida ajratilsin.
5. So‘ng8-sinfning birinchi haqiqiy mavzusidan5–10darslik partiyalar: original kartalar→misol→MCQ/qisqa obyektiv FRQ/xronologiya→feedback. Keyingi tartib9→10→11.8mavzu nomi va boshlanish sahifasi hozircha noma’lum; taxminiy «§1» mazmuni yozilmasin.
6. Kontent immutable yangi batch/reviewSHA bilan; literal mustaqil answer oracle; source audit/SQLite/API/XP/replay/parallel yakun/PostgreSQL fresh owned schema; Flutter capture va responsive/retry testlari. Har checkpoint docs/CLAUDE va ikki feature branchga xavfsiz commit/push. Production, main, veb, boshqa fanlar va parallel agent branchlari o‘zgarmasin.

## Ochiq integratsiya ishlari

42dars lokal/test preview’da; normal mobil katalogga ulanmagan. Olti bob tugallanish belgisi bor, alohida checkpoint quiz hali yo‘q. Esse uchun self/teacher rubrika bor, lekin teacher workflow implementatsiya qilinmagan. Immutable r1dan keyingi revisionni aktivlashtirish strategiyasi alohida ko‘rib chiqiladi. Flutter’dagi `docs/uzbekistan-history/ANDROID_QA_HANDOFF.md` va tegishli patch hali shared Gradlega qo‘llanmagan; Android SDK/build/telefon tekshiruvi yo‘q. Mustaqil tarix o‘qituvchisi va2026–2027rasmiy dastur auditi ham ochiq.
