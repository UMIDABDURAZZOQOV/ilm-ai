"""
Seeder script to populate IELTS database tables with content from IELTS Academic 21.
This script reads the parsed JSON and inserts data into the database.
"""
import json
import sys
import os

# Add parent directory to path to import from services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import get_db, engine, Base
from services.models import (
    IeltsListening, IeltsReading, IeltsWriting, IeltsSpeaking, IeltsQuestion
)

# Load parsed content
PARSED_JSON_PATH = r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\ielts_21_final.json"

def seed_ielts_content():
    """Seed IELTS content from parsed JSON into database."""
    
    # Load parsed content
    with open(PARSED_JSON_PATH, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    print(f"Loading content from: {content['book_info']['title']}")
    print(f"Tests to process: {len(content['tests'])}")
    
    # Create database session
    from services.db import SessionLocal
    db = SessionLocal()
    
    try:
        # Track IDs for creating questions
        listening_ids = []
        reading_ids = []
        writing_ids = []
        speaking_ids = []
        
        for test in content['tests']:
            test_num = test['test_number']
            print(f"\n--- Processing Test {test_num} ---")
            
            # Seed Listening
            for part in test['listening']['sections']:
                listening = IeltsListening(
                    section=part['part_number'],
                    title=f"Test {test_num} - Listening Part {part['part_number']}",
                    audio_url=None,  # Will be updated when MP3 files are provided
                    transcript=part['content_preview'],
                    difficulty="medium",
                    duration_seconds=None  # Will be updated when MP3 files are provided
                )
                db.add(listening)
                db.flush()
                listening_ids.append(listening.id)
                print(f"  Added Listening Part {part['part_number']} (ID: {listening.id})")
            
            # Seed Reading - filter out duplicates (keep only passages with substantial content)
            seen_passages = set()
            for passage in test['reading']['passages']:
                passage_num = passage['passage_number']
                
                # Skip if we've already seen this passage number (it's a duplicate)
                if passage_num in seen_passages:
                    continue
                
                # Skip passages with very short text (likely question-only entries)
                if len(passage['text'].split()) < 50:
                    continue
                
                seen_passages.add(passage_num)
                word_count = len(passage['text'].split())
                reading = IeltsReading(
                    section=passage_num,
                    title=passage['title'] if passage['title'] and len(passage['title']) > 20 else f"Test {test_num} - Reading Passage {passage_num}",
                    passage_text=passage['text'],
                    difficulty="medium",
                    word_count=word_count
                )
                db.add(reading)
                db.flush()
                reading_ids.append(reading.id)
                print(f"  Added Reading Passage {passage_num} (ID: {reading.id}, {word_count} words)")
            
            # Seed Writing
            for task in test['writing']['tasks']:
                writing = IeltsWriting(
                    task_type=task['task_type'].replace(' ', ''),
                    category=task['category'],
                    prompt=task['prompt'],
                    image_url=None,
                    min_words=150 if task['task_type'] == "Task 1" else 250,
                    duration_minutes=20 if task['task_type'] == "Task 1" else 40,
                    difficulty="medium"
                )
                db.add(writing)
                db.flush()
                writing_ids.append(writing.id)
                print(f"  Added Writing {task['task_type']} (ID: {writing.id})")
            
            # Seed Speaking
            for part in test['speaking']['parts']:
                speaking = IeltsSpeaking(
                    part=part['part_number'],
                    topic=part['topic'] or f"Test {test_num} - Speaking Part {part['part_number']}",
                    questions=part['questions'] or [],
                    cue_card=part.get('cue_card'),
                    prep_seconds=60 if part['part_number'] == 2 else None,
                    speak_seconds=120 if part['part_number'] == 2 else None,
                    difficulty="medium"
                )
                db.add(speaking)
                db.flush()
                speaking_ids.append(speaking.id)
                print(f"  Added Speaking Part {part['part_number']} (ID: {speaking.id})")
        
        # Commit all changes
        db.commit()
        
        print(f"\n=== Seeding Complete ===")
        print(f"Listening entries: {len(listening_ids)}")
        print(f"Reading entries: {len(reading_ids)}")
        print(f"Writing entries: {len(writing_ids)}")
        print(f"Speaking entries: {len(speaking_ids)}")
        
        # Note about questions
        print(f"\nNOTE: Questions were NOT seeded from the PDF.")
        print(f"The PDF contains question text but not answers/answer keys.")
        print(f"To seed questions, you need to:")
        print(f"1. Extract answer keys from pages 117-124 of the PDF")
        print(f"2. Or provide separate answer key data")
        print(f"3. Then run a question seeder script")
        
        # Note about listening audio
        print(f"\nNOTE: Listening audio files (MP3) are required.")
        print(f"Place MP3 files in the frontend public/audio/listening/ directory")
        print(f"Then update the audio_url field in the database")
        
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_ielts_content()
