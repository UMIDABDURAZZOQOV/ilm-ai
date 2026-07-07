import os
import socket
from urllib.parse import urlparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ilm_ai")


def check_postgres_port(url: str) -> bool:
    try:
        parsed = urlparse(url)
        host = parsed.hostname or "127.0.0.1"
        if host == "localhost":
            host = "127.0.0.1"
        port = parsed.port or 5432
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False



# Check if PostgreSQL is available, else fall back to SQLite
postgres_ok = False
if DATABASE_URL.startswith("postgresql"):
    postgres_ok = check_postgres_port(DATABASE_URL)

if postgres_ok:
    try:
        engine = create_engine(DATABASE_URL, echo=False, future=True)
    except Exception:
        postgres_ok = False

if not postgres_ok:
    print("PostgreSQL is not available. Falling back to SQLite database...")
    os.makedirs("data", exist_ok=True)
    DATABASE_URL = "sqlite:///data/ilm_ai.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
        future=True
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_profile_picture_column():
    """Add profile_picture column if it doesn't exist."""
    try:
        with engine.connect() as conn:
            # Check if column exists
            if DATABASE_URL.startswith("sqlite"):
                result = conn.execute(text("PRAGMA table_info(users)"))
                columns = [row[1] for row in result.fetchall()]
                if 'profile_picture' not in columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500)"))
                    conn.commit()
                    print("Added profile_picture column to users table")
            else:
                # PostgreSQL
                result = conn.execute(text("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'users' AND column_name = 'profile_picture'
                """))
                if not result.fetchone():
                    conn.execute(text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500)"))
                    conn.commit()
                    print("Added profile_picture column to users table")
    except Exception as e:
        print(f"Error adding profile_picture column: {e}")


# Try to add the column on import
add_profile_picture_column()


def migrate_sqlite_columns():
    """Add any missing columns to SQLite database (auto-migration)."""
    if not DATABASE_URL.startswith("sqlite"):
        return
    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(users)"))
            existing = [row[1] for row in result.fetchall()]

            new_columns = {
                "oauth_provider": "VARCHAR(50)",
                "oauth_provider_id": "VARCHAR(200)",
                "chat_count_today": "INTEGER DEFAULT 0",
                "chat_count_date": "VARCHAR(20)",
                "learning_goal": "TEXT",
                "target_date": "VARCHAR(20)",
            }
            for col, col_type in new_columns.items():
                if col not in existing:
                    conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {col_type}"))
                    conn.commit()
                    print(f"Added column: users.{col}")
    except Exception as e:
        print(f"Migration error: {e}")


migrate_sqlite_columns()

