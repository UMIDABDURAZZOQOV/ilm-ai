"""
Generate IELTS practice content using Gemini AI
Creates listening exercises, reading passages, writing tasks, and speaking topics
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import (
    IeltsListening, IeltsReading, IeltsWriting, IeltsSpeaking, IeltsQuestion
)
from services.gemini import generate_content
import json

def generate_listening_content(db: Session, count: int = 5):
    """Generate listening exercises with questions."""
    print(f"Generating {count} listening exercises...")
    
    for i in range(count):
        section = (i % 4) + 1  # Sections 1-4
        prompt = f"""Generate an IELTS Section {section} listening exercise.

Section {section} characteristics:
- Section 1: Everyday conversation (e.g., booking, information)
- Section 2: Monologue on general topic (e.g., tour guide)
- Section 3: Academic conversation (2-4 speakers)
- Section 4: Academic lecture

Provide response in this exact JSON format:
{{
    "title": "Descriptive title",
    "transcript": "Full transcript of the audio (200-300 words)",
    "duration_seconds": 180,
    "difficulty": "medium",
    "questions": [
        {{
            "question_type": "completion",
            "question_text": "Question text",
            "options": null,
            "correct_answer": "answer",
            "hint": "ONE WORD ONLY",
            "order_index": 1
        }},
        {{
            "question_type": "mcq",
            "question_text": "Question text",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A",
            "hint": null,
            "order_index": 2
        }}
    ]
}}

Return ONLY the JSON, no additional text."""
        
        try:
            response = generate_content(
                model="gemini-flash-latest",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            # Create listening exercise
            listening = IeltsListening(
                section=section,
                title=data["title"],
                transcript=data["transcript"],
                difficulty=data["difficulty"],
                duration_seconds=data["duration_seconds"]
            )
            db.add(listening)
            db.commit()
            db.refresh(listening)
            
            # Create questions
            for q_data in data["questions"]:
                question = IeltsQuestion(
                    skill="Listening",
                    parent_id=listening.id,
                    question_type=q_data["question_type"],
                    question_text=q_data["question_text"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    hint=q_data.get("hint"),
                    order_index=q_data["order_index"]
                )
                db.add(question)
            
            db.commit()
            print(f"  ✓ Created listening exercise {i+1}: {data['title']}")
            
        except Exception as e:
            print(f"  ✗ Failed to create listening exercise {i+1}: {e}")
            db.rollback()

def generate_reading_content(db: Session, count: int = 5):
    """Generate reading passages with questions."""
    print(f"Generating {count} reading passages...")
    
    topics = [
        "Technology and society",
        "Environmental conservation",
        "Health and medicine",
        "Education systems",
        "Urban development"
    ]
    
    for i in range(count):
        section = (i % 3) + 1  # Sections 1-3
        topic = topics[i % len(topics)]
        
        prompt = f"""Generate an IELTS Section {section} reading passage.

Topic: {topic}
Section {section} characteristics:
- Section 1: Short texts (advertisements, notices)
- Section 2: Two texts on same topic
- Section 3: Long academic passage

Provide response in this exact JSON format:
{{
    "title": "Descriptive title",
    "passage_text": "Full passage text (400-600 words for section 1, 600-800 for section 2, 800-1000 for section 3)",
    "difficulty": "medium",
    "word_count": 600,
    "questions": [
        {{
            "question_type": "tfng",
            "question_text": "Statement to evaluate",
            "options": ["True", "False", "Not Given"],
            "correct_answer": "True",
            "hint": null,
            "order_index": 1
        }},
        {{
            "question_type": "mcq",
            "question_text": "Question text",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A",
            "hint": null,
            "order_index": 2
        }},
        {{
            "question_type": "completion",
            "question_text": "Question text",
            "options": null,
            "correct_answer": "answer",
            "hint": "ONE WORD ONLY",
            "order_index": 3
        }}
    ]
}}

Return ONLY the JSON, no additional text."""
        
        try:
            response = generate_content(
                model="gemini-flash-latest",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            # Create reading passage
            reading = IeltsReading(
                section=section,
                title=data["title"],
                passage_text=data["passage_text"],
                difficulty=data["difficulty"],
                word_count=data["word_count"]
            )
            db.add(reading)
            db.commit()
            db.refresh(reading)
            
            # Create questions
            for q_data in data["questions"]:
                question = IeltsQuestion(
                    skill="Reading",
                    parent_id=reading.id,
                    question_type=q_data["question_type"],
                    question_text=q_data["question_text"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    hint=q_data.get("hint"),
                    order_index=q_data["order_index"]
                )
                db.add(question)
            
            db.commit()
            print(f"  ✓ Created reading passage {i+1}: {data['title']}")
            
        except Exception as e:
            print(f"  ✗ Failed to create reading passage {i+1}: {e}")
            db.rollback()

def generate_writing_content(db: Session, count: int = 10):
    """Generate writing tasks (Task 1 and Task 2)."""
    print(f"Generating {count} writing tasks...")
    
    task1_categories = ["Line graph", "Bar chart", "Pie chart", "Process diagram", "Map"]
    task2_categories = ["Technology", "Education", "Environment", "Health", "Society", "Work", "Culture", "Youth", "Urban life", "Media"]
    
    for i in range(count):
        if i < 5:  # First 5 are Task 1
            task_type = "Task1"
            category = task1_categories[i]
            prompt_text = f"""Generate an IELTS Task 1 writing prompt.

