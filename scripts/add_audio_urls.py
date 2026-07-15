"""
Add placeholder audio URLs to listening tests
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsListening

def add_audio_urls(db: Session):
    """Add placeholder audio URLs to listening tests"""
    print("Adding audio URLs to listening tests...")
    
    listenings = db.query(IeltsListening).all()
    for listening in listenings:
        # Use a placeholder audio URL - in production, replace with actual audio files
        # Could use TTS services like ElevenLabs, Google Cloud TTS, or AWS Polly
        listening.audio_url = f"/audio/listening/{listening.id}.mp3"
        print(f"  Added audio URL for: {listening.title}")
    
    db.commit()
    print("✓ Audio URLs added")

def main():
    db = SessionLocal()
    try:
        add_audio_urls(db)
        
        print("\nNote: These are placeholder audio URLs.")
        print("To add real audio files:")
        print("1. Use TTS services (ElevenLabs, Google Cloud TTS, AWS Polly)")
        print("2. Generate audio from transcripts")
        print("3. Upload to /audio/listening/ directory")
        print("4. Update audio_url field with actual file paths")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
