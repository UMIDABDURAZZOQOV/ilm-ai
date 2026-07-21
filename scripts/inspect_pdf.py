"""
Inspect PDF to understand its structure and content format.
"""
import pypdf
import sys

# Set UTF-8 encoding for output
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

pdf_path = r"c:\Users\Page\Downloads\IELTS_21.pdf"
pdf_reader = pypdf.PdfReader(pdf_path)
num_pages = len(pdf_reader.pages)

output_file = r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\pdf_inspection.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Total pages: {num_pages}\n")
    f.write("\n" + "="*80 + "\n")

    # Extract text from first 15 pages to see structure
    for page_num in range(min(15, num_pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        
        f.write(f"\n--- PAGE {page_num + 1} ---\n")
        f.write(text[:1500] if text else "No text extracted")
        f.write("\n" + "-"*80 + "\n")

print(f"Inspection saved to: {output_file}")
