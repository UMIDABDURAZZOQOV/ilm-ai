"""
Import real IELTS content from GitHub IELTS AI Dataset
https://github.com/LuchoBazz/ielts-ai-dataset
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsReading, IeltsWriting, IeltsSpeaking, IeltsQuestion

def import_github_reading(db: Session):
    """Import reading tests from GitHub IELTS AI Dataset"""
    print("Importing reading tests from GitHub IELTS AI Dataset...")
    
    # Import multiple reading tests
    test_urls = [
        "https://raw.githubusercontent.com/LuchoBazz/ielts-ai-dataset/main/synthetic_official_mocks/reading/ielts_reading_academic_001.json",
        "https://raw.githubusercontent.com/LuchoBazz/ielts-ai-dataset/main/synthetic_official_mocks/reading/ielts_reading_academic_002.json",
        "https://raw.githubusercontent.com/LuchoBazz/ielts-ai-dataset/main/synthetic_official_mocks/reading/ielts_reading_academic_003.json",
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Check if already imported
            existing = db.query(IeltsReading).filter(IeltsReading.title == data["title"]).first()
            if existing:
                print(f"  Skipping - already imported: {data['title']}")
                continue
            
            # Create reading passage
            for passage in data["passages"]:
                reading = IeltsReading(
                    section=passage["passage_number"],
                    title=passage["title"],
                    passage_text=passage["content"],
                    difficulty="medium",
                    word_count=len(passage["content"].split())
                )
                db.add(reading)
                db.commit()
                db.refresh(reading)
                
                # Create questions
                for group in passage["question_groups"]:
                    for question in group["questions"]:
                        q_type = group["question_type"].lower().replace("-", "_")
                        if q_type == "true_false_not_given":
                            q_type = "tfng"
                        elif q_type == "yes_no_not_given":
                            q_type = "yng"
                        
                        question_obj = IeltsQuestion(
                            skill="Reading",
                            parent_id=reading.id,
                            question_type=q_type,
                            question_text=question["text"],
                            options=None,
                            correct_answer=question["answer"],
                            hint=group.get("instructions"),
                            order_index=question["question_order"]
                        )
                        db.add(question_obj)
                
                db.commit()
                print(f"  ✓ Imported: {passage['title']}")
            
        except Exception as e:
            print(f"  ✗ Failed to import reading from {url}: {e}")

def import_github_writing(db: Session):
    """Import writing tasks from GitHub IELTS AI Dataset"""
    print("Importing writing tasks from GitHub IELTS AI Dataset...")
    
    # GitHub API to get writing tests
    url = "https://raw.githubusercontent.com/LuchoBazz/ielts-ai-dataset/main/synthetic_official_mocks/writing/ielts_writing_academic_001.json"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Create writing tasks
        for task in data["tasks"]:
            # Check if already imported
            existing = db.query(IeltsWriting).filter(
                IeltsWriting.task_type == task["task_type"],
                IeltsWriting.category == task["category"]
            ).first()
            if existing:
                print(f"  Skipping - already imported: {task['task_type']} - {task['category']}")
                continue
            
            writing = IeltsWriting(
                task_type=task["task_type"],
                category=task["category"],
                prompt=task["prompt"],
                image_url=task.get("image_url"),
                min_words=task["min_words"],
                duration_minutes=task["duration_minutes"],
                difficulty="medium"
            )
            db.add(writing)
            db.commit()
            print(f"  ✓ Imported writing: {task['task_type']} - {task['category']}")
        
    except Exception as e:
        print(f"  ✗ Failed to import writing: {e}")

def main():
    db = SessionLocal()
    try:
        print("=" * 50)
        print("Importing from GitHub IELTS AI Dataset")
        print("=" * 50)
        
        import_github_reading(db)
        import_github_writing(db)
        
        print("=" * 50)
        print("Import complete!")
        print("=" * 50)
        
        # Show final counts
        print("\nFinal content counts:")
        print(f"  Reading: {db.query(IeltsReading).count()} passages")
        print(f"  Writing: {db.query(IeltsWriting).count()} tasks")
        print(f"  Speaking: {db.query(IeltsSpeaking).count()} topics")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
