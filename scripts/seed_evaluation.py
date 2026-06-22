import random
from sqlalchemy.orm import Session
from services.db import engine
from services.models import LLMLog, Base

# Make sure tables are created
Base.metadata.create_all(bind=engine)

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

# We will generate 50 logs using variations of these prompt/response pairs with different Socratic follow-ups, languages (Uzbek, Russian, English), and realistic evaluation metrics.
rated_logs = []
for i in range(50):
    pr_pair = prompts_and_responses[i % len(prompts_and_responses)]
    prompt = pr_pair[0] + f" (session query context {i})"
    response = pr_pair[1] + f"\n[Follow-up {i}]: Let's dive deeper if you wish."
    model = pr_pair[2]
    
    # Generate realistic ratings (mostly high: 4 or 5)
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
        eval_comment=f"Sample evaluation {i+1}: response is grounded and maintains a Socratic tone."
    )
    rated_logs.append(log)

with Session(engine) as session:
    # Clear existing logs to start fresh
    session.query(LLMLog).delete()
    session.add_all(rated_logs)
    session.commit()

print(f"Successfully seeded {len(rated_logs)} rated LLM logs for evaluation report.")
