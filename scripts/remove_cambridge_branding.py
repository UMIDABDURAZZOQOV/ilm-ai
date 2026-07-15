"""
Remove Cambridge branding from IELTS content
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsReading, IeltsWriting, IeltsSpeaking, IeltsListening

def remove_cambridge_branding(db: Session):
    """Remove Cambridge branding from content titles"""
    print("Removing Cambridge branding...")
    
    # Update Listening titles
    listenings = db.query(IeltsListening).all()
    for listening in listenings:
        old_title = listening.title
        if "Cambridge" in old_title:
            # Extract the actual topic
            if "Section 1" in old_title:
                new_title = old_title.split(": ")[-1] if ": " in old_title else "Listening Practice - Section 1"
            elif "Section 2" in old_title:
                new_title = old_title.split(": ")[-1] if ": " in old_title else "Listening Practice - Section 2"
            elif "Section 3" in old_title:
                new_title = old_title.split(": ")[-1] if ": " in old_title else "Listening Practice - Section 3"
            elif "Section 4" in old_title:
                new_title = old_title.split(": ")[-1] if ": " in old_title else "Listening Practice - Section 4"
            else:
                new_title = old_title.replace("Cambridge", "").replace("Test 1", "").replace("Test 2", "").strip()
            
            listening.title = new_title
            print(f"  Updated: {old_title} → {new_title}")
    
    # Update Reading titles
    readings = db.query(IeltsReading).all()
    for reading in readings:
        old_title = reading.title
        if "Cambridge" in old_title:
            # Extract the actual topic
            if "Passage 1" in old_title:
                new_title = old_title.split(": ")[-1] if ": " in old_title else "Reading Passage 1"
            elif "Passage 2" in old_title:
                new_title = old_title.split(": ")[-1] if ": " in old_title else "Reading Passage 2"
            elif "Passage 3" in old_title:
                new_title = old_title.split(": ")[-1] if ": " in old_title else "Reading Passage 3"
            else:
                new_title = old_title.replace("Cambridge", "").replace("Test 1", "").replace("Test 2", "").strip()
            
            reading.title = new_title
            print(f"  Updated: {old_title} → {new_title}")
    
    # Update Writing prompts (keep content, just remove any Cambridge references if any)
    writings = db.query(IeltsWriting).all()
    for writing in writings:
        if "Cambridge" in writing.prompt:
            writing.prompt = writing.prompt.replace("Cambridge", "")
            print(f"  Updated writing prompt")
    
    db.commit()
    print("✓ Cambridge branding removed")

def main():
    db = SessionLocal()
    try:
        remove_cambridge_branding(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
