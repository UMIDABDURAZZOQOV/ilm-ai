"""
IELTS-specific API routes for 4 skills: Listening, Reading, Writing, Speaking
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from services.db import get_db
from services.models import (
    IeltsListening, IeltsReading, IeltsWriting, IeltsSpeaking,
    IeltsQuestion, IeltsWritingSubmission, IeltsSpeakingSubmission, IeltsMockTest
)

router = APIRouter(prefix="/ielts", tags=["IELTS"])


# ─── Pydantic Models ─────────────────────────────────────────────────────────

class ListeningResponse(BaseModel):
    id: int
    section: int
    title: str
    audio_url: Optional[str]
    audio_parts: Optional[List[str]] = None
    transcript: Optional[str]
    tables: Optional[List[List[List[str]]]] = None
    difficulty: str
    duration_seconds: Optional[int]

    class Config:
        from_attributes = True


class ReadingResponse(BaseModel):
    id: int
    section: int
    title: str
    passage_text: str
    tables: Optional[List[List[List[str]]]] = None
    difficulty: str
    word_count: Optional[int]

    class Config:
        from_attributes = True


class WritingResponse(BaseModel):
    id: int
    task_type: str
    category: str
    prompt: str
    image_url: Optional[str]
    min_words: int
    duration_minutes: int
    difficulty: str

    class Config:
        from_attributes = True


class SpeakingResponse(BaseModel):
    id: int
    part: int
    topic: str
    questions: List[str]
    cue_card: Optional[str]
    prep_seconds: Optional[int]
    speak_seconds: Optional[int]
    difficulty: str

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: int
    skill: str
    parent_id: Optional[int]
    question_type: str
    question_text: str
    options: Optional[List[str]]
    correct_answer: str
    hint: Optional[str]
    order_index: int

    class Config:
        from_attributes = True


class WritingSubmissionRequest(BaseModel):
    user_id: int
    task_id: int
    essay_text: str


class WritingSubmissionResponse(BaseModel):
    id: int
    user_id: int
    task_id: int
    essay_text: str
    word_count: Optional[int]
    band_score: Optional[float]
    feedback: Optional[str]
    task_response: Optional[str]
    coherence: Optional[str]
    lexical: Optional[str]
    grammar: Optional[str]
    submitted_at: str

    class Config:
        from_attributes = True


class SpeakingSubmissionRequest(BaseModel):
    user_id: int
    topic_id: int
    audio_url: str
    duration_seconds: Optional[int]


class SpeakingSubmissionResponse(BaseModel):
    id: int
    user_id: int
    topic_id: int
    audio_url: str
    duration_seconds: Optional[int]
    band_score: Optional[float]
    feedback: Optional[str]
    fluency: Optional[str]
    lexical: Optional[str]
    grammar: Optional[str]
    pronunciation: Optional[str]
    submitted_at: str

    class Config:
        from_attributes = True


class MockTestRequest(BaseModel):
    user_id: int
    test_type: str  # academic|general_training


class MockTestResponse(BaseModel):
    id: int
    user_id: int
    test_type: str
    status: str
    listening_score: Optional[float]
    reading_score: Optional[float]
    writing_score: Optional[float]
    speaking_score: Optional[float]
    overall_band: Optional[float]
    started_at: str
    completed_at: Optional[str]

    class Config:
        from_attributes = True


# ─── Listening Routes ────────────────────────────────────────────────────────

@router.get("/listening", response_model=List[ListeningResponse])
def get_listening(
    section: Optional[int] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get listening exercises with optional filters."""
    query = db.query(IeltsListening)
    if section:
        query = query.filter(IeltsListening.section == section)
    if difficulty:
        query = query.filter(IeltsListening.difficulty == difficulty)
    return query.all()


@router.get("/listening/{listening_id}", response_model=ListeningResponse)
def get_listening_by_id(listening_id: int, db: Session = Depends(get_db)):
    """Get a specific listening exercise."""
    listening = db.query(IeltsListening).filter(IeltsListening.id == listening_id).first()
    if not listening:
        raise HTTPException(status_code=404, detail="Listening exercise not found")
    return listening


@router.get("/listening/{listening_id}/questions", response_model=List[QuestionResponse])
def get_listening_questions(listening_id: int, db: Session = Depends(get_db)):
    """Get questions for a listening exercise."""
    questions = db.query(IeltsQuestion).filter(
        IeltsQuestion.skill == "Listening",
        IeltsQuestion.parent_id == listening_id
    ).order_by(IeltsQuestion.order_index).all()
    return questions


# ─── Reading Routes ─────────────────────────────────────────────────────────

