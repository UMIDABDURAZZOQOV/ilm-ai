"""
Extract audioscripts from pages 97-116 of IELTS 21 PDF - improved version.
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

# Find the "Audioscripts" section start
audioscripts_start = transcripts_text.find("Audioscripts")
if audioscripts_start > 0:
    transcripts_text = transcripts_text[audioscripts_start:]

transcripts = {}

# Split by TEST markers
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
    
    # Find PART markers within this test
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
        
        # Clean up the text - remove empty lines and speaker labels that are empty
        lines = [line.strip() for line in part_text.split('\n') if line.strip() and len(line) > 2]
        cleaned_text = '\n'.join(lines)
        
        if len(cleaned_text) > 100:  # Only keep substantial transcripts
            test_transcripts[part_num] = cleaned_text
    
    if test_transcripts:
        transcripts[test_num] = test_transcripts

# Save parsed transcripts
with open(r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\parsed_transcripts.json", 'w', encoding='utf-8') as f:
    json.dump(transcripts, f, indent=2, ensure_ascii=False)

print("\n=== Parsed Transcripts ===")
for test_num, parts in transcripts.items():
    print(f"\nTest {test_num}:")
    for part_num, text in parts.items():
        print(f"  Part {part_num}: {len(text)} characters")

print(f"\nTotal tests with transcripts: {len(transcripts)}")
