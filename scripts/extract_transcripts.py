"""
Extract audioscripts from pages 97-116 of IELTS 21 PDF.
"""
import pypdf
import json
import re

pdf_path = r"c:\Users\Page\Downloads\IELTS_21.pdf"
pdf_reader = pypdf.PdfReader(pdf_path)

# Extract audioscripts pages (97-116 based on Contents)
transcripts_text = ""
for page_num in range(96, 116):  # Pages 97-116 (0-indexed: 96-115)
    page = pdf_reader.pages[page_num]
    transcripts_text += page.extract_text() + "\n\n"

# Save raw extraction for inspection
with open(r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\raw_transcripts.txt", 'w', encoding='utf-8') as f:
    f.write(transcripts_text)

print("Raw transcripts extracted to raw_transcripts.txt")
print(f"Total characters: {len(transcripts_text)}")

# Now parse by test and part
transcripts = {}

# Pattern to find test headers in audioscripts section
test_pattern = r"TEST\s+(\d+)"
test_matches = list(re.finditer(test_pattern, transcripts_text, re.IGNORECASE))

for i, match in enumerate(test_matches):
    test_num = int(match.group(1))
    
    # Get text from this test to next test or end
    start_pos = match.start()
    if i + 1 < len(test_matches):
        end_pos = test_matches[i + 1].start()
    else:
        end_pos = len(transcripts_text)
    
    test_text = transcripts_text[start_pos:end_pos]
    
    # Find parts within this test
    part_pattern = r"PART\s+(\d+)"
    part_matches = list(re.finditer(part_pattern, test_text, re.IGNORECASE))
    
    test_transcripts = {}
    for j, part_match in enumerate(part_matches):
        part_num = int(part_match.group(1))
        
        # Get text from this part to next part or end
        part_start = part_match.start()
        if j + 1 < len(part_matches):
            part_end = part_matches[j + 1].start()
        else:
            part_end = len(test_text)
        
        part_text = test_text[part_start:part_end].strip()
        test_transcripts[part_num] = part_text
    
    transcripts[test_num] = test_transcripts

# Save parsed transcripts
with open(r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\parsed_transcripts.json", 'w', encoding='utf-8') as f:
    json.dump(transcripts, f, indent=2, ensure_ascii=False)

print("\n=== Parsed Transcripts ===")
for test_num, parts in transcripts.items():
    print(f"\nTest {test_num}:")
    for part_num, text in parts.items():
        print(f"  Part {part_num}: {len(text)} characters")
