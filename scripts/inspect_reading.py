"""
Inspect reading passage extraction to understand the issue.
"""
import pypdf
import re

pdf_path = r"c:\Users\Page\Downloads\IELTS_21.pdf"
pdf_reader = pypdf.PdfReader(pdf_path)

# Extract pages 10-31 (Test 1)
test_text = ""
for page_num in range(9, 31):
    page = pdf_reader.pages[page_num]
    test_text += page.extract_text() + "\n\n"

# Look for READING PASSAGE patterns
passage_pattern = r"READING PASSAGE\s+(\d+)\s*\n(.*?)(?=Questions\s+\d+-\d+|READING PASSAGE\s+\d+|$)"
matches = list(re.finditer(passage_pattern, test_text, re.IGNORECASE | re.DOTALL))

output_file = r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\reading_inspection.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Found {len(matches)} reading passages\n\n")
    
    for match in matches:
        passage_num = int(match.group(1))
        passage_text = match.group(2).strip()
        
        f.write(f"=== PASSAGE {passage_num} ===\n")
        f.write(f"Length: {len(passage_text)} chars\n")
        f.write(f"First 500 chars:\n{passage_text[:500]}\n\n")
        f.write(f"Full text (first 2000 chars):\n{passage_text[:2000]}\n\n")
        f.write("-" * 80 + "\n\n")

print(f"Reading inspection saved to: {output_file}")