Category: {category}
Task 1 requires describing visual information (charts, graphs, diagrams, maps).

Provide response in this exact JSON format:
{{
    "category": "{category}",
    "prompt": "Detailed description of what the visual shows (e.g., 'A line graph shows...')",
    "image_url": null,
    "min_words": 150,
    "duration_minutes": 20,
    "difficulty": "medium"
}}

Return ONLY the JSON, no additional text."""
        else:  # Next 5 are Task 2
            task_type = "Task2"
            category = task2_categories[i - 5]
            prompt_text = f"""Generate an IELTS Task 2 writing prompt.

Category: {category}
Task 2 requires writing an essay on an opinion, problem, or discussion topic.

Provide response in this exact JSON format:
{{
    "category": "{category}",
    "prompt": "Full essay prompt (e.g., 'Some people believe that... To what extent do you agree or disagree?')",
    "image_url": null,
    "min_words": 250,
    "duration_minutes": 40,
    "difficulty": "medium"
}}

Return ONLY the JSON, no additional text."""
        
        try:
            response = generate_content(
                model="gemini-flash-latest",
                contents=prompt_text,
                config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            writing = IeltsWriting(
                task_type=task_type,
                category=data["category"],
                prompt=data["prompt"],
                image_url=data.get("image_url"),
                min_words=data["min_words"],
                duration_minutes=data["duration_minutes"],
                difficulty=data["difficulty"]
            )
            db.add(writing)
            db.commit()
            print(f"  ✓ Created {task_type} writing task: {data['category']}")
            
        except Exception as e:
            print(f"  ✗ Failed to create writing task: {e}")
            db.rollback()

def generate_speaking_content(db: Session, count: int = 10):
    """Generate speaking topics."""
    print(f"Generating {count} speaking topics...")
    
    part1_topics = ["Hometown", "Work or study", "Free time", "Technology", "Food", "Weather", "Family", "Friends"]
    part2_topics = ["Describe a teacher", "Describe a place", "Describe a skill", "Describe a book", "Describe a trip"]
    part3_topics = ["Education", "Technology", "Environment", "Society", "Culture"]
    
    for i in range(count):
        if i < 4:  # Part 1
            part = 1
            topic = part1_topics[i % len(part1_topics)]
            prompt = f"""Generate IELTS Speaking Part 1 questions.

Topic: {topic}
Part 1 is a general conversation about familiar topics (4-5 minutes).

Provide response in this exact JSON format:
{{
    "part": 1,
    "topic": "{topic}",
    "questions": ["Question 1", "Question 2", "Question 3", "Question 4"],
    "cue_card": null,
    "prep_seconds": null,
    "speak_seconds": null,
    "difficulty": "medium"
}}

Return ONLY the JSON, no additional text."""
        elif i < 7:  # Part 2
            part = 2
            topic = part2_topics[(i - 4) % len(part2_topics)]
            prompt = f"""Generate IELTS Speaking Part 2 cue card.

Topic: {topic}
Part 2 is a long turn (1-2 minutes) with 1 minute preparation.

Provide response in this exact JSON format:
{{
    "part": 2,
    "topic": "{topic}",
    "questions": ["Describe {topic.lower()}. You should say: what it is, when you experienced it, why it's important, and explain how you feel about it."],
    "cue_card": "Full cue card with bullet points",
    "prep_seconds": 60,
    "speak_seconds": 120,
    "difficulty": "medium"
}}

Return ONLY the JSON, no additional text."""
        else:  # Part 3
            part = 3
            topic = part3_topics[(i - 7) % len(part3_topics)]
            prompt = f"""Generate IELTS Speaking Part 3 questions.

Topic: {topic}
Part 3 is a discussion (4-5 minutes) on abstract topics related to Part 2.

Provide response in this exact JSON format:
{{
    "part": 3,
    "topic": "{topic}",
    "questions": ["Abstract question 1", "Abstract question 2", "Abstract question 3", "Abstract question 4"],
    "cue_card": null,
    "prep_seconds": null,
    "speak_seconds": null,
    "difficulty": "medium"
}}

Return ONLY the JSON, no additional text."""
        
        try:
            response = generate_content(
                model="gemini-flash-latest",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            speaking = IeltsSpeaking(
                part=data["part"],
                topic=data["topic"],
                questions=data["questions"],
                cue_card=data.get("cue_card"),
                prep_seconds=data.get("prep_seconds"),
                speak_seconds=data.get("speak_seconds"),
                difficulty=data["difficulty"]
            )
            db.add(speaking)
            db.commit()
            print(f"  ✓ Created Part {part} speaking topic: {data['topic']}")
            
        except Exception as e:
            print(f"  ✗ Failed to create speaking topic: {e}")
            db.rollback()

def main():
    db = SessionLocal()
    try:
        print("=" * 50)
        print("Generating IELTS Practice Content")
        print("=" * 50)
        
        generate_listening_content(db, count=5)
        generate_reading_content(db, count=5)
        generate_writing_content(db, count=10)
        generate_speaking_content(db, count=10)
        
        print("=" * 50)
        print("Content generation complete!")
        print("=" * 50)
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
