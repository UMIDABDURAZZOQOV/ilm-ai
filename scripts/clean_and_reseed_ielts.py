"""
Clean duplicate IELTS entries and re-seed with audio mapping.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsListening, IeltsReading, IeltsWriting, IeltsSpeaking

def clean_and_reseed():
    """Delete all IELTS content and re-seed cleanly."""
    db = SessionLocal()
    
    try:
        # Delete all existing IELTS content
        print("Deleting existing IELTS content...")
        db.query(IeltsListening).delete()
        db.query(IeltsReading).delete()
        db.query(IeltsWriting).delete()
        db.query(IeltsSpeaking).delete()
        db.commit()
        print("All IELTS content deleted.")
        
        # Now re-seed
        print("\nRe-seeding IELTS content...")
        exec(open(r"c:\Users\Page\Desktop\Projects\ilm-ai\scripts\seed_ielts_21.py").read())
        
        # Update audio URL for Test 1 Part 1
        print("\nUpdating audio URL for Test 1 Part 1...")
        listening = db.query(IeltsListening).filter(IeltsListening.section == 1).first()
        if listening:
            listening.audio_url = "/audio/listening/205_we.mp3"
            db.commit()
            print(f"Updated listening ID {listening.id} with audio URL")
        
        # Show final status
        print("\n=== Final Status ===")
        print(f"Listening entries: {db.query(IeltsListening).count()}")
        print(f"Reading entries: {db.query(IeltsReading).count()}")
        print(f"Writing entries: {db.query(IeltsWriting).count()}")
        print(f"Speaking entries: {db.query(IeltsSpeaking).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clean_and_reseed()
