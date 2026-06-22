from fastapi import APIRouter, Depends, HTTPException
from services.auth_deps import verify_user_access, ensure_own_user, get_authenticated_user_id
from pydantic import BaseModel
from services.subscriptions import can_chat, record_chat
import os
import json
import numpy as np
from google import genai
from google.genai.errors import ClientError
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

import time
from services.monitoring import log_llm_call

router = APIRouter(prefix="/chat", tags=["chat"])

VECTOR_DIR = "vectors"
CHAT_HISTORY_DIR = "data/chat_history"
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)
MAX_HISTORY = 6  # Keep last 6 Q&A pairs for context


def _chat_history_path(user_id: int) -> str:
    return f"{CHAT_HISTORY_DIR}/user_{user_id}.json"


def load_chat_history(user_id: int) -> list[dict]:
    path = _chat_history_path(user_id)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_chat_history(user_id: int, history: list[dict]) -> None:
    with open(_chat_history_path(user_id), "w", encoding="utf-8") as f:
        json.dump(history[-MAX_HISTORY * 2:], f, ensure_ascii=False, indent=2)


def append_chat_message(user_id: int, role: str, content: str) -> None:
    history = load_chat_history(user_id)
    history.append({"role": role, "content": content})
    save_chat_history(user_id, history)

from services.users import USE_DB
from services.db import SessionLocal
from services.models import VectorEntry

def load_vectors(user_id: int):
    if USE_DB:
        db = SessionLocal()
        try:
            entries = db.query(VectorEntry).filter(VectorEntry.user_id == user_id).all()
            return [
                {
                    "id": e.chunk_id,
                    "filename": e.filename,
                    "topic": e.topic,
                    "text": e.text,
                    "embedding": e.embedding
                }
                for e in entries
            ]
        finally:
            db.close()

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
    language: str = "en"

@router.post("/ask")
def ask(data: ChatRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    ok, msg = can_chat(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    results = search_chunks(data.question, data.user_id)

    if not results:
        return {
            "answer": "I could not find any relevant information in your uploaded materials.",
            "citations": [],
            "sources": [],
            "sources_found": 0,
        }

    context = "\n\n---\n\n".join([f"[{r[2]}]: {r[1]}" for r in results])

    # Load recent chat history for conversational context
    history = load_chat_history(data.user_id)
    history_text = ""
    if history:
        history_lines = []
        for msg in history[-MAX_HISTORY * 2:]:
            role_label = "User" if msg["role"] == "user" else "Assistant"
            history_lines.append(f"{role_label}: {msg['content']}")
        history_text = "\n\nRECENT CONVERSATION HISTORY:\n" + "\n".join(history_lines)

    lang_instruction = ""
    if data.language:
        lang_instruction = f"\nIMPORTANT: Respond in {data.language} language."

    prompt = f"""You are Ilm AI — a warm, patient, and Socratic learning companion.
Your goal is to help the user learn from their uploaded materials.

Answer ONLY from the CONTEXT below.
If the answer is not in the context, say: 'I don't have enough information in your uploaded materials.'
Always cite the filename(s) you are using. Be specific.

Tone: Warm, patient, encouraging, and Socratic (ask follow-up questions to help them think).
Languages: Support Uzbek, Russian, and English. Respond in the same language the user uses.{lang_instruction}
{history_text}

CONTEXT:
{context}

QUESTION:
{data.question}"""

    start_time = time.time()
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    except ClientError as e:
        if hasattr(e, "status_code") and e.status_code == 429:
            raise HTTPException(status_code=429, detail="Gemini API rate limit exceeded (429). Please wait a moment and try again.")
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")
    
    latency_ms = int((time.time() - start_time) * 1000)
    
    token_count = None
    try:
        token_count = response.usage_metadata.total_token_count
    except AttributeError:
        pass

    log_llm_call(
        user_id=data.user_id,
        prompt=prompt,
        response_text=response.text,
        latency_ms=latency_ms,
        token_count=token_count,
        model="gemini-2.5-flash"
    )

    record_chat(data.user_id)

    # Save to chat history
    append_chat_message(data.user_id, "user", data.question)
    append_chat_message(data.user_id, "assistant", response.text)

    # Build citations list (unique filenames)
    citations = list({r[2] for r in results})

    return {
        "answer": response.text,
        "sources_found": len(results),
        "citations": citations,
        "sources": citations,
    }


@router.get("/history/{user_id}")
def get_chat_history(user_id: int = Depends(verify_user_access)):
    """Return chat history for a user."""
    history = load_chat_history(user_id)
    return {"history": history}


@router.delete("/history/{user_id}")
def clear_chat_history(user_id: int = Depends(verify_user_access)):
    """Clear chat history for a user."""
    path = _chat_history_path(user_id)
    if os.path.exists(path):
        os.remove(path)
    return {"message": "Chat history cleared"}
