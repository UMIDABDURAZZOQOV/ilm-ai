"""
Map all IELTS 21 audio files to listening sections in the database.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsListening

def map_all_audio():
    """Map all audio files to listening sections."""
    db = SessionLocal()
    
    try:
        # Audio file mapping based on the extracted files
        # For parts with .1 and .2 segments, we'll use both
        audio_mapping = {
            # Test 1
            "Test 1": {
                1: ["/audio/listening/C21T1P1.1.mp3", "/audio/listening/C21T1P1.2.mp3"],
                2: ["/audio/listening/C21T1P2.1.mp3", "/audio/listening/C21T1P2.2.mp3"],
                3: ["/audio/listening/C21T1P3.1.mp3", "/audio/listening/C21T1P3.2.mp3"],
                4: ["/audio/listening/C21T1P4.mp3"],
            },
            # Test 2
            "Test 2": {
                1: ["/audio/listening/C21T2P1.mp3"],
                2: ["/audio/listening/C21T2P2.1.mp3", "/audio/listening/C21T2P2.2.mp3"],
                3: ["/audio/listening/C21T2P3.1.mp3", "/audio/listening/C21T2P3.2.mp3"],
                4: ["/audio/listening/C21T2P4.mp3"],
            },
            # Test 3
            "Test 3": {
                1: ["/audio/listening/C21T3P1.mp3"],
                2: ["/audio/listening/C21T3P2.1.mp3", "/audio/listening/C21T3P2.2.mp3"],
                3: ["/audio/listening/C21T3P3.1.mp3", "/audio/listening/C21T3P3.2.mp3"],
                4: ["/audio/listening/C21T3P4.mp3"],
            },
            # Test 4
            "Test 4": {
                1: ["/audio/listening/C21T4P1.mp3"],
                2: ["/audio/listening/C21T4P2.1.mp3", "/audio/listening/C21T4P2.2.mp3"],
                3: ["/audio/listening/C21T4P3.1.mp3", "/audio/listening/C21T4P3.2.mp3"],
                4: ["/audio/listening/C21T4P4.mp3"],
            },
        }
        
        # Update each listening entry
        for test_name, parts in audio_mapping.items():
            for part_num, audio_urls in parts.items():
                # Find the listening entry
                entry = db.query(IeltsListening).filter(
                    IeltsListening.section == part_num,
                    IeltsListening.title.like(f"%{test_name}%")
                ).first()
                
                if entry:
                    # For multiple segments, join with comma (frontend can handle this)
                    entry.audio_url = ",".join(audio_urls)
                    print(f"Updated {test_name} Part {part_num} (ID {entry.id}): {entry.audio_url}")
                else:
                    print(f"NOT FOUND: {test_name} Part {part_num}")
        
        db.commit()
        print("\n=== All audio files mapped successfully! ===")
        
        # Show final status
        print("\n=== Final Listening Status ===")
        entries = db.query(IeltsListening).order_by(IeltsListening.id).all()
        for entry in entries:
            status = "[OK]" if entry.audio_url else "[MISSING]"
            print(f"{status} ID {entry.id}: {entry.title}")
            if entry.audio_url:
                print(f"   Audio: {entry.audio_url}")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    map_all_audio()
