"""
Remove duplicate IELTS content from database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsReading, IeltsWriting, IeltsSpeaking, IeltsListening, IeltsQuestion
from sqlalchemy import func

def remove_duplicates(db: Session):
    """Remove duplicate content based on title/topic"""
    print("Removing duplicate content...")
    
    # Remove duplicate readings (keep first occurrence)
    print("Checking Reading duplicates...")
    readings = db.query(IeltsReading).all()
    seen_titles = set()
    for reading in readings:
        if reading.title in seen_titles:
            print(f"  Deleting duplicate reading: {reading.title}")
            db.delete(reading)
        else:
            seen_titles.add(reading.title)
    
    # Remove duplicate writings (keep first occurrence)
    print("Checking Writing duplicates...")
    writings = db.query(IeltsWriting).all()
    seen_tasks = set()
    for writing in writings:
        task_key = f"{writing.task_type}-{writing.category}"
        if task_key in seen_tasks:
            print(f"  Deleting duplicate writing: {writing.task_type} - {writing.category}")
            db.delete(writing)
        else:
            seen_tasks.add(task_key)
    
    # Remove duplicate speaking (keep first occurrence)
    print("Checking Speaking duplicates...")
    speakings = db.query(IeltsSpeaking).all()
    seen_topics = set()
    for speaking in speakings:
        if speaking.topic in seen_topics:
            print(f"  Deleting duplicate speaking: {speaking.topic}")
            db.delete(speaking)
        else:
            seen_topics.add(speaking.topic)
    
    # Remove duplicate listenings (keep first occurrence)
    print("Checking Listening duplicates...")
    listenings = db.query(IeltsListening).all()
    seen_titles = set()
    for listening in listenings:
        if listening.title in seen_titles:
            print(f"  Deleting duplicate listening: {listening.title}")
            db.delete(listening)
        else:
            seen_titles.add(listening.title)
    
    # Remove orphaned questions
    print("Removing orphaned questions...")
    db.query(IeltsQuestion).filter(
        IeltsQuestion.skill == "Reading",
        ~IeltsQuestion.parent_id.in_(db.query(IeltsReading.id))
    ).delete(synchronize_session=False)
    
    db.query(IeltsQuestion).filter(
        IeltsQuestion.skill == "Listening",
        ~IeltsQuestion.parent_id.in_(db.query(IeltsListening.id))
    ).delete(synchronize_session=False)
    
    db.commit()
    print("✓ Duplicates removed")

def main():
    db = SessionLocal()
    try:
        remove_duplicates(db)
        
        # Show final counts
        print("\nFinal counts:")
        print(f"  Listening: {db.query(IeltsListening).count()} tests")
        print(f"  Reading: {db.query(IeltsReading).count()} passages")
        print(f"  Writing: {db.query(IeltsWriting).count()} tasks")
        print(f"  Speaking: {db.query(IeltsSpeaking).count()} topics")
        print(f"  Total Questions: {db.query(IeltsQuestion).count()}")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
