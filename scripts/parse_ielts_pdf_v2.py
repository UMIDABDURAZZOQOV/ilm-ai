"""
Improved script to parse IELTS Academic 21 PDF with better pattern matching.
"""
import pypdf
import json
import re
from pathlib import Path
from typing import Dict, List, Any

def parse_ielts_pdf(pdf_path: str) -> Dict[str, Any]:
    """Parse IELTS Academic PDF and extract structured content."""
    pdf_reader = pypdf.PdfReader(pdf_path)
    num_pages = len(pdf_reader.pages)
    
    content = {
        "book_info": {
            "title": "IELTS Academic 21",
            "year": 2026,
            "total_pages": num_pages
        },
        "tests": []
    }
    
    # Extract text from all pages with page numbers
    pages_text = []
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        pages_text.append({
            "page_num": page_num + 1,
            "text": text
        })
    
    # Combine all text
    full_text = "\n".join([p["text"] for p in pages_text])
    
    # Look for actual test structure - Cambridge IELTS books typically have "Test 1", "Test 2", etc.
    # Try multiple patterns
    test_patterns = [
        r"Test\s+(\d+)",  # Test 1, Test 2
        r"TEST\s+(\d+)",  # TEST 1, TEST 2
        r"Cambridge\s+IELTS\s+\d+.*?Test\s+(\d+)",  # Cambridge IELTS 21 Test 1
    ]
    
    test_matches = []
    for pattern in test_patterns:
        matches = list(re.finditer(pattern, full_text, re.IGNORECASE))
        if matches:
            test_matches.extend(matches)
            break
    
    # If no clear test markers, assume 4 tests based on page ranges
    if not test_matches:
        print("No clear test markers found. Assuming 4 tests based on page ranges.")
        pages_per_test = num_pages // 4
        for i in range(4):
            start_page = i * pages_per_test
            end_page = (i + 1) * pages_per_test if i < 3 else num_pages
            test_text = "\n".join([p["text"] for p in pages_text[start_page:end_page]])
            
            test_content = {
                "test_number": i + 1,
                "page_range": f"{start_page + 1}-{end_page}",
                "listening": extract_listening_section(test_text),
                "reading": extract_reading_section(test_text),
                "writing": extract_writing_section(test_text),
                "speaking": extract_speaking_section(test_text)
            }
            content["tests"].append(test_content)
    else:
        # Use found test markers
        for i, match in enumerate(test_matches[:4]):  # Limit to 4 tests
            test_num = int(match.group(1))
            test_start = match.start()
            test_end = test_matches[i + 1].start() if i + 1 < len(test_matches) else len(full_text)
            test_text = full_text[test_start:test_end]
            
            test_content = {
                "test_number": test_num,
                "listening": extract_listening_section(test_text),
                "reading": extract_reading_section(test_text),
                "writing": extract_writing_section(test_text),
                "speaking": extract_speaking_section(test_text)
            }
            content["tests"].append(test_content)
    
    return content

def extract_listening_section(text: str) -> Dict[str, Any]:
    """Extract listening section content."""
    listening = {
        "sections": [],
        "notes": "Listening requires separate audio files (MP3). This section extracts transcripts/questions."
    }
    
    # Look for Section 1-4 patterns
    section_patterns = [
        r"Section\s+(\d+):\s*(.*?)(?=Section\s+\d+|$)",
        r"SECTION\s+(\d+):\s*(.*?)(?=SECTION\s+\d+|$)",
        r"Part\s+(\d+):\s*(.*?)(?=Part\s+\d+|$)",  # Some books use Part instead of Section
    ]
    
    for pattern in section_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            section_num = int(match.group(1))
            content = match.group(2).strip()[:500]
            
            listening["sections"].append({
                "section_number": section_num,
                "content_preview": content
            })
    
    return listening

def extract_reading_section(text: str) -> Dict[str, Any]:
    """Extract reading passages."""
    reading = {
        "passages": []
    }
    
    # Look for Reading Passage patterns
    passage_patterns = [
        r"Reading Passage\s+(\d+)\s*\n(.*?)(?=Reading Passage\s+\d+|Questions\s+\d+-\d+|$)",
        r"READING PASSAGE\s+(\d+)\s*\n(.*?)(?=READING PASSAGE\s+\d+|QUESTIONS\s+\d+-\d+|$)",
    ]
    
    for pattern in passage_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            passage_num = int(match.group(1))
            passage_text = match.group(2).strip()
            
            # Extract title (first line)
            lines = passage_text.split('\n')
            title = lines[0] if lines else ""
            body = '\n'.join(lines[1:]) if len(lines) > 1 else passage_text
            
            reading["passages"].append({
                "passage_number": passage_num,
                "title": title[:200],
                "text": body[:3000]  # First 3000 chars
            })
    
    return reading

def extract_writing_section(text: str) -> Dict[str, Any]:
    """Extract writing tasks."""
    writing = {
        "tasks": []
    }
    
    # Look for Writing Task patterns
    task_patterns = [
        r"Writing Task\s+(\d+)\s*\n(.*?)(?=Writing Task\s+\d+|Speaking|$)",
        r"WRITING TASK\s+(\d+)\s*\n(.*?)(?=WRITING TASK\s+\d+|SPEAKING|$)",
    ]
    
    for pattern in task_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            task_num = int(match.group(1))
            task_text = match.group(2).strip()
            
            # Determine task type
            task_type = "Task 1" if task_num == 1 else "Task 2"
            category = "Academic Task 1" if task_num == 1 else "Essay"
            
            writing["tasks"].append({
                "task_type": task_type,
                "category": category,
                "prompt": task_text[:1500]
            })
    
    return writing

def extract_speaking_section(text: str) -> Dict[str, Any]:
    """Extract speaking topics."""
    speaking = {
        "parts": []
    }
    
    # Look for Speaking Part patterns
    part_patterns = [
        r"Part\s+(\d+)\s*\n(.*?)(?=Part\s+\d+|$)",
        r"PART\s+(\d+)\s*\n(.*?)(?=PART\s+\d+|$)",
    ]
    
    for pattern in part_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            part_num = int(match.group(1))
            part_text = match.group(2).strip()
            
            # Extract topic and questions
            lines = part_text.split('\n')
            topic = lines[0] if lines else ""
            questions = [line.strip() for line in lines[1:] if line.strip() and '?' in line][:5]
            
            speaking["parts"].append({
                "part_number": part_num,
                "topic": topic[:300],
                "questions": questions,
                "cue_card": part_text[:500] if part_num == 2 else None
            })
    
    return speaking

def main():
    pdf_path = r"c:\Users\Page\Downloads\IELTS_21.pdf"
    output_path = r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\ielts_21_parsed_v2.json"
    
    print(f"Parsing PDF: {pdf_path}")
    content = parse_ielts_pdf(pdf_path)
    
    print(f"\n=== Parsing Results ===")
    print(f"Book: {content['book_info']['title']}")
    print(f"Total pages: {content['book_info']['total_pages']}")
    print(f"Tests found: {len(content['tests'])}")
    
    for test in content['tests']:
        print(f"\n--- Test {test['test_number']} ---")
        if 'page_range' in test:
            print(f"Pages: {test['page_range']}")
        print(f"Listening sections: {len(test['listening']['sections'])}")
        print(f"Reading passages: {len(test['reading']['passages'])}")
        print(f"Writing tasks: {len(test['writing']['tasks'])}")
        print(f"Speaking parts: {len(test['speaking']['parts'])}")
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print(f"\nParsed content saved to: {output_path}")

if __name__ == "__main__":
    main()
