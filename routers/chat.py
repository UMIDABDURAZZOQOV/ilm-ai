from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.subscriptions import can_chat, record_chat
import os
import json
import numpy as np
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

router = APIRouter(prefix="/chat", tags=["chat"])

VECTOR_DIR = "vectors"

def load_vectors(user_id: int):
    path = f"{VECTOR_DIR}/user_{user_id}.json"
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_embedding(text: str):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_chunks(query: str, user_id: int, top_k: int = 4):
    data = load_vectors(user_id)
    if not data:
        return []
    query_embedding = get_embedding(query)
    scored = []
    for entry in data:
        score = cosine_similarity(query_embedding, entry["embedding"])
        scored.append((score, entry["text"], entry["filename"]))
    scored.sort(reverse=True)
    return scored[:top_k]

class ChatRequest(BaseModel):
    user_id: int
    question: str

@router.post("/ask")
def ask(data: ChatRequest):
    ok, msg = can_chat(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    results = search_chunks(data.question, data.user_id)

    if not results:
        return {"answer": "I could not find any relevant information in your uploaded materials."}

    context = "\n\n---\n\n".join([f"[{r[2]}]: {r[1]}" for r in results])

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""You are Ilm AI — a warm, patient, Socratic learning companion.
Answer ONLY from the CONTEXT below.
If the answer is not in the context, say: 'I don't have enough information in your uploaded materials.'
Always cite which part of the material your answer comes from.

CONTEXT:
{context}

QUESTION:
{data.question}"""
    )

    record_chat(data.user_id)
    return {
        "answer": response.text,
        "sources_found": len(results)
    }