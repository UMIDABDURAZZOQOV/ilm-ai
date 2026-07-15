"""
Generate real audio files for listening tests using gTTS (Google Text-to-Speech)
Free, no API key required
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsListening
from pathlib import Path

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

def generate_audio_for_listening(db: Session):
    """Generate audio files for all listening tests using gTTS"""
    print("Generating audio files for listening tests...")
    
    if not GTTS_AVAILABLE:
        print("  ✗ gTTS library not installed")
        print("  Install with: pip install gTTS")
        return
    
    # Create audio directory in frontend
    audio_dir = Path("c:/Users/123www/Desktop/Files/ilm-ai-frontend/public/audio/listening")
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    listenings = db.query(IeltsListening).all()
    
    for listening in listenings:
        audio_file = audio_dir / f"{listening.id}.mp3"
        
        # Skip if already exists
        if audio_file.exists():
            print(f"  Skipping - audio already exists: {listening.title}")
            continue
        
        try:
            print(f"  Generating audio for: {listening.title}")
            
            # Generate audio using gTTS
            tts = gTTS(text=listening.transcript, lang='en', slow=False)
            tts.save(str(audio_file))
            
            # Update audio_url in database
            listening.audio_url = f"/audio/listening/{listening.id}.mp3"
            db.commit()
            
            print(f"  ✓ Generated audio: {audio_file}")
            
        except Exception as e:
            print(f"  ✗ Failed to generate audio for {listening.title}: {e}")
    
    db.commit()
    print("✓ Audio generation complete")

def main():
    db = SessionLocal()
    try:
        generate_audio_for_listening(db)
        
        print("\nAudio files generated successfully!")
        print("Location: c:/Users/123www/Desktop/Files/ilm-ai-frontend/public/audio/listening/")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
