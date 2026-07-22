import os
import socket
from urllib.parse import urlparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ilm_ai")
IS_PRODUCTION = os.environ.get("ENVIRONMENT", "development") == "production"


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

if not postgres_ok and IS_PRODUCTION:
    raise RuntimeError(
        "DATABASE_URL is set to a Postgres URL and ENVIRONMENT=production, but "
        "Postgres is unreachable. Refusing to silently fall back to an ephemeral "
        "SQLite file in production (this would look like it works, then lose all "
        "user data, uploads, quiz history, and payments on the next restart/redeploy). "
        "Fix the DATABASE_URL / Postgres connectivity instead."
    )

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
                "email_verified": "BOOLEAN DEFAULT 0",
                "assistant_count_today": "INTEGER DEFAULT 0",
                "assistant_count_date": "VARCHAR(20)",
                "push_token": "VARCHAR(300)",
                "xp_total": "INTEGER DEFAULT 0",
                "referral_code": "VARCHAR(16)",
                "referred_by": "INTEGER",
            }
            added_email_verified = False
            for col, col_type in new_columns.items():
                if col not in existing:
                    conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {col_type}"))
                    conn.commit()
                    print(f"Added column: users.{col}")
                    if col == "email_verified":
                        added_email_verified = True

            if added_email_verified:
                # OAuth accounts are already verified by their provider —
                # don't lock out existing Google users on upgrade.
                conn.execute(text("UPDATE users SET email_verified = 1 WHERE oauth_provider IS NOT NULL"))
                conn.commit()

            # sat_ielts_questions: skill sub-domain column (SAT platform taxonomy)
            result = conn.execute(text("PRAGMA table_info(sat_ielts_questions)"))
            q_existing = [row[1] for row in result.fetchall()]
            if q_existing and "skill" not in q_existing:
                conn.execute(text("ALTER TABLE sat_ielts_questions ADD COLUMN skill VARCHAR(120)"))
                conn.commit()
                print("Added column: sat_ielts_questions.skill")

            # ielts_listening: Cambridge 21 parts were ripped as two files each
            result = conn.execute(text("PRAGMA table_info(ielts_listening)"))
            a_existing = [row[1] for row in result.fetchall()]
            if a_existing and "audio_parts" not in a_existing:
                conn.execute(text("ALTER TABLE ielts_listening ADD COLUMN audio_parts JSON"))
                conn.commit()
                print("Added column: ielts_listening.audio_parts")
            if a_existing and "tables" not in a_existing:
                conn.execute(text("ALTER TABLE ielts_listening ADD COLUMN tables JSON"))
                conn.commit()
            r_existing = [row[1] for row in conn.execute(text("PRAGMA table_info(ielts_reading)")).fetchall()]
            if r_existing and "tables" not in r_existing:
                conn.execute(text("ALTER TABLE ielts_reading ADD COLUMN tables JSON"))
                conn.commit()

            # skilltree_lessons: theory teaching-cards column (Duolingo-style learn-then-quiz)
            result = conn.execute(text("PRAGMA table_info(skilltree_lessons)"))
            l_existing = [row[1] for row in result.fetchall()]
            if l_existing and "theory" not in l_existing:
                conn.execute(text("ALTER TABLE skilltree_lessons ADD COLUMN theory JSON"))
                conn.commit()
                print("Added column: skilltree_lessons.theory")
    except Exception as e:
        print(f"Migration error: {e}")


