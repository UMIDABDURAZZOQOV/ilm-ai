"""
Script to parse IELTS Academic 21 PDF and extract content for database seeding.
This script extracts reading passages, writing tasks, and speaking topics.
Listening sections require separate audio files.
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
    
    # Extract text from all pages
    full_text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        full_text += page.extract_text() + "\n\n"
    
    # Parse tests (Test 1, Test 2, Test 3, Test 4)
    test_pattern = r"TEST\s+(\d+)"
    tests = re.finditer(test_pattern, full_text, re.IGNORECASE)
    
    test_starts = [match.start() for match in tests]
    
    for i, test_start in enumerate(test_starts):
        test_num = i + 1
        test_end = test_starts[i + 1] if i + 1 < len(test_starts) else len(full_text)
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
        "transcripts": []
    }
    
    # Look for Section 1, 2, 3, 4
    section_pattern = r"SECTION\s+(\d+)"
    sections = re.finditer(section_pattern, text, re.IGNORECASE)
    
    for match in sections:
        section_num = int(match.group(1))
        section_text = text[match.start():match.start() + 2000]  # Get context
        
        listening["sections"].append({
            "section_number": section_num,
            "content": section_text[:500]  # First 500 chars as preview
        })
    
    return listening

def extract_reading_section(text: str) -> Dict[str, Any]:
    """Extract reading passages."""
    reading = {
        "passages": []
    }
    
    # Look for Reading Passage 1, 2, 3
    passage_pattern = r"READING PASSAGE\s+(\d+)"
    passages = re.finditer(passage_pattern, text, re.IGNORECASE)
    
    for match in passages:
        passage_num = int(match.group(1))
        passage_start = match.end()
        
        # Extract passage text (until next passage or end)
        next_passage = re.search(r"READING PASSAGE\s+\d+", text[passage_start:], re.IGNORECASE)
        if next_passage:
            passage_end = passage_start + next_passage.start()
        else:
            passage_end = len(text)
        
        passage_text = text[passage_start:passage_end].strip()
        
        reading["passages"].append({
            "passage_number": passage_num,
            "title": passage_text[:100] if passage_text else "",
            "text": passage_text[:2000]  # First 2000 chars
        })
    
    return reading

def extract_writing_section(text: str) -> Dict[str, Any]:
    """Extract writing tasks."""
    writing = {
        "tasks": []
    }
    
    # Look for Writing Task 1 and Task 2
    task1_pattern = r"WRITING TASK\s+1"
    task2_pattern = r"WRITING TASK\s+2"
    
    task1_match = re.search(task1_pattern, text, re.IGNORECASE)
    task2_match = re.search(task2_pattern, text, re.IGNORECASE)
    
    if task1_match:
        task1_start = task1_match.end()
        task1_end = task2_match.start() if task2_match else len(text)
        task1_text = text[task1_start:task1_end].strip()
        
        writing["tasks"].append({
            "task_type": "Task 1",
            "category": "Academic",  # Could be General Training
            "prompt": task1_text[:1000]
        })
    
    if task2_match:
        task2_start = task2_match.end()
        task2_text = text[task2_start:task2_start + 1000].strip()
        
        writing["tasks"].append({
            "task_type": "Task 2",
            "category": "Essay",
            "prompt": task2_text[:1000]
        })
    
    return writing

def extract_speaking_section(text: str) -> Dict[str, Any]:
    """Extract speaking topics."""
    speaking = {
        "parts": []
    }
    
    # Look for Part 1, 2, 3
    part_pattern = r"PART\s+(\d+)"
    parts = re.finditer(part_pattern, text, re.IGNORECASE)
    
    for match in parts:
        part_num = int(match.group(1))
        part_start = match.end()
        
        # Extract part content
        next_part = re.search(r"PART\s+\d+", text[part_start:], re.IGNORECASE)
        if next_part:
            part_end = part_start + next_part.start()
        else:
            part_end = len(text)
        
        part_text = text[part_start:part_end].strip()
        
        speaking["parts"].append({
            "part_number": part_num,
            "topic": part_text[:200] if part_text else "",
            "questions": extract_questions(part_text)
        })
    
    return speaking

def extract_questions(text: str) -> List[str]:
    """Extract questions from text."""
    questions = []
    
    # Look for question patterns
    question_patterns = [
        r"[A-Z][^.?]*\?",  # Sentences ending with ?
        r"\d+\.\s+[A-Z][^.?]*\?"  # Numbered questions
    ]
    
    for pattern in question_patterns:
        matches = re.findall(pattern, text)
        questions.extend(matches[:5])  # Limit to first 5 questions
    
    return questions

def main():
    pdf_path = r"c:\Users\Page\Downloads\IELTS_21.pdf"
    output_path = r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\ielts_21_parsed.json"
    
    print(f"Parsing PDF: {pdf_path}")
    content = parse_ielts_pdf(pdf_path)
    
    print(f"Found {len(content['tests'])} tests")
    for test in content['tests']:
        print(f"  Test {test['test_number']}:")
        print(f"    Reading passages: {len(test['reading']['passages'])}")
        print(f"    Writing tasks: {len(test['writing']['tasks'])}")
        print(f"    Speaking parts: {len(test['speaking']['parts'])}")
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print(f"\nParsed content saved to: {output_path}")

if __name__ == "__main__":
    main()
