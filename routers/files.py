from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from services.auth_deps import verify_user_access, ensure_own_user, get_authenticated_user_id
from pydantic import BaseModel
from services.subscriptions import can_upload, record_upload
import os
import json
from google import genai
from dotenv import load_dotenv
import pypdf
import io

load_dotenv()

# Yangi google-genai client
from services.gemini import generate_content as gemini_generate, embed_content as gemini_embed

router = APIRouter(prefix="/files", tags=["files"])

VECTOR_DIR = "vectors"
os.makedirs(VECTOR_DIR, exist_ok=True)

from services.users import USE_DB
from services.db import SessionLocal
from services.models import VectorEntry

def get_user_file(user_id: int):
    return f"{VECTOR_DIR}/user_{user_id}.json"

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

    path = get_user_file(user_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_vectors(user_id: int, data: list):
    if USE_DB:
        db = SessionLocal()
        try:
            db.query(VectorEntry).filter(VectorEntry.user_id == user_id).delete()
            for item in data:
                entry = VectorEntry(
                    user_id=user_id,
                    filename=item["filename"],
                    chunk_id=item["id"],
                    text=item["text"],
                    embedding=item["embedding"],
                    topic=item.get("topic", "General")
                )
                db.add(entry)
            db.commit()
        finally:
            db.close()
        return

    with open(get_user_file(user_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        from docx import Document

        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception:
        return ""

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80):
    text = text.strip()
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks

from google.genai.errors import ClientError

def get_embedding(text: str):
    try:
        result = gemini_embed(
            model="gemini-embedding-001",
            contents=[text]
        )
        return result.embeddings[0].values
    except ClientError as e:
        if getattr(e, "code", None) == 429:
            raise HTTPException(status_code=429, detail="Embedding API rate limit exceeded. Please wait a moment.")
        raise HTTPException(status_code=500, detail=f"Embedding API Error: {str(e)}")

@router.post("/upload")
async def upload_file(
    user_id: int = Depends(verify_user_access),
    topic: str = "General",
    file: UploadFile = File(default=None),
):
    if file is None:
        raise HTTPException(status_code=422, detail="No file provided. Send file as multipart/form-data with field name 'file'.")
    ok, msg = can_upload(user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    content = await file.read()

    lower_name = file.filename.lower()
    if lower_name.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif lower_name.endswith(".docx"):
        text = extract_text_from_docx(content)
    else:
        text = content.decode("utf-8", errors="ignore")

    chunks = chunk_text(text)
    existing = load_vectors(user_id)

    new_entries = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        new_entries.append({
            "id": f"{file.filename}::chunk{i}::{os.urandom(4).hex()}",
            "filename": file.filename,
            "topic": topic,
            "text": chunk,
            "embedding": embedding
        })

    existing.extend(new_entries)
    save_vectors(user_id, existing)
    record_upload(user_id)

    return {
        "message": f"File uploaded to '{topic}' and indexed successfully",
        "filename": file.filename,
        "topic": topic,
        "chunks": len(chunks)
    }

class UploadTextRequest(BaseModel):
    user_id: int
    filename: str
    text: str
    topic: str = "General"

@router.post("/upload-text")
def upload_text(
    data: UploadTextRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    ensure_own_user(data.user_id, auth_user_id)
    ok, msg = can_upload(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    chunks = chunk_text(data.text)
    existing = load_vectors(data.user_id)

    new_entries = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        new_entries.append({
            "id": f"{data.filename}::chunk{i}::{os.urandom(4).hex()}",
            "filename": data.filename,
            "topic": data.topic,
            "text": chunk,
            "embedding": embedding
        })

    existing.extend(new_entries)
    save_vectors(data.user_id, existing)
    record_upload(data.user_id)

    return {
        "message": f"Text uploaded to '{data.topic}' and indexed successfully",
        "filename": data.filename,
        "topic": data.topic,
        "chunks": len(chunks)
    }

@router.get("/list")
def list_files(user_id: int = Depends(verify_user_access)):
    data = load_vectors(user_id)
    # Group by filename and include topic
    files_map = {}
    for d in data:
        fname = d["filename"]
        if fname not in files_map:
            files_map[fname] = {"filename": fname, "topic": d.get("topic", "General"), "chunks": 0}
        files_map[fname]["chunks"] += 1
    
    return {"files": list(files_map.values()), "total_chunks": len(data)}

@router.delete("/delete")
def delete_file(filename: str, user_id: int = Depends(verify_user_access)):
    from services.subscriptions import record_delete_upload
    if USE_DB:
        db = SessionLocal()
        try:
            deleted = db.query(VectorEntry).filter(
                VectorEntry.user_id == user_id,
                VectorEntry.filename == filename
            ).delete()
            db.commit()
            if deleted == 0:
                raise HTTPException(status_code=404, detail="File not found")
        finally:
            db.close()
        record_delete_upload(user_id)
        return {"message": f"File '{filename}' deleted successfully"}

    data = load_vectors(user_id)
    new_data = [d for d in data if d["filename"] != filename]
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="File not found")
    
    save_vectors(user_id, new_data)
    record_delete_upload(user_id)
    return {"message": f"File '{filename}' deleted successfully"}

class UpdateTopicRequest(BaseModel):
    user_id: int
    filename: str
    new_topic: str = None
    topic: str = None  # mobile sends 'topic', frontend may send 'new_topic'

    @property
    def resolved_topic(self) -> str:
        return self.new_topic or self.topic or "General"

@router.post("/update-topic")
def update_topic(
    data: UpdateTopicRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    ensure_own_user(data.user_id, auth_user_id)
    new_topic = data.resolved_topic

    if USE_DB:
        db = SessionLocal()
        try:
            updated = db.query(VectorEntry).filter(
                VectorEntry.user_id == data.user_id,
                VectorEntry.filename == data.filename
            ).update({VectorEntry.topic: new_topic})
            db.commit()
            if updated == 0:
                raise HTTPException(status_code=404, detail="File not found")
        finally:
            db.close()
        return {"message": f"Topic for '{data.filename}' updated to '{new_topic}'"}

    vectors = load_vectors(data.user_id)
    found = False
    for v in vectors:
        if v["filename"] == data.filename:
            v["topic"] = new_topic
            found = True

    if not found:
        raise HTTPException(status_code=404, detail="File not found")

    save_vectors(data.user_id, vectors)
    return {"message": f"Topic for '{data.filename}' updated to '{new_topic}'"}