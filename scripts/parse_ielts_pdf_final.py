"""
Final improved parser for IELTS Academic 21 PDF using exact page ranges from Contents.
"""
import pypdf
import json
import re
from typing import Dict, List, Any

# Page ranges from Contents (page 4)
TEST_PAGE_RANGES = {
    1: (10, 31),   # Test 1: pages 10-31
    2: (32, 53),   # Test 2: pages 32-53
    3: (54, 74),   # Test 3: pages 54-74
    4: (75, 96)    # Test 4: pages 75-96
}

def parse_ielts_pdf(pdf_path: str) -> Dict[str, Any]:
    """Parse IELTS Academic PDF using exact page ranges."""
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
    
    for test_num, (start_page, end_page) in TEST_PAGE_RANGES.items():
        # Extract text for this test's page range
        test_text = ""
        for page_num in range(start_page - 1, min(end_page, num_pages)):
            page = pdf_reader.pages[page_num]
            test_text += page.extract_text() + "\n\n"
        
        test_content = {
            "test_number": test_num,
            "page_range": f"{start_page}-{end_page}",
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
        "notes": "Listening requires separate audio files (MP3). This extracts questions/transcripts."
    }
    
    # Look for PART 1-4 patterns in Listening
    part_pattern = r"PART\s+(\d+)\s+Questions\s+(\d+)-(\d+)"
    matches = list(re.finditer(part_pattern, text, re.IGNORECASE))
    
    for match in matches:
        part_num = int(match.group(1))
        q_start = int(match.group(2))
        q_end = int(match.group(3))
        
        # Extract content after this part marker
        start_pos = match.start()
        next_match_idx = matches.index(match) + 1
        if next_match_idx < len(matches):
            end_pos = matches[next_match_idx].start()
        else:
            end_pos = start_pos + 2000
        
        part_text = text[start_pos:end_pos].strip()
        
        listening["sections"].append({
            "part_number": part_num,
            "question_range": f"{q_start}-{q_end}",
            "content_preview": part_text[:800]
        })
    
    return listening

def extract_reading_section(text: str) -> Dict[str, Any]:
    """Extract reading passages."""
    reading = {
        "passages": []
    }
    
    # Split by READING PASSAGE markers
    passage_markers = list(re.finditer(r"READING PASSAGE\s+(\d+)", text, re.IGNORECASE))
    
    for i, match in enumerate(passage_markers):
        passage_num = int(match.group(1))
        
        # Get the text from this passage marker to the next passage marker or end
        start_pos = match.end()
        if i + 1 < len(passage_markers):
            end_pos = passage_markers[i + 1].start()
        else:
            end_pos = len(text)
        
        passage_text = text[start_pos:end_pos].strip()
        
        # Find where the actual passage content starts (after instruction line)
        # Look for a line that's not an instruction
        lines = [line.strip() for line in passage_text.split('\n') if line.strip()]
        
        title = ""
        body_lines = []
        
        # Skip instruction lines (lines containing "You should spend", "Questions", etc.)
        for line in lines:
            if any(skip in line for skip in ["You should spend", "Questions", "based on Reading Passage"]):
                continue
            if not title and len(line) > 10:  # First substantial line is the title
                title = line
            elif title:
                body_lines.append(line)
        
        body = '\n'.join(body_lines)
        
        reading["passages"].append({
            "passage_number": passage_num,
            "title": title[:200] if title else f"Reading Passage {passage_num}",
            "text": body[:6000] if body else passage_text[:6000]
        })
    
    return reading

def extract_writing_section(text: str) -> Dict[str, Any]:
    """Extract writing tasks."""
    writing = {
        "tasks": []
    }
    
    # Look for Writing Task patterns
    task_pattern = r"WRITING\s+TASK\s+(\d+)\s*\n(.*?)(?=WRITING\s+TASK\s+\d+|SPEAKING|Test\s+\d+|$)"
    matches = list(re.finditer(task_pattern, text, re.IGNORECASE | re.DOTALL))
    
    for match in matches:
        task_num = int(match.group(1))
        task_text = match.group(2).strip()
        
        task_type = "Task 1" if task_num == 1 else "Task 2"
        category = "Academic Task 1" if task_num == 1 else "Essay"
        
        writing["tasks"].append({
            "task_type": task_type,
            "category": category,
            "prompt": task_text[:2000]
        })
    
    return writing

def extract_speaking_section(text: str) -> Dict[str, Any]:
    """Extract speaking topics."""
    speaking = {
        "parts": []
    }
    
    # Look for Speaking Part patterns
    part_pattern = r"Part\s+(\d+)\s*\n(.*?)(?=Part\s+\d+|Test\s+\d+|$)"
    matches = list(re.finditer(part_pattern, text, re.IGNORECASE | re.DOTALL))
    
    for match in matches:
        part_num = int(match.group(1))
        part_text = match.group(2).strip()
        
        # Extract topic and questions
        lines = [line.strip() for line in part_text.split('\n') if line.strip()]
        topic = lines[0] if lines else ""
        questions = [line for line in lines[1:] if '?' in line][:8]
        
        speaking["parts"].append({
            "part_number": part_num,
            "topic": topic[:300],
            "questions": questions,
            "cue_card": part_text[:600] if part_num == 2 else None
        })
    
    return speaking

def main():
    pdf_path = r"c:\Users\Page\Downloads\IELTS_21.pdf"
    output_path = r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\ielts_21_final.json"
    
    print(f"Parsing PDF: {pdf_path}")
    content = parse_ielts_pdf(pdf_path)
    
    print(f"\n=== Parsing Results ===")
    print(f"Book: {content['book_info']['title']}")
    print(f"Total pages: {content['book_info']['total_pages']}")
    print(f"Tests found: {len(content['tests'])}")
    
    for test in content['tests']:
        print(f"\n--- Test {test['test_number']} (Pages {test['page_range']}) ---")
        print(f"Listening parts: {len(test['listening']['sections'])}")
        print(f"Reading passages: {len(test['reading']['passages'])}")
        print(f"Writing tasks: {len(test['writing']['tasks'])}")
        print(f"Speaking parts: {len(test['speaking']['parts'])}")
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print(f"\nParsed content saved to: {output_path}")

if __name__ == "__main__":
    main()
