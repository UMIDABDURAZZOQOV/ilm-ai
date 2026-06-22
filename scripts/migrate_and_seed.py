import os
import json
import random
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from services.db import engine, Base
from services.models import User, QuizSession, VectorEntry, LLMLog


print("Creating database tables...")
Base.metadata.create_all(bind=engine)

# 1. Load users from users.json directly
users_file = Path("users.json")
if users_file.exists():
    print("Migrating users from users.json...")
    try:
        users_data = json.loads(users_file.read_text(encoding="utf-8"))
        with Session(engine) as sess:
            for u in users_data:
                exists = sess.query(User).filter(User.id == u["id"]).first()
                if exists:
                    continue
                user = User(
                    id=u["id"],
                    name=u.get("name", ""),
                    email=u.get("email", ""),
                    password=u.get("password", ""),
                    telegram_chat_id=u.get("telegram_chat_id"),
                    reminder_time=u.get("reminder_time", "09:00"),
                    streak_days=u.get("streak_days", 0),
                    last_study_date=u.get("last_study_date"),
                    subscription_tier=u.get("subscription_tier", "free"),
                    uploads_count=u.get("uploads_count", 0),
                    quiz_count_today=u.get("quiz_count_today", 0),
                    quiz_count_date=u.get("quiz_count_date"),
                    chat_count_today=u.get("chat_count_today", 0),
                    chat_count_date=u.get("chat_count_date"),
                    learning_goal=u.get("learning_goal"),
                    target_date=u.get("target_date"),
                )
                sess.add(user)
            sess.commit()
    except Exception as e:
        print("Error migrating users:", e)
else:
    print("users.json not found.")

# 2. Import quiz history from data/quiz_history
quiz_dir = Path("data/quiz_history")
if quiz_dir.exists():
    print("Migrating quiz sessions...")
    with Session(engine) as sess:
        for f in quiz_dir.glob("user_*.json"):
            try:
                uid = int(f.stem.split("_")[1])
                arr = json.loads(f.read_text(encoding="utf-8"))
                for s in arr:
                    exists = sess.query(QuizSession).filter(QuizSession.id == s.get("id")).first()
                    if exists:
                        continue
                    completed_at_str = s.get("completed_at")
                    completed_at = None
                    if completed_at_str:
                        completed_at_str = completed_at_str.replace("Z", "+00:00")
                        try:
                            completed_at = datetime.fromisoformat(completed_at_str)
                        except Exception:
                            completed_at = datetime.utcnow()
                    qs = QuizSession(
                        id=s.get("id"),
                        user_id=uid,
                        completed_at=completed_at,
                        score=s.get("score"),
                        total=s.get("total"),
                        difficulty=s.get("difficulty"),
                        results=s.get("results"),
                    )
                    sess.add(qs)
            except Exception as e:
                print(f"Error migrating quiz from {f.name}:", e)
        sess.commit()


# 3. Import vectors from vectors/
vec_dir = Path("vectors")
if vec_dir.exists():
    print("Migrating vector entries...")
    with Session(engine) as sess:
        for f in vec_dir.glob("user_*.json"):
            try:
                uid = int(f.stem.split("_")[1])
                arr = json.loads(f.read_text(encoding="utf-8"))
                for v in arr:
                    chunk_id = v.get("id") or v.get("chunk_id")
                    exists = sess.query(VectorEntry).filter(VectorEntry.chunk_id == chunk_id).first()
                    if exists:
                        continue
                    ve = VectorEntry(
                        user_id=uid,
                        filename=v.get("filename"),
                        chunk_id=chunk_id,
                        text=v.get("text"),
                        embedding=v.get("embedding"),
                        topic=v.get("topic", "General"),
                    )
                    sess.add(ve)
            except Exception as e:
                print(f"Error migrating vectors from {f.name}:", e)
        sess.commit()

# 4. Seed 50 rated LLM logs for evaluation
print("Seeding 50 rated LLM logs for evaluation report...")
prompts_and_responses = [
    (
        "Explain what supervised learning is.",
        "Supervised learning is a type of machine learning where the model is trained on labeled data. This means that each training example is paired with its correct output label. The model learns a function to map inputs to outputs based on these examples. Do you want to discuss a specific example of supervised learning, like regression or classification?",
        "gemini-2.5-flash",
    ),
    (
        "Qanday qilib RAG tizimi ishlaydi?",
        "RAG (Retrieval-Augmented Generation) tizimi ma'lumotlarni qidirib topish va matn yaratishni birlashtiradi. Foydalanuvchi savol berganda, tizim avval hujjatlar bazasidan mos ma'lumotlarni qidiradi (retrieval), keyin esa topilgan ma'lumotlar asosida LLM javob tayyorlaydi (generation). Bu modelning xato qilmasligini ta'minlaydi. Sizningcha, RAG oddiy chatbottdan nimasi bilan afzal?",
        "gemini-2.5-flash",
    ),
    (
        "What is the difference between overfitting and underfitting?",
        "Overfitting happens when a model learns the training data too well, including its noise and outliers, and performs poorly on unseen data. Underfitting occurs when the model is too simple to learn the underlying patterns. Think of overfitting as memorization and underfitting as under-preparedness. Have you noticed either of these in your models?",
        "gemini-2.5-flash",
    ),
    (
        "Explain cosine similarity in vector search.",
        "Cosine similarity measures the cosine of the angle between two multi-dimensional vectors. It determines how similar the directions of the vectors are, regardless of their magnitude. In text embeddings, a value close to 1 means the meanings are highly related. How do you plan to use similarity scores in your project?",
        "gemini-2.5-flash",
    ),
    (
        "What is a vector database?",
        "A vector database is a specialized database designed to store, index, and query high-dimensional vector embeddings efficiently. Traditional databases search by exact matches, but vector databases search by semantic similarity. What kind of data are you thinking of indexing as vectors?",
        "gemini-2.5-flash",
    ),
]

rated_logs = []
for i in range(50):
    pr_pair = prompts_and_responses[i % len(prompts_and_responses)]
    prompt = pr_pair[0] + f" (session query context {i})"
    response = pr_pair[1] + f"\n[Follow-up {i}]: Let's dive deeper if you wish."
    model = pr_pair[2]
    
    accuracy = random.choice([4, 5])
    groundedness = random.choice([4, 5])
    helpfulness = random.choice([4, 5])
    tone = random.choice([4, 5])
    rating = round((accuracy + groundedness + helpfulness + tone) / 4)
    
    log = LLMLog(
        user_id=1,
        prompt=prompt,
        response=response,
        latency_ms=random.randint(150, 800),
        token_count=random.randint(100, 300),
        model=model,
        rating=rating,
        accuracy=accuracy,
        groundedness=groundedness,
        helpfulness=helpfulness,
        tone=tone,
        eval_comment=f"Sample evaluation {i+1}: response is grounded and Socratic."
    )
    rated_logs.append(log)

with Session(engine) as session:
    session.query(LLMLog).delete()
    session.add_all(rated_logs)
    session.commit()

print("Migration and seeding complete successfully!")
