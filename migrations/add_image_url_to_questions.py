"""
Migration: Add image_url column to sat_ielts_questions
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from services.db import engine, SessionLocal

def upgrade():
    """Add image_url column to sat_ielts_questions table."""
    with engine.connect() as conn:
        # Check if column already exists (SQLite syntax)
        result = conn.execute(text("""
            PRAGMA table_info(sat_ielts_questions)
        """))
        columns = [row[1] for row in result.fetchall()]
        
        if 'image_url' not in columns:
            conn.execute(text("""
                ALTER TABLE sat_ielts_questions 
                ADD COLUMN image_url TEXT
            """))
            conn.commit()
            print("Added image_url column to sat_ielts_questions")
        else:
            print("image_url column already exists")

def downgrade():
    """Remove image_url column from sat_ielts_questions table."""
    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE sat_ielts_questions 
            DROP COLUMN IF EXISTS image_url
        """))
        conn.commit()
        print("Removed image_url column from sat_ielts_questions")

if __name__ == "__main__":
    upgrade()
