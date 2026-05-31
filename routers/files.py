from fastapi import APIRouter, UploadFile, File
import os
import json
import numpy as np
from google import genai
from dotenv import load_dotenv
import pypdf
import io

load_dotenv()

# Yangi google-genai client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

router = APIRouter(prefix="/files", tags=["files"])

VECTOR_DIR = "vectors"
os.makedirs(VECTOR_DIR, exist_ok=True)

def get_user_file(user_id: int):
    return f"{VECTOR_DIR}/user_{user_id}.json"

def load_vectors(user_id: int):
    path = get_user_file(user_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_vectors(user_id: int, data: list):
    with open(get_user_file(user_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80):
    text = text.strip()
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks

def get_embedding(text: str):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[text]
    )
    return result.embeddings[0].values

@router.post("/upload")
async def upload_file(user_id: int, file: UploadFile = File(...)):
    content = await file.read()

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    else:
        text = content.decode("utf-8", errors="ignore")

    chunks = chunk_text(text)
    existing = load_vectors(user_id)

    new_entries = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        new_entries.append({
            "id": f"{file.filename}::chunk{i}",
            "filename": file.filename,
            "text": chunk,
            "embedding": embedding
        })

    existing.extend(new_entries)
    save_vectors(user_id, existing)

    return {
        "message": "File uploaded and indexed successfully",
        "filename": file.filename,
        "chunks": len(chunks)
    }

@router.get("/list")
def list_files(user_id: int):
    data = load_vectors(user_id)
    filenames = list(set(d["filename"] for d in data))
    return {"files": filenames, "total_chunks": len(data)}