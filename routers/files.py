from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
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

# Larger chunks (1000 vs 500) roughly halve the number of pieces, so a big book
# needs half as many embeddings — much faster to ingest and lighter on the free
# tier's memory, while still small enough for good RAG retrieval.
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150):
    text = text.strip()
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks

from google.genai.errors import ClientError

def get_embedding(text: str):
    return get_embeddings([text])[0]


# A large book chunked at ~500 chars is hundreds of pieces. Embedding them one at
# a time is hundreds of sequential API calls — minutes of work, long enough that
# the upload connection is dropped and the browser reports "Failed to fetch".
# Batching (many chunks per request) turns that into a handful of calls. Capped so
# a pathologically large upload can't run unbounded.
EMBED_BATCH = 100
MAX_CHUNKS = 1400   # ~600 pages of text at 1000-char chunks


def _embed_one(text: str):
    result = gemini_embed(model="gemini-embedding-001", contents=[text])
    return result.embeddings[0].values


def get_embeddings(texts: list[str]) -> list:
    out: list = []
    for start in range(0, len(texts), EMBED_BATCH):
        group = texts[start:start + EMBED_BATCH]
        try:
            result = gemini_embed(model="gemini-embedding-001", contents=group)
            out.extend(emb.values for emb in result.embeddings)
        except ClientError as e:
            if getattr(e, "code", None) == 429:
                raise HTTPException(status_code=429, detail="Embedding API rate limit exceeded. Please wait a moment.")
            # Some models/quotas reject large batches — fall back to one-by-one for
            # this group so a batch-size limit never breaks the whole upload.
            try:
                out.extend(_embed_one(t) for t in group)
            except ClientError as e2:
                if getattr(e2, "code", None) == 429:
                    raise HTTPException(status_code=429, detail="Embedding API rate limit exceeded. Please wait a moment.")
                raise HTTPException(status_code=500, detail=f"Embedding API Error: {str(e2)}")
    return out

def _embed_and_store(user_id: int, filename: str, topic: str, chunks: list[str]):
    """Embed the chunks and append them to the user's vector store. Runs in the
    BACKGROUND (after the upload response is already sent), so a 500-page book
    never keeps the HTTP request open long enough to time out. Best-effort:
    embedding is batched, and a failure only affects this document."""
    try:
        embeddings = get_embeddings(chunks)
    except HTTPException:
        return  # e.g. quota — the document just won't be indexed this time
    existing = load_vectors(user_id)
    existing.extend(
        {
            "id": f"{filename}::chunk{i}::{os.urandom(4).hex()}",
            "filename": filename,
            "topic": topic,
            "text": chunk,
            "embedding": embeddings[i],
        }
        for i, chunk in enumerate(chunks)
    )
    save_vectors(user_id, existing)


@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
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

    chunks = chunk_text(text)[:MAX_CHUNKS]
    if not chunks:
        raise HTTPException(status_code=422, detail="No readable text found in the file.")

    # Text extraction (fast) is done here; the slow part — embedding every chunk —
    # runs in the background AFTER we respond, so the upload returns in ~1-2s no
    # matter how big the book is. The document appears searchable once indexing
    # finishes (a page refresh shows it).
    record_upload(user_id)
    background_tasks.add_task(_embed_and_store, user_id, file.filename, topic, chunks)

    return {
        "message": f"'{file.filename}' qabul qilindi — indekslanmoqda ({len(chunks)} bo'lak).",
        "filename": file.filename,
        "topic": topic,
        "chunks": len(chunks),
        "processing": True,
    }

