"""
Migration: Create IELTS-specific tables for 4 skills
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from services.db import engine
from services.models import Base

def upgrade():
    """Create all IELTS-specific tables."""
    print("Creating IELTS tables...")
    Base.metadata.create_all(bind=engine)
    print("IELTS tables created successfully")

def downgrade():
    """Drop all IELTS-specific tables."""
    print("Dropping IELTS tables...")
    with engine.connect() as conn:
        tables = [
            "ielts_mock_tests",
            "ielts_speaking_submissions",
            "ielts_writing_submissions",
            "ielts_questions",
            "ielts_speaking",
            "ielts_writing",
            "ielts_reading",
            "ielts_listening",
        ]
        for table in tables:
            conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
        conn.commit()
    print("IELTS tables dropped")

if __name__ == "__main__":
    upgrade()
