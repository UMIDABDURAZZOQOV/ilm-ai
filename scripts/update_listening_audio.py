"""
Script to update listening audio URLs in the database.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsListening

def update_listening_audio():
    """Update audio URLs for listening sections."""
    db = SessionLocal()
    
    try:
        # Get all listening entries
        listening_entries = db.query(IeltsListening).order_by(IeltsListening.id).all()
        
        print(f"Found {len(listening_entries)} listening entries")
        
        # Audio file naming convention: test{test_num}_part{part_num}.mp3
        # For now, update the first one (Test 1 Part 1) with the provided file
        # Find Test 1 Part 1 (section=1, title contains "Test 1")
        test1_part1 = db.query(IeltsListening).filter(
            IeltsListening.section == 1,
            IeltsListening.title.like("%Test 1%")
        ).first()
        
        if test1_part1:
            test1_part1.audio_url = "/audio/listening/205_we.mp3"
            print(f"Updated Test 1 Part 1 (ID {test1_part1.id}) with audio URL: /audio/listening/205_we.mp3")
        
        db.commit()
        print("\nAudio URLs updated successfully!")
        
        # Show current status
        print("\n=== Current Listening Entries ===")
        for entry in listening_entries:
            status = "[OK]" if entry.audio_url else "[MISSING]"
            print(f"{status} ID {entry.id}: Section {entry.section} - {entry.title}")
            if entry.audio_url:
                print(f"   Audio: {entry.audio_url}")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_listening_audio()