@router.post("/upload-image")
async def upload_image(
    user_id: int = Depends(verify_user_access),
    topic: str = "Notes",
    file: UploadFile = File(default=None),
):
    """Photograph handwritten (or printed) notes and add them to the materials
    library: Gemini reads the page into clean text, which is then chunked, embedded
    and appended just like an uploaded document — so RAG can answer from paper notes."""
    if file is None:
        raise HTTPException(status_code=422, detail="No image provided.")
    ok, msg = can_upload(user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty image")

    mime = file.content_type
    if not mime or mime == "application/octet-stream":
        name = (file.filename or "").lower()
        mime = "image/png" if name.endswith(".png") else "image/webp" if name.endswith(".webp") else "image/jpeg"

    from google.genai import types
    ocr_prompt = (
        "Transcribe ALL the text in this image (handwritten or printed) into clean, well-structured "
        "plain text. Fix obvious spacing, keep the original language, preserve lists and structure. "
        "Return only the transcribed text, nothing else."
    )
    try:
        resp = gemini_generate(
            model="gemini-flash-latest",
            contents=[ocr_prompt, types.Part.from_bytes(data=content, mime_type=mime)],
        )
        text = (resp.text or "").strip()
    except Exception:
        raise HTTPException(status_code=502, detail="ocr_failed")
    if len(text) < 15:
        raise HTTPException(status_code=422, detail="no_text_found")

    filename = file.filename or f"notes-{os.urandom(3).hex()}.jpg"
    chunks = chunk_text(text)[:MAX_CHUNKS]
    existing = load_vectors(user_id)
    embeddings = get_embeddings(chunks)
    for i, chunk in enumerate(chunks):
        existing.append({
            "id": f"{filename}::chunk{i}::{os.urandom(4).hex()}",
            "filename": filename,
            "topic": topic,
            "text": chunk,
            "embedding": embeddings[i],
        })
    save_vectors(user_id, existing)
    record_upload(user_id)
    return {"message": "Notes added to your library", "filename": filename, "chunks": len(chunks), "text": text}


class ImportUrlRequest(BaseModel):
    user_id: int
    url: str
    topic: str = "Web"


def _html_to_text(html: str) -> tuple[str, str]:
    """Dependency-free extraction: drop script/style/head, strip tags, unescape.
    Returns (title, text). Good enough for articles without pulling in bs4."""
    import html as html_lib
    import re

    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if m:
        title = html_lib.unescape(re.sub(r"\s+", " ", m.group(1))).strip()
    # Remove non-content blocks entirely.
    for tag in ("script", "style", "noscript", "head", "svg", "nav", "footer", "form"):
        html = re.sub(rf"<{tag}[^>]*>.*?</{tag}>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    # Block tags → newlines so paragraphs survive.
    html = re.sub(r"</(p|div|h[1-6]|li|br|tr|section|article)>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", html)
    text = html_lib.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return title, text.strip()


@router.post("/import-url")
def import_url(data: ImportUrlRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    """Fetch a web article/page, extract its text, and add it to the materials
    library (chunked + embedded, appended) so RAG/quizzes/course can use it."""
    ensure_own_user(data.user_id, auth_user_id)
    ok, msg = can_upload(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    url = data.url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    import requests as _rq
    try:
        resp = _rq.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0 (compatible; IlmAI/1.0)"})
        resp.raise_for_status()
    except Exception:
        raise HTTPException(status_code=400, detail="fetch_failed")

    ctype = resp.headers.get("content-type", "")
    if "text/html" in ctype or "<html" in resp.text[:2000].lower():
        title, text = _html_to_text(resp.text)
    else:
        title, text = "", resp.text
    if len(text) < 60:
        raise HTTPException(status_code=422, detail="no_text_found")

    from urllib.parse import urlparse
    filename = (title or urlparse(url).netloc or "webpage")[:120]
    chunks = chunk_text(text[:60000])[:MAX_CHUNKS]
    existing = load_vectors(data.user_id)
    embeddings = get_embeddings(chunks)
    for i, chunk in enumerate(chunks):
        existing.append({
            "id": f"{filename}::chunk{i}::{os.urandom(4).hex()}",
            "filename": filename,
            "topic": data.topic,
            "text": chunk,
            "embedding": embeddings[i],
        })
    save_vectors(data.user_id, existing)
    record_upload(data.user_id)
    return {"message": "Added to your library", "filename": filename, "chunks": len(chunks)}


@router.get("/documents/{user_id}")
def list_documents(user_id: int = Depends(verify_user_access)):
    """The learner's uploaded documents with how many chunks each holds — the data
    a materials manager needs to show and delete individual files."""
    vectors = load_vectors(user_id)
    counts: dict[str, dict] = {}
    for v in vectors:
        fn = v.get("filename", "")
        if not fn:
            continue
        d = counts.setdefault(fn, {"filename": fn, "chunks": 0, "topic": v.get("topic", "General")})
        d["chunks"] += 1
    return {"documents": sorted(counts.values(), key=lambda d: d["filename"])}


@router.delete("/documents/{user_id}")
def delete_document(user_id: int = Depends(verify_user_access), filename: str = ""):
    """Remove one uploaded document (all its chunks) from the materials library,
    keeping the rest. No-op-safe if the filename isn't found."""
    if not filename:
        raise HTTPException(status_code=400, detail="filename required")
    vectors = load_vectors(user_id)
    kept = [v for v in vectors if v.get("filename") != filename]
    removed = len(vectors) - len(kept)
    save_vectors(user_id, kept)
    return {"removed_chunks": removed, "remaining_documents": len({v.get("filename") for v in kept if v.get("filename")})}


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

    chunks = chunk_text(data.text)[:MAX_CHUNKS]
    existing = load_vectors(data.user_id)

    embeddings = get_embeddings(chunks)
    new_entries = [
        {
            "id": f"{data.filename}::chunk{i}::{os.urandom(4).hex()}",
            "filename": data.filename,
            "topic": data.topic,
            "text": chunk,
            "embedding": embeddings[i],
        }
        for i, chunk in enumerate(chunks)
    ]

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