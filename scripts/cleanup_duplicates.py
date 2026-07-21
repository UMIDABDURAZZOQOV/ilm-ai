"""
Clean up duplicate IELTS entries (keep IDs 1-16, delete 17-32).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsListening, IeltsReading, IeltsWriting, IeltsSpeaking

def cleanup_duplicates():
    """Delete duplicate entries (IDs > 16)."""
    db = SessionLocal()
    
    try:
        # Delete listening entries with ID > 16
        deleted_listening = db.query(IeltsListening).filter(IeltsListening.id > 16).delete()
        print(f"Deleted {deleted_listening} duplicate listening entries")
        
        # Delete reading entries with ID > 16
        deleted_reading = db.query(IeltsReading).filter(IeltsReading.id > 16).delete()
        print(f"Deleted {deleted_reading} duplicate reading entries")
        
        # Delete writing entries with ID > 16
        deleted_writing = db.query(IeltsWriting).filter(IeltsWriting.id > 16).delete()
        print(f"Deleted {deleted_writing} duplicate writing entries")
        
        # Delete speaking entries with ID > 16
        deleted_speaking = db.query(IeltsSpeaking).filter(IeltsSpeaking.id > 16).delete()
        print(f"Deleted {deleted_speaking} duplicate speaking entries")
        
        db.commit()
        
        # Show final counts
        print("\n=== Final Counts ===")
        print(f"Listening: {db.query(IeltsListening).count()}")
        print(f"Reading: {db.query(IeltsReading).count()}")
        print(f"Writing: {db.query(IeltsWriting).count()}")
        print(f"Speaking: {db.query(IeltsSpeaking).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_duplicates()
