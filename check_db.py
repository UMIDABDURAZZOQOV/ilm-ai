import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.models import LLMLog, User, QuizSession, VectorEntry
from services.db import DATABASE_URL

print("Connecting to:", DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    users_count = db.query(User).count()
    logs_count = db.query(LLMLog).count()
    rated_count = db.query(LLMLog).filter(LLMLog.rating.isnot(None)).count()
    quizzes_count = db.query(QuizSession).count()
    vectors_count = db.query(VectorEntry).count()

    print(f"Users: {users_count}")
    print(f"Logs: {logs_count}")
    print(f"Rated Logs: {rated_count}")
    print(f"Quizzes: {quizzes_count}")
    print(f"Vectors: {vectors_count}")
except Exception as e:
    print("Error querying database:", e)
finally:
    db.close()