@router.get("/reading", response_model=List[ReadingResponse])
def get_reading(
    section: Optional[int] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get reading passages with optional filters."""
    query = db.query(IeltsReading)
    if section:
        query = query.filter(IeltsReading.section == section)
    if difficulty:
        query = query.filter(IeltsReading.difficulty == difficulty)
    return query.all()


@router.get("/reading/{reading_id}", response_model=ReadingResponse)
def get_reading_by_id(reading_id: int, db: Session = Depends(get_db)):
    """Get a specific reading passage."""
    reading = db.query(IeltsReading).filter(IeltsReading.id == reading_id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading passage not found")
    return reading


@router.get("/reading/{reading_id}/questions", response_model=List[QuestionResponse])
def get_reading_questions(reading_id: int, db: Session = Depends(get_db)):
    """Get questions for a reading passage."""
    questions = db.query(IeltsQuestion).filter(
        IeltsQuestion.skill == "Reading",
        IeltsQuestion.parent_id == reading_id
    ).order_by(IeltsQuestion.order_index).all()
    return questions


# ─── Writing Routes ─────────────────────────────────────────────────────────

@router.get("/writing", response_model=List[WritingResponse])
def get_writing(
    task_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get writing tasks with optional filters."""
    query = db.query(IeltsWriting)
    if task_type:
        query = query.filter(IeltsWriting.task_type == task_type)
    if difficulty:
        query = query.filter(IeltsWriting.difficulty == difficulty)
    return query.all()


@router.get("/writing/{writing_id}", response_model=WritingResponse)
def get_writing_by_id(writing_id: int, db: Session = Depends(get_db)):
    """Get a specific writing task."""
    writing = db.query(IeltsWriting).filter(IeltsWriting.id == writing_id).first()
    if not writing:
        raise HTTPException(status_code=404, detail="Writing task not found")
    return writing


@router.post("/writing/submit", response_model=WritingSubmissionResponse)
def submit_writing(submission: WritingSubmissionRequest, db: Session = Depends(get_db)):
    """Submit a writing task for AI grading."""
    from services.gemini import generate_content
    
    word_count = len(submission.essay_text.split())
    
    # Get the task to determine task type
    task = db.query(IeltsWriting).filter(IeltsWriting.id == submission.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Writing task not found")
    
    # AI Grading with IELTS rubric
    grading_prompt = f"""You are an IELTS examiner. Grade the following {task.task_type} essay according to the official IELTS Writing rubric.

Task Type: {task.task_type}
Category: {task.category}
Prompt: {task.prompt}
Student Essay:
{submission.essay_text}

Provide your response in this exact JSON format:
{{
    "band_score": 6.5,
    "task_response": "6.0 - The task is partially addressed...",
    "coherence": "6.5 - Ideas are arranged coherently...",
    "lexical": "7.0 - Uses a sufficient range of vocabulary...",
    "grammar": "6.0 - Uses a mix of simple and complex sentence forms...",
    "feedback": "Overall feedback with specific suggestions for improvement..."
}}

Grading criteria:
- Task Response (TR): How well the task is addressed
- Coherence & Cohesion (CC): Organization and linking
- Lexical Resource (LR): Vocabulary range and accuracy
- Grammatical Range & Accuracy (GRA): Sentence structures and grammar

Return ONLY the JSON, no additional text."""
    
    try:
        response = generate_content(
            model="gemini-flash-latest",
            contents=grading_prompt,
            config={"response_mime_type": "application/json"}
        )
        
        import json
        grading_result = json.loads(response.text)
        
        db_submission = IeltsWritingSubmission(
            user_id=submission.user_id,
            task_id=submission.task_id,
            essay_text=submission.essay_text,
            word_count=word_count,
            band_score=grading_result.get("band_score"),
            feedback=grading_result.get("feedback"),
            task_response=grading_result.get("task_response"),
            coherence=grading_result.get("coherence"),
            lexical=grading_result.get("lexical"),
            grammar=grading_result.get("grammar"),
        )
    except Exception as e:
        # Fallback if AI grading fails
        db_submission = IeltsWritingSubmission(
            user_id=submission.user_id,
            task_id=submission.task_id,
            essay_text=submission.essay_text,
            word_count=word_count,
            band_score=None,
            feedback=f"AI grading failed: {str(e)}",
        )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


@router.get("/writing/submissions/{user_id}", response_model=List[WritingSubmissionResponse])
def get_writing_submissions(user_id: int, db: Session = Depends(get_db)):
    """Get all writing submissions for a user."""
    submissions = db.query(IeltsWritingSubmission).filter(
        IeltsWritingSubmission.user_id == user_id
    ).order_by(IeltsWritingSubmission.submitted_at.desc()).all()
    return submissions


# ─── Speaking Routes ────────────────────────────────────────────────────────

@router.get("/speaking", response_model=List[SpeakingResponse])
def get_speaking(
    part: Optional[int] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get speaking topics with optional filters."""
    query = db.query(IeltsSpeaking)
    if part:
        query = query.filter(IeltsSpeaking.part == part)
    if difficulty:
        query = query.filter(IeltsSpeaking.difficulty == difficulty)
    return query.all()


@router.get("/speaking/{speaking_id}", response_model=SpeakingResponse)
def get_speaking_by_id(speaking_id: int, db: Session = Depends(get_db)):
    """Get a specific speaking topic."""
    speaking = db.query(IeltsSpeaking).filter(IeltsSpeaking.id == speaking_id).first()
    if not speaking:
        raise HTTPException(status_code=404, detail="Speaking topic not found")
    return speaking


@router.post("/speaking/submit", response_model=SpeakingSubmissionResponse)
def submit_speaking(submission: SpeakingSubmissionRequest, db: Session = Depends(get_db)):
    """Submit a speaking recording for AI grading."""
    from services.gemini import generate_content
    
    # Get the topic
    topic = db.query(IeltsSpeaking).filter(IeltsSpeaking.id == submission.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Speaking topic not found")
    
    # Note: In production, you would transcribe the audio first using Speech-to-Text
    # For now, we'll provide a placeholder grading based on duration and topic
    # Real implementation would use Google Cloud Speech-to-Text + Gemini grading
    
    grading_prompt = f"""You are an IELTS examiner. Grade a speaking response based on the topic and duration.

Speaking Part: {topic.part}
Topic: {topic.topic}
Questions: {', '.join(topic.questions)}
Duration: {submission.duration_seconds} seconds

Since this is a placeholder (audio transcription not implemented), provide a realistic grading based on:
- Fluency & Coherence (FC): Flow, natural speech, connectors
- Lexical Resource (LR): Vocabulary range and accuracy
- Grammatical Range (GRA): Sentence structures and grammar
- Pronunciation (P): Clarity, intonation, stress

Provide your response in this exact JSON format:
{{
    "band_score": 6.5,
    "fluency": "6.0 - Speaks at length but may lose coherence...",
    "lexical": "7.0 - Uses a sufficient range of vocabulary...",
    "grammar": "6.5 - Uses a mix of simple and complex forms...",
    "pronunciation": "6.0 - Generally clear but with some issues...",
    "feedback": "Overall feedback with specific suggestions..."
}}

Return ONLY the JSON, no additional text."""
    
    try:
        response = generate_content(
            model="gemini-flash-latest",
            contents=grading_prompt,
            config={"response_mime_type": "application/json"}
        )
        
        import json
        grading_result = json.loads(response.text)
        
        db_submission = IeltsSpeakingSubmission(
            user_id=submission.user_id,
            topic_id=submission.topic_id,
            audio_url=submission.audio_url,
            duration_seconds=submission.duration_seconds,
            band_score=grading_result.get("band_score"),
            feedback=grading_result.get("feedback"),
            fluency=grading_result.get("fluency"),
            lexical=grading_result.get("lexical"),
            grammar=grading_result.get("grammar"),
            pronunciation=grading_result.get("pronunciation"),
        )
    except Exception as e:
        # Fallback if AI grading fails
        db_submission = IeltsSpeakingSubmission(
            user_id=submission.user_id,
            topic_id=submission.topic_id,
            audio_url=submission.audio_url,
            duration_seconds=submission.duration_seconds,
            band_score=None,
            feedback=f"AI grading failed: {str(e)}",
        )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


@router.get("/speaking/submissions/{user_id}", response_model=List[SpeakingSubmissionResponse])
def get_speaking_submissions(user_id: int, db: Session = Depends(get_db)):
    """Get all speaking submissions for a user."""
    submissions = db.query(IeltsSpeakingSubmission).filter(
        IeltsSpeakingSubmission.user_id == user_id
    ).order_by(IeltsSpeakingSubmission.submitted_at.desc()).all()
    return submissions


# ─── Mock Test Routes ────────────────────────────────────────────────────────

@router.post("/mock-test/start", response_model=MockTestResponse)
def start_mock_test(test: MockTestRequest, db: Session = Depends(get_db)):
    """Start a full IELTS computer-based mock test."""
    db_test = IeltsMockTest(
        user_id=test.user_id,
        test_type=test.test_type,
        status="in_progress"
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test


@router.get("/mock-test/{test_id}", response_model=MockTestResponse)
def get_mock_test(test_id: int, db: Session = Depends(get_db)):
    """Get a specific mock test."""
    test = db.query(IeltsMockTest).filter(IeltsMockTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Mock test not found")
    return test


@router.post("/mock-test/{test_id}/complete", response_model=MockTestResponse)
def complete_mock_test(test_id: int, db: Session = Depends(get_db)):
    """Complete a mock test and calculate overall band score."""
    test = db.query(IeltsMockTest).filter(IeltsMockTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Mock test not found")
    
    test.status = "completed"
    test.completed_at = datetime.utcnow()
    
    # Calculate overall band score (average of 4 skills)
    scores = [s for s in [test.listening_score, test.reading_score, test.writing_score, test.speaking_score] if s is not None]
    if scores:
        test.overall_band = sum(scores) / len(scores)
    
    db.commit()
    db.refresh(test)
    return test


@router.get("/mock-test/user/{user_id}", response_model=List[MockTestResponse])
def get_user_mock_tests(user_id: int, db: Session = Depends(get_db)):
    """Get all mock tests for a user."""
    tests = db.query(IeltsMockTest).filter(
        IeltsMockTest.user_id == user_id
    ).order_by(IeltsMockTest.started_at.desc()).all()
    return tests