def migrate_postgres_columns():
    """Add any missing columns to a Postgres (prod) database, idempotently, on
    every startup. Needed because Render's start command doesn't run Alembic and
    SQLAlchemy's create_all() only CREATEs new tables — it never ALTERs an
    existing table (e.g. `users`) to add newly-introduced columns. Uses
    Postgres' `ADD COLUMN IF NOT EXISTS`, so it's safe to run repeatedly."""
    if not DATABASE_URL.startswith("postgres"):
        return
    statements = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS xp_total INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS referral_code VARCHAR(16)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS referred_by INTEGER",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS push_token VARCHAR(300)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS assistant_count_today INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS assistant_count_date VARCHAR(20)",
        # skilltree_lessons may pre-exist from an earlier deploy without `theory`.
        "ALTER TABLE skilltree_lessons ADD COLUMN IF NOT EXISTS theory JSON",
        # Cambridge 21 listening parts are often two audio files, played in order.
        "ALTER TABLE ielts_listening ADD COLUMN IF NOT EXISTS audio_parts JSON",
        # Tables printed in the paper, rebuilt from per-word boxes; "[[7]]" marks a gap.
        "ALTER TABLE ielts_listening ADD COLUMN IF NOT EXISTS tables JSON",
        "ALTER TABLE ielts_reading ADD COLUMN IF NOT EXISTS tables JSON",
        # sat_ielts_questions gained these columns after prod's table was first
        # created; a missing mapped column makes the whole SELECT 500, so the
        # question bank returned an Internal Server Error until they were added.
        "ALTER TABLE sat_ielts_questions ADD COLUMN IF NOT EXISTS skill VARCHAR(120)",
        "ALTER TABLE sat_ielts_questions ADD COLUMN IF NOT EXISTS rubric TEXT",
        "ALTER TABLE sat_ielts_questions ADD COLUMN IF NOT EXISTS image_url TEXT",
        "ALTER TABLE sat_ielts_questions ADD COLUMN IF NOT EXISTS source_filename VARCHAR(300)",
        "ALTER TABLE sat_ielts_questions ADD COLUMN IF NOT EXISTS tags JSON",
        "ALTER TABLE sat_ielts_questions ADD COLUMN IF NOT EXISTS created_by INTEGER",
    ]
    try:
        with engine.connect() as conn:
            for stmt in statements:
                try:
                    conn.execute(text(stmt))
                    conn.commit()
                except Exception as e:  # table may not exist yet on a fresh DB — create_all handles that
                    conn.rollback()
                    print(f"PG column migrate skipped: {e}")
    except Exception as e:
        print(f"Postgres migration error: {e}")


migrate_sqlite_columns()
migrate_postgres_columns()


def make_password_nullable():
    """
    Rebuild the SQLite users table if `password` still has its original
    NOT NULL constraint. Google/OAuth signups never set a password, so this
    predates OAuth support — SQLite can't ALTER COLUMN to drop NOT NULL
    directly, so the table has to be rebuilt (rename, recreate with the
    current schema, copy rows back, drop the renamed original).
    """
    if not DATABASE_URL.startswith("sqlite"):
        return
    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(users)"))
            columns = result.fetchall()
            if not columns:
                return
            password_col = next((c for c in columns if c[1] == "password"), None)
            if not password_col or password_col[3] == 0:  # notnull flag; 0 = already nullable
                return

            col_names = [c[1] for c in columns]
            col_list = ", ".join(f'"{c}"' for c in col_names)

            conn.execute(text("ALTER TABLE users RENAME TO users_pre_oauth_migration"))
            conn.execute(text("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    email VARCHAR(200) NOT NULL,
                    password VARCHAR(256),
                    oauth_provider VARCHAR(50),
                    oauth_provider_id VARCHAR(200),
                    profile_picture VARCHAR(500),
                    telegram_chat_id VARCHAR(64),
                    reminder_time VARCHAR(8) DEFAULT '09:00',
                    streak_days INTEGER DEFAULT 0,
                    last_study_date VARCHAR(20),
                    subscription_tier VARCHAR(32) DEFAULT 'free',
                    uploads_count INTEGER DEFAULT 0,
                    quiz_count_today INTEGER DEFAULT 0,
                    quiz_count_date VARCHAR(20),
                    chat_count_today INTEGER DEFAULT 0,
                    chat_count_date VARCHAR(20),
                    learning_goal TEXT,
                    target_date VARCHAR(20)
                )
            """))
            conn.execute(text(f"INSERT INTO users ({col_list}) SELECT {col_list} FROM users_pre_oauth_migration"))
            conn.execute(text("DROP TABLE users_pre_oauth_migration"))
            conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email)"))
            conn.commit()
            print("Rebuilt users table so password is nullable (required for OAuth signups)")
    except Exception as e:
        print(f"Error making password nullable: {e}")


make_password_nullable()

