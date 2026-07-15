"""
Clear static IELTS content from database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsReading, IeltsWriting, IeltsSpeaking, IeltsQuestion, IeltsListening

def clear_content(db: Session):
    """Clear all IELTS content from database"""
    print("Clearing IELTS content...")
    
    # Delete questions first (foreign key dependency)
    db.query(IeltsQuestion).delete()
    
    # Delete all content
    db.query(IeltsListening).delete()
    db.query(IeltsReading).delete()
    db.query(IeltsWriting).delete()
    db.query(IeltsSpeaking).delete()
    
    db.commit()
    print("✓ All IELTS content cleared")

def main():
    db = SessionLocal()
    try:
        clear_content(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
