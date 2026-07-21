"""
Inspect pages 16-20 to see actual reading passage structure.
"""
import pypdf

pdf_path = r"c:\Users\Page\Downloads\IELTS_21.pdf"
pdf_reader = pypdf.PdfReader(pdf_path)

output_file = r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\pages_16_20.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    for page_num in range(15, 20):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        
        f.write(f"=== PAGE {page_num + 1} ===\n")
        f.write(text[:2000] if text else "No text")
        f.write("\n\n" + "-" * 80 + "\n\n")

print(f"Pages 16-20 saved to: {output_file}")
